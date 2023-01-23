#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- coding: utf-8 -*-
# Birth: 2022-08-15 10:52:32.599469578 +0530
# Modify: 2022-09-06 12:44:42.430979779 +0530

"""Mask various patterns for given data.
"""

import argparse
import json
import logging
import os
import re
from string import punctuation

import spacy
from joblib import Parallel, delayed

from utils import get_text, save_format, set_logger

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"

# Regex patterns used to mask different information
patterns = {
        '[PERSON]': re.compile(
            r'M(?:r|s|rs)\.\s*[A-Za-z.]+\s+[A-Za-z.]+(?:\s+[A-Za-z]+)?,?'),

        '[DATE]': re.compile(
                    "|".join(
                        [
                         r'([0-9]?[0-9](\.|\/)[0-9]{2}(\.|\/)[0-9]{4})',
                         r'([a-zA-Z]+\s+[0-9]?[0-9](\s)?(st|nd|rd|th)?,?\s+[0-9]{4})',
                         r'([0-9]?[0-9](\s)?(st|nd|rd|th)?\s+[A-Za-z]+,?\s+[0-9]{4})'
                         ]
                        )),
        '[TIME]': re.compile(
            r'([0-9]?[0-9]:\d{2}(:\d{2})?,?(\s+)?(am|pm|AM|PM)?(\s+)?,?(IST)?)'
                        ),

        '[MONEY]': re.compile(
                        r'(`|Rs.|rs.|rs |rs. |Rs. )[0-9,]+(/-)?'),

        '[ID]': re.compile(
                    "|".join(
                        [
                         r'(Crl.|CRL.|Crl|CRL)\s?(A.|a.|A|Appln|Appln.|Appeal)?\s?(no.)?\s?[0-9]{2,}/[0-9]{3,}',
                         r'BAIL\sAPPLN\.[0-9]+'
                         ]
                        )),
        '[PAGE]': re.compile(r'Page\s*(no)?.?\s*[0-9]+\s*of\s*[0-9]+',
                             flags=re.I)
    }


def mask(text: str) -> str:
    """ Mask given patterns by given mask strings.

    Parameters
    ----------
    text : str
        Text to process.
    Returns
    -------
    text : str
        Processed text.
    """

    for k, r in patterns.items():
        k = '' if k == '[PAGE]' else k
        text = r.sub(k, text)

    return text


def ner_mask(text, nlp) -> str:
    """ Mask names of persons and locations.

    Parameters
    ----------
    text : str
        Text to process.
    nlp : spacy Object
        Spacy model to use to get ner tags.

    Returns
    -------
    new_text : str
        Processed text.
    """

    new_text = ""

    doc = nlp(text)
    prev_token = ""
    num = 0
    for token in doc:

        append = token.text

        if token.ent_type_ != "":
            append = f"[{token.ent_type_}]"
            # Skip consecutive tokens of the same entity type
            if prev_token == append:
                continue
            prev_token = append
            num += 1

        if append in punctuation:
            new_text = new_text + append
        else:
            new_text = new_text + " " + append
    logging.info(f"{num} entities were found and masked")
    return new_text


def mask_targets(text: str, targets: list) -> str:
    """Mask names of targets in text (if any left)"""
    if targets == []:
        return text
    target_regex = re.compile("|".join(["\s+\.?".join(
                                re.findall(r"[A-Z][^A-Z]*", target))
                                        for target in targets]),
                              flags=re.I)
    hits = target_regex.findall(text)
    logging.info(f"{len(hits)} matches found for targets after entity "
                 "masking. Additionally masking them.")
    text = target_regex.sub("[PERSON]", text)
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

    set_logger(os.path.join(args.log_path, "mask"))
    logging.info("Inputs:")
    for name, value in vars(args).items():
        logging.info(f"{name}: {value}")

    nlp = spacy.load("en_core_web_sm")
    #  nlp = spacy.blank('en')
    #  nlp.add_pipe("ner", source=source_nlp)

    nlp.max_length = 2000000

    #  with Parallel(n_jobs=-1) as parallel:
        #  parallel([delayed(parallelize_mask)(fl=fl,
                                            #  input_path=args.input_path,
                                            #  output_path=args.output_path)
                  #  for fl in os.listdir(args.input_path)])

    for fl in os.listdir(args.input_path):
        flname = os.path.splitext(fl)[0]
        parallelize_mask(fl=fl,
                         input_path=args.input_path,
                         output_path=args.output_path,
                         nlp=nlp)


def parallelize_mask(**kwargs):
    """Parallelization of masking documents"""
    flname = os.path.splitext(kwargs["fl"])[0]

    #  text = get_text(os.path.join(kwargs["input_path"], kwargs["fl"]))
    with open(os.path.join(kwargs["input_path"], kwargs["fl"]), 'r') as f:
        text = f.read()
    text = ner_mask(text, kwargs["nlp"])
    #  text = mask_targets(text, kwargs["targets"])

    logging.info(f"Masked data from {flname}")
    with open(os.path.join(kwargs["output_path"], f"{flname}.txt"), 'w') as f:
        f.write(text)


if __name__ == "__main__":
    main()
