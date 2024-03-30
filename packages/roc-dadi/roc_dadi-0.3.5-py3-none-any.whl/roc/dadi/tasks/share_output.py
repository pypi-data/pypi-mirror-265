#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from distutils.file_util import copy_file, move_file
from glob import glob
from datetime import datetime
from distutils.dir_util import remove_tree, copy_tree

from poppy.core.logger import logger
from poppy.core.task import Task
from poppy.core.target import FileTarget, PyObjectTarget


__all__ = ['ShareOutput']

from roc.dadi.constants import TRASH_DIR, ISSUE_DIR, RPW_FILE_PATTERN, ISSUE_SUFFIX, LOG_DIR, FILE_FIELDS_MIN_NUM, \
    FILE_FIELDS_MAX_NUM, VALID_LEVEL_LIST
from roc.dadi.tools import remove, get_latest_file, are_same_files, get_new_data_version
from roc.dadi.tools.file_helper import set_data_version


class ShareOutput(Task):
    """
    Share RPW output files in the private data server.
    """
    plugin_name = 'roc.dadi'
    name = 'share_output'

    def add_targets(self):
        self.add_input(
                        identifier='source_dir',
                        target_class=PyObjectTarget,
                        filepath = self.get_source_dir,
                        many=True,
                       )
        self.add_input(
                        identifier='target_dir',
                        target_class=PyObjectTarget,
                        filepath = self.get_target_dir,
                        many=False,
                       )
    def get_source_dir(self, pipeline):
        try:
            source_dir = pipeline.args.source_dir
            if not isinstance(source_dir, list):
                source_dir = [source_dir]
            return source_dir
        except:
            # If not defined as input argument, then assume that it is already
            # defined as target input
            pass

    def get_target_dir(self, pipeline):
        try:
            return pipeline.args.target_dir
        except:
            # If not defined as input argument, then assume that it is already
            # defined as target input
            pass

    def setup_inputs(self):

        # Get input targets
        self.source_dir = self.inputs['source_dir'].filepath
        self.target_dir = self.inputs['target_dir'].filepath

        # Check target directory existence
        if not os.path.isdir(self.target_dir):
            raise FileNotFoundError(f'{self.target_dir} not found, aborting')
        else:
            self.target_dir = os.path.abspath(self.target_dir)

        # Get input parameters
        self.start_time = self.pipeline.get(
            'start_time', default=[None])[0]
        self.end_time = self.pipeline.get(
            'end_time', default=[None])[0]
        self.trash_dir = self.pipeline.get(
            'trash_dir', default=[TRASH_DIR])[0]
        self.issue_dir = self.pipeline.get(
            'issue_dir', default=[ISSUE_DIR])[0]
        self.log_dir = self.pipeline.get(
            'log_dir', default=[LOG_DIR])[0]
        self.exclude = self.pipeline.get(
            'exclude', default=[]
        )

        # Get input keywords
        self.clean_input_dir = self.pipeline.get(
            'clean_input_dir', default=[None])[0]
        self.clean_formers = self.pipeline.get(
            'clean_formers', default=False)
        self.clean_src_dir = self.pipeline.get(
            'clean_src_dir', default=False)
        self.clean_src_file = self.pipeline.get(
            'clean_src_file', default=False)
        self.clean_empty = self.pipeline.get(
            'clean_empty', default=False)
        self.update = self.pipeline.get(
            'update', default=False)
        self.force = self.pipeline.get(
            'force', default=False)
        self.is_plot = self.pipeline.get(
            'is_plot', default=False)
        self.compare = self.pipeline.get(
            'compare', default=False)

        # Initialize file status with keywords
        # [shared, failed, ignored, skipped, invalid]
        # directories (?)
        self.file_status = {'shared': [],
                            'failed': [],
                            'ignored': [],
                            'skipped': [],
                            'invalid': []}

    def run(self):

        logger.debug('[ShareData]: Task is starting')
        try:
            self.setup_inputs()
        except:
            logger.exception('[ShareData]: Initializing inputs has failed!')
            self.pipeline.exit()
            return

        # Get number of source directories
        source_dir_num = len(self.source_dir)

        # Loop over input source directories
        for i, source_dir in enumerate(self.source_dir):

            # Check source directory existences
            if not os.path.isdir(source_dir):
                raise FileNotFoundError(f'{source_dir} not found, aborting')
            else:
                source_dir = os.path.abspath(source_dir)
                source_basedir = os.path.basename(source_dir)
                logger.info(f'Processing {source_dir}    ({source_dir_num - i - 1} remaining directories')

            # Check if there is no lock file inside source directory
            # (if lock file found, it means that the pipeline job is still in progress)
            lock_file = glob(os.path.join(source_dir, '*.lock'))
            if lock_file:
                logger.warning(f'Lock file found inside {source_dir}, skip sharing')
                continue

            # Set some local variables
            clean_src_dir = self.clean_src_dir
            clean_input_dir = self.clean_input_dir

            # Check if source_dir contains SOLO RPW product files
            rpw_files = glob(os.path.join(source_dir, RPW_FILE_PATTERN))

            # Get number of files
            rpw_files_num = len(rpw_files)

            # Check if failed subdir found in source_dir
            failed_dir = os.path.join(source_dir, 'failed')
            if (rpw_files_num == 0 and
                not os.path.isdir(failed_dir) and
                not self.clean_empty):

                # if input_dir passed, then remove directory containing input
                # file used during pipeline run
                # (input and output sub-directories must have the same name)
                if clean_input_dir is not None:
                    current_input_dirname = os.path.join(clean_input_dir,
                                                         os.path.basename(source_dir))
                    if os.path.isdir(current_input_dirname):
                        logger.info(f'Removing {current_input_dirname}')
                        remove_tree(current_input_dirname)

                logger.info(f'{source_dir} is empty, skip sharing.')
                continue

            elif (rpw_files_num == 0 and
                  not os.path.isdir(failed_dir) and
                  self.clean_empty):
                # If there is no RPW output file in source directory
                # and clean_empty == True then delete source directory
                logger.info(f'{source_dir} is empty, cleaning directory')
                remove_tree(source_dir)

                # if input_dir passed, then remove directory containing input
                # file used during pipeline run
                # (input and output sub-directories must have the same name)
                if clean_input_dir is not None:
                    current_input_dirname = os.path.join(clean_input_dir,
                                                         os.path.basename(source_dir))
                    if os.path.isdir(current_input_dirname):
                        logger.info(f'Removing {current_input_dirname}')
                        remove_tree(current_input_dirname)

                logger.info(f'{source_dir} is empty, skip sharing.')
                continue

            elif os.path.isdir(failed_dir) and os.path.isdir(self.issue_dir):
                # If there is a "failed" subdir and issue-dir input argument is passed
                # move source directory into issue directory
                # (Append the __<now> suffix to the source directory,
                # where <now> is the current date/time)
                logger.warning(f'{source_dir} has failed element(s)')
                dst_dir = os.path.join(self.issue_dir, source_basedir + ISSUE_SUFFIX)
                copy_tree(source_dir, dst_dir)
                if self.log_dir and os.path.isdir(self.log_dir):
                    copy_tree(self.log_dir, os.path.join(dst_dir, 'logs'))
                logger.warning(f'Copy of {source_dir} has been saved in {dst_dir}')

                # if input_dir passed, then remove directory containing input
                # file used during pipeline run
                # (input and output sub-directories must have the same name)
                if clean_input_dir is not None:
                    current_input_dirname = os.path.join(clean_input_dir,
                                                         os.path.basename(source_dir))
                    if os.path.isdir(current_input_dirname):
                        logger.info(f'Removing {current_input_dirname}')
                        remove_tree(current_input_dirname)

                # Finally delete source directory where outputs have been originally
                # saved
                if clean_src_dir and os.path.isdir(source_dir):
                    # then remove also source files directory
                    remove(source_dir, rmtree=True, trash_dir=self.trash_dir)

                # Exit program
                logger.info(f'{source_dir} is failed, skip sharing.')
                continue

            # Loop over RPW product files found in source_dir
            copied_files = []
            for i, current_file in enumerate(rpw_files):

                logger.info(f'Sharing {current_file} '
                            f'({rpw_files_num - i - 1} remaining files in {source_dir})')

                # Get file basename
                basename = os.path.basename(current_file)

                # Do not share files in ignored list (if provided)
                is_ignored = [
                    True for ignore_item in self.exclude
                    if ignore_item in basename]
                if len(is_ignored) > 0:
                    logger.info(f'{current_file} ignored')
                    self.file_status['ignored'].append(current_file)
                    continue

                # Extract fields in the basename without extension
                # (file format must be '<source>_<level>_<descriptor>_<datetime>_V<data_version>_<free_field>.cdf', with <free_field> is optional)
                fields = os.path.splitext(basename)[0].split('_')
                fields_num = len(fields)

                # Check that there is the expected number of fields
                if (fields_num < FILE_FIELDS_MIN_NUM or
                    fields_num > FILE_FIELDS_MAX_NUM):
                    logger.error(f'Filename is not valid for {current_file}, skip file')
                    self.file_status['invalid'].append(current_file)
                    continue

                # Get processing level
                level = fields[1]

                # Get descriptor
                descriptor = fields[2]

                # Extract year, month and day of file from <datetime> field
                # N.B. If <datetime> format is time range (i.e., YYYYMMDDThhnnss-YYYYMMDDThhnnss)
                # Get year, month and day of the startime
                yyyy = fields[3][:4]
                mm = fields[3][4:6]
                dd = fields[3][6:8]
                file_time = datetime(int(yyyy), int(mm), int(dd))

                # Compare with input start_time/end_time filter values (if passed)
                if self.start_time and self.start_time.date() > file_time.date():
                    logger.info(f'{current_file} older than {self.start_time.date()}, ignore it')
                    self.file_status['ignored'].append(current_file)
                    continue
                if self.end_time and self.end_time.date() < file_time.date():
                    logger.info(f'{current_file} newer than {self.end_time.date()}, ignore it')
                    self.file_status['ignored'].append(current_file)
                    continue

                # Check that level is valid
                if level not in VALID_LEVEL_LIST:
                    logger.error(f'{level} is not valid in {current_file}, skip file.\n'
                                 f'(Valid levels are:{VALID_LEVEL_LIST}')
                    self.file_status['invalid'].append(current_file)
                    continue

                # Get file pattern without version and extension
                # (Used to search for existing files)
                file_pattern = '_'.join(fields[:4]) + '_*'

                # If RPW files to share are plots,
                # platform or BIAS data then target subfolder has a specific name
                if self.is_plot:
                    level = 'Summary_plots'

                if descriptor.startswith('platform'):
                    # Specific case of SOLO HK platform file
                    level = 'SOLO_HK'
                    # Build corresponding subdir name
                    target_subdir = os.path.join(level, yyyy, mm, dd)
                elif descriptor.startswith('rpw-bia-sweep-table'):
                    # Specific case of BIAS sweep data table
                    level = 'BIA'
                    # Build corresponding subdir name
                    target_subdir = os.path.join(level, 'ANC')
                    # Change file pattern to remove time range field
                    file_pattern = '_'.join(fields[:3]) + '_*'
                elif (descriptor.startswith('rpw-bia-sweep') or
                      descriptor.startswith('rpw-bia-current')):
                    # Specific case of BIAS current/sweep data
                    level = 'BIA'
                    # Build corresponding subdir name
                    target_subdir = os.path.join(level, yyyy, mm)
                else:
                    # Build corresponding subdir name
                    # (By default assuming daily subdir)
                    target_subdir = os.path.join(level, yyyy, mm, dd)

                # Build target directory path for current file to move
                # and check existence
                # (if not found, make it)
                target_dirpath = os.path.join(self.target_dir, target_subdir)

                if not os.path.isdir(target_dirpath):
                    logger.info(f'Making {target_dirpath}')
                    os.makedirs(target_dirpath)
                target_filepath = os.path.join(target_dirpath, basename)

                # Check for existing files
                existing_file_list = glob(os.path.join(target_dirpath, file_pattern))
                existing_file_num = len(existing_file_list)

                # Possible cases
                if existing_file_num == 0:
                    # If no existing file found, just copy
                    copy_file(current_file, target_filepath)
                    logger.info(f'{current_file} copied into {target_filepath}')
                    self.file_status['shared'].append(current_file)
                elif existing_file_num != 0 and self.force:
                    logger.warning(f'{current_file} already exists and will be superseded')
                    copy_file(current_file, target_filepath)
                    logger.info(f'{current_file} copied into {target_filepath}')
                    self.file_status['shared'].append(current_file)
                else:

                    # if compare=True and source/target files are the same...
                    current_latest_file = get_latest_file(existing_file_list)
                    if self.compare and are_same_files(current_file, current_latest_file):
                        # Then it doesn't need to make a copy
                        logger.info(f'{current_file}: same content found in {target_dirpath}, skip sharing')
                        # target filepath is set to the latest version file in
                        # the RPW data server
                        target_filepath = current_latest_file
                        self.file_status['skipped'].append(current_file)

                    # if update=True, then try to copy a new version of the file
                    elif self.update:
                        try:
                            # Define new version of the file
                            new_data_version = get_new_data_version(existing_file_list)

                            target_filepath = set_data_version([current_file],
                                                               [new_data_version],
                                                               build_dir=target_dirpath)[0]

                            self.file_status['shared'].append(current_file)
                            # If older files exist and clean_formers keyword is True,
                            # then move older files into a 'former_versions'
                            # subdirectory
                            if self.clean_formers:
                                former_dir = os.path.join(
                                    target_dirpath, 'former_versions')
                                if not os.path.isdir(former_dir):
                                    os.makedirs(former_dir)
                                for existing_file in existing_file_list:
                                    logger.info(f'Moving older {existing_file} into {former_dir}')
                                    target_former_path = os.path.join(former_dir,
                                                                      os.path.basename(existing_file))
                                    if os.path.isfile(target_former_path):
                                        logger.warning(f'{target_former_path} already exists and will be replaced!')
                                        os.remove(target_former_path)
                                    move_file(existing_file,
                                              target_former_path)
                        except:
                            logger.exception(f'Cannot generate new version for {current_file}')
                            self.file_status['failed'].append(current_file)
                            continue
                    else:
                        # Otherwise skip copy
                        logger.warning(f'{target_filepath} already found in {target_dirpath}, skip sharing')
                        self.file_status['skipped'].append(current_file)
                        continue

                if not os.path.isfile(target_filepath):
                    logger.error(f'Copying {current_file} into {target_dirpath} has failed!')

                    # Remove from "shared" file status list and add it to "failed"
                    if current_file in self.file_status['shared']:
                        self.file_status['shared'].remove(current_file)
                    if current_file not in self.file_status['failed']:
                        self.file_status['failed'].append(current_file)

                    # if failure, do not delete source files/dirs
                    clean_src_dir = False
                    clean_input_dir = None
                else:
                    copied_files.append(current_file)
                    # If clean_src_file is True, then remove source files (i.e., copied
                    # files)
                    if self.clean_src_file:
                        remove(current_file, trash_dir=self.trash_dir)

            # From list of well copied files
            for current_file in copied_files:

                # If clean_src_dir is True ...
                current_dirname = os.path.dirname(current_file)
                if clean_src_dir and os.path.isdir(current_dirname):
                    # then remove also source files directory
                    remove(current_dirname, rmtree=True, trash_dir=self.trash_dir)

                # if input_dir passed, then remove directory containing input
                # file used during pipeline run
                # (input and output sub-directories must have the same name)
                if clean_input_dir is not None:
                    current_input_dirname = os.path.join(clean_input_dir,
                                                         os.path.basename(current_dirname))
                    if os.path.isdir(current_input_dirname):
                        logger.info(f'Removing {current_input_dirname}')
                        remove_tree(current_input_dirname)

        # Get final file status overall the folders processed
        file_num = sum([len(val) for val in self.file_status.values()])
        logger.info(f'Final sharing status for {file_num} files in {source_dir_num} input directories is:')
        for key, val in self.file_status.items():
            logger.info(f'--> {len(val)} {key} file(s)')

