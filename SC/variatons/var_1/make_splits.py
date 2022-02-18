#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-02-15 10:23:17.331101292 +0530
# Modify: 2022-02-15 20:15:57.322043743 +0530

""" Get splits of cases"""

import argparse
import json
import os
import subprocess

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_path",
                        help="Path containing documents to be split up")
    parser.add_argument("-s", "--split_path",
                        help=("Path to load data containing split"
                              "information"))
    parser.add_argument("-o", "--output_path",
                        help="Path to save split data")

    args = parser.parse_args()

    with open(args.split_path, 'r') as f:
        splits = json.load(f)

    for sec, cases in splits.items():
        dir = os.path.join(args.output_path, sec)
        os.makedirs(dir)
        for case in cases:
            path = os.path.join(args.data_path, f"{case}.txt")
            subprocess.Popen(["cp", path, dir])


if __name__ == "__main__":
    main()
