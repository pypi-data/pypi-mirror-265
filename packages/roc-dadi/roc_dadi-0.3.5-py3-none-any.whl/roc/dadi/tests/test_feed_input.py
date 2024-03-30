#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests feed_input tasks in DADI plugin.
"""

# ________________ IMPORT _________________________
import os
import shutil
import zipfile

from tempfile import TemporaryDirectory
from pathlib import Path
import unittest.mock as mock

import pytest

from poppy.core.logger import logger
from poppy.core.test import CommandTestCase
from poppy.core.generic.requests import download_file

from roc.dadi.tests.test_dadi import DadiTest

# ________________ Global Variables _____________
# (define here the global variables)

# ________________ Class Definition __________
# (If required, define here classes)


class TestDadiFeedInput(CommandTestCase):

    def create_dirs(self):
        # define folders required for feed input
        self.root_dir = Path(TemporaryDirectory().name)

        # Define rpw private data path
        self.rpw_private_data_dir = self.root_dir / 'rpw_private_data_dir'

        # Define and create pipeline input path
        self.input_dir = self.root_dir / 'input_dir'
        self.input_dir.mkdir(parents=True)

    def create_test_data(self):
        """
        Create/get input/output data required to perform the test.
        """

        # Define ZIP file containing test data
        self.test_data_zip = self.root_dir / 'test_data.zip'
        self.test_data_url = DadiTest.base_url + '/feed_input/test_data.zip'

        # If ZIP file not found locally, then download it
        if (not self.test_data_zip.is_file() or
            not zipfile.is_zipfile(self.test_data_zip)):
            download_file(str(self.test_data_zip),
                          self.test_data_url,
                          auth=(DadiTest.username, DadiTest.password))

        # Then extract content
        with zipfile.ZipFile(self.test_data_zip) as myzip:
            myzip.extractall()

    def create_database(self):
        """
        Create database required to run the test.

        :return:
        """

        # Database setup
        self.setup_session()

        # Create database, schemas tables and types
        # Db migration
        db_upgrade = ['pop', 'db', 'upgrade', 'heads', '-ll', 'INFO']
        # apply database migrations
        self.run_command(db_upgrade)

    def teardown_method(self, method):
        """
        Method called immediately after the test method has been called and the result recorded.

        This is called even if the test method raised an exception.

        :param method: the test method
        :return:
        """

        # rollback the database
        super().teardown_method(method)

        # clear the test data file tree
        shutil.rmtree(str(self.root_dir))


    @pytest.mark.parametrize('rodp_cmd','start_time, end_time, symlink' ,[
        ('l0_to_hk', '20200705', '20200706', True),
        ('l0_to_hk', '20200705', '20200706', False),
    ])
    def test_feed_input(self, rodp_cmd, start_time, end_time, symlink):
        """
        Test DeliverData Task for nominal use (no CDAG data).

        :param rodp_cmd:
        :param start_time:
        :param end_time:
        :param symlink
        :return:
        """
        from poppy.core.conf import Settings

        # First create database
        self.create_database()

        # Create directories for test
        self.create_dirs()

        # Create or retrieve test data
        self.create_test_data()

       # # build deliver_data command
        cmd = ['pop',
               '-ll', 'INFO',
                'dadi',
                '--start-time', start_time,
                '--end-time', end_time,
                '--input-dir', str(self.input_dir),
                '--rpw-private-data-dir', str(self.rpw_private_data_dir),
                'feed_input',
               rodp_cmd,
                ]
        if symlink:
            cmd.append('--symlink')
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

        # Check we have expected files in input_dir
        cmd = ''.join(rodp_cmd.split('_')).upper()

        date_format = '%Y%m%d'
        for root, dirs, files in os.walk(str(self.rpw_private_data_dir / "L0")):
            print(root, dirs, files)


