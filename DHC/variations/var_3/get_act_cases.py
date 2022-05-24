#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-02-23 19:18:52.291096642 +0530
# Modify: 2022-02-23 19:45:04.704403825 +0530

"""Get cases of the given acts. Copy the selected cases from the provided
directory to the target directory."""

import json
import os
import argparse
import subprocess

__author__ = "Upal Bhattacharya"
__license__ = ""
__copyright__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_path",
                        help="Path to files to select from and move.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save selected files.")
    parser.add_argument("-s", "--statute_info_path",
                        help="Path to case_statute_info.json file.")
    parser.add_argument("-a", "--acts_path",
                        help=("Path to file with names of acts to use to "
                              "select."))

    args = parser.parse_args()

    # Getting the file extension of files
    ext = os.path.splitext(os.listdir(args.data_path)[0])[-1]

    with open(args.statute_info_path, 'r') as f:
        case_statute_info = json.load(f)

    # Getting the names of the acts
    with open(args.acts_path, 'r') as f:
        acts = f.read()
    acts = list(filter(lambda x: x != "", acts.split("\n")))

    for doc, v in case_statute_info.items():
        if set(v['acts']).intersection(set(acts)) != set():
            # Copy document to the destination
            subprocess.Popen(
                        ['cp',
                         os.path.join(args.data_path,
                                      f"{doc}{ext}"), args.output_path])
            # Documenting which cases were selected
            with open(os.path.join(args.output_path, "act_cases.txt"),
                      'a') as f:
                print(doc, file=f, end="\n")


if __name__ == "__main__":
    main()
