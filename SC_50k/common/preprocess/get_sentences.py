#!/usr/bin/env python

"""Extract sentences from sentence-separated json files"""

import argparse
import json
import logging
import os

from joblib import Parallel, delayed

from utils import set_logger

__author__ = "Upal Bhattacharya"
__license__ = ""
__version__ = "1.0"
__copyright__ = ""
__email__ = "upal.bhattacharya@gmail.com"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to input data")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data")
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
    """Parallelization of sentence extraction"""
    set_logger(os.path.join(kwargs["log_path"], "get_sentences"))
    logging.info("Inputs:")
    for name, value in kwargs.items():
        logging.info(f"{name}: {value}")

    with open(os.path.join(kwargs["input_path"], kwargs["fl"]), 'r') as f:
        dct = json.load(f)

    flname = os.path.splitext(kwargs["fl"])[0]
    logging.info(f"Getting sentences of {flname}")
    with open(os.path.join(kwargs["output_path"], f"{flname}.txt"), 'w') as f:
        for idx, data in dct.items():
            print(data["text"], file=f, end="\n")


if __name__ == "__main__":
    main()
