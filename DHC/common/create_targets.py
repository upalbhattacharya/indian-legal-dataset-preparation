#!/home/workboots/workEnv/bin/python3
"""get_targets.py: Map cases of adv_case_splits to targets according to the
train, db, val and test split setup.
"""
import argparse
import json
import logging
import os
from pathlib import Path

from utils import set_logger, time_logger

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_path",
                    help="Directory to load data from.")
parser.add_argument("-o", "--output_path", default=None,
                    help="Directory to save data to.")
parser.add_argument("-n", "--nfold", type=int, default=20,
                    help="Number of folds.")


@time_logger
def main():
    args = parser.parse_args()
    if (args.output_path is None):
        args.output_path = args.input_path

    set_logger(os.path.join(args.output_path, "create_targets.log"))

    logging.info(f"Loading data from {args.input_path}.")
    logging.info(f"Saving data to {args.output_path}.")

    fold_path = os.path.join(args.output_path,
                             f"cross_val/{args.nfold}_fold/")

    with open(os.path.join(args.input_path, "case_advs.json"), 'r') as f:
        case_advs = json.load(f)

    for i in range(args.nfold):
        with open(os.path.join(fold_path,
                               Path(f"fold_{i}/adv_case_splits.json")),
                  'r') as f:
            adv_case_splits = json.load(f)

        # Getting all the cases in the high count advocate dataset

        cases = []

        # Getting all cases of high count advocates
        for item in adv_case_splits.values():
            cases.extend(item['train'])
            cases.extend(item['db'])
            cases.extend(item['test'])
            cases.extend(item['val'])

        cases_list = list(set(cases))
        advs = list(adv_case_splits.keys())

        cases = {}
        for case in cases_list:
            cases[case] = list(filter(lambda x: x in advs,
                                      case_advs[case]))

        with open(os.path.join(fold_path,
                               Path(f"fold_{i}/case_targets.json")),
                  'w') as f:
            json.dump(cases, f, indent=4)


if __name__ == '__main__':
    main()
