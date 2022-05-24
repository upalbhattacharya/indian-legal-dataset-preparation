#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-02-21 12:54:29.667877015 +0530
# Modify: 2022-02-21 12:57:12.264544453 +0530

""" Create a list of cases for a particular fold that is to be used for
generation of sentence embeddings."""

import os
import json
import argparse
import subprocess

__author__ = "Upal Bhattacharya"
__license__ = ""
__copyright__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--split_path",
                        help="Path to split information.")
    parser.add_argument("-d", "--data_path",
                        help="Path to data")
    parser.add_argument("-o", "--output_path",
                        help="Path to copy training cases.")

    args = parser.parse_args()

    # Getting the training cases
    with open(args.split_path, 'r') as f:
        adv_case_split = json.load(f)

    cases = [case for adv in adv_case_split.values()
             for seg in adv
             for case in adv[seg] if seg not in ['val', 'test']]
    cases = list(set(cases))

    # Copying the cases to output directory
    for case in cases:
        path = os.path.join(args.data_path, f"{case}.txt")
        subprocess.Popen(["cp", path, args.output_path])

    with open(os.path.join(args.output_path, "embed_train_cases.txt"),
              'a') as f:
        for case in cases:
            print(case, file=f, end="\n")


if __name__ == "__main__":
    main()
    
