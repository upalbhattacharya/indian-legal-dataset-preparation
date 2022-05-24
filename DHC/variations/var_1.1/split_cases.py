#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-02-24 17:22:00.817263704 +0530
# Modify: 2022-02-24 17:22:00.817263704 +0530

"""Split a given set of cases in train and test splits based on split json file
provided. Also delete cases if their text is empty."""

import argparse
import json
import os
import subprocess
from copy import copy

__author__ = "Upal Bhattacharya"
__license__ = ""
__copyright__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--cases_dir",
                        help="Directory with all the cases.")
    parser.add_argument("-l", "--cases_list_path",
                        help="Path to document with list of cases to update.")
    parser.add_argument("-s", "--split_path",
                        help="Path to document with split information.")
    parser.add_argument("-o", "--output_path",
                        help="Path to move files to.")

    args = parser.parse_args()

    with open(args.cases_list_path, 'r') as f:
        cases = f.read()
    cases = list(filter(lambda x: x != "", cases.split("\n")))
    cases_clean = copy(cases)

    with open(args.split_path, 'r') as f:
        split_info = json.load(f)

    # Getting the training and testing cases
    train = []
    test = []
    for adv in split_info:
        train.extend(split_info[adv]["train"])
        train.extend(split_info[adv]["db"])
        test.extend(split_info[adv]["test"])
        test.extend(split_info[adv]["val"])

    train = list(set(train))
    test = list(set(test))

    ext = os.path.splitext(os.listdir(args.cases_dir)[0])[-1]

    for case in cases:
        # Reading the document and removing it if it is empty
        with open(os.path.join(args.cases_dir, f"{case}{ext}"), 'r') as f:
            doc = f.read()
        doc = doc.replace("\n", "")
        if doc == "":
            cases_clean.remove(case)
            continue
        # If the case is a training case:
        if case in train:
            subprocess.Popen(['cp',
                              os.path.join(args.cases_dir, f"{case}{ext}"),
                              os.path.join(args.output_path, "train")])

        elif case in test:
            subprocess.Popen(['cp',
                              os.path.join(args.cases_dir, f"{case}{ext}"),
                              os.path.join(args.output_path, "test")])

        else:
            print(f"Found absurd case {case}.")


if __name__ == "__main__":
    main()
