#!/usr/bin/env python

"""Extract sentences from sentence-separated json files"""

import json
import argparse
import os
from utils import set_logger
from joblib import Parallel, delayed

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

    args = parser.parse_args()

    with Parallel(n_jobs=-1) as parallel:
        parallel([delayed(parallelize)(fl=fl,
                                    input_path=args.input_path,
                                    output_path=args.output_path)
                  for fl in os.listdir(args.input_path)])


def parallelize(**kwargs):
    """Parallelization of sentence extraction"""
    with open(os.path.join(kwargs["input_path"], kwargs["fl"]), 'r') as f:
        dct = json.load(f)

    flname = os.path.splitext(kwargs["fl"])[0]
    with open(os.path.join(kwargs["output_path"], f"{flname}.txt"), 'w') as f:
        for idx, data in dct.items():
            print(data["text"], file=f, end="\n")


if __name__ == "__main__":
    main()
