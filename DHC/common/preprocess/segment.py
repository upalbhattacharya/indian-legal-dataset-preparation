#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- coding: utf-8 -*-
# Birth: 2022-08-15 10:52:32.675467926 +0530
# Modify: 2022-08-16 19:22:19.949992230 +0530

"""Segments documents into sentences.
"""

import argparse
import logging
import os
from collections import defaultdict

import spacy
from spacy.language import Language

from utils import get_text, save_format, set_logger

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


@Language.component("custom_sentencizer")
def custom_sentencizer(doc: str) -> object:
    """ Custom sentencizer for DHC corpus.

    Parameters
    ----------
    doc : str
        Text to process.

    Returns
    -------
    doc : spacy.Doc
        spacy document with sentence boundaries.

    Notes
    -----

    """
    # Exception tokens
    exceptions = ["mr.", "ms.", "mrs.", "adv.", "advs.", "sr.",
                  "dr.", "m.", "crl.", "a.", "advocate.", "advocates.",
                  "w.", "p.", "fir.", "ltd."]

    # The last token cannot start a sentence
    for i, token in enumerate(doc[:-2]):
        #  if token.text[0] == "." or token.text[-1] == ".":

        if token.text[-1] == "." or token.text[-1] == ":":

            doc[i+1].is_sent_start = True

            if (not doc[i+1].text[0].isupper() or
                    doc[i+1].text[-1] == '.'):
                doc[i+1].is_sent_start = False

            if (token.text.lower() in exceptions):
                doc[i+1].is_sent_start = False

            if (token.text == '.'):
                doc[i+1].is_sent_start = True

            if (doc[i].is_sent_start is True):
                doc[i+1].is_sent_start = False

    return doc


def segment(text: str, nlp) -> dict:
    """Segment sentences by boundary.

    Parameters
    ----------
    text : str
        Text to process.
    nlp : spacy object(?)
        Spacy object to use for segmentation.

    Returns
    -------
    sent_dict : dict
        Dictionary containing each sentence and their span.
    """
    doc = nlp(text)

    sent_dict = defaultdict(lambda: dict())

    for i, sent in enumerate(doc.sents):
        start = sent.start_char
        end = sent.end_char
        sent_dict[i] = {
            "span": tuple((start, end)),
            "text": sent.text,
        }

    sent_dict = fix_sentence_boundaries(sent_dict)
    return sent_dict


def fix_sentence_boundaries(sentence_dict: dict) -> dict:
    """Fix sentence boundaries to account for extra spaces ignored by spacy.

    Parameters
    ----------
    sentence_dict: dict
        Dictionary containing sentence text and spans.


    Returns
    -------
    sent_dict: dict
        Dictionary containing sentence texts and rectified spans.
    """
    shift = 0
    sent_dict = defaultdict(lambda: dict())
    text = " ".join([items["text"] for items in sentence_dict.values()])

    for idx, items in sentence_dict.items():
        start, end = items["span"]
        for char in text[start + shift: end + shift]:
            if char not in [' ', '.']:
                break
            shift += 1

        sent_dict[idx] = {
            "span": tuple((start + shift, end + shift)),
            "text": items["text"]
        }
    return dict(sent_dict)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load data from.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data.")

    args = parser.parse_args()

    set_logger(os.path.join(args.output_path, "segment"))

    nlp = spacy.blank('en')
    # Adding the sentencizer to the pipeline
    nlp.add_pipe("custom_sentencizer")
    # Accomodating longer sentences
    nlp.max_length = 5000000

    for fl in os.listdir(args.input_path):
        # Get text
        text = get_text(os.path.join(args.input_path, fl))
        if len(text) > nlp.max_length:
            text = text[:nlp.max_length]
        text = segment(text, nlp)

        logging.info(f"Segmented sentences for {fl}")

        flname = os.path.splitext(fl)[0]
        save_format(args.output_path, flname, text)


if __name__ == "__main__":
    main()
