#!/home/workboots/workEnv/bin/python3

"""script.py: Run all pre-processing scripts

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = ""
__email__ = "upal.bhattacharya@gmail.com"
"""
import spacy

from clean import clean
from mask import mask, patterns
from segment import segment, custom_sentencizer
from extract_statutes import extract_statutes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load data from.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data.")

    args = parser.parse_args()

    set_logger(os.path.join(args.output_path, "process.log"))

    # Defining the nlp object
    nlp = spacy.load("en_core_web_trf",
                     disable=['transformer', 'ner', 'parser',
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
         "kwargs": {"per_sentence": True}}
    ]

    for fl in os.listdir(args.input_path):
        # Get text
        text = get_text(os.path.join(args.input_path, fl))

        for params in pipelines:
            # TODO implement dot based access
            text = params["method"](text=text, **params["kwargs"])

        logging.info(f"Pre-processed data from {fl}")

        flname = os.path.splitext(fl)[0]
        save_format(args.output_path, flname, text)


if __name__ == "__main__":
    import argparse
    import logging
    import os

    from utils import get_text, set_logger, save_format
    main()
