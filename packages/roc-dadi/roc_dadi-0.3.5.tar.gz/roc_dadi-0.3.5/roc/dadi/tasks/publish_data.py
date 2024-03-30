#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import shutil
from datetime import timedelta
from pathlib import Path

from sqlalchemy import and_

from poppy.core.logger import logger
from poppy.core.task import Task
from poppy.core.target import FileTarget, PyObjectTarget
from poppy.core.db.connector import Connector

from roc.dingo.models.file import FileLog
from roc.dingo.tools import query_db

from roc.dadi.constants import RPW_PRIVATE_DATA_DIR, RPW_PUB_DATA_DIR, CP_START_TIME, TODAY, TRYOUTS, TIME_WAIT_SEC, \
    SQL_LIMIT, PIPELINE_DATABASE, ACCESS_URL_ROOT
from roc.dadi.tools import date_of_file, extract_file_fields, open_file, get_latest_file, get_new_data_version
from roc.dadi.tools.file_helper import valid_data_version, update_target_file


# Tasks to publish RPW data in the ROC public server at LESIA
__all__ = ['PublishData']


class PublishData(Task):
    """
    Publish RPW files in the public data server.
    """
    plugin_name = 'roc.dadi'
    name = 'publish_data'

    def add_targets(self):
        self.add_input(target_class=PyObjectTarget,
                       identifier='rpw_file_pattern',
                       many=False,
                       )
        self.add_output(target_class=FileTarget,
                       identifier='rpw_files',
                       many=True,
                       )

    @Connector.if_connected(PIPELINE_DATABASE)
    def setup_inputs(self):

        # Get list of input rpw files to
        self.rpw_file_pattern = self.inputs['rpw_file_pattern']

        self.private_data_dir = self.pipeline.get(
            'rpw_private_data_dir', default=[RPW_PRIVATE_DATA_DIR]
        )[0]
        self.pub_data_dir = self.pipeline.get(
            'rpw_pub_data_dir', default=[RPW_PUB_DATA_DIR]
        )[0]
        self.latency = self.pipeline.get(
            'wait_nday', default=[None]
        )[0]
        self.exclude = self.pipeline.get(
            'exclude', default=[]
        )
        self.include = self.pipeline.get(
            'include', default=[]
        )
        self.start_time = self.pipeline.get(
            'start_time', default=[None])[0]
        self.end_time = self.pipeline.get(
            'end_time', default=[None])[0]

        # Get input keywords
        self.clean_formers = self.pipeline.get(
            'clean_formers', default=False)
        self.skip_reprocessed = self.pipeline.get(
            'skip_reprocessed', default=False)

        self.published = []
        self.skipped = []
        self.failed = []

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

        logger.debug('[PublishData]: Task is starting')
        try:
            self.setup_inputs()
        except:
            logger.exception('[PublishData]: Initializing inputs has failed!')
            self.pipeline.exit()
            return

        # Check that start_time is not before cruise phase beginning
        start_time = self.start_time
        if start_time < CP_START_TIME:
            logger.error(f'start_time ({start_time.date()}) '
                         f'is before Cruise Phase beginning ({CP_START_TIME}) ')
            return

        # Retrieve list of RPW files to process
        rpw_file_list = list(self.private_data_dir.glob(self.file_pattern))
        rpw_file_num = len(rpw_file_list)

        if rpw_file_num == 0:
            logger.warning(
                f'No RPW file matches with the input pattern {self.private_data_dir / self.file_pattern}')
            return
        else:
            logger.info(
                f'{rpw_file_num} RPW files match with the input pattern "{self.private_data_dir / self.file_pattern}"')

        # We can use a with statement to ensure threads are cleaned up promptly
        for i, rpw_file in enumerate(rpw_file_list):

            if not self.is_expected(rpw_file,
                           start_time=self.start_time,
                           end_time=self.end_time,
                           include=self.include,
                           exclude=self.exclude):
                logger.info(f'{rpw_file} is outside the scope of processing, skip it')
                self.skipped.append(rpw_file)
                continue

            # Get file fields
            file_fields = extract_file_fields(rpw_file)
            source = file_fields[0]
            level = file_fields[1]
            descriptor = file_fields[2].replace('-cdag', '')  # (without -cdag suffix)
            date_time = file_fields[3]
            version = file_fields[4]
            extension = rpw_file.suffix

            # Get the date of the file
            file_datetime = date_of_file(rpw_file)

            if self.latency:
                # if it is the first publication
                # check that the proprietary period to wait is respected
                latency_deadline = (TODAY - timedelta(days=self.latency)).date()

                if file_datetime.date() > latency_deadline:
                    logger.info(
                        f'Skipping {rpw_file} (cannot be published before {(file_datetime + timedelta(days=self.latency)).date()})')
                    self.skipped.append(rpw_file)
                    continue

            # Check from database if file is valid (i.e., file_log.state = "OK")
            if not self.is_state_ok(rpw_file):
                logger.warning(f'{rpw_file} state not is flagged as "OK" in the database and will not published')
                continue

            # Build target file pattern
            target_file_pattern = '_'.join([
                source,
                level,
                descriptor,
                date_time,
            ]) + '*' + extension

            # Get data file subdirectory path
            target_subdir = str(rpw_file.parent).replace(
                str(self.private_data_dir), '')
            if target_subdir.startswith('/'):
                target_subdir = target_subdir[1:]

            # Build file target directory
            target_dir = self.pub_data_dir / Path(target_subdir)

            # Check that target_dir exist
            if not target_dir.is_dir():
                logger.info(f'{target_dir} target directory not found, create it')
                try:
                    target_dir.mkdir(parents=True, exist_ok=True)
                except:
                    raise OSError(f'{target_dir} directory cannot be created!')


            # Check if versions of the file already exist in target_dir
            existing_files = list(target_dir.glob(target_file_pattern))

            # If existing files found, then ...
            new_data_version = 1
            if existing_files:
                # Get latest version file
                latest_file = get_latest_file(existing_files)

                # Check if current file already published
                # (If skip_reprocessed=True, then force skip)
                if self.is_already_published(rpw_file, latest_file) or self.skip_reprocessed:
                    self.skipped.append(rpw_file)
                    continue
                else:
                    # Determinate the version of the target file
                    new_data_version = get_new_data_version(existing_files)

            # Build name and path of the target file to publish
            # (with expected version)
            target_basename = '_'.join([
                source,
                level,
                descriptor,
                date_time,
                'V' + valid_data_version(new_data_version)
            ]) + extension
            target_file = target_dir / target_basename

            # Copy file
            logger.info(f'Publishing {target_file.name} into {target_file.parent} ...')
            shutil.copyfile(str(rpw_file), str(target_file))

            # Update Data_version, Logical_file_id, Validate, ACCESS_URL and add CDAG_PARENT attributes
            # in the target file
            attributes_to_set = dict()
            attributes_to_set['Data_version'] = valid_data_version(new_data_version)
            attributes_to_set['Logical_file_id'] = target_basename.stem
            attributes_to_set['CDAG_PARENT'] = rpw_file.name
            attributes_to_set['ACCESS_URL'] = str(
                Path(ACCESS_URL_ROOT) / Path('/'.join(rpw_file.parts[-5:])))
            attributes_to_set['Validate'] = 1
            if not update_target_file(target_file, attributes_to_set):
                logger.error(f'Updating {target_file} metadata has failed!')
                self.failed.append(rpw_file)
                if target_file.is_file():
                    # remove failed file
                    target_file.unlink()
                continue
            else:
                logger.debug(f'{target_file.name} has been successfully published in {target_file.parent}')
                self.published.append(str(target_file))

                # Clean older files clean_formers == True
                if existing_files and self.clean_formers:
                    former_dir = target_dir / Path('former_versions')
                    if not former_dir.is_dir():
                        former_dir.mkdir()
                    for existing_file in existing_files:
                        shutil.move(str(existing_file), str(former_dir))
                        logger.info(f'{existing_file} moved into {former_dir}')

        self.outputs['rpw_files'].filepath = self.published
        if len(self.published) > 0:
            logger.info(f'{len(self.published)} files have been well published in {self.pub_data_dir}')
        if len(self.skipped) > 0:
            logger.info(f'{len(self.skipped)} files have been skipped')
        if len(self.failed) > 0:
            logger.warning(f'{len(self.failed)} files have not been published in {self.pub_data_dir}')



    def is_already_published(self, rpw_file_to_publish, latest_published_file):
        """
        Check if the RPW "CDAG" file has been already published.

        :param rpw_file_to_publish: RPW "CDAG" to publish
        :param latest_published_file: Latest version of the published file
        :return: True if the RPW "CDAG" to publish has been already published, False otherwise
        """
        is_published = False

        # Open file
        cdag_parent = None
        try:
            buffer = open_file(latest_published_file, read_only=False)

            # and get 'CDAG_PARENT' attribute value
            if latest_published_file.suffix == '.cdf':
                cdag_parent = buffer.attrs['CDAG_PARENT'][...]
            elif latest_published_file.suffix == '.h5':
                cdag_parent = buffer.attrs['CDAG_PARENT']

            # Make sure it is not a list
            if isinstance(cdag_parent, list):
                cdag_parent = cdag_parent[0]
        except:
            logger.exception(f'Cannot open {latest_published_file}!')
            is_published = True
        else:
            buffer.close()

        # Compare 'CDAG_PARENT' attribute value with rpw_file_name
        if rpw_file_to_publish.name == cdag_parent:
            logger.info(f'Skipping {rpw_file_to_publish} (already published as {latest_published_file})')
            is_published = True

        return is_published

    def is_expected(self, rpw_file,
                        start_time=None,
                        end_time=None,
                        include=[],
                        exclude=[]):
        """
        Compare input file against some criteria.

        :param rpw_file: Input file to check (Path object)
        :param start_time: If passed, filter by start_time (datetime.date() object)
        :param end_time: If passed, filter by end_time (datetime.date() object)
        :param cp_start_time: Cruise Phase start time
        :param exclude: If passed, return False if the input file descriptor field is in the exclude list
        :param include: If passed, return True if the input file descriptor field is in the include list
        :return: True if file follow criteria, False otherwise
        """

        # Extract fields in the basename without extension
        # (file format must be '<source>_<level>_<descriptor>_<datetime>_V<data_version>_<free_field>.cdf', with <free_field> is optional)
        fields = extract_file_fields(rpw_file)

        # Extract descriptor (without '-cdag' suffix, if any)
        descriptor = fields[2].replace('-cdag', '')
        # Return False if descriptor is in exclude list
        if descriptor in exclude:
            logger.info(f'Skipping {rpw_file} (dataset in the exclude list)')
            self.skipped += 1
            return False

        # Return False if descriptor is not in the include list (if any)
        if include and descriptor not in include:
            logger.info(f'Skipping {rpw_file} (dataset not in the include list)')
            self.skipped += 1
            return False

        file_date = date_of_file(rpw_file).date()

        # Compare with input start_time/end_time filter values (if passed)
        if start_time and start_time > file_date:
            logger.info(f'Skipping {rpw_file} (older than {start_time})')
            self.skipped += 1
            return False

        if end_time and end_time < file_date:
            logger.info(f'Skipping {rpw_file} (newer than {end_time})')
            self.skipped += 1
            return False

        # Otherwise return True
        return True


    def is_state_ok(self, rpw_file):
        """
        Returns True if the file_log.state database column is "OK" for input file,
        False otherwise

        :param rpw_file: input file to check
        :return: True if file_log.state == 'OK', False otherwise
        """
        is_ok = False

        # Check if input file is in the file_log table
        # and if the state column is "OK"
        filters = (FileLog.basename == rpw_file.name)
        # query database and return the results as a pandas.DataFrame object
        file_state = query_db(self.session, FileLog.state,
                               filters=filters,
                               tryouts=self.tryouts,
                               wait=self.wait,
                               limit=self.limit,
                               )
        # if input file is found in the database and its state is OK,
        # then return True
        if file_state.shape[0] == 1 and file_state['state'][0] == 'OK':
            is_ok = True

        return is_ok
