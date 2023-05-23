#!/usr/bin/env python

"""Create silver-standard target information using overlap criteria of
attributes of datapoints and targets"""

import argparse
import json
import logging
import os

from utils import set_logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-dt", "--data_targets", help="Mapping of datapoints to targets"
    )
    parser.add_argument(
        "-at",
        "--attribute_targets",
        type=str,
        help="Mapping of concerned attribute to targets",
    )
    parser.add_argument(
        "-ta",
        "--target_attribute_info",
        type=str,
        help="Attribute information of targets",
    )
    parser.add_argument(
        "-da",
        "--data_attribute_info",
        type=str,
        help="Attribute information of datapoints",
    )
    parser.add_argument(
        "-s",
        "--similarity",
        type=float,
        default=1.0,
        help="Degree of attribute overlap",
    )
    parser.add_argument(
        "-k",
        "--key",
        type=str,
        default="areas",
        help="Information key for use in attribute dictionaries",
    )
    parser.add_argument(
        "-oa",
        "--omit_attribute",
        type=str,
        default=None,
        help="Attributes to omit in selecting silver standards",
    )
    parser.add_argument(
        "-o", "--output_dir", help="Path to save generated target information"
    )

    args = parser.parse_args()

    set_logger(os.path.join(args.output_dir, "get_silver_targets"))
    logging.info("Inputs")
    for name, value in vars(args).items():
        logging.info(f"{name}: {value}")

    # Load data
    with open(args.data_targets, "r") as f:
        data_targets = json.load(f)
    with open(args.attribute_targets, "r") as f:
        attribute_targets = json.load(f)
    with open(args.target_attribute_info, "r") as f:
        target_attributes = json.load(f)
    with open(args.data_attribute_info, "r") as f:
        data_attributes = json.load(f)
    omit = []
    if args.omit_attribute is not None:
        with open(args.omit_attribute, "r") as f:
            omit = f.readlines()
        omit = list(filter(None, map(lambda x: x.strip("\n"), omit)))

    data_silver_targets = {}

    for data, attributes in data_attributes.items():
        logging.info(f"Getting silver-standard targets for {data}")
        logging.info(f"Found attributes: {attributes}")
        potential_targets = set(
            [
                target
                for attribute in attributes[args.key]
                for target in attribute_targets[attribute]
                if attribute not in omit
            ]
        )
        # Retain targets with specified overlap
        silver_targets = [
            target
            for target in potential_targets
            if overlap(
                attributes[args.key], target_attributes[target][args.key]
            )
            >= args.similarity
        ]
        # Remove gold-standards
        silver_targets = list(
            set(silver_targets).difference(data_targets[data])
        )
        logging.info(f"Found silver-standard targets: {silver_targets}")
        data_silver_targets[data] = silver_targets

    # Get counts
    data_silver_targets_count = {
        k: len(v)
        for k, v in sorted(
            data_silver_targets.items(), key=lambda x: len(x[1]), reverse=True
        )
    }

    # Save data
    with open(
        os.path.join(args.output_dir, "data_silver_targets.json"), "w"
    ) as f:
        json.dump(data_silver_targets, f, indent=4)
    with open(
        os.path.join(args.output_dir, "data_silver_targets_num.json"), "w"
    ) as f:
        json.dump(data_silver_targets_count, f, indent=4)


def overlap(data_attribute: list, target_attribute: list) -> float:
    """Overlap between data attribute and target attribute

    Parameters
    ----------
    data_attribute : list
        Data attribute(s)
    target_attribute : list
        Target attribute(s)

    Returns
    -------
    float
        Overlap value
    """
    return (
        len(set(data_attribute).intersection(set(target_attribute)))
        * 1.0
        / len(set(data_attribute))
    )


if __name__ == "__main__":
    main()
