#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Functions common to DADI tests
"""
import os
from pathlib import Path

import yaml

__all__ = ['DadiTest']


class DadiTest:

    test_dir = Path(__file__).parent.resolve()

    base_url = 'https://rpw.lesia.obspm.fr/roc/data/private/devtest/roc/test_data/rodp/dadi'
    # test credentials
    username = 'roctest'
    try:
        password = os.environ['ROC_TEST_PASSWORD']
    except KeyError:
        raise KeyError('You have to define the test user password using'
                       'the "ROC_TEST_PASSWORD" environment variable')

    @staticmethod
    def parse_ymal(yaml_file):
        """
        Simple wrapper to parse ymal file with pyyaml package

        :param yaml_file: ymal file to parse
        :return: parsed yaml file data as returned by yaml.load()
        """
        with open(str(yaml_file), 'r') as yaml_buffer:
            data = yaml.load(yaml_buffer, Loader=yaml.CLoader)
        return data
