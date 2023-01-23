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

import numpy as np

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def avg_win_ratio(p_cases: set, d_cases: set, scores: dict) -> float:
    """Compute average win-ratio of one advocate from a given list of cases.

    Parameters
    ----------
    p_cases: set
        Set of cases where advocate was petitioner.
    d_cases: set
        Set of cases where advocate was defendant.
    scores: dict
        Dictionary with case decisions.

    Returns
    -------
    ratio: float
        Computed win_ratio.
    """
    case_list = list(p_cases.union(d_cases))
    won_p = (np.array([scores[case] for case in case_list]) *
             np.array([case in p_cases for case in case_list]))
    won_d = (np.array([1 - scores[case] for case in case_list]) *
             np.array([case in d_cases for case in case_list]))

    return ((sum(won_p + won_d) * 1./len(case_list))
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
    parser.add_argument("--petitioner_info",
                        help=("Path to dictionary containing petitioner "
                              " cases of each advocate json."))
    parser.add_argument("--defendant_info",
                        help=("Path to dictionary containing defendant "
                              " cases of each advocate json."))
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

    # Get advocate petitioner and advocate cases
    with open(args.petitioner_info, 'r') as f:
        p_info = json.load(f)

    with open(args.defendant_info, 'r') as f:
        d_info = json.load(f)

    charge_adv_win_ratios = defaultdict(lambda: dict())
    for charge in charges:
        for adv in advs.values():
            case_list = set(adv_cases[adv]).intersection(
                        set(charge_cases[charge]))
            if p_info.get(adv, -1) == -1:
                print(f"{adv} has no petitioner cases")

            if d_info.get(adv, -1) == -1:
                print(f"{adv} has no respondent cases")

            p_cases = case_list.intersection(
                                        set(p_info.get(adv, [])))
            d_cases = case_list.intersection(
                                        set(d_info.get(adv, [])))
            charge_adv_win_ratios[charge][adv] = avg_win_ratio(p_cases,
                                                               d_cases,
                                                               case_decisions)
        # Order by score
        charge_adv_win_ratios[charge] = {
                                    k: v
                                    for k, v in sorted(
                                        charge_adv_win_ratios[charge].items(),
                                        key=lambda x: x[1], reverse=True)}

    # Save results
    with open(os.path.join(args.output_path,
                           "charge_adv_win_ratios_new.json"), 'w') as f:
        json.dump(charge_adv_win_ratios, f, indent=4)


if __name__ == "__main__":
    main()
