#!/usr/bin/env python

"""Select cases based on provided selection conditions."""

import argparse
import json
import logging
import os
import re
from collections import Counter, defaultdict
from copy import deepcopy
from itertools import chain

from utils import order, set_logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--case_info",
        help="Act, Chapter and Section Information of cases",
    )
    parser.add_argument(
        "-c",
        "--conditions",
        type=str,
        help=(
            "Conditional to use to find relevant targets."
            "Use single quotes '' for strings, parentheses "
            "() for complex conditions and wrap the entire "
            'condition in double quotes ""'
        ),
    )
    parser.add_argument(
        "-s", "--section_chapters", help="Chapter information for section"
    )
    parser.add_argument("-a", "--act_areas", help="Area information for acts")
    parser.add_argument(
        "-aam",
        "--area_min",
        type=int,
        default=None,
        help="Minimum number of cases to consider an area",
    )
    parser.add_argument(
        "-am",
        "--act_min",
        type=int,
        default=None,
        help="Minimum number of cases to consider an act",
    )
    parser.add_argument(
        "-cm",
        "--chapter_min",
        type=int,
        default=None,
        help="Minimum number of cases to consider a chapter",
    )
    parser.add_argument(
        "-sm",
        "--section_min",
        type=int,
        default=None,
        help="Minimum number of cases to consider a section",
    )
    parser.add_argument(
        "-sc",
        "--selected_cases",
        default=None,
        help="List of selected cases to work with",
    )
    parser.add_argument(
        "-o", "--output_dir", help="Path to save generated set of cases"
    )

    args = parser.parse_args()
    set_logger(os.path.join(args.output_dir, "select_cases_from_groups"))
    logging.info("Inputs:")
    for name, val in vars(args).items():
        logging.info(f"{name}: {val}")

    # Load data
    with open(args.case_info, "r") as f:
        case_info = json.load(f)

    with open(args.section_chapters, "r") as f:
        section_chapters = json.load(f)

    with open(args.act_areas, "r") as f:
        act_areas = json.load(f)

    if args.selected_cases is not None:
        with open(args.selected_cases, "r") as f:
            selected_cases = f.readlines()
        selected_cases = {
            k: k
            for k in list(
                filter(None, map(lambda x: x.strip(), selected_cases))
            )
        }
    select_case_info = {}
    area_case_info = defaultdict(list)
    act_case_info = defaultdict(list)
    chapter_case_info = defaultdict(list)
    section_case_info = defaultdict(list)

    # Parse elements to get act, chapter and section mentions

    if args.conditions is not None:
        all_targets = re.finditer("'(.*?)'", args.conditions)
        all_targets = [match.groups()[0] for match in all_targets]
        logging.info(f"Parsed elements: {all_targets}")
        targets_dict = defaultdict(list)
        for t in all_targets:
            segs = t.split("_")
            if len(segs) == 1:
                if segs[0].isupper():
                    targets_dict["areas"].append(segs[0])
                else:
                    targets_dict["acts"].append(segs[0])
                    targets_dict["areas"].append(act_areas[segs[0]])
            if len(segs) > 1:
                if segs[-1][0].isupper():
                    targets_dict["chapters"].append(t)
                else:
                    targets_dict["sections"].append(t)

        logging.info(
            f"Parsed areas, acts, chapters and sections: {targets_dict}"
        )

        for case, info in case_info.items():
            # Skip irrelevant cases
            if args.selected_cases is not None:
                if selected_cases.get(case, -1) == -1:
                    continue

            areas = info["areas"]
            acts = info["acts"]
            sections = info["sections"]
            chapters = info["chapters"]

            # Check conditions satisfied
            check = eval(args.conditions)

            if not check:
                continue

            # Recalculate Area, Act, Chapter and Section information

            if targets_dict["areas"] != []:
                rel_areas = set(targets_dict["areas"]).intersection(set(areas))
            else:
                rel_areas = set(areas)

            if targets_dict["acts"] != []:
                rel_acts = set(targets_dict["acts"]).intersection(set(acts))

                rel_areas = [act_areas.get(act, None) for act in rel_acts]
                rel_areas = set(filter(None, rel_areas))
            else:
                rel_acts = set(
                    [
                        act
                        for act in acts
                        if set(act_areas.get(act, set())).intersection(
                            rel_areas
                        )
                        != set()
                    ]
                )

                rel_areas = list(
                    chain.from_iterable(
                        [act_areas.get(act, None) for act in rel_acts]
                    )
                )
                rel_areas = set(filter(None, rel_areas))

            if targets_dict["sections"] != []:
                rel_sections = set(targets_dict["sections"]).intersection(
                    set(sections)
                )
                rel_acts = set(
                    [section.split("_")[0] for section in rel_sections]
                )

                rel_areas = list(
                    chain.from_iterable(
                        [act_areas.get(act, None) for act in rel_acts]
                    )
                )
                rel_areas = set(filter(None, rel_areas))
            else:
                rel_sections = set(
                    [
                        section
                        for section in sections
                        if section.split("_")[0] in rel_acts
                    ]
                )

                rel_acts = set(
                    [section.split("_")[0] for section in rel_sections]
                )

                rel_areas = list(
                    chain.from_iterable(
                        [act_areas.get(act, None) for act in rel_acts]
                    )
                )
                rel_areas = set(filter(None, rel_areas))
            if targets_dict["chapters"] != []:
                rel_chapters = set(targets_dict["chapter"]).intersection(
                    set(chapters)
                )
            else:
                rel_chapters = [
                    section_chapters.get(section, None)
                    for section in rel_sections
                ]
                rel_chapters = set(filter(None, rel_chapters))

            logging.info(f"Case {case} is relevant")
            logging.info(f"Found areas: {rel_areas}")
            logging.info(f"Found acts: {rel_acts}")
            logging.info(f"Found chapters: {rel_chapters}")
            logging.info(f"Found sections: {rel_sections}")
            new_info = {
                "areas": order(Counter(rel_areas)),
                "acts": order(Counter(rel_acts)),
                "chapters": order(Counter(rel_chapters)),
                "sections": order(Counter(rel_sections)),
            }
            select_case_info[case] = new_info

            for area in new_info["areas"]:
                area_case_info[area].append(case)

            for act in new_info["acts"]:
                act_case_info[act].append(case)

            for chapter in new_info["chapters"]:
                chapter_case_info[chapter].append(case)

            for section in new_info["sections"]:
                section_case_info[section].append(case)

        area_case_num = {
            k: len(v)
            for k, v in sorted(
                area_case_info.items(), key=lambda x: len(x[1]), reverse=True
            )
        }

        act_case_num = {
            k: len(v)
            for k, v in sorted(
                act_case_info.items(), key=lambda x: len(x[1]), reverse=True
            )
        }

        chapter_case_num = {
            k: len(v)
            for k, v in sorted(
                chapter_case_info.items(),
                key=lambda x: len(x[1]),
                reverse=True,
            )
        }

        section_case_num = {
            k: len(v)
            for k, v in sorted(
                section_case_info.items(),
                key=lambda x: len(x[1]),
                reverse=True,
            )
        }
    else:
        select_case_info = case_info
        for case, info in case_info.items():
            for area in info["areas"]:
                area_case_info[area].append(case)

            for act in info["acts"]:
                act_case_info[act].append(case)

            for chapter in info["chapters"]:
                chapter_case_info[chapter].append(case)

            for section in info["sections"]:
                section_case_info[section].append(case)

        area_case_num = {
            k: len(v)
            for k, v in sorted(
                area_case_info.items(), key=lambda x: len(x[1]), reverse=True
            )
        }

        act_case_num = {
            k: len(v)
            for k, v in sorted(
                act_case_info.items(), key=lambda x: len(x[1]), reverse=True
            )
        }

        chapter_case_num = {
            k: len(v)
            for k, v in sorted(
                chapter_case_info.items(),
                key=lambda x: len(x[1]),
                reverse=True,
            )
        }

        section_case_num = {
            k: len(v)
            for k, v in sorted(
                section_case_info.items(),
                key=lambda x: len(x[1]),
                reverse=True,
            )
        }

    # Remove cases of low area, act, chapter or section frequency

    if args.area_min is not None:
        prune_areas = [
            area for area, num in area_case_num.items() if num < args.area_min
        ]
        logging.info(f"Pruning the following areas: {prune_areas}")
        select_case_info = clean_min_areas(
            select_case_info, prune_areas, act_areas
        )

    if args.act_min is not None:
        prune_acts = [
            act for act, num in act_case_num.items() if num < args.act_min
        ]
        logging.info(f"Pruning the following acts: {prune_acts}")
        select_case_info = clean_min_acts(
            select_case_info, prune_acts, act_areas
        )

    if args.chapter_min is not None:
        prune_chapters = [
            chapter
            for chapter, num in chapter_case_num.items()
            if num < args.chapter_min
        ]
        logging.info(f"Pruning the following chapters: {prune_chapters}")
        select_case_info = clean_min_chapters(
            select_case_info, prune_chapters, section_chapters, act_areas
        )

    if args.section_min is not None:
        prune_sections = [
            section
            for section, num in section_case_num.items()
            if num < args.section_min
        ]
        logging.info(f"Pruning the following sections: {prune_sections}")
        select_case_info = clean_min_sections(
            select_case_info, prune_sections, section_chapters, act_areas
        )

    logging.info(list(select_case_info.values())[0])

    area_case_info = defaultdict(list)
    act_case_info = defaultdict(list)
    chapter_case_info = defaultdict(list)
    section_case_info = defaultdict(list)

    for case, info in select_case_info.items():
        for area in info["areas"]:
            area_case_info[area].append(case)

        for act in info["acts"]:
            act_case_info[act].append(case)

        for chapter in info["chapters"]:
            chapter_case_info[chapter].append(case)

        for section in info["sections"]:
            section_case_info[section].append(case)

    area_case_num = {
        k: len(v)
        for k, v in sorted(
            area_case_info.items(), key=lambda x: len(x[1]), reverse=True
        )
    }

    act_case_num = {
        k: len(v)
        for k, v in sorted(
            act_case_info.items(), key=lambda x: len(x[1]), reverse=True
        )
    }

    chapter_case_num = {
        k: len(v)
        for k, v in sorted(
            chapter_case_info.items(), key=lambda x: len(x[1]), reverse=True
        )
    }

    section_case_num = {
        k: len(v)
        for k, v in sorted(
            section_case_info.items(), key=lambda x: len(x[1]), reverse=True
        )
    }

    logging.info(f"{len(select_case_info)} cases were retained.")
    logging.info(f"{len(area_case_info)} areas were retained.")
    logging.info(f"{len(act_case_info)} acts were retained.")
    logging.info(f"{len(chapter_case_info)} chapters were retained.")
    logging.info(f"{len(section_case_info)} sections were retained.")

    with open(
        os.path.join(
            args.output_dir, "case_area_act_chapter_section_info.json"
        ),
        "w",
    ) as f:
        json.dump(select_case_info, f, indent=4)

    with open(os.path.join(args.output_dir, "selected_cases.txt"), "w") as f:
        for case in select_case_info:
            print(case, file=f, end="\n")

    with open(os.path.join(args.output_dir, "area_case_info.json"), "w") as f:
        json.dump(area_case_info, f, indent=4)

    with open(os.path.join(args.output_dir, "act_case_info.json"), "w") as f:
        json.dump(act_case_info, f, indent=4)

    with open(
        os.path.join(args.output_dir, "chapter_case_info.json"), "w"
    ) as f:
        json.dump(chapter_case_info, f, indent=4)

    with open(
        os.path.join(args.output_dir, "section_case_info.json"), "w"
    ) as f:
        json.dump(section_case_info, f, indent=4)

    with open(os.path.join(args.output_dir, "area_case_num.json"), "w") as f:
        json.dump(area_case_num, f, indent=4)

    with open(os.path.join(args.output_dir, "act_case_num.json"), "w") as f:
        json.dump(act_case_num, f, indent=4)

    with open(
        os.path.join(args.output_dir, "chapter_case_num.json"), "w"
    ) as f:
        json.dump(chapter_case_num, f, indent=4)

    with open(
        os.path.join(args.output_dir, "section_case_num.json"), "w"
    ) as f:
        json.dump(section_case_num, f, indent=4)


