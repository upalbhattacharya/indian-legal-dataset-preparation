#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- coding: utf-8 -*-
# Last Modified: Wed Jan 05, 2022  02:17PM

"""
Find section, chapter and act information of cases.
"""

import argparse
import json
import logging
import os
from collections import Counter, defaultdict

from utils import order, set_logger

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def get_act_chapter_section_info(secs: list, chapter_info: dict) -> dict:
    """Return act, chapter and section frequency dictionary
    from list of sections.

    Parameters
    ----------
    secs : list
        List of sections cited
    chapter_info: dict
        Information of chapters for all sections to get chapter information

    Returns
    -------
    dict

    """

    acts = list(map(lambda x: x.split("_")[0], secs))
    acts = dict(Counter(acts))
    acts = order(acts)
    sections = dict(Counter(secs))
    sections = order(sections)
    chapters = list(filter(None, map(lambda x: chapter_info.get(x, ""), secs)))
    chapters = dict(Counter(chapters))
    chapters = order(chapters)

    statute = {
            "acts": acts,
            "chapters": chapters,
            "sections": sections,
            }

    return statute


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load files from.")
    parser.add_argument("-c", "--chapter_info",
                        help="Dictionary with chapter information")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data.")

    args = parser.parse_args()
    set_logger(os.path.join(args.output_path, "get_act_chapter_section_info"))

    with open(args.chapter_info, 'r') as f:
        chapter_info = json.load(f)

    case_act_chapter_section_info = {}
    act_case_info = defaultdict(list)
    chapter_case_info = defaultdict(list)
    section_case_info = defaultdict(list)

    for fl in os.listdir(args.input_path):
        logging.info(f"Get statute information from {fl}.")
        flname = os.path.splitext(fl)[0]
        with open(os.path.join(args.input_path, fl), 'r') as f:
            doc = json.load(f)
        secs = [sec for sent in doc.values()
                for sec in sent["sections"].keys()]

        act_sec = get_act_chapter_section_info(secs, chapter_info)
        case_act_chapter_section_info[flname] = act_sec

        for act in act_sec["acts"]:
            act_case_info[act].append(flname)

        for chapter in act_sec["chapters"]:
            chapter_case_info[chapter].append(flname)

        for section in act_sec["sections"]:
            section_case_info[section].append(flname)

    act_case_num = {
            k: len(v) for k, v in sorted(act_case_info.items(),
                                         key=lambda x: len(x[1]),
                                         reverse=True)}

    chapter_case_num = {
            k: len(v) for k, v in sorted(chapter_case_info.items(),
                                         key=lambda x: len(x[1]),
                                         reverse=True)}

    section_case_num = {
            k: len(v) for k, v in sorted(section_case_info.items(),
                                         key=lambda x: len(x[1]),
                                         reverse=True)}

    with open(os.path.join(args.output_path, "case_act_chapter_section_info.json"),
              'w') as f:
        json.dump(case_act_chapter_section_info, f, indent=4)

    with open(os.path.join(args.output_path, "act_case_info.json"),
              'w') as f:
        json.dump(act_case_info, f, indent=4)

    with open(os.path.join(args.output_path, "chapter_case_info.json"),
              'w') as f:
        json.dump(chapter_case_info, f, indent=4)

    with open(os.path.join(args.output_path, "section_case_info.json"),
              'w') as f:
        json.dump(section_case_info, f, indent=4)

    with open(os.path.join(args.output_path, "act_case_num.json"),
              'w') as f:
        json.dump(act_case_num, f, indent=4)

    with open(os.path.join(args.output_path, "chapter_case_num.json"),
              'w') as f:
        json.dump(chapter_case_num, f, indent=4)

    with open(os.path.join(args.output_path, "section_case_num.json"),
              'w') as f:
        json.dump(section_case_num, f, indent=4)


if __name__ == "__main__":
    main()
