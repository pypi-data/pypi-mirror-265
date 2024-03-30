#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exceptions definition for DADI plugin.
"""

from poppy.core.logger import logger

__all__ = ['InvalidDataset']

class InvalidDataset(Exception):

    def __init__(self, message=None, *args, **kwargs):
        super(InvalidDataset, self).__init__(*args, **kwargs)
        if message:
            logger.error(message)
            self.message = message
