#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# stat: cannot statx 'get_per_charge_win_ratios.py': No such file or directory
# stat: cannot statx 'get_per_charge_win_ratios.py': No such file or directory

"""Compute per-charge win ratios of advocates. Different strategies can be used
for this computation."""

import argparse
import json
import os
from collections import defaultdict


def avg_win_ratio(case_list: list, scores: dict) -> float:
    """Compute average win-ratio from a given list of cases.

    Parameters
    ----------
    case_list: list
        List of cases.
    scores: dict
        Dictionary with case decisions.

    Returns
    -------
    ratio: float
        Computed win_ratio.
    """
    return ((sum([scores[case] for case in case_list]) * 1./len(case_list))
            if len(case_list) != 0 else 0.0)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--case_decisions",
                        help="Path to case decisions json.")
    parser.add_argument("--charges",
                        help="Path to charges to consider.")
    parser.add_argument("--advocates",
                        help="Path to dictionary of advocates to consider.")
    parser.add_argument("--charge_cases",
                        help="Path to cases of each charge json.")
    parser.add_argument("--advocate_cases",
                        help="Path to advocate cases json.")
    parser.add_argument("--output_path",
                        help="Path to save generated scores.")

    args = parser.parse_args()

    # Get relevant charges
    with open(args.charges, 'r') as f:
        charges = f.readlines()
    charges = list(filter(None, map(lambda x: x.strip("\n"), charges)))

    # Get cases of charges
    with open(args.charge_cases, 'r') as f:
        charge_cases = json.load(f)

    # Get relevant advocates
    with open(args.advocates, 'r') as f:
        advs = json.load(f)

    # Get cases of each advocate
    with open(args.advocate_cases, 'r') as f:
        adv_cases = json.load(f)

    # Get case decisions
    with open(args.case_decisions, 'r') as f:
        case_decisions = json.load(f)

    charge_adv_win_ratios = defaultdict(lambda: dict())
    for charge in charges:
        for adv in advs.values():
            case_list = set(adv_cases[adv]).intersection(
                        set(charge_cases[charge]))
            charge_adv_win_ratios[charge][adv] = avg_win_ratio(case_list,
                                                               case_decisions)
        # Order by score
        charge_adv_win_ratios[charge] = {
                                    k: v
                                    for k, v in sorted(
                                        charge_adv_win_ratios[charge].items(),
                                        key=lambda x: x[1], reverse=True)}

    # Save results
    with open(os.path.join(args.output_path,
                           "charge_adv_win_ratios.json"), 'w') as f:
        json.dump(charge_adv_win_ratios, f, indent=4)


if __name__ == "__main__":
    main()
