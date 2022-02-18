#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- coding: utf-8 -*-
# Last Modified: Wed Jan 05, 2022  02:17PM

"""
Find aggregated section and act information of a provided set of cases from
per-sentence information. Takes as input a directory containing a set of cases
for which the per-sentence section information is provided. Returns a
dictionary containing the statute information of each case.
"""

import argparse
import json
import logging
import os
from collections import Counter

from utils import order, set_logger

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def get_statute_info(secs: list) -> dict:
    """Return act and section frequency dictionary from list of sections.

    Parameters
    ----------
    secs : list
        List of sections cited

    Returns
    -------
    dict

    """

    acts = list(map(lambda x: x.split("_")[0], secs))
    acts = dict(Counter(acts))
    acts = order(acts)
    sections = dict(Counter(secs))
    sections = order(sections)

    statute = {
            "acts": acts,
            "sections": sections,
            }

    return statute


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load files from.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data.")

    args = parser.parse_args()
    set_logger(os.path.join(args.output_path, "aggregate_section_info.log"))

    agg_info = {}

    for fl in os.listdir(args.input_path):
        logging.info(f"Get statute information from {fl}.")
        with open(os.path.join(args.input_path, fl), 'r') as f:
            doc = json.load(f)
        secs = [sec for sent in doc.values()
                for sec in sent["sections"].keys()]

        agg_info[os.path.splitext(fl)[0]] = get_statute_info(secs)

    with open(os.path.join(args.output_path, "case_statute_info.json"),
              'w') as f:
        json.dump(agg_info, f, indent=4)


if __name__ == "__main__":
    main()
