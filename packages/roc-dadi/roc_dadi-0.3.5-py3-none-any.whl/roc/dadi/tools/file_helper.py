#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import glob
import os
import shutil
import sys
from pathlib import Path
from datetime import datetime
from distutils.dir_util import remove_tree, copy_tree
from distutils.file_util import copy_file

import spacepy
import h5py
from poppy.core.logger import logger

from roc.dadi.constants import TRASH_DIR, TMP_DIR, LIST_IGNORE_GATT

__all__ = ['get_from_env',
           'valid_dir',
           'get_latest_file',
           'get_new_data_version',
           'set_data_version',
           'set_cdf_version',
           'set_l0_version',
           'are_same_files',
           'remove',
           'extract_file_fields',
           'open_file',
           'date_of_file',
           'update_target_file',
           'glob_file_list',
           'get_l0_attr',
           'is_validate']


def get_from_env(varname, task,
            env_varname=None,
            is_arg=False):
    """
    Try to return a variable value
    from the pipeline environment
    (from property, config file or shell environment)

    :param varname: Name of the variable to get
    :param task: Current POPPy Task instance
    :param env_varname: name of the variable in the config file or environment
    :param is_arg: if True check in the pipeline input arguments list
    :return: value of the variable. Return NoneType if not found.
    """

    # If env varname is not defined
    # try using the varname but in uppercase
    if not env_varname:
        env_varname = varname.upper()

    # 1. Try to get variable value from pipeline properties
    var_value = task.pipeline.get(varname,
                                    default=[None],
                                    args=is_arg)[0]

    if var_value is None:
        # 2. Else try from the pipeline configuration JSON file
        if env_varname in task.pipeline.properties.configuration["environment"]:
            var_value = task.pipeline.properties.configuration[
                f"environment.{env_varname}"]
        # 3. Else try from the OS environment
        elif env_varname in os.environ:
            var_value = os.environ[env_varname]
        else:
            logger.debug(f'{env_varname} not defined in environment')

    return var_value


def valid_dir(path):

    if path:
        try:
            if not os.path.isdir(path):
                print(f'{path} not found!')
                raise IsADirectoryError
        except:
            logger.exception(f'Invalid input {path}!')
            raise ValueError
        else:
            return path

def get_latest_file(file_list):
    """
    Get the latest version file from an input list of files.
    Input files must be formatted using ROC standards
    and must be from the same dataset (i.e., only date and/or version must differ).

    :param file_list: List of input files
    :return: path to the latest file
    """

    # Ordering input file list by alphabetical/numerical characters
    file_list.sort(key=lambda x: os.path.basename(x))

    return file_list[-1]


def get_new_data_version(existing_file_list):
    """
    From a list of input RPW data files, define the
    version of new data file to be shared.

    Process is getting the higher file version from input list,
    then increment it by 1.
    (RPW data file naming convention must apply to input list.
    input list must only contain same RPW data products)

    :param existing_file_list: List of RPW data files
    :return: new data version as an integer
    """

    # Step 1. Extract data file version from
    # the latest file in the input list
    latest_file = get_latest_file(existing_file_list)
    # Version 'VXX' should be the 5th field in the file name
    # (keep version without the 'V' prefix)
    latest_version = os.path.basename(
        os.path.splitext(latest_file)[0]).split('_')[4]
    if latest_version.startswith('V'):
        latest_version = latest_version[1:]
    return int(latest_version) + 1


def remove(item_to_remove,
           rmtree=False,
           trash_dir=TRASH_DIR):
    """
    Remove input item (or move it into a trash directory)

    """

    if os.path.isdir(trash_dir):
        logger.info(f'Copying {item_to_remove} to {trash_dir}')
        basename = os.path.basename(item_to_remove)
        dst = os.path.join(trash_dir, basename)
        if os.path.isdir(item_to_remove):
            copy_tree(item_to_remove, dst)
        else:
            copy_file(item_to_remove, dst)

    logger.info(f'Removing {item_to_remove}')
    if rmtree:
        remove_tree(item_to_remove)
    else:
        os.remove(item_to_remove)


def are_same_files(file1, file2,
                   list_ignore_gatt=LIST_IGNORE_GATT):
    """
    Compare two input files.
    (Only works with the CDF, CSV or XML files for the moment.)

    :param file1: First file to compare
    :param file2: Second file to compare
    :param list_ignore_gatt: List of global attributes to ignore
    :return: True if the two files are identical, False otherwise
    """
    # Initialize output
    same_file = False

    if file1.endswith('.cdf') and file2.endswith('.cdf'):
        # For CDF files, use cdf_compare method of maser4py
        try:
            from maser.tools.cdf.cdfcompare import cdf_compare
        except:
            sys.exit('Cannot import maser module!')

        same_file = not cdf_compare(file1, file2,
                                    list_ignore_gatt=list_ignore_gatt)
    elif file1.endswith('.csv') and file2.endswith('.csv'):
        # For csv files, use filecmp module
        import filecmp
        same_file = filecmp.cmp(file1, file2)
    elif file1.endswith('.xml') and file2.endswith('.xml'):
        import xmltodict
        with open(file1, 'r') as xml:
            xml1 = xmltodict.parse(xml.read())
        with open(file2, 'r') as xml:
            xml2 = xmltodict.parse(xml.read())

        try:
            assert xml1 == xml2
        except:
            same_file = False
        else:
            same_file = True

    return same_file


