#!/usr/bin/env python

# Creation of train-test-validation splits using per-target information to
# ensure representation

# TODOs: Train and test splits MUST have representation of each target

import argparse
import json
import logging
import os
import random
from collections import defaultdict
from itertools import combinations

from utils import set_logger

# Setting seed for reproducability
random.seed(42)


def main():
    # Creation of train-test-validation splits using per-target information to
    # ensure representation
    #
    # Args
    # ----
    # target_data: Path to target-datapoint json file
    # train_size: Size of training split
    # test_size: Size of test split
    # val_size: Size of val split
    # output_path: Path to save generated information

    parser = argparse.ArgumentParser(
        description=(
            "Create train-test-validation "
            "spilts using per-target information to "
            "ensure representation"
        )
    )

    parser.add_argument(
        "--target_data", type=str, help="Path to target-datapoint json file"
    )
    parser.add_argument(
        "--data_targets",
        type=str,
        help="Path to target information of datapoints",
    )
    parser.add_argument(
        "--train_size", type=float, default=0.8, help="Size of training split"
    )
    parser.add_argument(
        "--test_size", type=float, default=0.2, help="Size of test split"
    )
    parser.add_argument(
        "--val_size", type=float, default=0.0, help="Size of val split"
    )
    parser.add_argument(
        "--min_train",
        type=int,
        default=3,
        help="Minimum number of training cases for each target",
    )
    parser.add_argument(
        "--min_test",
        type=int,
        default=1,
        help="Minimum number of test cases for each target",
    )

    parser.add_argument(
        "--output_path", type=str, help="Path to save generated information"
    )
    args = parser.parse_args()
    set_logger(
        os.path.join(args.output_path, "create-per-target-balanced-splits")
    )
    logging.info("Inputs:")
    for name, value in vars(args).items():
        logging.info(f"{name}: {value}")

    if round(args.train_size + args.test_size + args.val_size) != 1:
        raise ValueError("Three splits should sum up to 1.0")

    # Load target information
    with open(args.target_data, "r") as f:
        target_data = json.load(f)

    # Load data targets
    with open(args.data_targets, "r") as f:
        data_targets = json.load(f)

    # Create variables for holding relevant information
    train = set()
    test = set()
    val = set()

    target_train_data = defaultdict(lambda: set())
    target_test_data = defaultdict(lambda: set())
    target_val_data = defaultdict(lambda: set())

    target_datapoints = set(
        [
            datapoint
            for datapoints in target_data.values()
            for datapoint in datapoints
        ]
    )
    datapoints = set(data_targets.keys())

    # Check agreement of two sets of datapoints
    if target_datapoints != datapoints:
        logging.warning(
            "Data points from 'target_data' and 'data_targets' have mismatch. "
            "Using data points of 'target_data'."
        )

    # Create splits
    for target, data in target_data.items():
        total = len(data)
        train_len = round(total * args.train_size)
        test_len = round(total * args.test_size)
        val_len = round(total * args.val_size)
        sum_segments = sum([train_len, test_len, val_len])

        # Add mismatches to training data
        if sum_segments != total:
            train_len += total - sum_segments

        train_cases = set(random.sample(sorted(data), train_len))
        train_test = train_cases.intersection(test)
        train_val = train_cases.intersection(val)

        if (
            len(train_test)
            != 0 & len(train_cases.difference(train_test))
            > args.min_train
        ):
            train_cases = train_cases.difference(train_test)
        else:
            diff = args.min_train - len(train_cases.difference(train_test))
            train_add, test, target_test_data = checkandremove(
                train_test,
                test,
                target_test_data,
                data_targets,
                args.min_test,
                diff,
            )
        if len(train_cases.difference(test).difference(val)) != len(
            train_cases
        ):
            common_test = train_cases.intersection(test)
            common_val = train_cases.intersection(val)
            val = val.difference(train_cases)
            test = test.difference(train_cases)
        train.update(train_cases)
        data = set(data).difference(train_cases)
        test_cases = set(random.sample(sorted(data), test_len))
        if len(test_cases.difference(train).difference(val)) != len(
            test_cases
        ):
            train = train.difference(test_cases)
            val = val.difference(test_cases)
        test.update(test_cases)
        data = set(data).difference(test_cases)
        val_cases = data
        val.update(val_cases)
        target_train_data[target] = train_cases
        target_test_data[target] = test_cases
        target_val_data[target] = val_cases

    # Check leakage
    for seg1, seg2 in combinations([train, test, val], 2):
        logging.info(f"Overlap: {len(seg1.intersection(seg2))}")

    # Check empty
    target_empty_train = [
        target for target, data in target_train_data.items() if len(data) == 0
    ]
    target_empty_test = [
        target for target, data in target_test_data.items() if len(data) == 0
    ]
    target_empty_val = [
        target for target, data in target_val_data.items() if len(data) == 0
    ]

    # Convert to list
    target_train_data = {k: list(v) for k, v in target_train_data.items()}
    target_test_data = {k: list(v) for k, v in target_test_data.items()}
    target_val_data = {k: list(v) for k, v in target_val_data.items()}

    # Numerical Stats
    target_train_data_num = {
        k: len(v)
        for k, v in sorted(
            target_train_data.items(), key=lambda x: len(x[1]), reverse=True
        )
    }
    target_test_data_num = {
        k: len(v)
        for k, v in sorted(
            target_test_data.items(), key=lambda x: len(x[1]), reverse=True
        )
    }
    target_val_data_num = {
        k: len(v)
        for k, v in sorted(
            target_val_data.items(), key=lambda x: len(x[1]), reverse=True
        )
    }

    # Save
    with open(
        os.path.join(args.output_path, "train", "train_targets.json"), "w"
    ) as f:
        json.dump(target_train_data, f, indent=4)

    with open(
        os.path.join(args.output_path, "test", "test_targets.json"), "w"
    ) as f:
        json.dump(target_test_data, f, indent=4)

    with open(
        os.path.join(args.output_path, "val", "val_targets.json"), "w"
    ) as f:
        json.dump(target_val_data, f, indent=4)

    with open(
        os.path.join(args.output_path, "train", "train_targets_num.json"), "w"
    ) as f:
        json.dump(target_train_data_num, f, indent=4)

    with open(
        os.path.join(args.output_path, "test", "test_targets_num.json"), "w"
    ) as f:
        json.dump(target_test_data_num, f, indent=4)

    with open(
        os.path.join(args.output_path, "val", "val_targets_num.json"), "w"
    ) as f:
        json.dump(target_val_data_num, f, indent=4)

    with open(
        os.path.join(args.output_path, "train", "train_cases.txt"), "w"
    ) as f:
        for line in train:
            print(line, file=f, end="\n")

    with open(
        os.path.join(args.output_path, "test", "test_cases.txt"), "w"
    ) as f:
        for line in test:
            print(line, file=f, end="\n")

    with open(
        os.path.join(args.output_path, "val", "val_cases.txt"), "w"
    ) as f:
        for line in val:
            print(line, file=f, end="\n")

    with open(
        os.path.join(args.output_path, "train", "target_train_empty.txt"), "w"
    ) as f:
        for line in target_empty_train:
            print(line, file=f, end="\n")

    with open(
        os.path.join(args.output_path, "test", "target_test_empty.txt"), "w"
    ) as f:
        for line in target_empty_test:
            print(line, file=f, end="\n")

    with open(
        os.path.join(args.output_path, "val", "target_val_empty.txt"), "w"
    ) as f:
        for line in target_empty_val:
            print(line, file=f, end="\n")


def checkandremove(
    datapoints: list,
    segment: set,
    target_data: dict,
    data_targets: dict,
    min_count: int,
    diff: int,
) -> (list, set, dict):
    """

    Parameters
    ----------
    datapoints : list
        Datapoints to check.
    segment : set
        Segment to check.
    target_data : dict
        Target data information for feasibility check.
    data_targets : dict
        Overall data targets for making best selection.
    min_count : int
        Minimum of datapoints to try to ensure for each target.
    diff: int
        Number of cases to remove.

    Returns
    -------
    (list, set, dict)
        List of points that can be removed, new segment values, updated
        dictionary of values.
    """
    if len(datapoints) == 0:
        return datapoints, segment, target_data

    # Order in increasing number of associated targets
    ordered = sorted(datapoints, lambda x: len(data_targets[x]))
    remove = []

    for datapoint in ordered:
        for target in data_targets[datapoint]:



if __name__ == "__main__":
    main()
