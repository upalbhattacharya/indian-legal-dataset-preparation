#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-02-15 16:46:12.851710847 +0530
# Modify: 2022-02-15 17:37:15.408460406 +0530

"""Selecting cases for a given list of sections."""

import argparse
import json
import os
from collections import defaultdict


def remove_cases(cases_dict: dict, remove: list) -> dict:
    """Remove given list of cases from each dictionary element

    Parameters
    ----------
    cases_dict : dict
        Dictionary from which to remove the list of cases.
    remove : list
        List of cases to remove.

    Returns
    -------
    dict

    """

    for key in cases_dict:
        for case in remove:
            if case in set(cases_dict[key]):
                cases_dict[key].remove(case)

    return cases_dict


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--section_list_path",
                        help="Path to document containing relevant sections.")
    parser.add_argument("-c", "--case_statute_path",
                        help="Path to case statute information.")
    parser.add_argument("-n", "--num_cases", type=int, default=250,
                        help="Number of cases to select for each section.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated split data.")

    args = parser.parse_args()

    with open(args.section_list_path, 'r') as f:
        sections = f.readlines()

    sections = [sec.strip("\n") for sec in sections]

    with open(args.case_statute_path, 'r') as f:
        case_statute_info = json.load(f)

    statute_cases = defaultdict(lambda: list())

    # Getting the cases for each statute
    for case in case_statute_info:
        for statute in case_statute_info[case]["sections"]:
            statute_cases[statute].append(case)

    # Selecting only the relevant sections and their cases
    rel_statute_cases = {
            k: v for k, v in statute_cases.items() if k in sections}

    # Sorting the cases in terms of number of relevant sections cited
    rel_statute_cases = {
            k: sorted(v,
                      key=lambda x: len(
                        set(case_statute_info[x]["sections"]).intersection(
                            set(sections))))
            for k, v in rel_statute_cases.items()}

    # Selecting cases for each statute
    selected_cases = {}
    for sec in rel_statute_cases:
        selected_cases[sec] = rel_statute_cases[sec][:args.num_cases]
        # Removing selected cases from the pool of available cases
        rel_statute_cases = remove_cases(rel_statute_cases,
                                         selected_cases[sec])

    # For sanity checks
    #  for sec in selected_cases:
        #  print(sec)
        #  for case in selected_cases[sec]:
            #  print(case, len(
                #  set(case_statute_info[case]["sections"]).intersection(
                    #  set(sections))))

    with open(os.path.join(args.output_path, "selected_cases.json"), 'w') as f:
        json.dump(selected_cases, f, indent=4)


if __name__ == "__main__":
    main()
