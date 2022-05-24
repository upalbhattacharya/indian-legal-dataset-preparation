#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-02-23 17:20:26.461216037 +0530
# Modify: 2022-02-23 17:21:20.301215125 +0530

"""Get sentences of each document based on the rhetorical roles provided."""

import os
import json
import argparse

__author__ = "Upal Bhattacharya"
__license__ = ""
__copyright__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load sentence separated data from.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save selected sentences per document.")
    parser.add_argument("-r", "--roles", nargs='+', type=str,
                        default=["Facts"],
                        help="Rhetorical roles of sentences to collect.")

    args = parser.parse_args()

    # Loading each file and getting the appropriate sentences
    for filename in os.listdir(args.input_path):
        with open(os.path.join(args.input_path, filename), 'r') as f:
            json_obj = json.load(f)

        # Getting the document name/ID
        flname = os.path.splitext(filename)[0]
        with open(os.path.join(args.output_path, f"{flname}.txt"), 'a') as f:
            for idx in json_obj:
                # Skip document if it does not have rhetorical roles
                if (json_obj[idx].get("role", -1) == -1):
                    break
                if json_obj[idx]["role"] in args.roles:
                    print(json_obj[idx]["text"], file=f, end="\n")


if __name__ == "__main__":
    main()
