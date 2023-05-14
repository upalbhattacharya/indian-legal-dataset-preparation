#!/usr/bin/env python

"""Select cases for databank from training cases"""

import argparse
import os
from random import sample

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-tp", "--train_cases_path", type=str,
                        help="Path to list of training cases")
    parser.add_argument("-o", "--output_path", type=str,
                        help="Path to save generated data")
    parser.add_argument("-d", "--databank_percent", type=float,
                        default=0.40,
                        help="Percentage of cases for databank")

    args = parser.parse_args()

    # Load relevant data
    with open(args.train_cases_path, 'r') as f:
        train_cases = f.readlines()
    train_cases = list(filter(
        None, map(lambda x: x.strip("\n"), train_cases)))
    db_cases = set()

    db_cases = sample(
            train_cases,
            int(len(train_cases) * args.databank_percent))

    print(f"Number of db cases is: {len(db_cases)}")

    with open(
            os.path.join(args.output_path, "databank_cases.txt"), 'w') as f:
        for case in db_cases:
            print(case, file=f, end="\n")


if __name__ == "__main__":
    main()
