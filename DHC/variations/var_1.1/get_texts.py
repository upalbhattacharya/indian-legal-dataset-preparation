#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-02-15 20:11:51.005370572 +0530
# Modify: 2022-02-15 20:12:49.548705450 +0530

"""Extract text portions of text from json files."""

import argparse
import json
import os

__author__ = "Upal Bhattacharya"
__license__ = ""
__copyright__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load data from.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated text data.")

    args = parser.parse_args()

    for flname in os.listdir(args.input_path):
        with open(os.path.join(args.input_path, flname), 'r') as f:
            raw = json.load(f)

        fl = os.path.splitext(flname)[0]

        with open(os.path.join(args.output_path, f"{fl}.txt"), 'a') as f:
            for v in raw.values():
                print(v["text"], file=f, end="\n")


if __name__ == "__main__":
    main()
