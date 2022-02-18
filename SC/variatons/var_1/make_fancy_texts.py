#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-02-15 18:16:50.318521777 +0530
# Modify: 2022-02-15 18:28:55.418540652 +0530

"""Generate fancy human-readable formats of the cases and cited sections."""

import json
import os
import argparse

__author__ = "Upal Bhattacharya"
__license__ = ""
__copyright__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dict_path",
                        help="Path to load relevant sections and cases.")
    parser.add_argument("-s", "--statute_path",
                        help="Path to case statute information.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated fancy text.")

    args = parser.parse_args()

    with open(args.dict_path, 'r') as f:
        relevant_cases = json.load(f)
    sections = list(relevant_cases.keys())

    with open(args.statute_path, 'r') as f:
        case_statute_info = json.load(f)

    for sec in sections:
        with open(os.path.join(args.output_path, f"{sec}.md"), 'a') as f:
            segments = sec.split("_")
            # Ugly way of pretty printing
            p_sec = segments[0] + f"; Section {segments[-1]}"
            print(f"# Cases of {p_sec}", file=f, end="\n")

            # Printing each case
            for case in relevant_cases[sec]:
                print(f"- {case}:", file=f, end="\n\n")
                secs = set(case_statute_info[case]["sections"]).intersection(
                        set(sections))
                for s in secs:
                    segments = s.split("_")
                    p_s = segments[0] + f"; Section {segments[-1]}"
                    print(f"\t\t - {p_s}", file=f, end="\n\n")


if __name__ == "__main__":
    main()
