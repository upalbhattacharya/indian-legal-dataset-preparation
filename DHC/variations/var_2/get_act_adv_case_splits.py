#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf8 -*-

# Birth: 2022-04-25 14:18:02.160969859 +0530
# Modify: 2022-04-25 14:31:42.527624016 +0530

"""Get case splits of advocates from a given list of cases."""

import argparse
import os
import json

__author__ = "Upal Bhattacharya"
__license__ = ""
__copyright__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load original advocate case split.")
    parser.add_argument("-c", "--act_cases",
                        help="Path to file containing cases to retain.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated output.")

    args = parser.parse_args()

    # Loading advocate case split information
    with open(args.input_path, 'r') as f:
        adv_case_split = json.load(f)

    # Loading the set of cases to consider
    with open(args.act_cases, 'r') as f:
        cases = f.readlines()

    cases = list(filter(None, map(lambda x: x.strip("\n"), cases)))
    print(cases)

    # Creating the new split up
    for adv, case_splits in adv_case_split.items():
        adv_case_split[adv] = {
                k: list(set(cases).intersection(set(v)))
                for k, v in case_splits.items()}

    # Saving
    with open(os.path.join(args.output_path, "adv_case_splits.json"),
              'w') as f:
        json.dump(adv_case_split, f, indent=4)


if __name__ == "__main__":
    main()
