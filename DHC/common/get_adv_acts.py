#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf8 -*-
# Last Modified: Wed Jan 05, 2022  01:56PM

"""
Find Acts cited by advocates.
"""

import argparse
import json
import logging
import os
from collections import defaultdict

from utils import order, set_logger

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def get_acts(dict_obj: dict) -> dict:
    """Return dictionary of acts from a dictionary of sections.

    Parameters
    ----------
    dict_obj : dict
        Dictionary of sections.

    Returns
    -------
    dict

    """

    acts = defaultdict(int)
    for k, v in dict_obj.items():
        logging.info(f"Logging for {k}.")
        acts[k.split("_")[0]] += v
    acts = order(acts)

    return acts


def main():
    parser = argparse.ArgumentParser(
                                description="Find acts cited by advocates.")
    parser.add_argument("-i", "--input_path",
                        help="Path to load data from.")
    parser.add_argument("-o", "--output_path",
                        help="Path to store generated data.")

    args = parser.parse_args()

    set_logger(os.path.join(args.output_path, "get_adv_acts.log"))

    with open(args.input_path, 'r') as f:
        section_info = json.load(f)

    act_info = {}

    for k, v in section_info.items():
        act_info[k] = get_acts(v)

    with open(args.output_path, 'w') as f:
        json.dump(act_info, f, indent=4)


if __name__ == "__main__":
    main()
