#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- coding: utf-8 -*-
# Birth: 2022-02-15 12:41:58.071318513 +0530
# Modify: 2022-02-18 11:44:26.654297114 +0530

"""Mask various patterns for given data.
"""

import re
from typing import List, Pattern, Tuple
from string import punctuation

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"

# Regex patterns used to mask different information
patterns = [
    ('name',
        r'M(?:r|s|rs)\.\s*[A-Za-z.]+\s+[A-Za-z.]+(?:\s+[A-Za-z]+)?,?',
        '[PERSON]'),
    ('date_1',
        r'([0-9]?[0-9](\.|\/)[0-9]{2}(\.|\/)[0-9]{4})',
        '[DATE]'),
    ('date_2',
        r'([a-zA-Z]+\s+[0-9]?[0-9](\s)?(st|nd|rd|th)?,?\s+[0-9]{4})',
        '[DATE]'),
    ('date_3',
        r'([0-9]?[0-9](\s)?(st|nd|rd|th)?\s+[A-Za-z]+,?\s+[0-9]{4})',
        '[DATE]'),
    ('page',
        r'(Page \d+ of \d+)',
        ''),
    ('time',
        (r'([0-9]?[0-9]:\d{2}(:\d{2})?,?(\s+)?'
         r'(am|pm|AM|PM)?(\s+)?,?(IST)?)'),
        '[TIME]'),
    ('money',
        r'(`|Rs.|rs.|rs |rs. |Rs. )[0-9,]+(/-)?',
        '[MONEY]'),
    ('id',
        r'(Crl.|CRL.|Crl|CRL)\s?(A.|a.|A|Appln|Appln.|Appeal)?\s?(no.)?\s?[0-9]{2,}/[0-9]{3,}',
        '[ID]'),
    ('bail',
        r'BAIL\sAPPLN\.[0-9]+',
        '[ID]')
]


def mask(text: str, patterns: List[Tuple[str, Pattern, str]]) -> str:
    """ Mask given patterns by given mask strings.

    Parameters
    ----------
    text : str
        Text to process.
    patterns : List[Tuple[str, Pattern, str]]
        List of regex patterns and replacement tokens.

    Returns
    -------
    text : str
        Processed text.
    """

    for (_, pattern, rep) in patterns:
        text = re.sub(pattern, rep, text)

    return text


def ner_mask(text: str, nlp: object) -> str:
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

    doc = nlp(text)

    new_text = ""

    for token in doc:
        append = token.text
        if (token.ent_type_ in ['ORG', 'PERSON']):
            append = f"[{token.ent_type_}]"

        if (append in punctuation):
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

    set_logger(os.path.join(args.output_path, "mask.log"))
    
    nlp = spacy.load("en_core_web_trf")
    nlp.max_length = 2000000

    for fl in os.listdir(args.input_path):
        # Get text
        text = get_text(os.path.join(args.input_path, fl))
        text = mask(text, patterns)
        text = ner_mask(text, nlp)

        logging.info(f"Masked data from {fl}")

        flname = os.path.splitext(fl)[0]
        save_format(args.output_path, flname, text)


if __name__ == "__main__":
    import argparse
    import logging
    import os
    import spacy

    from utils import get_text, save_format, set_logger
    main()
