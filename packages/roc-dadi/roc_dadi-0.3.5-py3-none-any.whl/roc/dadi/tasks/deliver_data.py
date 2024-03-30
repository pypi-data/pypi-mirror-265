#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import shutil
import uuid
from datetime import timedelta
from pathlib import Path

from sqlalchemy import or_
import pandas as pd

from poppy.core.logger import logger
from poppy.core.task import Task
from poppy.core.target import FileTarget, PyObjectTarget
from poppy.core.db.connector import Connector

from roc.dingo.models.file import FileLog
from roc.dingo.tools import query_db

from roc.dadi.constants import RPW_FILE_PATTERN, TRYOUTS, TIME_WAIT_SEC, SQL_LIMIT, PIPELINE_DATABASE, SOC_GFTS_DIR, \
    TODAY, WAIT_NDAY, TRASH_DIR
from roc.dadi.tools.file_helper import glob_file_list, is_validate
from roc.dadi.tools.time import strtime_to_datetime

__all__ = ['DeliverData']

# Tasks to deliver RPW data files to ESAC


class DeliverData(Task):
    """
    Deliver RPW data to ESAC.
    """
    plugin_name = 'roc.dadi'
    name = 'deliver_data'

    def add_targets(self):
        self.add_input(target_class=FileTarget,
                       identifier='rpw_files',
                       filepath=DeliverData.get_rpw_files,
                       many=True,
                       )

    @staticmethod
    def get_rpw_files(pipeline):
        try:
            rpw_files = glob_file_list(pipeline.args.rpw_files, as_path=True)
            return sorted(rpw_files)
        except:
            # If not defined as input argument, then assume that it is already
            # defined as target input
            pass

    @Connector.if_connected(PIPELINE_DATABASE)
    def setup_inputs(self):

        # Get input list of RPW files to deliver
        self.rpw_file_list = self.inputs['rpw_files'].filepath
        self.rpw_file_num = len(self.rpw_file_list)

        # Get some inputs
        self.sync_only = self.pipeline.get('sync_only', default=False)
        self.force = self.pipeline.get('force', default=False)
        self.dry_run = self.pipeline.get('dry_run', default=False)
        self.clear_transferred = self.pipeline.get('clear_transferred',
                                              default=False)
        self.clear_delivered = self.pipeline.get('clear_delivered',
                                              default=False)
        self.ignore = self.pipeline.get('ignore', default=[])
        self.ignore_list = [item.lower() for item in self.ignore]

        self.start_time = self.pipeline.get('start_time',
                                            default=[None],
                                            )[0]
        self.end_time = self.pipeline.get('end_time',
                                            default=[None],
                                            )[0]
        self.wait_nday = self.pipeline.get('wait_nday',
                                            default=[WAIT_NDAY],
                                            )[0]
        self.soc_gfts_dir = self.pipeline.get('soc_gfts_dir',
                                              default=[SOC_GFTS_DIR],
                                              )[0]
        self.to_soc_dir = self.pipeline.get('to_soc_dir',
                                              default=[None],
                                              )[0]
        self.transferred_dir = self.pipeline.get('transferred_dir',
                                              default=[None],
                                              )[0]
        self.delivered_dir = self.pipeline.get('delivered_dir',
                                              default=[None],
                                              )[0]
        self.failed_dir = self.pipeline.get('failed_dir',
                                              default=[None],
                                              )[0]
        self.trash_dir = self.pipeline.get('trash_dir',
                                              default=[TRASH_DIR],
                                              )[0]

        # Get CDAG latency deadline
        self.cdag_latency_deadline = TODAY - timedelta(days=self.wait_nday)

        # Build "to_soc", "transferred" and "delivered" sub-directories path
        if not self.to_soc_dir:
            self.to_soc_dir = Path(self.soc_gfts_dir) / 'to_soc'
        else:
            self.to_soc_dir = Path(self.to_soc_dir)

        if not self.transferred_dir:
            self.transferred_dir = Path(self.soc_gfts_dir) / 'transferred'
        else:
            self.transferred_dir = Path(self.transferred_dir)

        if not self.delivered_dir:
            self.delivered_dir = Path(self.soc_gfts_dir) / 'delivered'
        else:
            self.delivered_dir = Path(self.delivered_dir)

        if not self.failed_dir:
            self.failed_dir = Path(self.soc_gfts_dir) / 'failed'
        else:
            self.failed_dir = Path(self.failed_dir)

        # And check existence
        if not self.to_soc_dir.is_dir():
            raise NotADirectoryError(f'{self.to_soc_dir} cannot be found!')

        if not self.transferred_dir.is_dir():
            raise NotADirectoryError(f'{self.transferred_dir} cannot be found!')

        if not self.delivered_dir.is_dir():
            raise NotADirectoryError(f'{self.delivered_dir} cannot be found!')

        # Get tryouts from pipeline properties
        self.tryouts = self.pipeline.get(
            'tryouts', default=[TRYOUTS], create=True)[0]

        # Get wait from pipeline properties
        self.wait = self.pipeline.get(
            'wait', default=[TIME_WAIT_SEC], create=True)[0]

        # Retrieve --limit keyword value
        self.limit = self.pipeline.get('limit',
                                       default=[SQL_LIMIT],
                                       args=True)[0]

        # get a database session
        self.session = Connector.manager[PIPELINE_DATABASE].session

    def run(self):
        # Define task job ID and task process id
        self.job_id = str(uuid.uuid4())
        self.task_pid = f'DeliverData-{self.job_id[:8]}'
        logger.info(f'Task {self.task_pid} is starting')
        try:
            self.setup_inputs()
        except:
            logger.exception(f'Initializing inputs has failed for task {self.task_pid}!')
            self.pipeline.exit()
            return

        # If not force
        if not self.force:
            # Then synchronize the content of the 'transferred' directory
            # with the 'delivered' directory
            # And return the list of transferred files
            transferred_file_list = self.transferred_to_delivered(
                self.transferred_dir, self.delivered_dir,
                clear_transferred=self.clear_transferred)
            logger.info(f'{transferred_file_list} files found in {self.transferred_dir}')

            # Return the list of delivered files from delivered/ folder and ROC database
            # Return basename only
            delivered_file_list = self.get_delivered_files(self.delivered_dir,
                                                           clear_delivered=self.clear_delivered,
                                                           trash_dir=self.trash_dir)
        else:
            # If dry_run mode, then assume empty list of deliveries
            delivered_file_list = []

        delivered_file_num = len(delivered_file_list)
        logger.info(f'{delivered_file_num} files have been loaded '
                    f'from {self.delivered_dir} folder')

        # If sync only, skip delivery process
        if self.sync_only:
            return

        # Initialize loop variables
        failed_list = []
        skipped_list = []
        processed_list = []

        # Loop over list of input RPW files
        for i, current_file in enumerate(self.rpw_file_list):
            if not current_file.exists():
                logger.error(f'{current_file} not found!')
                failed_list.append(current_file)
                continue

            # Get filename fields
            current_file_fields = str(current_file.name).split('_')

            # get descriptor
            current_descriptor = current_file_fields[2]

            # Get file date (if time range, get start time)
            current_time = strtime_to_datetime(current_file_fields[3],
                                               valid_format=['%Y%m%d',
                                                             '%Y%m%dT%H%M%S',
                                                             '%Y%m%dT%H%M'])
            if not current_time:
                logger.error(f'{current_file} has an invalid time format!')
                failed_list.append(current_file)
                continue

            # Check file date against start_time
            if self.start_time and current_time.date() < self.start_time.date():
                logger.info(f'Skipping {current_file} (older than {self.start_time.date()})')
                skipped_list.append(current_file)
                continue

            # Check file date against end_time
            if self.end_time and current_time.date() > self.end_time.date():
                logger.info(f'Skipping {current_file} newer than {self.end_time.date()}, skip it')
                skipped_list.append(current_file)
                continue

            # If input file is a CDAG file
            if current_descriptor.endswith('-cdag'):

                # Check if the CDAG file can be delivered
                if current_time.date() > self.cdag_latency_deadline.date():
                    logger.info(f'Skipping {current_file} (cannot be delivered before {(current_time + timedelta(days=self.wait_nday)).date()})')
                    skipped_list.append(current_file)
                    continue
                else:
                    # Remove any -cdag from descriptor
                    current_descriptor = current_descriptor.replace('-cdag', '')

            # Check if current file must be ignored
            if current_descriptor in self.ignore_list:
                logger.info(f'Skipping {current_file} (found in ignore list)')
                skipped_list.append(current_file)
                continue

            # Check file against already delivered list
            # (To avoid re-delivery)
            if current_file.name in delivered_file_list and not self.force:
                logger.info(f'Skipping {current_file} (already delivered)')
                skipped_list.append(current_file)
                continue

            # Deliver only CDF file with Validate=1
            if current_file.suffix == '.cdf' and not is_validate(current_file):
                logger.warning(f'{current_file} is not valid and will be not delivered')
                failed_list.append(current_file)
                continue

            # If all previous checks have passed,
            # then send a copy of the file to deliver in the "to_soc" folder
            target_copy = self.to_soc_dir / current_file.name
            if target_copy.is_file():
                logger.info(f'Skipping {target_copy} file (already found in {self.to_soc_dir})')
                skipped_list.append(current_file)
            else:
                try:
                    logger.info(f'Copying {current_file} into {target_copy.parent} ... ({self.rpw_file_num - i - 1} remaining)')
                    shutil.copyfile(str(current_file), str(target_copy))
                except:
                    logger.exception(f'Copying {current_file} into {target_copy.parent} has failed')
                    failed_list.append(current_file)
                else:
                    logger.debug(f'{current_file} has been well copied into {self.to_soc_dir} ')
                    processed_list.append(target_copy)

        processed_num = len(processed_list)
        failed_num = len(failed_list)
        skipped_num = len(skipped_list)
        logger.info(f'{processed_num} files have been copied into {self.to_soc_dir}')
        logger.info(f'{skipped_num} files have been skipped')
        if failed_num > 0:
            # Move failed files in the failed/ directory
            for current_file in failed_list:
                target_file = self.failed_dir / current_file.name
                target_file.touch(exist_ok=True)
            logger.warning(f'Delivery has failed for {failed_num} files (see {self.failed_dir})')



    def transferred_to_delivered(self, transferred_dir, delivered_dir,
                                 clear_transferred=False):
        """
        Retrieve list of files in 'transferred' folder
        and create empty files with the name in the 'delivered' folder (as a footprint)

        :param transferred_dir: Path to the transferred directory (Path object)
        :param delivered_dir: Path to the delivered directory (Path object)
        :param clear_transferred: If True, delete files in the transferred/ directory after processing
        :return: List of transferred files
        """

        # get list of files in transferred
        transferred_list = list(transferred_dir.glob(RPW_FILE_PATTERN))

        transferred_num = len(transferred_list)
        logger.info(f'{transferred_num} files to be moved '
                    f'from {transferred_dir} to {delivered_dir}...')
        transferred_files = []
        for current_file in transferred_list:
            target_file = delivered_dir / current_file.name
            target_file.touch(exist_ok=True)
            logger.info(f'{target_file} footprint created')

            if clear_transferred:
                current_file.unlink()
                logger.info(f'{current_file} deleted')

            transferred_files.append(target_file)

        # return the list of files moved into delivered folder
        return transferred_files

    def get_delivered_files(self, delivered_dir,
                            clear_delivered=False,
                            trash_dir=Path(TRASH_DIR)):
        """
        Get list of RPW files already delivered to SOAR.
        Check in both /delivered folder and ROC database.

        :param delivered_dir: Path of the delivered/ folder
        :param clear_delivered: If True, delete files in the delivered/ directory
                                which already are flagged as "delivered" in the ROC database
        :param trash_dir: Path of the trash directory
        :return:
        """
        # Get list of delivered files from the delivered/ folder
        delivered_file_list = list(delivered_dir.glob(RPW_FILE_PATTERN))

        # Define a new pandas.DataFrame
        delivered_files = pd.DataFrame()
        # And fill it with previous list of delivered files
        delivered_files['filepath'] = delivered_file_list
        # Also add basenames (for comparison with database content)
        delivered_files['filename'] = [current_file.name
            for current_file in delivered_file_list]

        # Query ROC database to get list of RPW files with "delivered=True" status
        filters = (FileLog.is_delivered == True)
        # Only process delivered levels
        #filters.append(or_(FileLog.level == 'L0',
        #                   FileLog.level == 'L1',
        #                   FileLog.level == 'L2',
        #                   FileLog.level == 'L3'))
        # query database and return the results as a pandas.DataFrame object
        db_data = query_db(self.session, FileLog.public_filename,
                               filters=filters,
                               tryouts=self.tryouts,
                               wait=self.wait,
                               limit=self.limit,
                               )
        n_data = db_data.shape[0]
        logger.info(f'{n_data} RPW public files found with delivered=True status in ROC database')
        if n_data > 0:
            # Rename field
            db_data.rename(columns={"public_filename": "filename"},
                           inplace=True)

            # keep files found both in the database
            # and the list of files in delivered/ folder
            inserted_files = delivered_files[
                delivered_files.filename.isin(db_data.filename)]
            # Remove files found in the database from delivered/ folder (i.e., move to trash_dir)
            if inserted_files.shape[0] > 0 and clear_delivered:
                inserted_files.apply(
                    lambda x: self.to_trash(x['filepath'], trash_dir=trash_dir),
                    axis=1)
            # Remove filepath column from delivered_files dataframe
            delivered_files.drop(columns=['filepath'], inplace=True)

            # Concatenate "basename" column values from the two dataframes
            delivered_files = pd.concat([db_data, delivered_files]).drop_duplicates(subset=['filename'])

        # return full list of delivered file basenames
        return delivered_files['filename'].values.tolist()

    def to_trash(self, file_path,
                 trash_dir=Path(TRASH_DIR)):
        """
        Move input file to trash directory

        :param file_path: Path of the file to delete
        :param trash_dir: Path of the trash directory
        :return: destination path
        """
        dst = Path(trash_dir) / Path(file_path).name
        shutil.move(str(file_path), str(dst))
        logger.info(f'{file_path} removed')
        return dst

