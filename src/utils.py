#!/usr/bin/env python
# -*- encoding: utf8 -*-
# Last Modified: Wed Jan 05, 2022  01:53PM

"""Common utilities.
"""

import logging
import time
from functools import wraps
import re

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def time_logger(original_func):
    """Time logging for method."""

    @wraps(original_func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = original_func(*args, **kwargs)
        elapsed = time.time() - start
        logging.info(
            f"Method {original_func.__name__} ran for {elapsed:.3f} sec(s)")
        return result
    return wrapper


def set_logger(log_path):
    """Set logger to log information to the terminal and the specified path.

    Parameters
    ----------
    log_path : str
        Path to log run-stats to.
    """
    timestamp = time.strftime("%Y-%m-%d-%H-%m-%S")

    log_path = log_path + "_" + timestamp + ".log"

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


def clean_names(adv_list, check=None):
    """Takes a list of advocate names, a dictionary of advocates with their
    assigned cases and a case text and adds the case to the appropriate
    advocate with the right prefix for petitioner or respondent
    """

    salutations = ['Mr', 'Ms', 'Mrs', 'Dr', 'Mr.', 'Mrs.', 'Ms.', 'Dr.']
    except_tokens = ["For", "CORAM", "Hon'ble", "Advocate", "Advocates"]
    cleaned_advs = []

    for adv in adv_list:
        adv = re.split(r',|\.|\s+', adv)

        adv = list(filter(None, adv))

        # Using replace instead of strip due to abbreviated names with
        adv = [token for token in adv
               if token[0].isupper() and token not in salutations
               and token not in except_tokens]

        if(len(adv) <= 1):
            continue
        cleaned_advs.append("".join(adv))

    if check is not None:
        return list(set([adv for adv in cleaned_advs if adv not in check]))

    return list(set(cleaned_advs))


def update_dict(d, names_list, fl):
    for name in names_list:
        if(d.get(name, -1) == -1):
            logging.info(f"Key {name} does not exist.")
            d[name] = [fl, ]
        else:
            logging.info(f"Adding {fl} to {name}.")
            d[name].append(fl)
    return d


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
