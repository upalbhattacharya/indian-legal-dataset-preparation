#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- coding: utf-8 -*-
# Birth: 2022-02-28 11:55:29.254896018 +0530
# Modify: 2022-02-28 17:05:35.002060082 +0530

"""Remove extra whitespaces, non-utf-8 characters and carry out substitutions.
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
    "Cr. PC",
    "Cr.P.C."]

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

    # Remove indexed points
    text = re.sub(r'[0-9]+\.', '', text)

    # Remove extra newline and whitespace characters
    text = re.sub(r'\s+', ' ', text)

    # Remove headers
    header_end = re.search(r'\* \* \*', text)
    end = header_end.span()[-1]
    text = text[end:]

    # Remove footers

    # Might be a more efficient way than conversion of iterators to list
    # Possible usage of regex library instead of re which has the flag
    # regex.REVERSE

    end_1 = re.finditer(r'\\-+', text)
    end_1 = list(end_1)
    end_2 = re.finditer(r'\* \* \*', text)
    end_2 = list(end_2)
    end_2 = end_2[-1] if len(end_2) > 1 else end_2[0]
    if end_1 != []:
        end_1 = end_1[-1] if len(end_1) > 1 else end_1[0]
        doc_end = min(end_1.span()[0], end_2.span()[0])
    else:
        doc_end = end_2.span()[0]
    text = text[:doc_end]

    # Remove citations

    # Deliberately handle particular case
    text = re.sub(r'cgi- ', 'cgi-', text)

    citation_match = re.findall(
            r'\((?:http[s]?)?:?/?/(?:[a-zA-Z]|[0-9]|[$-_@.&+?]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\)',
            text)

    for match in citation_match:
        print(match)
        text = re.sub(re.escape(rf"{match}"), '', text)

    # Remove strange characters and non fullstop punctuations
    if (punct is None):
        punct = punctuation
    text = re.sub(r"[^\w./\s-]", '', text)

    # Remove extra hyphens and multiple dots

    text = re.sub(r'(\.\s*){2,}', '.', text)
    # Removing all punctuations except those appearing for sections
    text = re.sub(r'([a-zA-Z]+\s?)[-/]+(\s?[a-zA-Z]+)', r'\1 \2', text)
    text = re.sub(r'\s+', ' ', text)
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
        if text is None:
            continue
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
