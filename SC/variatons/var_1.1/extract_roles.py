#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf8 -*-
# Birth: 2022-02-14 10:09:36.337701331 +0530
# Modify: 2022-02-14 11:04:45.638505971 +0530

"""Extract provided roles from documents given document text and per-line
roles."""

import argparse
import logging
import os

from utils import set_logger

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load data from.")
    parser.add_argument("-r", "--roles_path",
                        help="Path to load rhetorical roles from.")
    parser.add_argument("-t", "--target_roles", nargs="+", type=str,
                        default=["Facts"],
                        help="Roles to extract.")
    parser.add_argument("-o", "--output_path",
                        help="Path to store generated data.")

    args = parser.parse_args()
    set_logger("extract_roles.log")

    for doc in os.listdir(args.roles_path):
        logging.info(f"Logging information for document {doc}")

        with open(os.path.join(args.roles_path, doc), 'r') as f:
            roles = f.readlines()
        logging.info(f"Number of lines in roles: {len(roles)}")

        with open(os.path.join(args.input_path, doc), 'r') as f:
            text = f.readlines()
        logging.info(f"Number of lines in text: {len(text)}")

        assert len(roles) == len(text), "Lengths do not match"

        for line, role in zip(text, roles):
            if (role in args.target_roles):
                with open(os.path.join(args.output_path, doc), 'a') as f:
                    f.write(line)
                    f.write("\n")


if __name__ == "__main__":
    main()
