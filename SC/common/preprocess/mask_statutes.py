#!/usr/bin/env python

"""Mask sections in cases"""

import argparse
import json
import logging
import os
import re
from copy import deepcopy

from utils import set_logger


def mask_statutes(data: dict, sections: list) -> dict:
    """Mask given sections from sentences and remove certain elements

    Parameters
    ----------
    data: dict
        Dictionary with per-sentence information
    sections: list
        List of all sections cited in document
    """

    data_dict = deepcopy(data)
    case_section_regex = re.compile(
            "|".join([sec for sec in sections]))

    alt_case_section_regex = re.compile(
            "|".join([r"Section\s+{}\s+of\s+the\s+Code".format(
                sec.split("_")[-1])
                for sec in sections]))

    for idx, content in data_dict.items():
        replace_texts = []
        if content["sections"]:
            # Get textual spans of sections in sentence to replace
            for sec, spans in content["sections"].items():
                replace_texts.extend([content["text"][start:end]
                                      for (start, end) in spans])

            content["text"] = re.sub("|".join(replace_texts), "[SECTION]",
                                     content["text"])
            content["text"] = case_section_regex.sub("[SECTION]",
                                                     content["text"])
            content["text"] = alt_case_section_regex.sub("[SECTION]",
                                                         content["text"])
        # Remove invalid sentence span
        del content["span"]
        # Remove spans of sections
        content["sections"] = list(content["sections"].keys())

    return data_dict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir",
                        help="Directory to load per-sentence information")
    parser.add_argument("-a", "--case_section_info",
                        help="Path to load case section information")
    parser.add_argument("-o", "--output_dir",
                        help="Path to save new data")
    parser.log_path("-l", "--log_path", type=str, default=None,
                    help="Path to save generated logs")

    args = parser.parse_args()
    if args.log_path is None:
        args.log_path = args.output_path

    set_logger(os.path.join(args.log_path, "mask_statutes"))
    logging.info("Inputs:")
    for name, value in vars(args).items():
        logging.info(f"{name}: {value}")

    with open(args.case_section_info, 'r') as f:
        case_sections = json.load(f)

    # Load data
    for fl in os.listdir(args.input_dir):
        logging.info("Masking statutes for {fl}")
        with open(os.path.join(args.input_dir, fl), 'r') as f:
            data = json.load(f)
        flname = os.path.splitext(fl)[0]
        data = mask_statutes(data, case_sections[flname]["sections"].keys())

        with open(os.path.join(args.output_dir, f"{flname}.json"), 'w') as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    main()
