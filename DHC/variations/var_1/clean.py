#!/home/workboots/workEnv/bin/python3
# -*- coding: utf-8 -*-

"""initial_clean.py: Remove extra whitespaces, non-utf-8 characters and carry
out substitutions.
"""

import os
import re
from string import punctuation

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

acts_dict = {k: [k] for k in acts}

acts_dict["Code of Criminal Procedure, 1898"] = [
    "Code of Criminal Procedure, 1898",
    "Criminal Procedure Code, 1898",
    "Cr.PC, 1898",
    "Cr.P.C., 1898",
    "Criminal Procedure Code, 1898",
    "Cr.PC, 1898",
    "Cr.P.C., 1898",
    "CrPC",
    "Cr PC",
    "Cr. P.C.",
    "Cr PC.",
    "Cr. P.C.",
    "Cr. PC"]

acts_dict["Code of Criminal Procedure, 1973"] = [
    "Code of Criminal Procedure, 1973",
    "Criminal Procedure Code, 1973",
    "Cr.PC, 1973",
    "Cr.P.C., 1973",
    "Criminal Procedure Code, 1973",
    "Cr.PC, 1973",
    "Cr.P.C., 1973"]

acts_dict["Code of Civil Procedure, 1908"] = [
    "Code of Civil Procedure, 1908",
    "Code of Civil Procedure",
    "Civil Procedure Code",
    "Code of Civil Procedure",
    "Civil Procedure Code",
    "CPC",
    "C.P.C",
    "C P C",
    "cPC",
    "C. P. C."]

acts_dict["Indian Penal Code, 1860"] = [
    "Indian Penal Code, 1860",
    "Indian Penal Code",
    "Penal Code",
    "IPC",
    "IPC",
    "I.P.C",
    "I.P.C",
    "I.P.C.",
    "I.P.C.",
    "I. P. C."]


def clean(text: str, **kwargs) -> str:
    """Clean unwanted characters, extra whitespaces, unnecessary punctuations
    and sentence splits.

    Parameters
    ----------
    text : str
        Text to process.

    Returns
    -------
    text : str
        Processed text.
    """
    # Remove non-utf-8 characters
    text = bytes(text, 'utf-8').decode('utf-8', 'ignore')

    # Remove indexed points
    text = re.sub(r'[0-9]+\.', '', text)

    # Remove strange characters
    text = re.sub(rf"[^\w{punctuation}\s]", '', text)

    # Remove extra whitespaces, hyphens and multiple dots

    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(\.\s*){2,}', '.', text)
    #  text = re.sub(r'(\.\s*){2-}', ' ', text)

    text = text.strip()

    # Substituting for consistency
    special_cases = {
        "Rs.": "rs.", "No.": "no.", "no.": "no.", "v.": "vs",
        "vs.": "vs", "i.e.": "i.e.", "viz.": "viz.", "M/s.": "m/s.",
        "Mohd.": "mohd.", "Ex.": "exhibit", "Art.": "article",
        "Arts.": "articles", "S.": "section", "s.": "section",
        "ss.": "sections", "u/s.": "section", "u/ss.": "sections",
        "art.": "article", "arts.": "articles", "u/arts.": "articles",
        "u/art.": "article", "hon'ble": "honourable"}

    # Subsituting citation variations
    for k, v in special_cases.items():
        if (k == 's.' and 'ss.' in text):
            text = text.replace("ss.", "sections")
        text = text.replace(f" {k}", f" {v}")
        text = text.replace("Constitution of India", "Constitution")

    for name, variations in acts_dict.items():
        for var in variations:
            if var in text:
                text = text.replace(var, name)

    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load data from.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data.")

    args = parser.parse_args()

    set_logger(os.path.join(args.output_path, "clean.log"))

    for fl in os.listdir(args.input_path):
        # Get text
        text = get_text(os.path.join(args.input_path, fl))
        text = clean(text)

        logging.info("Removed extra whitespaces and non-utf-8 characters from "
                     f"{fl}")

        flname = os.path.splitext(fl)[0]
        save_format(args.output_path, flname, text)


if __name__ == "__main__":
    import argparse
    import logging
    import os

    from utils import get_text, save_format, set_logger
    main()
