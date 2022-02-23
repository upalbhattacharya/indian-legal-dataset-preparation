#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-02-23 20:06:57.071048775 +0530
# Modify: 2022-02-23 21:08:36.330988277 +0530

"""Get the offences or charges of cases based on their section information.
NOTE: presently written to work with a single act's section charges.
NEEDS TO BE IMPROVED."""

import os
import json
import argparse
from collections import defaultdict

__author__ = "Upal Bhattacharya"
__license__ = ""
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__email__ = "upal.bhattachara@gmail.com"


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cases_file_path",
                        help="Path to file containing cases to consider.")
    parser.add_argument("-a", "--act_path",
                        help="Path to file with acts to consider.")
    parser.add_argument("-s", "--statute_info_path",
                        help="Path to case_statute_info.json file.")
    parser.add_argument("-f", "--offences_key_path",
                        help="Path to section-offences mapping.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated dictionary file.")

    args = parser.parse_args()

    # Loading the set of cases
    with open(args.cases_file_path, 'r') as f:
        cases = f.read()
    cases = list(filter(lambda x: x != "", cases.split("\n")))

    # Loading the acts
    with open(args.act_path, 'r') as f:
        acts = f.read()
    acts = list(filter(lambda x: x != "", acts.split("\n")))

    # Loading case statute information
    with open(args.statute_info_path, 'r') as f:
        case_statute_info = json.load(f)

    # Loading the section to offences mapping
    with open(args.offences_key_path, 'r') as f:
        offences = json.load(f)

    case_offences = defaultdict(lambda: list())
    for case in cases:
        sections = case_statute_info[case]["sections"]
        for section in sections:
            case_offences[case].extend(offences.get(section, ""))
        case_offences[case] = list(filter(lambda x: x != "",
                                          list(set(case_offences[case]))))

    # Saving data
    with open(os.path.join(args.output_path, "case_offences.json"), 'w') as f:
        json.dump(case_offences, f, indent=4)


if __name__ == "__main__":
    main()
