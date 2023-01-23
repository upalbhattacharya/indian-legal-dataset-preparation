#!/usr/bin/env python

"""Getting winning advocates of each case based on ruling in favour of
Petitioner or Defendant"""

import argparse
import json
import logging
import os
from collections import defaultdict

from utils import set_logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--case_decisions",
                        help="Path to json file with case ruling")
    parser.add_argument("-t", "--overall_targets", type=str, default=None,
                        help="Overall targets of cases")
    parser.add_argument("-p", "--petitioner_cases",
                        help="Path to json with petitioners of each case")
    parser.add_argument("-d", "--defendant_cases",
                        help="Path to json with defendants of each case")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data")

    args = parser.parse_args()
    set_logger(os.path.join(args.output_path, "get_winning_advs"))
    logging.info("Inputs:")
    for name, value in vars(args).items():
        logging.info(f"{name}: {value}")

    # Load data
    with open(args.case_decisions, 'r') as f:
        case_decisions = json.load(f)

    with open(args.petitioner_cases, 'r') as f:
        petitioner_cases = json.load(f)

    with open(args.defendant_cases, 'r') as f:
        defendant_cases = json.load(f)

    if args.overall_targets is not None:
        with open(args.overall_targets, 'r') as f:
            overall_targets = json.load(f)
        case_decisions = {
                k: case_decisions[k]
                for k in overall_targets}

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
        p_adv = case_petitioners[case]
        d_adv = case_defendants[case]
        advs = list(set(p_adv).union(set(d_adv)))
        if args.overall_targets is not None:
            advs = overall_targets[case]
            p_adv = list(set(p_adv).intersection(set(advs)))
            d_adv = list(set(d_adv).intersection(set(advs)))
        # Reverting to all advocates if either portion is empty
        p_adv = p_adv if p_adv != [] else advs
        d_adv = d_adv if d_adv != [] else advs

        if verdict == 1:
            case_winners[case] = p_adv
        else:
            case_winners[case] = d_adv

    with open(os.path.join(args.output_path, "case_winners.json"), 'w') as f:
        json.dump(case_winners, f, indent=4)


if __name__ == "__main__":
    main()
