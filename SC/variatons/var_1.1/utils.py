#!/home/workboots/workEnv/bin/python3
# -*- coding: utf-8 -*-
# Birth: 2022-02-28 11:54:43.348228152 +0530
# Modify: 2022-02-28 13:00:22.678332350 +0530

"""Utilities for pre-processing.
"""

import logging
from bs4 import BeautifulSoup as bs
import json
import os

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def set_logger(log_path):
    """Set logger to log information to the terminal and the specified path.

    Parameters
    ----------
    log_path : str
        Path to log run-stats to.
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # FileHandler to log to a file
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s : [%(levelname)s] %(message)s",
            "%Y-%m-%d %H:%M:%S"))
        logger.addHandler(file_handler)

        # StreamHandler to log to terminal
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(
            "%(asctime)s : [%(levelname)s] %(message)s",
            "%Y-%m-%d %H:%M:%S"))
        logger.addHandler(stream_handler)


def get_text(path: str) -> str:
    """Load html data and return text of the data."""
    with open(path, 'r') as f:
        raw = f.read()

    raw = raw.split("\n")
    raw = list(filter(lambda x: x != "", raw))
    if raw == []:
        return None
    raw = " ".join(raw)
    return raw


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    def __getattr__(*args):
        val = dict.get(*args)
        return DotDict(val) if type(val) is dict else val

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def save_format(path, flname, data):
    """Saves data to the given path depending on the data type."""

    if (type(data) == str):
        with open(os.path.join(path, f"{flname}.txt"), 'w') as f:
            f.write(data)

    if (type(data) == dict):
        with open(os.path.join(path, f"{flname}.json"), 'w') as f:
            json.dump(data, f, indent=4)


def order(dict_obj: dict) -> dict:
    """Order dictionary in decreasing order of values

    Parameters
    ----------
    dict_obj : dict
        Dictionary to be sorted.

    Returns
    -------
    dict

    """

    ordered_dict = {
            k: v for k, v in sorted(dict_obj.items(),
                                    key=lambda x: x[1],
                                    reverse=True)}
    return ordered_dict
