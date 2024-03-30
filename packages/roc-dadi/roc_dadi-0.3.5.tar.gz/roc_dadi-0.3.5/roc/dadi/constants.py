#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path as osp
from datetime import datetime, timedelta

from poppy.core.conf import settings
from poppy.core.logger import logger

__all__ = ['PLUGIN',
           'PIPELINE_DATABASE',
           'TEST_DATABASE',
            'RPW_FILE_PATTERN',
           '_ROOT_DIRECTORY',
           'TIME_DAILY_STRFORMAT',
           'TIME_INPUT_STRFORMAT',
           'TIME_MONTHLY_STRFORMAT',
           'ARCHIVE_DAILY_SUBDIR',
           'ARCHIVE_MONTHLY_SUBDIR',
           'RPW_PUB_DATA_DIR',
           'RPW_PRIVATE_DATA_DIR',
           'L0_FILE_PATTERN',
           'L0_GENTIME_STRFORMAT',
           'RPW_CDF_PATTERN',
           'ANC_BIA_SWEEP_TABLE_PATTERN',
           'L1_BIA_CURRENT_FILE_PATTERN',
           'SOC_GFTS_DIR',
           'TRASH_DIR',
           'ISSUE_DIR',
           'LOG_DIR',
           'TMP_DIR',
           'INPUT_DIR',
           'ISSUE_SUFFIX',
           'VALID_LEVEL_LIST',
           'TODAY',
           'WAIT_NDAY',
           'CP_START_TIME',
           'FILE_FIELDS_MAX_NUM',
           'FILE_FIELDS_MIN_NUM',
           'LIST_IGNORE_GATT',
           'ACCESS_URL_ROOT',
           'TRYOUTS',
           'TIME_WAIT_SEC',
           'SQL_LIMIT',
           'START_TIME',
           'END_TIME']

# root directory of the module
_ROOT_DIRECTORY = osp.abspath(
    osp.join(
        osp.dirname(__file__),
    )
)

# Name of the plugin
PLUGIN = "roc.dadi"

# Load pipeline database identifier
try:
    PIPELINE_DATABASE = settings.PIPELINE_DATABASE
except Exception:
    PIPELINE_DATABASE = 'PIPELINE_DATABASE'
    logger.warning(f'settings.PIPELINE_DATABASE not defined for {__file__}, \
                     use "{PIPELINE_DATABASE}" by default!')

try:
    TEST_DATABASE = settings.TEST_DATABASE
except Exception:
    TEST_DATABASE = 'TEST_DATABASE'
    logger.warning(f'settings.TEST_DATABASE not defined for {__file__}, \
                     use "{TEST_DATABASE}" by default!')

# Today
TODAY = datetime.now()

# pipeline default directories
INPUT_DIR = '/pipeline/input'
RPW_PUB_DATA_DIR = '/pipeline/data/pub/solo/rpw/data'
RPW_PRIVATE_DATA_DIR = '/pipeline/data/private/solo/rpw/data'
SOC_GFTS_DIR = '/pipeline/data/sftp/soc/gfts'
TRASH_DIR = '/pipeline/.trash'
ISSUE_DIR = '/pipeline/data/private/issues'
LOG_DIR = '/pipeline/logs'
TMP_DIR = '/pipeline/tmp'

# RPW data site URL at LESIA (required to build ACCESS_URL attribute)
ACCESS_URL_ROOT = 'https://rpw.lesia.obspm.fr/roc/data/pub/solo/rpw/data'

# Time string format
TIME_SQL_STRFORMAT = '%Y-%m-%dT%H:%M:%S.%f'
TIME_INPUT_STRFORMAT = '%Y-%m-%dT%H:%M:%S'
TIME_OUTPUT_STRFORMAT = '%Y%m%dT%H%M%S'
TIME_DAILY_STRFORMAT = '%Y%m%d'
TIME_MONTHLY_STRFORMAT = '%Y%m'

# Data archive subdir for daily products
ARCHIVE_DAILY_SUBDIR = '%Y/%m/%d'
ARCHIVE_MONTHLY_SUBDIR = '%Y/%m'

# L0 generation date string format
L0_GENTIME_STRFORMAT = '%Y-%m-%dT%H:%M:%S.%f'

# Number of days to wait before delivering RPW CDAG data V01 files to ESAC
WAIT_NDAY = 30

# Default value for date/time
DEF_DATETIME = datetime(2000, 1, 1)

# Cruise Phase start time
CP_START_TIME = datetime(2020, 6, 15).date()

# Period to process end time (default value is today)
END_TIME = datetime.today()

# Period to process start time (default value is today - 90)
START_TIME = END_TIME - timedelta(days=90)

# RPW L0 daily file pattern
L0_FILE_PATTERN = 'solo_L0_rpw*.h5'

# RPW CDF file pattern
RPW_CDF_PATTERN = 'solo_*_rpw-*_V??.cdf'

# RPW File pattern
RPW_FILE_PATTERN = 'solo_*_rpw*_V??.*'

# RPW BIAS file pattern
ANC_BIA_SWEEP_TABLE_PATTERN = 'solo_ANC_rpw-bia-sweep-table*_V??.csv'
L1_BIA_CURRENT_FILE_PATTERN = 'solo_L1_rpw-bia-current*_V??.cdf'

# Valid data processing levels
VALID_LEVEL_LIST = ['TM', 'TC', 'L0', 'L1', 'L1R', 'L2', 'L3', 'HK', 'ANC']

# Maximal/Minimal expected number of fields in the filename (underscore
# separator)
FILE_FIELDS_MIN_NUM = 5
FILE_FIELDS_MAX_NUM = 6

# Issue subdir suffix
# (added at the end of the output subdirectory when moved into issue dir)
ISSUE_SUFFIX = f"__{datetime.now().strftime('%Y%m%dT%H%M%S')}"

# List of global attributes to ignore
# when comparing to RPW data files
LIST_IGNORE_GATT = [
                    'File_ID',
                    'Data_version',
                    'Generation_date',
                    'Logical_file_id',
                    'Parents',
                    'Parent_version',
                #    'Pipeline_version',
                    'Software_version'
                ]

# Number of database connexion tryouts
TRYOUTS = 3

# Time to wait in seconds between two database connection tryouts
TIME_WAIT_SEC = 3

# Limit of rows to be returned by the database
SQL_LIMIT = 1000000000
