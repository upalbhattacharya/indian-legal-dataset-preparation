#!/home/workboots/workEnv/bin/python3
# -*- coding: utf-8 -*-

"""Mask various patterns for given data.
"""

import re
from typing import List, Pattern, Tuple

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"

# Regex patterns used to mask different information
patterns = [
    ('name',
        r'M(?:r|s|rs)\.\s*[A-Za-z.]+\s+[A-Za-z.]+(?:\s+[A-Za-z]+)?,?',
        '[NAME]'),
    ('date_1',
        r'([0-9]?[0-9](\.|\/)[0-9]{2}(\.|\/)[0-9]{4})',
        '[DATE]'),
    ('date_2',
        r'([a-zA-Z]+\s+[0-9]?[0-9](st|nd|rd|th)?,?\s+[0-9]{4})',
        '[DATE]'),
    ('date_3',
        r'([0-9]?[0-9](st|nd|rd|th)?\s+[A-Za-z]+,?\s+[0-9]{4})',
        '[DATE]'),
    ('page',
        r'(Page \d+ of \d+)',
        ''),
    ('time',
        (r'([0-9]?[0-9]:\d{2}(:\d{2})?,?(\s+)?'
         r'(am|pm|AM|PM)?(\s+)?,?(IST)?)'),
        '[TIME]')
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load data from.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data.")

    args = parser.parse_args()

    set_logger(os.path.join(args.output_path, "mask.log"))

    for fl in os.listdir(args.input_path):
        # Get text
        text = get_text(os.path.join(args.input_path, fl))
        text = mask(text, patterns)

        logging.info(f"Masked data from {fl}")

        flname = os.path.splitext(fl)[0]
        save_format(args.output_path, flname, text)


if __name__ == "__main__":
    import argparse
    import logging
    import os

    from utils import set_logger, get_text, save_format
    main()
