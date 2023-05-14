#!/usr/bin/env python

"""Get split of targets based on dataset train-test split and per-target
datapoints"""

import argparse
import json
import logging
import os

from utils import set_logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target_items",
                        help="Dictionary with items of each target")
    parser.add_argument("-s", "--split_info",
                        help="Split information of dataset")
    parser.add_argument("-o", "--output_dir",
                        help="Path to save generated split information")

    args = parser.parse_args()
    set_logger(os.path.join(args.output_dir, "get_target_splits"))
    logging.info("Inputs:")
    for name, value in vars(args).items():
        logging.info(f"{name}: {value}")

    with open(args.target_items, 'r') as f:
        target_items = json.load(f)

    with open(args.split_info, 'r') as f:
        split_info = json.load(f)

    target_split = {}
    target_split_num = {}

    for target, items in target_items.items():
        logging.info(f"Getting split information for {target}")
        target_split[target] = {
                "train": list(set(items).intersection(
                                                set(split_info["train"]))),
                "test": list(set(items).intersection(
                                                set(split_info["test"])))
                }
        target_split_num[target] = {
                "train": len(target_split[target]["train"]),
                "test": len(target_split[target]["test"])
                }

    with open(os.path.join(args.output_dir, "target_split_info.json"),
              'w') as f:
        json.dump(target_split, f, indent=4)

    with open(os.path.join(args.output_dir, "target_split_num.json"),
              'w') as f:
        json.dump(target_split_num, f, indent=4)


if __name__ == "__main__":
    main()
