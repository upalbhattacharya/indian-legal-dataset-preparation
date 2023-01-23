#!/usr/bin/env python

"""Combine rhetorical roles into per-sentence information"""

import argparse
import json
import logging
import os

from joblib import Parallel, delayed

from utils import set_logger

__author__ = "Upal Bhattacharya"
__license__ = ""
__version__ = "1.0"
__copyright__ = ""
__email__ = "upal.bhattacharya@gmail.com"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--combined_data_path",
                        help="Path to combined json documents")
    parser.add_argument("-r", "--roles_path",
                        help="Path to per-document rhetorical roles")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data")
    parser.add_argument("-l", "--log_path", type=str, default=None,
                        help="Path to save generated logs")

    args = parser.parse_args()
    if args.log_path is None:
        args.log_path = args.output_path
    set_logger(os.path.join(args.log_path, "combine"))
    logging.info("Inputs")
    for name, value in vars(args).items():
        logging.info(f"{name}: {value}")

    for fl in os.listdir(args.roles_path):
        flname = os.path.splitext(fl)[0]
        combined_path = os.path.join(args.combined_data_path, f"{flname}.json")
        if not os.path.exists(combined_path):
            logging.info(f"Did not find file {fl}")
            continue
        logging.info(f"Combining roles for {flname}")
        with open(os.path.join(args.roles_path, fl), 'r') as f:
            roles = f.readlines()
        roles = list(filter(None, map(lambda x: x.strip(), roles)))
        with open(combined_path, 'r') as f:
            sents = json.load(f)

        sents = {
                k: {**v, **{"role": role}}
                for role, (k, v) in zip(roles, sents.items())}

        with open(os.path.join(args.output_path, f"{flname}.json"), 'w') as f:
            json.dump(sents, f, indent=4)


if __name__ == "__main__":
    main()
