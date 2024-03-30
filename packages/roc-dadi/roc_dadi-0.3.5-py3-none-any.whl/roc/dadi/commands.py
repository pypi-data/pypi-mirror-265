#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Commands for DADI plugin.
"""

from pathlib import Path

from poppy.core.command import Command
from poppy.core.tools.exceptions import MissingArgument
from poppy.core.logger import logger

#from roc.dadi.tasks import FetchData
from roc.dadi.tasks.deliver_data import DeliverData
from roc.dadi.tasks.publish_data import PublishData
from roc.dadi.tasks.share_output import ShareOutput
from roc.dadi.constants import RPW_PRIVATE_DATA_DIR, RPW_PUB_DATA_DIR, SOC_GFTS_DIR, ISSUE_DIR, TRASH_DIR, LOG_DIR, \
    WAIT_NDAY, INPUT_DIR
from roc.dadi.tools import valid_dir
from roc.dadi.tools.time import valid_date

__all__ = ['DadiCommand', 'DeliverDataCmd']

class DadiCommand(Command):
    __command__ = "dadi"
    __command_name__ = "dadi"
    __parent__ = "master"
    __parent_arguments__ = ["base"]
    __help__ = "Commands relative to the Data Dispatcher (DADI) plugin"

    def add_arguments(self, parser):
        """
        Add input arguments common to all the FILM plugin.

        :param parser: high-level pipeline parser
        :return:
        """
        parser.add_argument(
            '-s', '--start-time',
            nargs=1,
            type=valid_date,
            help='Filter file to share by start time. '
            'Valid format is %%Y%%m%%d',
            default=[None])
        parser.add_argument(
            '-e', '--end-time',
            nargs=1,
            type=valid_date,
            help='Filter file to share by end time. '
            'Valid format is %%Y%%m%%d',
            default=[None])

        parser.add_argument(
            '--rpw-private-data-dir',
            help='RPW private data directory path',
            default=[RPW_PRIVATE_DATA_DIR],
            nargs=1,
            type=str,
        )

        parser.add_argument(
            '--rpw-pub-data-dir',
            help='RPW public data directory path',
            default=[RPW_PUB_DATA_DIR],
            nargs=1,
            type=str,
        )

        parser.add_argument(
            '--soc-gfts-dir',
            help='SOC GFTS root directory path',
            default=[SOC_GFTS_DIR],
            nargs=1,
            type=str,
        )

        parser.add_argument('-i', '--input-dir',
                            nargs=1,
                            type=valid_dir,
                            help='RODP pipeline input directory '
                                 f'Default is {INPUT_DIR}',
                            default=[INPUT_DIR])

        parser.add_argument(
            '--trash-dir',
            help='trash directory path',
            default=[TRASH_DIR],
            nargs=1,
            type=str,
        )

        parser.add_argument(
            '-x', '--exclude',
            nargs='+',
            type=str,
            default=[],
            help='List of RPW data products to exclude.'
        )
        parser.add_argument(
            '-c', '--include',
            nargs='+',
            type=str,
            default=[],
            help='List of RPW data products to include. '
            'If not passed or empty list, then include all data products by default.'
        )

        parser.add_argument(
            '--force',
            action='store_true',
            default=False,
            help='Force processing.'
        )

class ShareDataCmd(Command):
    """
    Command to share RPW data files in the ROC private data server.
    """
    __command__ = "dadi_share_data"
    __command_name__ = "share_data"
    __parent__ = "dadi"
    __parent_arguments__ = ["base"]
    __help__ = """
        Command to share RPW files in the ROC private data server.
    """

    def add_arguments(self, parser):

        parser.add_argument('-sc', '--source-dir',
                            nargs='+',
                            type=valid_dir,
                            required=True,
                            help='Paths of the directories containing the RPW files to share')
        parser.add_argument('-tg', '--target-dir',
                            nargs=1,
                            type=valid_dir,
                            required=True,
                            help='ROC private data archive root directory path')
        parser.add_argument('-id', '--issue-dir',
                            nargs=1,
                            type=str,
                            default=[ISSUE_DIR],
                            help='Root directory path where failed products '
                                 'are transferred.')
        parser.add_argument('-th','--trash-dir',
                            nargs=1,
                            type=str,
                            default=[TRASH_DIR],
                            help='If passed, then move deleted files/folders into the trash directory (otherwise delete them).')
        parser.add_argument('--clean-src-file',
                            action='store_true',
                            default=False,
                            help='Clean files in source directory at the end '
                            '(only for well copied files)')
        parser.add_argument('--clean-src-dir',
                            action='store_true',
                            default=False,
                            help='Clean source directory at the end '
                            '(only for well copied files)')
        parser.add_argument('--clean-formers',
                            action='store_true',
                            default=False,
                            help='Move former versions of the files to share '
                                 'into a "former_versions" subdirectory')
        parser.add_argument('--update',
                            action='store_true',
                            default=False,
                            help='Do generate a new version of file '
                                 'if target directory already contains '
                                 'the same file.')
        parser.add_argument('--clean-empty',
                            action='store_true',
                            default=False,
                            help='Clean empty source directory.')
        parser.add_argument('--clean-input-dir',
                            nargs=1,
                            default=[None],
                            help='Specify input directory path to be clean. '
                            'Only works if --clean-dir keyword is passed')
        parser.add_argument('--is-plot',
                            action='store_true',
                            default=False,
                            help='If passed, input files to share are summary plots.')
        parser.add_argument('-C', '--compare',
                            action='store_true',
                            default=False,
                            help='If passed, compare content of files to share '
                                 'with existing files in the target directory. '
                                 'If files are identical, do not perform copy. '
                                 '(only works with CDF and CSV files.)')

    def setup_tasks(self, pipeline):
        """
        Execute the sharing of the RPW file(s).
        """

        # Define start/end task
        start_end = ShareOutput()

        pipeline | start_end

        # define the start points of the pipeline
        pipeline.start = start_end


class PublishDataCmd(Command):
    """
    Command to publish RPW private data files in the ROC public data server.
    """
    __command__ = "dadi_publish_data"
    __command_name__ = "publish_data"
    __parent__ = "dadi"
    __parent_arguments__ = ["base"]
    __help__ = """
        Command to publish RPW private data files in the ROC public data server.
    """

    def add_arguments(self, parser):
        parser.add_argument('file_pattern',
                            nargs=1,
                            type=str,
                            help='Pattern to use to filter RPW files to publish. '
                                 'Fetching input files will be performed by running "private_data_dir.glob(file_pattern)"'
                            )
        parser.add_argument('-n', '--wait-nday',
                            required=True,
                            nargs=1,
                            type=int,
                            help='Number of days to wait before publishing RPW files for the first time. '
                                 'Do not pass any value for this keyword will disable the publication of new files.'
                            )
        parser.add_argument('--clean-formers',
                            action='store_true',
                            default=False,
                            help='Move former versions of the files to publish '
                                 'into a "former_versions" subdirectory')
        parser.add_argument('--skip-reprocessed',
                            action='store_true',
                            default=False,
                            help='Disable the publication of re-processed files')

    def setup_tasks(self, pipeline):
        """
        Execute the publishing of the RPW file(s).
        """

        # Define start/end task
        start_end = PublishData()

        pipeline | start_end

        # define the start points of the pipeline
        pipeline.start = start_end


class FeedInput(Command):
    """
    Command to feed RODP input directory with expected files to process.
    """
    __command__ = "feed_input"
    __command_name__ = "feed_input"
    __parent__ = "dadi"
    __parent_arguments__ = ["base"]
    __help__ = """
        Command to feed RODP input directory with expected files to process.
    """

    def add_arguments(self, parser):
        parser.add_argument('rodp_cmd',
                            type=str,
                            choices=('dds_to_l0',
                                     'l0_to_hk',
                                     'l0_to_l1_surv',
                                     'l0_to_l1_sbm',
                                     'l0_to_anc_bia_sweep_table',
                                     'l0_to_l1_bia_sweep',
                                     'l0_to_l1_bia_current'),
                            )
        parser.add_argument('-d', '--date-list',
                            nargs='+',
                            default=None, type=str,
                            help='Specify list of days (YYYYMMDD) to process. '
                                 'For l0_to_l1_bia_current, monthly '
                                 'CDF files are generated.'
                                 '(If passed, start_time, end_time and month input values are ignored)')
        parser.add_argument('-m', '--month-list',
                            nargs='+',
                            type=str, default=None,
                            help='Specify list of months (YYYYMM) to process. '
                                 '(If passed, start_time and end_time input values are ignored)'
                            )
        parser.add_argument('-l0', '--l0-path',
                            nargs=1,
                            type=valid_dir,
                            help='RPW L0 data file local archive '
                                 f'root directory path.',
                            default=None)
        parser.add_argument('--symlink',
                            action='store_true',
                            default=False,
                            help='Use symlink instead of copying physical files into the input directory')


    def setup_tasks(self, pipeline):

        # Define start/end tasks
        startend = FeedInput()


        # Set pipeline workflow
        pipeline | startend

        # define the start points of the pipeline
        pipeline.start = startend

# #
# # class ShareOutput(Command):
# #     """
# #     Command to share RODP output files in the RPW data server.
# #     """
# #     __command__ = "feed_input"
# #     __command_name__ = "feed_input"
# #     __parent__ = "dadi"
# #     __parent_arguments__ = ["base"]
# #     __help__ = """
# #         Command to share RODP output files in the RPW data server.
# #     """
# #
# # #     def add_arguments(self, parser):
# # #         parser.add_argument('rodp_cmd',
# # #                             type=str,
# # #                             choices=('dds_to_l0',
# # #                                      'l0_to_hk',
# # #                                      'l0_to_l1_surv',
# # #                                      'l0_to_l1_sbm',
# # #                                      'l0_to_anc_bia_sweep_table',
# # #                                      'l0_to_l1_bia_sweep',
# # #                                      'l0_to_l1_bia_current'),
# # #                             )
#
# class PublishPubDataCmd(Command):
#     """
#     Command to share RODP output files in the RPW data server.
#     """
#     __command__ = "publish_pub_data"
#     __command_name__ = "publish_pub_data"
#     __parent__ = "dadi"
#     __parent_arguments__ = ["base"]
#     __help__ = """
#         Command to publish RPW data files in the RPW public data server.
#     """
#
#     def add_arguments(self, parser):
#         pass
#
#     def setup_tasks(self, pipeline):
#
#         pipeline | PublishData()
#
#
#
class DeliverDataCmd(Command):
    """
    Command to deliver RPW data files to Solar Orbiter Archive (SOAR) at ESAC.
    """
    __command__ = "dadi_deliver_data"
    __command_name__ = "deliver_data"
    __parent__ = "dadi"
    __parent_arguments__ = ["base"]
    __help__ = """
        Command to deliver RPW data files to Solar Orbiter Archive (SOAR) at ESAC.
    """

    def add_arguments(self, parser):
        parser.add_argument('-f', '--rpw-files',
                            required=True,
                            nargs='+',
                            type=Path,
                            help='List of RPW files to deliver.')
        parser.add_argument('-t', '--to-soc-dir',
                            nargs=1,
                            type=valid_dir,
                            default=[None],
                            help='Directory where files to deliver are copied')
        parser.add_argument('-r', '--transferred-dir',
                            nargs=1,
                            type=valid_dir,
                            default=[None],
                            help='Directory where delivered files are saved by SOC')
        parser.add_argument('-d', '--delivered-dir',
                            nargs=1,
                            type=valid_dir,
                            default=[None],
                            help='Path to the directory containing '
                                 'delivered file footprints (i.e., empty files)')
        parser.add_argument('-n', '--wait-nday',
                            nargs=1,
                            type=int,
                            default=[WAIT_NDAY],
                            help='Number of days to wait before delivering RPW CDAG V01 files to ESAC. '
                                 f'Default is {WAIT_NDAY} days.')
        parser.add_argument('--failed-dir',
                            nargs=1,
                            type=valid_dir,
                            default=[None],
                            help='Path to the directory containing '
                                 'failed file footprints (i.e., empty files)')
        parser.add_argument('--clear-transferred', action='store_true',
                            default=False,
                            help='Delete files in /transferred folder after synchronization with /delivered folder')
        parser.add_argument('--clear-delivered', action='store_true',
                            default=False,
                            help='Delete files in /deliver folder when there are already flagged as delivered in the ROC database')
        parser.add_argument('--sync-only', action='store_true',
                            default=False,
                            help='Just run the synchronization of /transferred with /delivered folders (i.e., skip delivery)')

    def setup_tasks(self, pipeline):
        # Define start/end task
        start_end = DeliverData()
        # Build workflow
        pipeline | start_end
        # set start task
        pipeline.start = start_end
