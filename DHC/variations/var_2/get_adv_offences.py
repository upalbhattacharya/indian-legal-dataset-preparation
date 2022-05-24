#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-04-08 12:32:05.180685182 +0530
# Modify: 2022-04-08 13:01:40.754065441 +0530

"""Get offences information about advocates from their case offences."""

import os
import json
import argparse
from collections import Counter

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def main():

    parser = argparse.ArgumentParser(
                description=("Get offences information about advocates from"
                             " their case offences."))

    parser.add_argument("-s", "--split_path",
                        help="Path to advocate split information.")
    parser.add_argument("-c", "--case_charges_path",
                        help="Path to case charges information.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data.")

    args = parser.parse_args()

    # Loading the case split information
    with open(args.split_path, 'r') as f:
        adv_split = json.load(f)

    # Loading the case charge information
    with open(args.case_charges_path, 'r') as f:
        case_charges = json.load(f)

    # Getting the cases of each advocate
    adv_charges = {}
    for adv in adv_split:
        adv_cases = set()
        charges = []
        adv_cases.update(adv_split[adv]["train"])
        adv_cases.update(adv_split[adv]["db"])
        # Retaining only the cases with the relevant charges
        adv_cases = adv_cases.intersection(set(case_charges.keys()))
        # Getting the charges
        _ = [charges.extend(case_charges[case]) for case in adv_cases]
        # Getting the number of cases with charges
        adv_charges[adv] = Counter(charges)

        adv_charges[adv] = {
                k: v for k, v in sorted(adv_charges[adv].items(),
                                        key=lambda x: x[1], reverse=True)}

    # Saving the charge information
    with open(os.path.join(args.output_path, "adv_offences.json"), 'w') as f:
        json.dump(adv_charges, f, indent=4)


if __name__ == "__main__":
    main()
