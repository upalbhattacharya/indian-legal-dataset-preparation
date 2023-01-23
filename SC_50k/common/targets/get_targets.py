#!/usr/bin/env python

"""Create target information for items"""

import argparse
import json
import logging
import os
from collections import defaultdict

from utils import set_logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mapping",
                        help="Mapping of items to targets")
    parser.add_argument("-o", "--output_dir",
                        help="Path to save generated target information")

    args = parser.parse_args()

    set_logger(os.path.join(args.output_dir, "get_targets"))
    logging.info("Inputs")
    for name, value in vars(args).items():
        logging.info(f"{name}: {value}")

    # Load data
    with open(args.mapping, 'r') as f:
        target_items = json.load(f)

    item_targets = defaultdict(list)

    for target, items in target_items.items():
        logging.info(f"Adding {target} as a target for its items")
        for item in items:
            item_targets[item].append(target)

    # Save data
    with open(os.path.join(args.output_dir, "item_targets.json"), 'w') as f:
        json.dump(item_targets, f, indent=4)


if __name__ == "__main__":
    main()
