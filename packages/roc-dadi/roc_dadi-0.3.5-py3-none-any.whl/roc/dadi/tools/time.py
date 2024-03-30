#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from datetime import datetime

from poppy.core.logger import logger

__all__ = ['strtime_to_datetime', 'valid_date', 'valid_time']

from roc.dadi.constants import TIME_INPUT_STRFORMAT, TIME_DAILY_STRFORMAT


def strtime_to_datetime(time_string,
                        valid_format=['%Y%m%d', '%Y%j', '%Y%m%dT%H%M%S', '%Y%m%dT%H%M']):
    """
    Convert input time string into datetime

    :param time_string: Time string in one of the allowed formats
    :param valid_format: List of valid string formats
    :return: datetime
    """

    output_time = None
    for current_format in valid_format:
        try:
            output_time = datetime.strptime(time_string, current_format)
            break
        except:
            continue

    return output_time


def valid_time(string_time, format=TIME_INPUT_STRFORMAT):

    if string_time:
        try:
            string_time = datetime.strptime(string_time, format)
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(string_time)
            raise argparse.ArgumentTypeError(msg)

    return string_time


def valid_date(t, format=TIME_DAILY_STRFORMAT):
    """
    Validate input date string format.

    :param t: input date string
    :param format: expected date string format
    :return: date object with input date info
    """
    if t:
        try:
            return datetime.strptime(t, format)
        except ValueError:
            argparse.ArgumentTypeError(f"Not a valid date: '{t}'!")
