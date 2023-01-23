#!/usr/bin/env python

"""Select advocates from a given list of advocates and their cases based on
the number of cases."""

import argparse
import json
import logging
import os
from itertools import chain

from utils import set_logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ac", "--advocate_cases",
                        help="Path to json file with advocate cases")
    parser.add_argument("-s", "--selected_cases", default=None,
                        help="List of cases to consider")
    parser.add_argument("-n", "--num", type=int, default=100,
                        help="Least number of cases to consider advocate")
    parser.add_argument("-p", "--petitioner_cases",
                        help="Path to file with petitioner cases of advocates")
    parser.add_argument("-d", "--defendant_cases",
                        help="Path to file with defendant cases of advocates")
    parser.add_argument("-o", "--output_dir",
                        help="Directory to save generated data")

    args = parser.parse_args()
    set_logger(os.path.join(args.output_dir, "select_advocates"))

    # Log inputs
    logging.info("Inputs:")
    for name, value in vars(args).items():
        logging.info(f"{name}: {value}")

    # Load data
    with open(args.advocate_cases, 'r') as f:
        adv_cases = json.load(f)

    with open(args.petitioner_cases, 'r') as f:
        pet_cases = json.load(f)

    with open(args.defendant_cases, 'r') as f:
        def_cases = json.load(f)

    if args.selected_cases is not None:
        with open(args.selected_cases, 'r') as f:
            selected_cases = f.readlines()
        selected_cases = list(filter(None, map(lambda x: x.strip(),
                                               selected_cases)))
        adv_cases = {k: list(set(v).intersection(set(selected_cases)))
                     for k, v in adv_cases.items()}

        pet_cases = {k: list(set(v).intersection(set(selected_cases)))
                     for k, v in pet_cases.items()}

        def_cases = {k: list(set(v).intersection(set(selected_cases)))
                     for k, v in def_cases.items()}

    adv_nums = {k: len(v) for k, v in adv_cases.items()}

    # Select advocates
    advs = [adv for adv, num in adv_nums.items() if num >= args.num]
    logging.info(f"{len(advs)} advocates were selected")
    logging.info(f"Selected advocates are: {advs}")

    select_adv_cases = {}
    select_pet_cases = {}
    select_def_cases = {}

    for adv in advs:
        select_adv_cases[adv] = adv_cases[adv]
        select_pet_cases[adv] = pet_cases[adv]
        select_def_cases[adv] = def_cases[adv]

    select_adv_nums = {k: len(v) for k, v in
                       sorted(select_adv_cases.items(),
                              key=lambda x: len(x[1]), reverse=True)}

    select_pet_cases_nums = {k: len(v) for k, v in
                             sorted(select_pet_cases.items(),
                                    key=lambda x: len(x[1]), reverse=True)}

    select_def_cases_nums = {k: len(v) for k, v in
                             sorted(select_def_cases.items(),
                                    key=lambda x: len(x[1]), reverse=True)}

    selected_cases = set(chain.from_iterable(
                                    [v for v in select_adv_cases.values()]))

    logging.info(f"Total number of retained cases: {len(selected_cases)}")

    # Save data
    with open(os.path.join(args.output_dir, "adv_cases.json"), 'w') as f:
        json.dump(select_adv_cases, f, indent=4)

    with open(os.path.join(args.output_dir, "adv_cases_num.json"), 'w') as f:
        json.dump(select_adv_nums, f, indent=4)

    with open(os.path.join(args.output_dir, "pet_cases.json"), 'w') as f:
        json.dump(select_pet_cases, f, indent=4)

    with open(os.path.join(args.output_dir, "res_cases.json"), 'w') as f:
        json.dump(select_def_cases, f, indent=4)

    with open(os.path.join(args.output_dir, "pet_cases_num.json"), 'w') as f:
        json.dump(select_pet_cases_nums, f, indent=4)

    with open(os.path.join(args.output_dir, "res_cases_num.json"), 'w') as f:
        json.dump(select_def_cases_nums, f, indent=4)

    with open(os.path.join(args.output_dir, "selected_cases.txt"), 'w') as f:
        for case in selected_cases:
            print(case, file=f, end="\n")


if __name__ == "__main__":
    main()