def set_data_version(input_file_list, data_version_list,
                     build_dir=TMP_DIR):

    if not os.path.isdir(build_dir):
        logger.info(f'Making {build_dir}')
        os.makedirs(build_dir)

    input_file_num = len(input_file_list)
    data_version_num = len(data_version_list)

    if input_file_num == 0:
        logger.info('Empty list of input file, exiting')
        return []

    if data_version_num == 1 and input_file_num > 1:
        data_version_num = input_file_num
        data_version_list = [data_version_list[0]] * input_file_num
    elif data_version_num != input_file_num:
        logger.error(f'input_files and data_version lists have not the same number of elements, aborting!')
        return []
    else:
        logger.info(f'{input_file_num} files to update')

    # Loop over each file in the list
    new_version_file_list = []
    for i, current_file in enumerate(input_file_list):

        new_data_version = valid_data_version(data_version_list[i])
        if not new_data_version.startswith('V'):
            new_data_version = 'V' + new_data_version

        # Extract filename fields
        basename = os.path.basename(current_file)
        basename_without_ext = os.path.splitext(basename)[0]
        basename_fields = basename_without_ext.split('_')
        level = basename_fields[1]
        descriptor = basename_fields[2]
        old_data_version = basename_fields[4]

        # Identify level of RPW file and define the method to use
        if level == 'TM' or level == 'TC':
            # No metadata about version in the TM/TC files
            current_func = None
        elif level == 'L0':
            current_func = set_l0_version
        elif level == 'L1':
            current_func = set_cdf_version
        elif level == 'L2':
            current_func = set_cdf_version
        elif level == 'HK' and descriptor.startswith('rpw'):
            current_func = set_cdf_version
        elif level == 'ANC':
            # No metadata about version in the ANC file (for the moment)
            current_func = None
        elif level == 'HK' and descriptor.startswith('platform'):
            # If HK platform XML file, no metadata to set
            current_func = None
        else:
            logger.warning(f'Level {level} is not valid in {current_file}, skipping')
            continue

        # First make a copy of the file in the build directory
        # with the new data version in the filename
        new_basename = basename.replace(old_data_version, new_data_version)

        # Copy file with new name into build directory
        new_filepath = os.path.join(build_dir, new_basename)
        logger.info(f'Copying {current_file} in {new_filepath}')
        shutil.copyfile(current_file, new_filepath)

        if not os.path.isfile(new_filepath):
            logger.error(f'Copying {new_filepath} has failed!')
            return []

        # Update the data version value in the file metadata
        # (depending of the level of file)
        try:
            if current_func:
                target_file = current_func(new_filepath, data_version_list[i])
        except:
            logger.exception(f'Updating {new_filepath} has failed')
        else:
            logger.info(f'{new_filepath} updated')
            new_version_file_list.append(new_filepath)

    return new_version_file_list


def set_l0_version(l0_file, data_version):
    """
    Set version in the metadata of the input l0 file

    :param l0_file: Input L0 file to update
    :param data_version: version of the file
    :return: True if CDF is well updated, False otherwise
    """
    import h5py
    is_updated = True
    try:
        # Update L0 content
        with h5py.File(l0_file, 'a') as l0:
            l0.attrs['Data_version'] = data_version
            l0.attrs['Logical_file_id'] = os.path.splitext(
                os.path.basename(l0_file))[0]
    except:
        logger.exception(f'Updating {l0_file} has failed!')
        is_updated = False

    return is_updated

def set_cdf_version(cdf_file, data_version):
    """
    Set the version in the metadata of the input CDF file

    :param cdf_file: Path of the CDF file to update (string)
    :param data_version: version of the data file (string)
    :return: True if file is well updated, False otherwise
    """
    from spacepy.pycdf import CDF
    is_updated = True
    try:
        # Update CDF g.attribute
        with CDF(cdf_file) as cdf:
            cdf.readonly(False)
            cdf.attrs['Data_version'][0] = data_version
            cdf.attrs['Logical_file_id'][0] = os.path.splitext(
                os.path.basename(cdf_file))[0]
    except:
        logger.exception(f'Updating {cdf_file} has failed!')
        is_updated = False

    return is_updated

def is_dir(dir):

    if not os.path.isdir(dir):
        logger.error(f'{dir} is not a valid directory')
        raise NotADirectoryError
    else:
        return dir


