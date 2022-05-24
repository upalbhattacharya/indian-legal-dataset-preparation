#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-03-01 12:17:41.315679879 +0530
# Modify: 2022-03-01 12:17:41.335679880 +0530

"""Verify length of rhetorical roles document matches number of sentences."""

import argparse
import logging
import os
import json

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
                        help=("Path to save names of documents with length "
                              "mismatch"))
    args = parser.parse_args()

    set_logger(os.path.join(args.output_path, "mismatch.log"))
    for filename in os.listdir(args.input_path):
        with open(os.path.join(args.input_path, filename), 'r') as f:
            dict_obj = json.load(f)

        flname = os.path.splitext(filename)[0]

        with open(os.path.join(args.roles_path, f"{flname}.txt"), 'r') as f:
            roles = f.read()
        roles = roles.split("\n")
        roles = list(filter(lambda x: x != "", roles))
        logging.info(f"Processed {flname}")

        if (len(roles) != len(dict_obj.keys())):
            with open(os.path.join(args.output_path, "mismatch_roles.txt"),
                      'a') as f:
                print((f"{flname}, {len(roles)}, "
                       f"{len(dict_obj.keys())}"), file=f, end="\n")


if __name__ == "__main__":
    main()