def clean_min_areas(
    select_case_info: dict, prune_areas: list, act_areas: dict
) -> dict:
    """
    Prune given set of areas from all cases, removing cases with no other area
    information

    Parameters
    ----------
    select_case_info: dict
        Dictionary with act, chapter and section information of cases
    prune_areas: list
        List of areas to prune
    act_areas: dict
        Mapping of acts to areas

    Returns
    -------
    case_info: dict
        Dictionary with act, chapter and section information of cases after
        removing acts
    """
    case_info = deepcopy(select_case_info)

    for case, info in select_case_info.items():
        areas = set(info["areas"]) - set(prune_areas)
        if not areas:
            del case_info[case]
            continue

        acts = [
            act
            for act in info["acts"]
            if act_areas[act.split("_")[0]] not in prune_areas
        ]
        sections = [
            section
            for section in info["sections"]
            if act_areas[section.split("_")[0]] not in prune_areas
        ]
        chapters = [
            chapter
            for chapter in info["chapters"]
            if act_areas[chapter.split("_")[0]] not in prune_areas
        ]

        case_info[case] = {
            "areas": order({area: info["areas"][area] for area in areas}),
            "acts": order({act: info["acts"][act] for act in acts}),
            "chapters": order(
                {chapter: info["chapters"][chapter] for chapter in chapters}
            ),
            "sections": order(
                {section: info["sections"][section] for section in sections}
            ),
        }

    return case_info


