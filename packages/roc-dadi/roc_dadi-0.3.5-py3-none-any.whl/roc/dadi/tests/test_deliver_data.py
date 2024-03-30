#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests deliver_data tasks in DADI plugin.
"""

import shutil
from tempfile import TemporaryDirectory
from pathlib import Path
import unittest.mock as mock

import pytest

from poppy.core.logger import logger
from poppy.core.test import CommandTestCase

from roc.dadi.tests.test_dadi import DadiTest
from roc.dingo.tools import insert_in_db, query_db
from roc.dingo.models.file import FileLog


class TestDadiDeliverData(CommandTestCase):

    def create_dirs(self):
        # define folders required for data delivery
        self.root_dir = Path(TemporaryDirectory().name)
        self.data_dir = self.root_dir / 'data'
        self.data_dir.mkdir(parents=True)
        self.to_soc_dir = self.root_dir / 'to_soc'
        self.to_soc_dir.mkdir(parents=True)
        self.from_soc_dir = self.root_dir / 'from_soc'
        self.from_soc_dir.mkdir(parents=True)
        self.transferred_dir = self.root_dir / 'transferred'
        self.transferred_dir.mkdir(parents=True)
        self.delivered_dir = self.root_dir / 'delivered'
        self.delivered_dir.mkdir(parents=True)
        self.failed_dir = self.root_dir / 'failed'
        self.failed_dir.mkdir(parents=True)
        self.trash_dir = self.root_dir / 'trash'
        self.trash_dir.mkdir(parents=True)

    def create_database(self):
        """


        :return:
        """

        # Database setup
        self.setup_session()

        # Create database, schemas tables and types
        # Db migration
        db_upgrade = ['pop', 'db', 'upgrade', 'heads', '-ll', 'INFO']
        # apply database migrations
        self.run_command(db_upgrade)

        # Prepare data to insert
        test_file = DadiTest.test_dir / Path('data-tasks') / 'test_deliver_data.yml'
        data_to_insert = DadiTest.parse_ymal(test_file)

        # Insert data
        for key, val in data_to_insert.items():
           if insert_in_db(self.session, FileLog, val) < 0:
              logger.error(f'Cannot insert data from {test_file}')
              assert False
           else:
               filters = (FileLog.basename == val['basename'])
               results = query_db(self.session, FileLog,
                              filters=filters, to_dict='records',
                            )
               logger.debug(results[0])


    def teardown_method(self, method):
        """
        Method called immediately after the test method has been called and the result recorded.

        This is called even if the test method raised an exception.

        :param method: the test method
        :return:
        """

        # rollback the database
        super().teardown_method(method)

        # clear the downloaded files
        shutil.rmtree(str(self.root_dir))

    @pytest.mark.parametrize('start_time, end_time', [
        ('20200701', '20200731'),
    ])
    def test_deliver_pub_data(self, start_time, end_time):
        """
        Test DeliverData Task for nominal use (no CDAG data).

        :param start_time:
        :param end_time:
        :return:
        """
        from poppy.core.conf import Settings

        # # TODO - Add the query to database (to check for delivered data)
        # First create database

        # Then fill database with information for the delivered file
        self.create_database()

        # # Create directories for test
        self.create_dirs()
        #
        # # Create dummy RPW files to test deliver_data
        self.create_test_data()
        #
        # # build deliver_data command
        cmd = ['pop',
               '-ll', 'INFO',
                'dadi',
                '--start-time', start_time,
                '--end-time', end_time,
                '--trash-dir', str(self.trash_dir),
                'deliver_data',
                 '--to-soc-dir', str(self.to_soc_dir),
                 '--transferred-dir', str(self.transferred_dir),
                 '--delivered-dir', str(self.delivered_dir),
                 '--failed-dir', str(self.failed_dir),
                 '--clear-transferred',
                 '--clear-delivered',
                 '--rpw-files',
                 ' '.join([str(current_file[0])
                         for current_file in self.files_to_deliver]),
                ]
        #
        # # --- run the command ---

        # define the required plugins
        plugin_list = ['poppy.pop', 'roc.dadi']

        # run the command
        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
            logger.debug(cmd)
            self.run_command(cmd)

        #Check if resulting operations have succeeded ...
        #For input files
        for current_file in self.files_to_deliver:
           if not current_file[1].is_file():
                logger.error(f"{current_file[1]} not found")
                assert False
        #For files initially saved in /transferred
        for current_file in self.files_transferred:
           if not current_file[1].is_file():
               logger.error(f"{current_file[1]} not found")
               assert False
        #For files initially saved in /delivered (not working yet)
        for current_file in self.files_delivered:
           if not current_file[1].is_file():
               logger.error(f"{current_file[1]} not found")
               assert False


    def create_test_data(self):
        """

        :return:
        """

        # TODO - Add a test case for file with delivered=False in the database
        # Create four test files to be delivered
        # (One new, one already delivered,
        # one outside the time range
        # and one badly formatted)
        # For each test file, give a tuple with the initial path and final path
        self.files_to_deliver = [
            (self.data_dir / 'solo_L1_rpw-tnr-surv_20200701_V01.cdf',
             self.to_soc_dir / 'solo_L1_rpw-tnr-surv_20200701_V01.cdf'),
            (self.data_dir / 'solo_L2_rpw-tds-surv-rswf-e_20200702_V01.cdf',
             self.trash_dir / 'solo_L2_rpw-tds-surv-rswf-e_20200702_V01.cdf'),
            (self.data_dir / 'solo_L2_rpw-tds-surv-rswf-e_20210902_V01.cdf',
             self.data_dir / 'solo_L2_rpw-tds-surv-rswf-e_20210902_V01.cdf'),
            (self.data_dir / 'solo_L2_rpw-lfr-surv-cwf-b_200703_V10.cdf',
             self.failed_dir / 'solo_L2_rpw-lfr-surv-cwf-b_200703_V10.cdf')
        ]
        for current_file in self.files_to_deliver:
            current_file[0].touch(exist_ok=True)

        # Create a test file already transferred
        self.files_transferred = [
            (self.transferred_dir / 'solo_L2_rpw-tds-surv-tswf-b_20200704_V01.cdf',
             self.delivered_dir / 'solo_L2_rpw-tds-surv-tswf-b_20200704_V01.cdf')
        ]
        for current_file in self.files_transferred:
            current_file[0].touch(exist_ok=True)

        # Create a test file already delivered
        # (This file is already in the database and will be sent to trash at the end
        self.files_delivered = [
            (self.delivered_dir / 'solo_L2_rpw-tds-surv-rswf-e_20200702_V01.cdf',
            self.trash_dir / 'solo_L2_rpw-tds-surv-rswf-e_20200702_V01.cdf')
        ]
        for current_file in self.files_delivered:
            current_file[0].touch(exist_ok=True)

    def setup_session(self):
        """

        :return:
        """

        # empty the table FileLog
        self.session.query(FileLog).delete()
        self.session.flush()

        return self.session
