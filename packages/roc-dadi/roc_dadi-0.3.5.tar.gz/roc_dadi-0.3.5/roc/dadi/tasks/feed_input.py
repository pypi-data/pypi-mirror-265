#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tasks to fill RODP pipeline input directory with input files
in order to run following pipeline commands:
- l0_to_hk
- l0_to_l1_surv
- l0_to_l1_sbm
- l0_to_anc_bia_sweep_table
- l0_to_l1_bia_sweep
- l0_to_l1_bia_current
"""

# ________________ IMPORT _________________________
import uuid

from poppy.core.logger import logger
from poppy.core.task import Task

import shutil
import os
from glob import glob
import calendar
from datetime import datetime, timedelta

from spacepy.pycdf import CDF


from roc.dadi.constants import INPUT_DIR, RPW_PRIVATE_DATA_DIR, START_TIME, END_TIME, \
    TIME_DAILY_STRFORMAT, TIME_MONTHLY_STRFORMAT, L0_FILE_PATTERN, ARCHIVE_DAILY_SUBDIR, ARCHIVE_MONTHLY_SUBDIR, \
    L1_BIA_CURRENT_FILE_PATTERN, L0_GENTIME_STRFORMAT, RPW_CDF_PATTERN, ANC_BIA_SWEEP_TABLE_PATTERN
from roc.dadi.tools import get_latest_file, get_l0_attr

# ________________ Global Variables _____________
# (define here the global variables)

# ________________ Class Definition __________
# (If required, define here classes)

class FeedInput(Task):
    """
    Publish RPW files in the public data server.
    """
    plugin_name = 'roc.dadi'
    name = 'publish_data'

    def add_targets(self):
        pass

    def setup_inputs(self):
        # Data to feed with
        self.rodp_cmd = self.pipeline.get(
            'rodp_cmd', default=None,
        )

        # Time-related input arguments
        self.start_time = self.pipeline.get(
            'start_time', default=[START_TIME],
        )[0]
        self.end_time = self.pipeline.get(
            'start_time', default=[END_TIME],
        )[0]
        self.date_list = self.pipeline.get(
            'date_list', default=[],
        )
        self.month_list = self.pipeline.get(
            'month_list', default=[],
        )

        # Path input arguments
        self.archive_path = self.pipeline.get(
            'rpw_private_data_dir', default=[RPW_PRIVATE_DATA_DIR]
        )[0]
        self.input_dir = self.pipeline.get(
            'input_dir', default=[INPUT_DIR]
        )[0]
        self.l0_path = self.pipeline.get(
            'l0_path', default=[None]
        )[0]
        if not self.l0_path:
            self.l0_path = os.path.join(self.archive_path, 'L0')

        # Boolean input keywords
        self.force = self.pipeline.get(
            'force', default=False
        )
        self.symlink = self.pipeline.get(
            'symlink', default=False
        )

    def run(self):

        # Define task job ID (long and short)
        self.job_uuid = str(uuid.uuid4())
        self.job_id = f'FeedInput-{self.job_uuid[:8]}'
        logger.info(f'Task {self.job_id} is starting')
        try:
            self.setup_inputs()
        except:
            logger.exception(
                f'Initializing inputs has failed for {self.job_id}!')
            self.pipeline.exit()
            return

        # Build list of dates to process
        if self.date_list:
            logger.info(f'DATE_LIST is {self.date_list}')
            self.date_list = [datetime.strptime(current_date, TIME_DAILY_STRFORMAT)
                         for current_date in self.date_list]

            # Make sure that start_time and end_time are well defined
            self.start_time = min(self.date_list)
            self.end_time = max(self.date_list)
        elif self.month_list:
            logger.info(f'MONTH_LIST is {self.month_list}')
            # build list of days from input list of months
            self.date_list = []
            for current_month in self.month_list:
                # Get first day of the month
                self.start_time = datetime.strptime(current_month, TIME_MONTHLY_STRFORMAT)
                mday_num = calendar.monthrange(
                    self.start_time.year, self.start_time.month)[1]
                # Get latest day of the month
                self.end_time = self.start_time + timedelta(days=mday_num - 1)
                # Generate all days of the month
                self.date_list.extend(self.gen_date_list(self.start_time, self.end_time))

            # Make sure that start_time and end_time are well defined
            self.start_time = min(self.date_list)
            self.end_time = max(self.date_list)
        elif self.start_time and self.end_time:
            logger.info(f'START_TIME is {self.start_time}')
            logger.info(f'END_TIME is {self.end_time}')
            self.date_list = self.gen_date_list(self.start_time, self.end_time)
        else:
            logger.error('Missing input to define time range to process!')
            return

        # Loop over dates in order to get list of L0 input files to process
        # (Classify by starttime-endtime or by dates (for daily files)
        key_startend = self.start_time.strftime(
            TIME_DAILY_STRFORMAT) + '-' + self.end_time.strftime(TIME_DAILY_STRFORMAT)
        input_files = {}
        no_anc_file = False
        for current_time in self.date_list:
            # Initialize anc file (for bias sweep products only)
            anc_file = []

            # Get date
            current_date = current_time.date()

            # Build sub-folder from date
            current_subdir = current_time.strftime(ARCHIVE_DAILY_SUBDIR)

            # Get latest L0 file for the current date
            latest_l0 = get_latest_file(glob(os.path.join(self.l0_path,
                                                          current_subdir,
                                                          L0_FILE_PATTERN)))

            if not latest_l0:
                logger.info(f'No L0 daily file for {current_date} in {self.l0_path}')
                # Go to next day
                continue
            else:
                already_processed = False
                # If daily output files production ...
                if self.rodp_cmd == 'l0_to_hk':
                    # Current key is the date to process
                    current_key = current_time.strftime(TIME_DAILY_STRFORMAT)

                    if not self.force:
                        # Check for existing HK for the current date
                        hk_path = os.path.join(self.archive_path, 'HK',
                                               current_time.strftime(ARCHIVE_DAILY_SUBDIR))
                        already_processed = self.is_daily_processed(latest_l0, hk_path)
                elif self.rodp_cmd == 'l0_to_l1_surv':
                    # Current key is the date to process
                    current_key = current_time.strftime(TIME_DAILY_STRFORMAT)

                    if not self.force:
                        # Check for existing HK for the current date
                        l1_path = os.path.join(self.archive_path, 'L1',
                                               current_time.strftime(ARCHIVE_DAILY_SUBDIR))
                        already_processed = self.is_daily_processed(latest_l0, l1_path)
                elif self.rodp_cmd == 'l0_to_l1_bia_sweep':
                    # Key is current time range for bias sweep products
                    current_key = key_startend

                    # For Bias sweep products, check also for ANC bias sweep
                    # table file
                    anc_dir = os.path.join(self.archive_path, 'BIA', 'ANC')
                    anc_file = self.get_bia_anc_sweep_table(anc_dir)
                    if not anc_file and not no_anc_file:
                        logger.warning('No Bias sweep sweep ANC file '
                                       f'found in {anc_dir}!')
                        no_anc_file = True
                elif self.rodp_cmd == 'l0_to_anc_bia_sweep_table':
                    # Else current key is the time range to process
                    current_key = key_startend

                    # For Bias sweep products, check also for ANC bias sweep
                    # table file
                    anc_dir = os.path.join(self.archive_path, 'BIA', 'ANC')
                    anc_file = self.get_bia_anc_sweep_table(anc_dir)
                    if not anc_file and not no_anc_file:
                        logger.warning('No Bias sweep sweep ANC file '
                                       f'found in {anc_dir}!')
                        no_anc_file = True
                elif self.rodp_cmd == 'l0_to_l1_bia_current':
                    # Key is current time month for bias current products
                    current_key = current_time.strftime(TIME_MONTHLY_STRFORMAT)
                else:
                    # Else current key is the time range to process
                    current_key = key_startend

                if already_processed:
                    logger.info(f'{latest_l0} has been already processed, skip it')
                    # If L0 has been already processed, skip it
                    continue
                elif self.rodp_cmd != 'l0_to_l1_bia_current':
                    logger.info(f'{latest_l0} needs to be processed')

                # Initialize list of files for current key (if not already found)
                if current_key not in input_files:
                    input_files[current_key] = []

                # Add current L0 file to the list of files to
                # copy in the input directory for current date/time range
                if latest_l0 not in input_files[current_key]:
                    input_files[current_key].append(latest_l0)

                # If ancillary file must be also copied in the input directory ...
                if anc_file and anc_file not in input_files[current_key]:
                    logger.info(f'Add {anc_file} for {self.rodp_cmd}')
                    input_files[current_key].append(anc_file)

        if len(input_files) == 0:
            logger.warning(f'No input file to process for {self.rodp_cmd} '
                           f'between {self.start_time} and {self.end_time}')
            return

        # Loop over dictionary of input files to process
        for date_to_process, list_of_files in input_files.items():

            # Special case for monthly CDF products (l1_bia_current only for now):
            # Check if every input L0 files for the month are provided and
            # are the latest ones
            if self.rodp_cmd == 'l0_to_l1_bia_current':
                l1_data_pattern = os.path.join(self.archive_path, 'BIA',
                                               datetime.strftime(
                                                   datetime.strptime(
                                                       date_to_process, TIME_MONTHLY_STRFORMAT),
                                                   ARCHIVE_MONTHLY_SUBDIR),
                                               L1_BIA_CURRENT_FILE_PATTERN)

                if self.is_monthly_processed(list_of_files, l1_data_pattern) and not self.force:
                    logger.info(f'l1_bia_current dataset already '
                                f'processed for {date_to_process}, skip it')
                    continue

            # Generate input subdirectory for current command and date
            cmd = ''.join(self.rodp_cmd.split('_')).upper()
            input_subdir = os.path.join(self.input_dir,
                                        f'RODP_{cmd}_{date_to_process}')
            if os.path.isdir(input_subdir):
                if not self.force:
                    logger.warning(f'{input_subdir} already exists, '
                                   f'skip {self.rodp_cmd} execution.')
                    continue
                else:
                    logger.warning(f'{input_subdir} already exists and will be replaced!')
                    shutil.rmtree(input_subdir)

            # Create input subdirectory to host file(s) to process
            logger.info(f'Making {input_subdir}')
            os.makedirs(input_subdir)

            # Copy input files (or build symlink if --symlink is passed)
            for current_file in list_of_files:
                target_path = os.path.join(
                    input_subdir, os.path.basename(current_file))
                if not os.path.isfile(target_path):
                    if self.symlink:
                        logger.info(f'Building symlink {target_path} from {current_file}')
                        os.symlink(current_file, target_path)
                    else:
                        logger.info(f'Copying {current_file} into {input_subdir}')
                        shutil.copyfile(current_file, target_path)
                else:
                    logger.warning(f'{target_path} already exists')

    def is_daily_processed(self, l0_file, existing_path):
        """
        Check if output CDF files already exist for the input L0 file.

        :param l0_file:
        :param existing_path:
        :return:
        """

        if not os.path.isdir(existing_path):
            return False

        # Get L0 creation time
        l0_gen_time = get_l0_attr(l0_file, 'Generation_date',
                                           strftime=L0_GENTIME_STRFORMAT)

        # Get list of CDFs into existing_path
        cdf_files = glob(os.path.join(existing_path, RPW_CDF_PATTERN))
        if not cdf_files:
            return False
        else:
            # and get generation date
            for cdf_file in cdf_files:
                cdf = CDF(cdf_file)
                cdf_gen_time = datetime.strptime(
                    cdf.attrs['Generation_date'][0],
                    L0_GENTIME_STRFORMAT)

                # if L0 file has been generated after the output CDFs
                # then new CDFs need to be re-produced
                if l0_gen_time >= cdf_gen_time:
                    return False

        return True


    def is_monthly_processed(self, list_of_l0, output_file_pattern):
        """
        Check if input list of L0 files need to be processed or not.
        They do if:
            - No expected output file exists already
            - At least one L0 file is new or has upper version w.r.t.
              the L0 parent file list in the existing output file
        Output file is assumed to be a CDF format file.

        :param list_of_l0: Input list of L0 files to process
        :param output_file_pattern: Expected output file pattern
        :return: True if there is no need to process list of input L0 files, False otherwise
        """

        # Get latest existing output file (if any)
        existing_output_file = get_latest_file(glob(output_file_pattern))
        if not existing_output_file:
            # If no output file already produced, then run the processing
            return False

        try:
            # Else retrieve the list of L0 parent files from output file
            # (and corresponding versions)
            cdf = CDF(existing_output_file)
            # Remove 'L0>' prefix and split string into
            # list of L0 files (separator is ',')
            # Make sure to have no blank space
            l0_parent_list = [string.strip() for string in cdf.attrs['Parents'][
                0].split('>')[1].split(',')]
            l0_version_list = [string.strip() for string in cdf.attrs[
                'Parent_version'][0].split(',')]
        except:
            # If cannot read output, then assume processing is needed.
            logger.exception(f'Cannot read {existing_output_file}!')
            return False
        else:
            l0_parent_num = len(l0_parent_list)
            l0_version_num = len(l0_version_list)

        if l0_parent_num == 0:
            # If no l0 parent file found in the output file...
            logger.warning(f'"Parents" g.attribute '
                           f'has no value in {existing_output_file}!')
            # Then assume processing is needed
            return False
        elif l0_parent_num != l0_version_num:
            # If no l0 parent file and version lists has not the same number of
            # elements...
            logger.warning(f'"Parents" and "Parent_version" g.attributes '
                           f'has not the same number of elements in {existing_output_file}! '
                           f'({l0_parent_num} against {l0_version_num})')
            # Then assume processing is needed
            return False
        else:
            # Convert l0 parent list into dictionary
            # with l0 basenames (without _VXX.cdf suffix) as keys
            # and corresponding versions as values
            l0_parent_dict = {'_'.join(os.path.basename(current_l0).split('_')[:4]): l0_version_list[i]
                              for i, current_l0 in enumerate(l0_parent_list)
                              }

        # Compare L0 parent files into the output file
        # with the list loaded by the program
        for current_l0 in list_of_l0:
            # Extract l0 basename (without _VXX.cdf suffix) and version
            l0_fields = os.path.splitext(os.path.basename(current_l0))[
                0].split('_')
            l0_prefix = '_'.join(l0_fields[:4])
            l0_version = l0_fields[4][1:]

            # Then check w.r.t the l0 parent files in the ouput file
            if l0_prefix not in l0_parent_dict:
                # If l0 is not found in the parent list, then processing is required
                # (i.e., new L0 has been generated since the latest output file creation)
                logger.info(f'{current_l0} has not been processed')
                return False
            elif l0_parent_dict[l0_prefix] < l0_version:
                # If version of the parent file is lesser than the input l0
                # Then processing is required
                logger.info(f'{current_l0} is a new version to process')
                return False
            else:
                logger.debug(f'{current_l0} already found in {existing_output_file}')

        return True


    def get_bia_anc_sweep_table(self, sweep_table_dir):
        """
        Get latest RPW Bias sweep table anc file.

        :param sweep_table_dir: Directory where RPW anc bias sweep table data file is stored
        :return: RPW Bias sweep table anc file found
        """

        return get_latest_file(glob(os.path.join(
            sweep_table_dir, ANC_BIA_SWEEP_TABLE_PATTERN)))


    def gen_date_list(self, start_time, end_time):
        """
        Generate a list of datetime objects between start_time
        and end_time

        :param start_time:
        :param end_time:
        :return:
        """
        date_list = []
        current_time = start_time
        while current_time <= end_time:
            date_list.append(current_time)
            current_time += timedelta(days=1)
        return date_list

# ________________ Global Functions __________
# (If required, define here global functions)













