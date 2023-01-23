#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Birth: 2022-08-29 23:38:46.023331026 +0530
# Modify: 2022-09-05 23:24:19.750522651 +0530

"""Remove extra whitespaces, non-utf-8 characters and carry out substitutions.
"""

import argparse
import logging
import os
import re
from string import punctuation

from utils import get_text, save_format, set_logger

from joblib import Parallel, delayed

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = ""
__email__ = "upal.bhattacharya@gmail.com"

# To avoid issues with Sphinx
present_dir = os.path.dirname(__file__)
# For substitutions
with open(os.path.join(present_dir, "act_titles.txt"), 'r') as f:
    acts = f.read()
acts = acts.split("\n")
acts.remove("Constitution")

acts_dict = {}
for act in acts:
    parts = act.split(",")
    date = parts[-1].strip()
    #  date = re.sub(r"^[0-9]+", "", date).strip()
    title = parts[0].strip()
    if len(parts) > 2:
        title = ", ".join(map(lambda x: x.strip(), parts[:-1]))
    title = title.replace("\(", "(\(")
    title = title.replace("\)", "\))?")
    title = title.strip()
    acts_dict[act] = rf"{title}(?:,|\s+of)?\s*({date})?"


acts_dict.update({
        "Code of Criminal Procedure, 1898": [
            r"Code\s+of\s+Criminal\s+Procedure,?\s*(?:1898)",
            r"Criminal\s+Procedure\s+Code,?\s*(?:1898)",
            r"Cr.?\s*P.?\s*C(?:.?\s*,?\s*1898)"
            ],
        "Code of Criminal Procedure, 1973": [
            r"Code\s+of\s+Criminal\s+Procedure,?\s*(?:1973)?",
            r"Criminal\s+Procedure\s+Code,?\s*(?:1973)?",
            r"Cr.?\s*P.?\s*C(?:.?\s*,?\s*1973)?"
            ],
        "Code of Civil Procedure, 1908": [
            r"Code\s+of\s+Civil\s+Procedure,?\s*(?:1908)?",
            r"Civil\s+Procedure\s+Code,?\s*(?:1908)?",
            r"C.?P.?C(?:.?,?\s*1908)?"
            ],
        "Indian Penal Code, 1860": [
            r"(?:Indian\s+)?Penal\s+Code,?\s*(?:1860)?",
            r"I.?\s*P.?\s*C(?:.?\s*,?\s*1860)?"
            ]
    })

acts_regexes = {
        k: re.compile("|".join(v), flags=re.I | re.DOTALL) if type(v) == list
        else re.compile(v, flags=re.I | re.DOTALL)
        for k, v in acts_dict.items()}

special_cases = {
        "rs.": ["Rs\."], "no.": ["No\."], "vs": ["\bv\.", "vs\."],
        "m/s.": ["M/s\."], "mohd.": ["Mohd\."], "exhibit": ["Ex\."],
        "article": ["Art\.", "art\.", "u/art\."],
        "articles": ["Arts\.", "arts\.", "u/arts\."],
        "sections": ["\bss\.", "\bu/ss\.", "\bSs\."],
        "section": ["\bS\.", "\bs\.", "\bu/s\."],
        "honourable": ["hon'ble"]
        }

special_case_regexes = {
        k: re.compile("|".join(v))
        for k, v in special_cases.items()
        }

regexes = {
        #  "page_idx": re.compile(r"[0-9]+\."),
        "nonwords": re.compile(r"[^\w./,\s-]"),
        "extra_spaces": re.compile(r"\s+"),
        "dots": re.compile(r"(\s*\.\s*){2,}"),
        "section": re.compile(r"([a-zA-Z]+\s?)[-/]+(\s?[a-zA-Z]+)"),
        "links": re.compile(r"\(/?([a-zA-Z0-9]+[.,@?^=%&:\/~+#-]+)+[a-zA-Z0-9]+?\)"),
        "header_footer": re.compile("(?:\*\s+){3,}", flags=re.DOTALL),
        "page": re.compile(r'Page\s*(no)?.?\s*[0-9]+\s*of\s*[0-9]+',
                           flags=re.I)
        }


def clean(text: str, punct: str = None, **kwargs) -> str:
    """Clean unwanted characters, extra whitespaces, unnecessary punctuations
    and sentence splits.

    Parameters
    ----------
    text : str
        Text to process.
    punct : str
        Punctuation string to use. (Mainly for second run through after
        masking)

    Returns
    -------
    text : str
        Processed text.
    """
    # Remove non-utf-8 characters
    text = bytes(text, 'utf-8').decode('utf-8', 'ignore')

    # Remove links
    text = regexes["links"].sub('', text)

    # Remove strange characters and non fullstop punctuations
    text = regexes["nonwords"].sub('', text)

    # Remove extra whitespaces, hyphens and multiple dots
    text = regexes["extra_spaces"].sub(' ', text)
    text = regexes["dots"].sub('.', text)

    # Removing all punctuations except those appearing for sections
    text = regexes["section"].sub(r'\1 \2', text)
    text = regexes["extra_spaces"].sub(' ', text)
    text = regexes["page"].sub('', text)
    text = text.strip()

    # Subsituting citation variations for special sequences
    for k, r in special_case_regexes.items():
        text = r.sub(k, text)

    # Replacing common abbreviations of acts
    text = text.replace("Constitution of India", "Constitution")

    for k, r in acts_regexes.items():
        text = r.sub(k + " ", text)
        text = regexes["extra_spaces"].sub(' ', text)

    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load data from.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data.")
    parser.add_argument("-l", "--log_path", type=str, default=None,
                        help="Path to save generated logs")

    args = parser.parse_args()
    if args.log_path is None:
        args.log_path = args.output_path

    with Parallel(n_jobs=-1) as parallel:
        parallel([delayed(parallelize)(fl=fl,
                                       input_path=args.input_path,
                                       output_path=args.output_path,
                                       log_path=args.log_path)
                  for fl in os.listdir(args.input_path)])


def parallelize(**kwargs):
    """Parallelization of cleaning documents"""

    set_logger(os.path.join(kwargs["log_path"], "clean"))
    with open(os.path.join(kwargs["input_path"], kwargs["fl"]), 'r') as f:
        text = f.read()
    text = clean(text)

    flname = os.path.splitext(kwargs["fl"])[0]
    logging.info("Removed extra whitespaces and non-utf-8 characters from "
                 f"{flname}")

    save_format(kwargs["output_path"], flname, text)


if __name__ == "__main__":
    main()
