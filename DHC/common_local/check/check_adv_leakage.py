#!/usr/bin/env python

"""Check leakage of advocate information in texts"""

import argparse
import json
import logging
import os
import re

from utils import set_logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir",
                        help="Path to load data from")
    parser.add_argument("-a", "--case_advs",
                        help="Path to case advocate information")
    parser.add_argument("-o", "--output_dir",
                        help="Path to save generated stats")
    parser.add_argument("-l", "--log_path", type=str, default=None,
                        help="Path to save generated logs")

    args = parser.parse_args()
    if args.log_path is None:
        args.log_path = args.output_dir

    set_logger(os.path.join(args.log_path, "check_adv_leakage"))
    logging.info("Inputs:")
    for name, value in vars(args).items():
        logging.info(f"{name}: {value}")

    with open(args.case_advs, 'r') as f:
        case_advs = json.load(f)

    leaky_cases = {}

    for fl in os.listdir(args.input_dir):
        flname = os.path.splitext(fl)[0]
        if case_advs.get(flname, -1) == -1:
            logging.info(f"{flname} has no defined advocates. Skipping")
            continue
        advs = case_advs[flname]
        advs = [r"\.?\s*".join(re.findall(r"[A-Z][^A-Z]*", name))
                for name in advs]
        adv_regex = re.compile("|".join(advs))
        logging.info(f"Using regex {adv_regex}")
        with open(os.path.join(args.input_dir, fl), 'r') as f:
            text = f.read()

        leakage = adv_regex.findall(text)
        if leakage != []:
            leaky_cases[flname] = leakage
            logging.info(f"Found advocate leakage for {flname}")
        else:
            logging.info(f"No leakage for {flname}")

    with open(os.path.join(args.output_dir, "adv_leakage.json"), 'w') as f:
        json.dump(leaky_cases)


if __name__ == "__main__":
    main()
