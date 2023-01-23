#!/usr/bin/env python

"""Check for section leakage after masking"""

import json
import os
import argparse
import logging
import re

from utils import set_logger
from collections import defaultdict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir",
                        help="Path to load masked data files from")
    parser.add_argument("-s", "--section_info",
                        help="Path to load section info from")
    parser.add_argument("-l", "--log_path", type=str, default=None,
                        help="Path to save generated logs")
    parser.add_argument("-o", "--output_dir",
                        help="Path to save generated output stats")

    args = parser.parse_args()
    if args.log_path is None:
        args.log_path = args.output_dir

    set_logger(os.path.join(args.log_path, "check_section_leakage"))
    logging.info("Inputs:")
    for name, value in vars(args).items():
        logging.info(f"{name}: {value}")

    leaky_cases = defaultdict(dict)

    for fl in os.listdir(args.input_dir):
        flname = os.path.splitext(fl)[0]
        with open(os.path.join(args.input_dir, fl), 'r') as f:
            text = f.read()

        with open(os.path.join(args.section_info, f"{flname}.json"), 'r') as f:
            sections = json.load(f)

        leakage = []
        leakage_2 = []

        if sections:
            section_regex = "|".join(
                    [r"Section\s+{0}\s+(?:of\s+)?(?:the\s+){1}".format(
                        section.split("_")[-1], section.split("_")[0].replace(
                            "(", "\(").replace(")", "\)"))
                        for section in sections.keys()])
            section_regex = section_regex.replace(" ", "\s+")
            section_regex = section_regex.replace(",", ",?")
            section_regex = re.compile(section_regex)

            section_regex_2 = "|".join([rf"Sections?\s+{0}".format(
                section.split("_")[-1])
                for section in sections.keys()])
            section_regex_2 = re.compile(section_regex_2)

            leakage = section_regex.findall(text)
            leakage_2 = section_regex_2.findall(text)

            if leakage != []:
                logging.info(f"Found primary leakage for {flname}")
                logging.info(leakage)
                leaky_cases[flname]["A"] = leakage

            if leakage_2 != []:
                logging.info(f"Found secondary leakage for {flname}")
                logging.info(leakage_2)
                leaky_cases[flname]["B"] = leakage_2

            spans = [span for spans in sections.values() for span in spans]
            for (start, end) in spans:
                if text[start:end] != "[SECTION]":
                    logging.info(f"Incorrect span found in {flname}")
                    logging.info(f"{text[start:end]}")

        section_regex_3 = re.compile(r"Sections?\s+[0-9]+")
        leakage_3 = section_regex_3.findall(text)

        if leakage_3 != []:
            logging.info(f"Found misc. leakage for {flname}")
            logging.info(leakage_3)
            leaky_cases[flname]["C"] = leakage_3

        if all(ele == [] for ele in [leakage, leakage_2, leakage_3]):
            logging.info(f"No leakage for {flname}")

    with open(os.path.join(args.output_dir, "leakage_stats.json"), 'w') as f:
        json.dump(leaky_cases, f, indent=4)


if __name__ == "__main__":
    main()