def valid_data_version(data_version):
    """
    Make sure to have a valid data version.

    :param data_version: integer or string containing the data version
    :return: string containing valid data version (i.e., 2 digits string)
    """
    try:
        data_version = int(data_version)
        return f'{data_version:02d}'
    except:
        raise ValueError(f'Input value for data_version is not valid! ({data_version})')

def extract_file_fields(rpw_file):
    """
    Extract fields from input rpw file.
    Filename must be compliant with SOLO data standards.

    :param rpw_file: input RPW file (Path object)
    :return: tuple containing fields
    """
    basename = Path(rpw_file).stem
    # Return fields
    # should be
    # (source, version, descriptor, datetime, version, free_field)
    # N.B. free_field is optional
    return basename.split('_')

def open_file(rpw_file,
              read_only=False):
    """
    Open input file (must be a CDF or HDF5 format file).

    :param rpw_file: file to open (Path object)
    :param read_only: If True, do a read-only opening
    :return: file buffer
    """
    file_buffer = None
    extension = rpw_file.suffix
    if extension == '.h5':
        import h5py
        if read_only:
            file_access = 'r'
        else:
            file_access = 'a'
        file_buffer = h5py.File(str(rpw_file), file_access)
    elif extension == '.cdf':
        from spacepy.pycdf import CDF
        file_buffer = CDF(str(rpw_file))
        file_buffer.readonly(read_only)
    else:
        raise IOError

    return file_buffer


def update_target_file(rpw_file, attributes_to_set):
    """
    # Update file attributes in the input RPW file

    :param rpw_file: input rpw file to update (pathlib.Path object)
    :param attributes_to_set: Dictionary with attributes to update (key=name, val=entries)
    :return:True if file has been correctly updated, False otherwise
    """
    is_updated = False

    # Open file
    try:
        buffer = open_file(rpw_file, read_only=False)
    except:
        logger.exception(f'Cannot open {rpw_file}!')
    else:
        for key, val in attributes_to_set.items():
            buffer.attrs[key] = val
            logger.debug(f'Changing {key} to {val} in {rpw_file}')
        buffer.close()

        is_updated = True

    return is_updated


def date_of_file(rpw_file):
    """
    Return date of the input RPW file.
    Date is extracted from the filename (assuming Solar Orbiter file naming convention)

    :param rpw_file: input RPW file
    :return: datetime of the RPW file
    """

    # Extract fields in the basename without extension
    # (file format must be '<source>_<level>_<descriptor>_<datetime>_V<data_version>_<free_field>.cdf', with <free_field> is optional)
    fields = extract_file_fields(rpw_file)

    # Extract year, month and day of file from <datetime> field
    # N.B. If <datetime> format is time range (i.e., YYYYMMDDThhnnss-YYYYMMDDThhnnss)
    # Get year, month and day of the startime
    yyyy = fields[3][:4]
    mm = fields[3][4:6]
    dd = fields[3][6:8]

    return datetime(int(yyyy), int(mm), int(dd))

def glob_file_list(file_list, as_path=False):
    """
    Perform glob.glob method for each file in the input list.
    If input argument file_list is a string, then first apply split() method on it.

    :param file_list: List of files to glob.
                      Can be a string or list of strings or pathlib.Path objects.
    :param as_path: Force output list of files to be pathlib.Path objects
    :return: list of files as returned by glob.glob() method
    """
    # Initialize output list
    globbed_list = []
    # Be sure that input file_list argument is a list
    if not isinstance(file_list, (list,)):
        file_list = [file_list]

    # For each file in the list, run glob.glob() method
    for current_file in file_list:
        for current_path in str(current_file).split():
            globbed_list.extend(list(glob.glob(current_path)))

    if as_path:
        globbed_list = [Path(current_file)
                        for current_file in globbed_list]

    return globbed_list


def get_l0_attr(l0_file, attr_name,
                strftime=None):
    """
    Get RPW L0 HDF5 root attribute value

    :param l0_file: Path of the l0 file
    :param attr_name: Name of the root attribute
    :param strftime: If attribute is a date/time, specify format to be passed to datetime
    :return: attribute value
    """

    attr_value = None
    try:
        with h5py.File(l0_file, 'r') as l0:
            attr_value = l0.attrs[attr_name]
    except:
        logger.warning(f'{attr_name} cannot be retrieved from {l0_file}')
    else:
        if strftime:
            attr_value = datetime.strptime(attr_value, strftime)

    return attr_value


def is_validate(current_file):
    """
    Returns True if input file is flagged as validate (Validate = 1),
    False otherwise.
    Only CDF files with Validate g.attribute are checked for the moment.

    :param current_file: CDF file to check
    :return: True if CDF file is validate, False otherwise
    """
    is_valid = False

    try:
        # Open CDF and check Validate attribute value
        with spacepy.pycdf.CDF(str(current_file)) as cdf:
            # True if Validate == 1
            is_valid = cdf.attrs["Validate"][0] == 1
    except:
        logger.exception(f'Validate global attribute is not readable in {current_file}!')

    return is_valid