def clean_min_acts(
    select_case_info: dict, prune_acts: list, act_areas: dict
) -> dict:
    """
    Prune given set of acts from all cases, removing cases with no other act
    information

    Parameters
    ----------
    select_case_info: dict
        Dictionary with act, chapter and section information of cases
    prune_acts: list
        List of acts to prune
    act_areas: dict
        Mapping of acts to areas

    Returns
    -------
    case_info: dict
        Dictionary with act, chapter and section information of cases after
        removing acts
    """
    case_info = deepcopy(select_case_info)

    for case, info in select_case_info.items():
        acts = set(info["acts"]) - set(prune_acts)
        if not acts:
            del case_info[case]
            continue

        areas = [act_areas.get(act, "") for act in acts]

        sections = [
            section
            for section in info["sections"]
            if section.split("_")[0] not in prune_acts
        ]
        chapters = [
            chapter
            for chapter in info["chapters"]
            if chapter.split("_")[0] not in prune_acts
        ]

        case_info[case] = {
            "areas": order({area: info["areas"][area] for area in areas}),
            "acts": order({act: info["acts"][act] for act in acts}),
            "chapters": order(
                {chapter: info["chapters"][chapter] for chapter in chapters}
            ),
            "sections": order(
                {section: info["sections"][section] for section in sections}
            ),
        }

    return case_info


