#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last Modified: Wed Jan 05, 2022  02:17PM

"""
Find section, chapter and act information of advocates.
"""

import argparse
import json
import os
from collections import Counter, defaultdict
from itertools import chain

from utils import order, set_logger

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def get_area_act_chapter_section_info(secs: list, area_info: dict,
                                      chapter_info: dict) -> dict:
    """Return act, chapter and section frequency dictionary
    from list of sections.

    Parameters
    ----------
    secs : list
        List of sections cited
    area_info: dict
        Information of areas for all acts to get area information
    chapter_info: dict
        Information of chapters for all sections to get chapter information

    Returns
    -------
    dict

    """

    acts = list(map(lambda x: x.split("_")[0], secs))
    acts = dict(Counter(acts))
    acts = order(acts)
    areas = list(filter(None, map(lambda x: area_info.get(x, ""),
                                  acts.keys())))
    areas = list(chain.from_iterable(areas))
    areas = dict(Counter(list(areas)))
    areas = order(areas)
    sections = dict(Counter(secs))
    sections = order(sections)
    chapters = list(filter(None, map(lambda x: chapter_info.get(x, ""), secs)))
    chapters = dict(Counter(chapters))
    chapters = order(chapters)

    statute = {
            "areas": areas,
            "acts": acts,
            "chapters": chapters,
            "sections": sections,
            }

    return statute


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load case information from.")
    parser.add_argument("-ca", "--case_advs",
                        help="Case advocate information")
    parser.add_argument("-sc", "--selected_cases", type=str, default=None,
                        help="Cases to select")
    parser.add_argument("-sa", "--selected_advs", type=str, default=None,
                        help="Advocates to select")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data.")
    parser.add_argument("-l", "--log_path", type=str, default=None,
                        help="Path to save generated logs")

    args = parser.parse_args()
    if args.log_path is None:
        args.log_path = args.output_path

    set_logger(os.path.join(args.log_path,
               "get_area_act_chapter_section_info"))

    selected_cases = []
    if args.selected_cases is not None:
        with open(args.selected_cases, 'r') as f:
            selected_cases = f.readlines()
            selected_cases = list(filter(None, map(lambda x: x.strip("\n"),
                                                   selected_cases)))

    selected_advs = []
    if args.selected_advs is not None:
        with open(args.selected_advs, 'r') as f:
            selected_advs = f.readlines()
            selected_advs = list(filter(None, map(lambda x: x.strip("\n"),
                                                  selected_advs)))

    with open(args.input_path, 'r') as f:
        case_info = json.load(f)

    with open(args.case_advs, 'r') as f:
        case_advs = json.load(f)

    adv_area_act_chapter_section_info = defaultdict(dict)
    area_adv_info = defaultdict(list)
    act_adv_info = defaultdict(list)
    chapter_adv_info = defaultdict(list)
    section_adv_info = defaultdict(list)
    adv_cases = defaultdict(list)

    for case in case_info:
        if args.selected_cases is not None:
            if case not in selected_cases:
                continue

        advs = case_advs.get(case, [])
        advs = list(set(advs).intersection(set(selected_advs)))
        if advs == []:
            continue

        act_sec = case_info[case]

        for adv in advs:
            adv_cases[adv].append(case)
            if adv_area_act_chapter_section_info.get(adv, -1) == -1:
                adv_area_act_chapter_section_info[adv] = {
                                                        "areas": [],
                                                        "acts": [],
                                                        "chapters": [],
                                                        "sections": [],
                                                        }
            else:

                adv_area_act_chapter_section_info[adv]["areas"].extend(
                                                    act_sec["areas"])

                adv_area_act_chapter_section_info[adv]["acts"].extend(
                                                    act_sec["acts"].keys())

                adv_area_act_chapter_section_info[adv]["chapters"].extend(
                                                    act_sec["chapters"].keys())

                adv_area_act_chapter_section_info[adv]["sections"].extend(
                                                    act_sec["sections"].keys())

            for act in act_sec["acts"]:
                act_adv_info[act].append(adv)

            for area in act_sec["areas"]:
                area_adv_info[area].append(adv)

            for chapter in act_sec["chapters"]:
                chapter_adv_info[chapter].append(adv)

            for section in act_sec["sections"]:
                section_adv_info[section].append(adv)

    adv_area_act_chapter_section_info = {
            k: {item: dict(Counter(val)) for item, val in v.items()}
            for k, v in adv_area_act_chapter_section_info.items()}

    act_adv_info = {k: list(set(v)) for k, v in act_adv_info.items()}
    area_adv_info = {k: list(set(v)) for k, v in area_adv_info.items()}
    chapter_adv_info = {k: list(set(v)) for k, v in chapter_adv_info.items()}
    section_adv_info = {k: list(set(v)) for k, v in section_adv_info.items()}

    adv_case_num = {
            k: len(v) for k, v in sorted(adv_cases.items(),
                                         key=lambda x: len(x[1]),
                                         reverse=True)}

    area_adv_num = {
            k: len(v) for k, v in sorted(area_adv_info.items(),
                                         key=lambda x: len(x[1]),
                                         reverse=True)}

    act_adv_num = {
            k: len(v) for k, v in sorted(act_adv_info.items(),
                                         key=lambda x: len(x[1]),
                                         reverse=True)}

    chapter_adv_num = {
            k: len(v) for k, v in sorted(chapter_adv_info.items(),
                                         key=lambda x: len(x[1]),
                                         reverse=True)}

    section_adv_num = {
            k: len(v) for k, v in sorted(section_adv_info.items(),
                                         key=lambda x: len(x[1]),
                                         reverse=True)}

    with open(os.path.join(args.output_path,
                           "adv_area_act_chapter_section_info.json"),
              'w') as f:
        json.dump(adv_area_act_chapter_section_info, f, indent=4)

    with open(os.path.join(args.output_path,
                           "adv_cases.json"),
              'w') as f:
        json.dump(adv_cases, f, indent=4)

    with open(os.path.join(args.output_path,
                           "adv_case_num.json"),
              'w') as f:
        json.dump(adv_case_num, f, indent=4)

    with open(os.path.join(args.output_path, "area_adv_info.json"),
              'w') as f:
        json.dump(area_adv_info, f, indent=4)

    with open(os.path.join(args.output_path, "act_adv_info.json"),
              'w') as f:
        json.dump(act_adv_info, f, indent=4)

    with open(os.path.join(args.output_path, "chapter_adv_info.json"),
              'w') as f:
        json.dump(chapter_adv_info, f, indent=4)

    with open(os.path.join(args.output_path, "section_adv_info.json"),
              'w') as f:
        json.dump(section_adv_info, f, indent=4)

    with open(os.path.join(args.output_path, "area_adv_num.json"),
              'w') as f:
        json.dump(area_adv_num, f, indent=4)

    with open(os.path.join(args.output_path, "act_adv_num.json"),
              'w') as f:
        json.dump(act_adv_num, f, indent=4)

    with open(os.path.join(args.output_path, "chapter_adv_num.json"),
              'w') as f:
        json.dump(chapter_adv_num, f, indent=4)

    with open(os.path.join(args.output_path, "section_adv_num.json"),
              'w') as f:
        json.dump(section_adv_num, f, indent=4)


if __name__ == "__main__":
    main()
