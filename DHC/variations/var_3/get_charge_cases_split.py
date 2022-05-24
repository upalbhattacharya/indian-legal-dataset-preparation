#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-05-16 11:20:57.171563830 +0530
# Modify: 2022-05-16 13:29:37.842060215 +0530

"""Get cases of each charge in train and test splits along with their
frequencies."""

import argparse
import json
import os
from collections import defaultdict

__author__ = "Upal Bhattacharya"
__license__ = ""
__copyright__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--split_path",
                        help="Path to split information.")
    parser.add_argument("-c", "--case_charges_path",
                        help="Path to case charges to split along.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated charge split info.")

    args = parser.parse_args()

    # Loading split information
    with open(args.split_path, 'r') as f:
        split_data = json.load(f)

    # Loading case charge information
    with open(args.case_charges_path, 'r') as f:
        case_charges = json.load(f)

    charge_cases = {}

    # TODO: figure out a better strategy than four nested loops
    for item, splits in split_data.items():
        charge_cases[item] = {
                "train": splits["train"] + splits["db"],
                "test": splits["test"] + splits["val"]
                }


    charge_stats = {}
    for charge, splits in charge_cases.items():
        charge_stats[charge] = {split: len(cases)
                                for split, cases in splits.items()}

    # Saving
    with open(os.path.join(args.output_path, "charge_case_splits.json"),
              'w') as f:
        json.dump(charge_cases, f, indent=4)

    with open(os.path.join(args.output_path, "charge_case_stats.json"),
              'w') as f:
        json.dump(charge_stats, f, indent=4)


if __name__ == "__main__":
    main()
