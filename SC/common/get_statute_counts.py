#!/usr/bin/env python

"""Get counts for each statute"""

import argparse
import json
import os
from collections import defaultdict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case_statute_path",
                        help="json file with statutes for each case")
    parser.add_argument("--output_path",
                        help="Path to save generated data")

    args = parser.parse_args()

    with open(args.case_statute_path, 'r') as f:
        case_statute_info = json.load(f)

    statute_cases = defaultdict(lambda: list())
    act_cases = defaultdict(lambda: list())
    for case, info in case_statute_info.items():
        for act in info["acts"]:
            act_cases[act].append(case)

        for statute in info["sections"]:
            statute_cases[statute].append(case)

    act_cases_count = {k: len(v) for k, v in sorted(act_cases.items(),
                                                    key=lambda x: len(x[1]),
                                                    reverse=True)}

    statute_cases_count = {k: len(v) for k, v in sorted(statute_cases.items(),
                                                    key=lambda x: len(x[1]),
                                                    reverse=True)}

    with open(os.path.join(args.output_path, "statute_case_info.json"),
              'w') as f:
        json.dump(statute_cases, f, indent=4)

    with open(os.path.join(args.output_path, "statute_case_counts.json"),
              'w') as f:
        json.dump(statute_cases_count, f, indent=4)

    with open(os.path.join(args.output_path, "act_case_info.json"),
              'w') as f:
        json.dump(act_cases, f, indent=4)

    with open(os.path.join(args.output_path, "act_case_counts.json"),
              'w') as f:
        json.dump(act_cases_count, f, indent=4)

if __name__ == "__main__":
    main()
