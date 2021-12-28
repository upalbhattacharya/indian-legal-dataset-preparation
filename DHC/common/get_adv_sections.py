#!/home/workboots/workEnv/bin/python3
"""get_adv_sections.py: Finds the sections cited for each advocate from their
cases.

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = "1.1"
__email__ = "upal.bhattacharya@gmail.com"
"""
import argparse
import json
import logging
import os
import pickle
#  import re
from collections import Counter, defaultdict
from itertools import combinations

from utils import set_logger

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_path",
                    help="Path to load advocate cases.")
parser.add_argument("-a", "--advocates_path", default=None,
                    help="Path to load selected advocates from.")
parser.add_argument("-o", "--output_path", default=None,
                    help="Path to save generated data.")
parser.add_argument("-s", "--section_path",
                    help="Path to load section information for cases.")


def prettify(text: str) -> str:
    text = text.split("_")
    if (text[0] == "Constitution"):
        return (text[0] + "; Article " + text[-1])

    return (text[0] + "; Section " + text[-1])


def get_case_sections(path: str, case: str) -> list:
    """Return list of statutes cited."""

    with open(os.path.join(path, f"{case}.json"), 'r') as f:
        data = json.load(f)

    secs = list(set(
        [sec for line in data.values() for sec in line["sections"]]))

    return secs


def main():
    args = parser.parse_args()

    if (args.output_path is None):
        args.output_path = args.input_path

    if (args.advocates_path is None):
        args.advocates_path = args.input_path

    set_logger(os.path.join(args.output_path, "get_adv_sections.log"))

    # Loading selected advocates
    with open(os.path.join(
            args.advocates_path, "selected_advs.json"), 'r') as f:
        advs = json.load(f)

    with open(os.path.join(args.input_path, "adv_cases.json"), 'r') as f:
        adv_cases = json.load(f)

    cases = list(set([case for k, cases in adv_cases.items()
                      for case in cases if k in advs.values()]))

    section_dict = {}
    common_sections = {}
    common_sections_num = {}
    num_count = defaultdict(lambda: dict())

    case_sections = {}

    for i, case in enumerate(cases):
        case_sections[case] = get_case_sections(args.section_path, case)
        logging.info(f"Found sections {case_sections[case]} for {case}. "
                     f"{i+1}/{len(cases)}")

    for k, cases in adv_cases.items():
        if not(k in list(advs.values())):
            continue

        num_count[k]["total"] = len(cases)
        num_count[k]["rel"] = 0
        sec_list = []
        for case in cases:
            secs = case_sections[case]

            if (secs == []):
                continue

            sec_list.extend(secs)
            num_count[k]["rel"] += 1

        section_dict[k] = Counter(sec_list)
        logging.info(f"Found sections {sec_list} for adv {k}.")

    for adv_1, adv_2 in combinations(advs.values(), 2):
        common_sections[(adv_1, adv_2)] = (section_dict[adv_1] &
                                           section_dict[adv_2])
        common_sections_num[(adv_1, adv_2)] = len(common_sections[(adv_1,
                                                                   adv_2)])

    p_section_dict = {}

    for k, v in section_dict.items():
        p_section_dict[k] = {
            prettify(k1): v1
            for k1, v1 in sorted(v.items(),
                                 key=lambda x: x[1],
                                 reverse=True)}

    min_num_sections = min([len(secs) for secs in p_section_dict.values()])
    max_num_sections = max([len(secs) for secs in p_section_dict.values()])
    avg_num_sections = (1./len(p_section_dict.keys())
                        * sum([len(secs) for secs in p_section_dict.values()]))

    with open(os.path.join(args.output_path, "adv_num_counts.json"), 'w') as f:
        json.dump(num_count, f, indent=4)

    with open(os.path.join(args.output_path, "adv_sections.json"), 'w') as f:
        json.dump(section_dict, f, indent=4)

    with open(os.path.join(args.output_path, "adv_sections_pretty.json"),
              'w') as f:
        json.dump(p_section_dict, f, indent=4)

    with open(os.path.join(args.output_path, "adv_sections_pretty.txt"),
              'w') as f:
        for k, v in p_section_dict.items():
            print(k, file=f, end='\n')
            for sec, freq in v.items():
                print(f"\t{sec}: {freq}", file=f, end='\n')

    with open(os.path.join(args.output_path, "adv_section_stats.txt"),
              'w') as f:
        print(f"max: {max_num_sections}", file=f, end='\n')
        print(f"min: {min_num_sections}", file=f, end='\n')
        print(f"avg: {avg_num_sections}", file=f, end='\n')

    with open(os.path.join(args.output_path, "common_sections.pkl"),
              'wb') as f:
        pickle.dump(common_sections, f)

    with open(os.path.join(args.output_path, "common_sections_num.pkl"),
              'wb') as f:
        pickle.dump(common_sections_num, f)


if __name__ == "__main__":
    main()
