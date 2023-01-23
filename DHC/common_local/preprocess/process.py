#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- coding: utf-8 -*-

# Birth: 2022-08-15 10:52:32.603469491 +0530
# Modify: 2022-08-16 10:55:20.710236438 +0530

"""Run all pre-processing scripts in a pipeline.
"""

import os

import spacy
from joblib import Parallel, delayed
from spacy.language import Language

from clean import clean
from extract_statutes import extract_statutes
from mask import mask, ner_mask, patterns
from segment import custom_sentencizer, segment

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = ""
__email__ = "upal.bhattacharya@gmail.com"

present_dir = os.path.dirname(__file__)
# Getting the set of statutes
with open(os.path.join(present_dir, "act_titles.txt"), 'r') as f:
    acts = f.read()
acts = acts.split("\n")
acts.remove("Constitution")

with open(os.path.join(present_dir, "section_titles.txt"), 'r') as f:
    statutes = f.read()
statutes = statutes.split("\n")

statutes = {k: k for k in statutes}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load data from. Processes HTML files")
    parser.add_argument("-o", "--output_path",
                        help="Path to save cleaned data. Generates JSON files")

    args = parser.parse_args()

    set_logger(os.path.join(args.output_path, "process"))

    # Defining the nlp object
    nlp = spacy.load("en_core_web_trf",
                     disable=['transformer', 'parser',
                              'tagger', 'attribute_ruler', 'lemmatizer'])

    # Accomodating longer sentences
    nlp.max_length = 2000000

    # Adding the sentencizer to the pipeline
    nlp.add_pipe("custom_sentencizer")

    # Various pre-processing strategies
    pipelines = [
        {"method": clean,
         "kwargs": {}},
        {"method": mask,
         "kwargs": {"patterns": patterns}},
        {"method": segment,
         "kwargs": {"nlp": nlp}},
        {"method": extract_statutes,
            "kwargs": {"per_sentence": True,
                       "acts": acts,
                       "statutes": statutes}}
    ]

    with Parallel(n_jobs=-1) as parallel:
        parallel([delayed(parallelize)(fl=fl,
                                       input_path=args.input_path,
                                       output_path=args.output_path,
                                       pipelines=pipelines)
                  for fl in os.listdir(args.input_path)])


def parallelize(**kwargs):
    fl = kwargs["fl"]
    input_path = kwargs["input_path"]
    output_path = kwargs["output_path"]

    logging.info(f"Pre-processing data from {fl}")
    text = get_text(os.path.join(input_path, fl))

    for params in kwargs["pipelines"]:
        # TODO implement dot based access
        text = params["method"](text=text, **params["kwargs"])

    flname = os.path.splitext(fl)[0]
    save_format(output_path, flname, text)
    logging.info("="*40)


if __name__ == "__main__":
    import argparse
    import logging
    import os

    from utils import get_text, save_format, set_logger
    main()
