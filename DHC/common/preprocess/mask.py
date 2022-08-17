#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- coding: utf-8 -*-
# Birth: 2022-08-15 10:52:32.599469578 +0530
# Modify: 2022-08-17 09:51:09.053523011 +0530

"""Mask various patterns for given data.
"""

import argparse
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


def ner_mask(text) -> str:
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
    source_nlp = spacy.load("en_core_web_trf")
    nlp = spacy.blank('en')
    nlp.add_pipe("ner", source=source_nlp)
    #  nlp.add_pipe("mask")

    nlp.max_length = 2000000

    new_text = ""

    doc = nlp(text)
    print(type(doc))
    for token in doc:

        append = token.text

        if (token.ent_type_ in ['ORG', 'PERSON']):
            append = f"[{token.ent_type_}]"

        if append in punctuation:
            new_text = new_text + append
        else:
            new_text = new_text + " " + append

    return new_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load data from.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data.")

    args = parser.parse_args()

    with Parallel(n_jobs=-1) as parallel:
        parallel([delayed(parallelize_mask)(fl=fl,
                                            input_path=args.input_path,
                                            output_path=args.output_path)
                  for fl in os.listdir(args.input_path)])


def parallelize_mask(**kwargs):
    """Parallelization of masking documents"""
    set_logger(os.path.join(kwargs["output_path"], "mask"))
    flname = os.path.splitext(kwargs["fl"])[0]

    text = get_text(os.path.join(kwargs["input_path"], kwargs["fl"]))
    text = mask(text)

    logging.info(f"Masked data from {flname}")
    with open(os.path.join(kwargs["output_path"], f"{flname}.txt"), 'w') as f:
        f.write(text)


if __name__ == "__main__":
    main()
