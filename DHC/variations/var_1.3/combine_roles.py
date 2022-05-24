#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-02-21 11:14:28.367847438 +0530
# Modify: 2022-02-23 14:12:41.874598979 +0530

"""Add rhetorical roles information to document json files"""

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
                        help="Path to json files.")
    parser.add_argument("-r", "--roles_path",
                        help="Path to rhetorical roles.")

    args = parser.parse_args()

    set_logger("combine_roles.log")

    for filename in os.listdir(args.input_path):
        # Loading the json files
        with open(os.path.join(args.input_path, filename), 'r') as f:
            json_obj = json.load(f)
        # Loading the rhetorical roles
        flname = os.path.splitext(filename)[0]
        logging.info(f"{flname}, {filename}")
        with open(os.path.join(args.roles_path, f"{flname}.txt"), 'r') as f:
            roles = f.read()
        roles = roles.split("\n")
        roles = list(filter(lambda x: x != "", roles))
        logging.info(f"{len(list(json_obj.keys()))} {len(roles)}")
        # Working only with documents where the number of roles match:
        if (len(list(json_obj.keys())) == len(roles)):
            for sent_idx, role in zip(json_obj, roles):
                json_obj[sent_idx]["role"] = role
            # Saving the updated document
            with open(os.path.join(args.input_path, filename), 'w') as f:
                json.dump(json_obj, f, indent=4)
            logging.info(f"Updated document {filename} with roles.")
        else:
            logging.info("Mismatch in number of sentences and roles for"
                         f"{filename}. Skipping.")


if __name__ == "__main__":
    main()
