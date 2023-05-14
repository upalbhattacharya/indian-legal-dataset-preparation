#!/usr/bin/env python

"""Create heterogeneous targets using label hierarchy to reduce imbalance"""

import argparse
import json
import logging
import os
from collections import Counter, defaultdict
from statistics import mean, stdev
from typing import Tuple

from utils import set_logger


def imbalance_ratios(target_cases: dict) -> Tuple[float, float, float, float]:
    """Compute imbalance ratios for given targets"""
    max_class = max(map(lambda x: len(x), target_cases.values()))
    imbl = [max_class * 1./len(v) for v in target_cases.values()]
    max_imbl = max(imbl)
    min_imbl = min(imbl)
    stdev_imbl = stdev(imbl)
    mean_imbl = mean(imbl)
    return max_imbl, min_imbl, stdev_imbl, mean_imbl


def split_area(
        target_cases: dict,
        largest_class: str,
        label_cases: dict,
        present_lb1_lb2: dict,
        min_cases: int,
        big_atomic_classes: list) -> Tuple[dict, float]:
    new_areas = {
        k: label_cases[k] for k in present_lb1_lb2[largest_class]
        if len(label_cases[k]) >= min_cases}
    if len(new_areas) == 0:
        big_atomic_classes.append(largest_class)

        n_max_imbl, n_min_imbl, n_stdev_imbl, n_mean_imbl = imbalance_ratios(
                                                                target_cases)
        logging.info(f"{largest_class} is atomic. Mean IMbl: {n_mean_imbl} "
                     f"Stdev IMbl: {n_stdev_imbl}")
        return big_atomic_classes, target_cases, n_mean_imbl

    composite_area = list(set(target_cases[largest_class]) -
                          set([v for val in new_areas.values() for v in val]))
    if len(composite_area) != 0 and len(composite_area) < min_cases:
        least_new = min([len(v) for v in new_areas.values()])
        least_new_class = [
                k for k, v in new_areas.items()
                if len(v) == least_new]
        least_new_class = least_new_class[0]
        composite_area.extend(new_areas[least_new_class])
        del new_areas[least_new_class]

    del target_cases[largest_class]
    target_cases.update(new_areas)
    if len(composite_area) != 0:
        target_cases.update({f"{largest_class}_COMPOSITE": composite_area})
        big_atomic_classes.append(f"{largest_class}_COMPOSITE")
    n_max_imbl, n_min_imbl, n_stdev_imbl, n_mean_imbl = imbalance_ratios(
                                                                target_cases)
    logging.info(f"Split {largest_class}. Mean IMbl: {n_mean_imbl} "
                 f"Stdev IMbl: {n_stdev_imbl}")
    return big_atomic_classes, target_cases, n_mean_imbl


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case_info_path", "-i", type=str,
                        help="Path to load case information")
    parser.add_argument("--act_area_path", "-a", type=str,
                        help="Path to load act to area mapping")
    parser.add_argument("--section_chapter_path", "-s", type=str,
                        help="Path to load section to chapter mapping")
    parser.add_argument("--min_cases", "-m", type=int, default=50,
                        help="Minimum number of cases to retain a label")
    parser.add_argument("--imbl", "-b", type=float, default=25.0,
                        help="Mean imbalance ratio to achieve")
    parser.add_argument("--output_path", "-o", type=str,
                        help="Path to save generated data")

    args = parser.parse_args()
    set_logger(os.path.join(args.output_path, "get_balanced_targets"))
    logging.info("Passed arguments:")
    for name, value in vars(args).items():
        logging.info(f"{name}: {value}")

    with open(args.case_info_path, 'r') as f:
        case_info = json.load(f)

    with open(args.act_area_path, 'r') as f:
        act_areas = json.load(f)

    with open(args.section_chapter_path, 'r') as f:
        section_chapters = json.load(f)

    # Get reverse mapping
    area_acts = defaultdict(lambda: list())
    chapter_sections = defaultdict(lambda: list())
    # area to acts
    for act, areas in act_areas.items():
        for area in areas:
            area_acts[area].append(act)
    # chapter to acts
    for section, chapters in section_chapters.items():
        for chapter in chapters:
            chapter_sections[chapter].append(section)

    # Get present areas, acts, chapters and sections and their cases
    target_cases = defaultdict(lambda: list())
    present_areas = []
    present_acts = []
    present_chapters = []
    present_sections = []
    present_area_acts = defaultdict(lambda: set())
    present_act_chapters = defaultdict(lambda: set())
    present_chapter_sections = defaultdict(lambda: set())
    area_cases = defaultdict(lambda: list())
    act_cases = defaultdict(lambda: list())
    chapter_cases = defaultdict(lambda: list())
    section_cases = defaultdict(lambda: list())

    for case, info in case_info.items():
        for area in info["areas"]:
            # Start at highest granularity i.e. areas
            target_cases[area].append(case)
            present_areas.append(area)
            area_cases[area].append(case)
        for act in info["acts"]:
            present_acts.append(act)
            act_cases[act].append(case)
            for area in act_areas.get(act, []):
                present_area_acts[area].update([act])
        for chapter in info["chapters"]:
            present_chapters.append(chapter)
            chapter_cases[chapter].append(case)
            act = chapter.split("_")[0]
            present_act_chapters[act].update([chapter])
        for section in info["sections"]:
            present_sections.append(section)
            chapter = section_chapters.get(section, "")
            # HACKY
            # TODO: Fix at the area act chapter section annotation level
            if "Constitution" in section:
                logging.info(f"Fixing for {section}")
                present_chapters.append(chapter)
                present_act_chapters["Constitution"].update([chapter])
                chapter_cases[chapter].append(case)
            present_chapter_sections[chapter].update([section])
            section_cases[section].append(case)

    # Convert to dictionaries with frequencies
    present_areas = dict(Counter(present_areas))
    present_acts = dict(Counter(present_acts))
    present_chapters = dict(Counter(present_chapters))
    present_sections = dict(Counter(present_sections))
    big_atomic_classes = []
    non_atomic_usable_classes = [
            k for k, v in target_cases.items()
            if len(v) >= args.min_cases and
            k not in big_atomic_classes]

    # Define initial imbalance ratio
    max_imbl, min_imbl, stdev_imbl, mean_imbl = imbalance_ratios(target_cases)

    while len(non_atomic_usable_classes) > 0:
        # Get largest class
        largest = max([len(v) for k, v in target_cases.items()
                       if k not in big_atomic_classes])
        largest_class = [
                k for k, v in target_cases.items()
                if len(v) == largest and k not in big_atomic_classes]
        largest_class = largest_class[0]
        # Check what hierarchy largest class belongs to
        # and split accordingly
        if present_areas.get(largest_class, -1) != -1:
            big_atomic_classes, target_cases, mean_imbl = split_area(
                    target_cases, largest_class,
                    act_cases, present_area_acts,
                    args.min_cases, big_atomic_classes)
        elif present_acts.get(largest_class, -1) != -1:
            big_atomic_classes, target_cases, mean_imbl = split_area(
                    target_cases, largest_class,
                    chapter_cases, present_act_chapters,
                    args.min_cases, big_atomic_classes)
        elif present_chapters.get(largest_class, -1) != -1:
            big_atomic_classes, target_cases, mean_imbl = split_area(
                    target_cases, largest_class,
                    section_cases, present_chapter_sections,
                    args.min_cases, big_atomic_classes)
        else:
            logging.info(f"Largest class '{largest_class}' is either "
                         "an unsplittable class or a composite class")
            big_atomic_classes.append(largest_class)

        non_atomic_usable_classes = [
                k for k, v in target_cases.items()
                if len(v) > args.min_cases and
                k not in big_atomic_classes]

    logging.info(f"Dataset balanced to create {len(target_cases)} labels")
    case_targets = defaultdict(lambda: list())
    for label, cases in target_cases.items():
        for case in cases:
            case_targets[case].append(label)

    label_case_num = {
            k: len(v)
            for k, v in sorted(target_cases.items(),
                               key=lambda x: len(x[1]),
                               reverse=True)}

    with open(os.path.join(
              args.output_path, "label_case_info.json"), 'w') as f:
        json.dump(target_cases, f, indent=4)
    with open(os.path.join(
              args.output_path, "label_case_num.json"), 'w') as f:
        json.dump(label_case_num, f, indent=4)
    with open(os.path.join(
              args.output_path, "balanced_case_labels.json"), 'w') as f:
        json.dump(case_targets, f, indent=4)


if __name__ == "__main__":
    main()