def clean_min_chapters(
    select_case_info: dict,
    prune_chapters: list,
    section_chapters: dict,
    act_areas: dict,
) -> dict:
    """
    Prune given set of chapters from all cases, along with relevant sections
    and acts, removing cases with no other chapter information

    Parameters
    ----------
    select_case_info: dict
        Dictionary with act, chapter and section information of cases
    prune_chapters: list
        List of chapters to prune
    section_chapters: dict
        Dictionary with the chapter information of acts

    Returns
    -------
    case_info: dict
        Dictionary with act, chapter and section information of cases after
        removing chapters
    """
    case_info = deepcopy(select_case_info)

    for case, info in select_case_info.items():
        chapters = set(info["chapters"]) - set(prune_chapters)
        if not chapters:
            del case_info[case]
            continue

        sections = [
            section
            for section in info["sections"]
            if section_chapters[section] not in prune_chapters
        ]

        case_info[case] = {
            "areas": order(
                Counter(
                    [
                        act_areas.get(section.split("_")[0], "")[0]
                        for section in sections
                    ]
                )
            ),
            "acts": order(
                Counter([section.split("_")[0] for section in sections])
            ),
            "chapters": order(
                {chapter: info["chapters"][chapter] for chapter in chapters}
            ),
            "sections": order(
                {section: info["sections"][section] for section in sections}
            ),
        }

    return case_info


def clean_min_sections(
    select_case_info: dict,
    prune_sections: list,
    section_chapters: dict,
    act_areas: dict,
) -> dict:
    """
    Prune given set of sections from all cases, along with relevant chapters
    and acts, removing cases with no other section information

    Parameters
    ----------
    select_case_info: dict
        Dictionary with act, chapter and section information of cases
    prune_section: list
        List of sections to prune
    section_chapters: dict
        Dictionary with the chapter information of acts

    Returns
    -------
    case_info: dict
        Dictionary with act, chapter and section information of cases after
        removing sections
    """
    case_info = deepcopy(select_case_info)

    for case, info in select_case_info.items():
        sections = set(info["sections"]) - set(prune_sections)
        if not sections:
            del case_info[case]
            continue

        print(info)

        print(act_areas.get(list(sections)[0].split("_")[0], ""))
        case_info[case] = {
            "areas": order(
                Counter(
                    [
                        act_areas.get(section.split("_")[0], "")[0]
                        for section in sections
                    ]
                )
            ),
            "acts": order(
                Counter([section.split("_")[0] for section in sections])
            ),
            "chapters": order(
                Counter(
                    [section_chapters.get(section, "") for section in sections]
                )
            ),
            "sections": order(
                {section: info["sections"][section] for section in sections}
            ),
        }

    return case_info


if __name__ == "__main__":
    main()
