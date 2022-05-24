#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-02-19 12:54:33.671525485 +0530
# Modify: 2022-02-21 11:48:57.311190695 +0530

"""Extract text portions of text from json files."""

import argparse
import json
import logging
import os

from utils import set_logger

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

    set_logger(os.path.join(args.output_path, "get_texts.log"))

    for flname in os.listdir(args.input_path):
        logging.info(f"Processing {flname}.")
        with open(os.path.join(args.input_path, flname), 'r') as f:
            raw = json.load(f)

        fl = os.path.splitext(flname)[0]
        path = os.path.join(args.output_path, f"{fl}.txt")

        # Delete the file if it already exists to avoid duplication writing
        if os.path.exists(path):
            os.system(f"rm {path}")
        
        with open(path, 'a') as f:
            for v in raw.values():
                print(v["text"], file=f, end="\n")


if __name__ == "__main__":
    main()
