#!/home/workboots/VirtualEnvs/aiml/bin/python3

"""get_case_advocates.py: Maps advocates to cases.
"""
import os
import json
import argparse
from utils import set_logger, time_logger
import logging

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_path",
                    help="Directory to load data from.")
parser.add_argument("-o", "--output_path", default=None,
                    help="Directory to store results.")

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


@time_logger
def main():
    args = parser.parse_args()

    if(args.output_path is None):
        args.output_path = args.input_path

    set_logger(os.path.join(args.output_path, "get_case_advocates_new.log"))

    logging.info((f"Loading data from {args.input_path} and saving to "
                  f"{args.output_path}."))

    case_advs = {}  # For getting the names extracted for a particular case

    with open(os.path.join(args.input_path, 'adv_cases_new.json'), 'r') as f:
        adv_cases = json.load(f)

    for adv, cases in adv_cases.items():
        for case in cases:
            # To check if the dictionary item already exists
            if (case_advs.get(case, -1) != -1):
                case_advs[case].append(adv)
            else:
                case_advs[case] = []
                case_advs[case].append(adv)

    with open(os.path.join(args.output_path, 'case_advs_new.json'), 'w') as f:
        json.dump(case_advs, f, indent=4)


if __name__ == "__main__":
    main()
