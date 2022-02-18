#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-02-14 10:22:28.647721556 +0530
# Modify: 2022-02-14 10:30:06.434400199 +0530

import logging

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def set_logger(log_path):
    """Set loggger to log information to the terminal and specified path.

    Parameters
    ----------
    log_path : str
        Path to log to.
    """

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

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
