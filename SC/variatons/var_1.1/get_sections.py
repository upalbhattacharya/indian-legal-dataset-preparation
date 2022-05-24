#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-02-15 16:07:33.198314149 +0530
# Modify: 2022-02-15 16:19:22.181666765 +0530

"""Get relevant sections of cases."""

import argparse
import json
import os
from collections import defaultdict
from pprint import pprint

__author__ = "Upal Bhattacharya"
__license__ = ""
__copyright__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dict_path",
                        help=("Path to dictionary for getting the cases of"
                              "the relevant sections."))
    parser.add_argument("-s", "--statute_path",
                        help=("Path to file containing mapping of all cases"
                              "to their statutes."))
    parser.add_argument("-o", "--output_path",
                        help="Path to store generated data.")

    args = parser.parse_args()

    with open(args.dict_path, 'r') as f:
        mapping = json.load(f)

    with open(args.statute_path, 'r') as f:
        case_statute_info = json.load(f)

    relevant_sections = list(mapping.keys())
    cases = list(set([case for cases in mapping.values() for case in cases]))

    rel_cases = defaultdict(lambda: set)
    for case in cases:
        rel_cases[case] = set(relevant_sections).intersection(
                set(case_statute_info[case]["sections"]))

    # pprint(relevant_sections)
    pprint(rel_cases)


if __name__ == "__main__":
    main()
