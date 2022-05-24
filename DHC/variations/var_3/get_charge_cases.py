#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-05-16 12:25:43.685146851 +0530
# Modify: 2022-05-16 12:26:15.735148909 +0530

""" Get cases for each charge."""

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"

import argparse
import json
import os
from collections import defaultdict


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--case_charges_path",
                        help="Path to case charges.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data.")

    args = parser.parse_args()

    with open(args.case_charges_path, 'r') as f:
        case_charges = json.load(f)

    charge_cases = defaultdict(lambda: list())

    for case, charges in case_charges.items():
        _ = [charge_cases[charge].append(case)
             for charge in charges]

    with open(os.path.join(args.output_path, "ipc_charge_cases.json"),
              'w') as f:
        json.dump(charge_cases, f, indent=4)


if __name__ == "__main__":
    main()
