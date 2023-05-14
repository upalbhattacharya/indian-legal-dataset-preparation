#!/usr/bin/env python

"""Mask sections in cases"""

import argparse
import json
import logging
import os
import re
from copy import deepcopy
from typing import Union

from utils import set_logger


def get_closest(tuple_a: tuple, tuple_list: list) -> tuple:
    """Return closest tuple based on first coordinate criteria"""
    least = 0
    dist = tuple_a[0] - tuple_list[0][0]
    for i in range(len(tuple_list)):
        if not tuple_list[i][0] <= tuple_a[0]:
            continue
        n_dist = tuple_a[0] - tuple_list[i][0]
        if n_dist <= dist:
            dist = n_dist
            least = i
    return tuple_list[least]


def get_new_spans(data: str, sections: dict) -> dict:
    """Realign spans of sections after Masking

    Parameters
    ----------
    data: str
        Text information
    sections: dict
        Dictionary with sections and their spans
    """

    spans = []
    for match in re.finditer(r"\[SECTION\]", data):
        spans.append(match.span())
        
    if spans == []:
        logging.info("Could not find the relevant tag")
        return sections

    for (start, end) in spans:
        assert end == start + 9, f"Span is of length {end - start}"

    for section, sec_spans in sections.items():
        n_spans = []
        for span in sec_spans:
            n_span = get_closest(span, spans)
            n_spans.append(n_span)
        sections[section] = n_spans

    return sections


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir",
                        help="Directory to load text information")
    parser.add_argument("-a", "--case_section_info",
                        help="Path to load case section information")
    parser.add_argument("-s", "--new_section_spans_dir",
                        help="Path to save new section spans after masking")
    parser.add_argument("-l", "--log_path", type=str, default=None,
                        help="Path to save generated logs")

    args = parser.parse_args()
    if args.log_path is None:
        args.log_path = args.masked_statute_output_dir

    set_logger(os.path.join(args.log_path, "align_statute_spans"))
    logging.info("Inputs:")
    for name, value in vars(args).items():
        logging.info(f"{name}: {value}")

    # Load data
    for fl in os.listdir(args.input_dir):
        logging.info(f"Masking statutes for {fl}")
        flname = os.path.splitext(fl)[0]
        with open(os.path.join(args.input_dir, fl), 'r') as f:
            data = f.read()
        with open(os.path.join(args.case_section_info, f"{flname}.json"),
                  'r') as f:
            section_info = json.load(f)
        n_sections = get_new_spans(data, section_info)

        with open(os.path.join(args.new_section_spans_dir, f"{flname}.json"),
                  'w') as f:
            json.dump(n_sections, f, indent=4)


if __name__ == "__main__":
    main()
