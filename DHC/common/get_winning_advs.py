#!/usr/bin/env python

"""Getting winning advocates of each case based on ruling in favour of
Petitioner or Defendant"""

import argparse
import json
import os
from collections import defaultdict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case_decisions",
                        help="Path to json file with case ruling")
    parser.add_argument("--petitioner_cases",
                        help="Path to json with petitioners of each case")
    parser.add_argument("--defendant_cases",
                        help="Path to json with defendants of each case")
    parser.add_argument("--output_path",
                        help="Path to save generated data")

    args = parser.parse_args()

    with open(args.case_decisions, 'r') as f:
        case_decisions = json.load(f)

    with open(args.petitioner_cases, 'r') as f:
        petitioner_cases = json.load(f)

    with open(args.defendant_cases, 'r') as f:
        defendant_cases = json.load(f)

    case_winners = {}

    case_petitioners = defaultdict(list)
    case_defendants = defaultdict(list)

    for adv, cases in petitioner_cases.items():
        for case in cases:
            case_petitioners[case].append(adv)

    for adv, cases in defendant_cases.items():
        for case in cases:
            case_defendants[case].append(adv)

    for case, verdict in case_decisions.items():
        if verdict == 1:
            case_winners[case] = case_petitioners[case]
        else:
            case_winners[case] = case_defendants[case]

    with open(os.path.join(args.output_path, "case_winners.json"), 'w') as f:
        json.dump(case_winners, f, indent=4)


if __name__ == "__main__":
    main()
