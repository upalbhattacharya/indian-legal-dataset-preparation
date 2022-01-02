#!/home/workboots/workEnv/bin/python3
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


def clean_names(adv_list):
    """Takes a list of advocate names, a dictionary of advocates with their
    assigned cases and a case text and adds the case to the appropriate
    advocate with the right prefix for petitioner or respondent
    """

    salutations = ['Mr', 'Ms', 'Mrs', 'Dr', 'Mr.', 'Mrs.', 'Ms.', 'Dr.']
    cleaned_advs = []

    for adv in adv_list:
        adv = re.split(r',|\.|\s+', adv)

        adv = list(filter(None, adv))

        # Using replace instead of strip due to abbreviated names with
        adv = [token for token in adv
               if token[0].isupper() and token not in salutations]

        if(len(adv) <= 1):
            continue
        cleaned_advs.append("".join(adv))

    return list(set(cleaned_advs))


def update_dict(d, names_list, fl):
    for name in names_list:
        if(d.get(name, -1) == -1):
            d[name] = [fl, ]
        else:
            d[name].append(fl)
    return d
