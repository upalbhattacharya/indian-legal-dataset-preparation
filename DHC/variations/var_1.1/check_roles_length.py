#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-02-20 12:27:53.171207956 +0530
# Modify: 2022-02-20 12:39:35.424559499 +0530

"""Verify length of rhetorical roles document matches number of sentences."""

import argparse
import logging
import os

from utils import set_logger

__author__ = "Upal Bhattacharya"
__licencse__ = ""
__copyright__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load documents.")
    parser.add_argument("-r", "--roles_path",
                        help="Path to rhetorical roles.")
    parser.add_argument("-o", "--output_path",
                        help=("Path to save names of documents with length"
                              "mismatch"))
    args = parser.parse_args()

    set_logger(os.path.join(args.output_path, "mismatch.log"))
    for flname in os.listdir(args.input_path):
        with open(os.path.join(args.input_path, flname), 'r') as f:
            text = f.read()
        text = text.split("\n")
        # Removing empty list elements
        text = list(filter(lambda x: x != "", text))

        with open(os.path.join(args.roles_path, flname), 'r') as f:
            roles = f.read()
        roles = roles.split("\n")
        roles = list(filter(lambda x: x != "", roles))
        logging.info(f"Processed {flname}")

        if (len(roles) != len(text)):
            with open(os.path.join(args.output_path, "mismatch_roles.txt"),
                      'a') as f:
                print(f"{flname}, {len(roles)}, {len(text)}", file=f, end="\n")


if __name__ == "__main__":
    main()
