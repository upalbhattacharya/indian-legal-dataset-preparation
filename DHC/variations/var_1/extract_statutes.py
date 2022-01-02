#!/home/workboots/workEnv/bin/python3
# -*- coding: utf-8 -*-
"""
extract_statutes.py: Extract statutes from documents.
"""

import logging
import re
from collections import defaultdict
from itertools import groupby
from operator import itemgetter
from typing import Union

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"

# Getting the set of statutes
with open("act_titles.txt", 'r') as f:
    acts = f.read()
acts = acts.split("\n")
acts.remove("Constitution")

with open("section_titles.txt", 'r') as f:
    statutes = f.read()
statutes = statutes.split("\n")

statutes = {k: k for k in statutes}


def get_statutes(text: str, actlist: list, unit: str) -> set:
    """Find all statutes cited in text.

    Parameters
    ----------
    text : str
        Text to find statutes from.
    actlist : list
        List of acts to use for reference.
    unit : str
        Article or section.

    Returns
    -------
    actsec : set
        Set containing cited statutes and spans.
    """

    act_sec = set()
    for act in actlist:

        # Matching pattern for each act
        matches = re.finditer(
            rf'({unit}s?)\s+([0-9()a-zA-Z/,\-\s]+)\s*(of\s+)?(the\s+)?({act})',
            text, flags=re.I)

        # Going through each match
        for match in matches:
            if match is None:
                break

            # Span of the match (useful for masking)
            start, end = match.start(1), match.end(5)
            #  match_nums = match.groups()[1]
            match_nums = match.groups()[1]
            # Splitting when multiple sections are cited
            nums = re.split(r'/|and|\s+|,', match_nums)
            for num in nums:
                if num != '':
                    act_sec.add((f"{act}_{num}", start, end))

            # When section ranges are specified
            ranges = re.finditer(
                r'([0-9]+)\s*?(?:\-|to)\s*?([0-9]+)',
                match_nums,
                flags=re.I)

            for rng in ranges:
                if rng is None:
                    break

                sec_start, sec_end = rng.groups()
                for sec_num in range(int(sec_start), int(sec_end) + 1):
                    act_sec.add((f"{act}_{sec_num}", start, end))

    if act_sec != set():
        cleaned = clean(act_sec)
        return cleaned

    return act_sec


def clean(act_sec: set) -> set:
    """Clean up given set of extracted sections to standard format.

    Parameters
    ----------
    actsec : set
        Set containing statutes and their spans.

    Returns
    -------
    actsec : set
        Set containing formatted statutes and their spans.
    """
    actsec = set()

    for (a, start, end) in act_sec:
        # Splitting along underscore to get the act and the section number
        a = a.strip()
        parts = a.split("_")

        # Pattern 1 Removing brackets
        num = parts[1]

        # Removing bracketed information
        if "(" in parts[1]:
            pos1 = parts[1].index("(")
            num = parts[1][:pos1]
        if "-" in parts[1]:
            pos1 = parts[1].index("-")
            num = parts[1][:pos1]
        num = re.sub(r'\D', '', num)
        a3 = f"{parts[0]}_{num}"

        actsec.add((a3, start, end))

    return actsec


def check_exists(actsec: set, statutes: dict) -> set:
    """Return valid cited statutes.

    Parameters
    ----------
    actsec : set
        Set of statutes cited and their spans.
    statutues: dict
        Dictionary of statutes to reference.

    Returns
    -------
    cleaned : set
        Valid set of statutes and their spans.
    """
    cleaned = set()
    for (a, start, end) in actsec:
        a = a.replace(r'  ', ' ')
        if statutes.get(a, -1) != -1:
            cleaned.add((statutes[a], start, end))
    return cleaned


def extract_statutes(text: Union[str, dict],
                     per_sentence: bool = True) -> dict:
    """Finds all statutes mentioned in the given text.

    Parameters
    ----------
    text : str or dict
        Text to extract statutes from.
    per_sentence : bool, default : True
        Whether to find the statutes for each sentence. (Only works when a
        dictionary is passed to text.)

    Returns
    -------
    secs : dict
        Dictionary of cited statutes.
    """

    orig = text
    if (type(orig) == dict):
        text = " ".join([item["text"] for item in text.values()])

    actsec = set()
    actsec1 = set()
    actsec2 = set()

    actsec1 = get_statutes(text, acts, "section")
    actsec2 = get_statutes(text, ["Constitution"], "article")

    cites = [actsec1, actsec2]
    actsec = set(frozenset().union(*cites))
    #  logging.info(f"{actsec}")
    cleaned = check_exists(actsec, statutes)
    logging.info(f"{cleaned}")

    secs = {
        k: [*map(lambda x: (x[1], x[2]), values)]
        for k, values in groupby(
            sorted(cleaned, key=lambda x: x[0]),
            itemgetter(0))
    }

    if (per_sentence and type(orig) == dict):
        secs = sentence_align(secs, orig)

    #  logging.info(f"Found {secs}")

    return secs


def sentence_align(sentence_dict: dict, orig: dict) -> dict:
    """Align citations to sentences.

    Parameters
    ----------
    sentence_dict : dict
        Dictionary of statute citations.
    orig : dict
        Dictionary of sentences.

    Returns
    -------
    orig : dict
        Dictionary with sections given for each sentence.
    """

    for idx, items in orig.items():
        start, end = items["span"]
        sections = defaultdict(list)
        for cite, spans in sentence_dict.items():
            for c_start, c_end in spans:
                if(c_start >= start and c_end <= end):

                    sections[cite].append(
                        (c_start - start, c_end - start))
        orig[idx]["sections"] = dict(sections)

    return orig


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load data from.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data.")

    args = parser.parse_args()

    set_logger(os.path.join(args.output_path, "logs", "extract_statutes.log"))

    for fl in os.listdir(args.input_path):
        # Get text
        text = get_text(os.path.join(args.input_path, fl))
        text = extract_statutes(text)

        logging.info(f"Extracted statutes for {fl}")
        logging.info(f"Found statutes: {text}")

        flname = os.path.splitext(fl)[0]
        save_format(args.output_path, flname, text)


if __name__ == "__main__":
    import argparse
    import os

    from utils import get_text, save_format, set_logger
    main()
