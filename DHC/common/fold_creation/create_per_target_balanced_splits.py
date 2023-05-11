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

# setting seed for reproducability
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
        data = set(data)
        total = len(data)
        train_len = round(total * args.train_size)
        test_len = round(total * args.test_size)
        val_len = round(total * args.val_size)
        sum_segments = sum([train_len, test_len, val_len])

        # Add mismatches to training data
        if sum_segments != total:
            train_len += total - sum_segments

        train_target = set(random.sample(sorted(data), train_len))
        data = data.difference(train_target)
        test_target = set(random.sample(sorted(data), test_len))
        data = data.difference(test_target)
        val_target = data

        # Remove leakage
        # Priority: Train -> Test -> Validation
        # Train split
        train_target, test = checkandremove(
            datapoints=train_target,
            segment=test,
            data_targets=data_targets,
            min_count=args.min_train,
        )
        train_target, val = checkandremove(
            datapoints=train_target,
            segment=val,
            data_targets=data_targets,
            min_count=args.min_train,
        )
        train.update(train_target)

        # Test split
        test_target, train = checkandremove(
            datapoints=test_target,
            segment=train,
            data_targets=data_targets,
            min_count=args.min_test,
        )
        test_target, val = checkandremove(
            datapoints=test_target,
            segment=val,
            data_targets=data_targets,
            min_count=args.min_test,
        )
        test.update(test_target)

        # Validation split
        # Can be empty
        val_target = val_target.difference(train).difference(test)
        val.update(val_target)

    # Populate values
    for target, data in target_data.items():
        target_train_data[target] = set(data).intersection(train)
        target_test_data[target] = set(data).intersection(test)
        target_val_data[target] = set(data).intersection(val)

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

    logging.info(f"Targets with no training data: {target_empty_train}")
    logging.info(f"Targets with no testing data: {target_empty_test}")
    # Fix empty
    while any(
        [
            len(segment) != 0
            for segment in [target_empty_train, target_empty_test]
        ]
    ):
        for target in target_empty_train:
            if len(set(target_data[target]).intersection(train)) != 0:
                logging.info(f"Representation for {target} exists. Skip.")
                continue
            val_data = set(target_data[target]).intersection(val)
            test_data = set(target_data[target]).intersection(test)
            # Take from validation first (if it exists)
            if len(val_data) != 0:
                to_add = random.sample(
                    sorted(val_data),
                    min(len(val_data), args.min_train),
                )
                val = val.difference(to_add)
                # target_val_data = {
                #     k: v.intersection(val) for k, v in target_val_data.items()
                # }
                train.update(to_add)
            elif len(test_data) != 0:
                # Retain at least one case for test
                to_add = random.sample(
                    sorted(test_data),
                    min(len(test_data), args.min_train) - 1,
                )
                test = test.difference(to_add)
                # target_test_data = {
                #     k: v.intersection(test)
                #     for k, v in target_test_data.items()
                # }
                train.update(to_add)
            else:
                logging.warning(
                    f"Unable to ensure representation for target {target} in "
                    "training split"
                )

        for target, data in target_data.items():
            target_train_data[target] = set(data).intersection(train)
            target_test_data[target] = set(data).intersection(test)
            target_val_data[target] = set(data).intersection(val)

        target_empty_train = [
            target
            for target, data in target_train_data.items()
            if len(data) == 0
        ]
        target_empty_test = [
            target
            for target, data in target_test_data.items()
            if len(data) == 0
        ]

        for target in target_empty_test:
            if len(set(target_data[target]).intersection(test)) != 0:
                logging.info(f"Representation for {target} exists. Skip.")
                continue
            val_data = set(target_data[target]).intersection(val)
            train_data = set(target_data[target]).intersection(train)
            # Take from validation first (if it exists)
            if len(val_data) != 0:
                to_add = random.sample(
                    sorted(val_data),
                    min(len(val_data), args.min_test),
                )
                val = val.difference(to_add)
                # target_val_data = {
                #     k: v.intersection(val) for k, v in target_val_data.items()
                # }
                test.update(to_add)
            elif len(train_data) != 0:
                # Retain at least one case for test
                to_add = random.sample(
                    sorted(train_data),
                    min(len(train_data), args.min_test) - 1,
                )
                train = train.difference(to_add)
                # target_test_data = {
                #     k: v.intersection(test)
                #     for k, v in target_test_data.items()
                # }
                test.update(to_add)
            else:
                logging.warning(
                    f"Unable to ensure representation for target {target} in "
                    "testing split"
                )
        for target, data in target_data.items():
            target_train_data[target] = set(data).intersection(train)
            target_test_data[target] = set(data).intersection(test)
            target_val_data[target] = set(data).intersection(val)

        target_empty_train = [
            target
            for target, data in target_train_data.items()
            if len(data) == 0
        ]
        target_empty_test = [
            target
            for target, data in target_test_data.items()
            if len(data) == 0
        ]

        logging.info(f"Targets with no training data: {target_empty_train}")
        logging.info(f"Targets with no testing data: {target_empty_test}")
        if any(
            [
                len(segment) == 0
                for segment in [target_empty_train, target_empty_test]
            ]
        ):
            logging.info("Rerunning")
    target_empty_val = [
        target for target, data in target_val_data.items() if len(data) == 0
    ]
    # Check leakage
    for seg1, seg2 in combinations([train, test, val], 2):
        logging.info(f"Overlap: {len(seg1.intersection(seg2))}")

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
    save([args.output_path, "train", "train_targets.json"], target_train_data)
    save([args.output_path, "test", "test_targets.json"], target_test_data)
    save([args.output_path, "val", "val_targets.json"], target_val_data)
    save(
        [args.output_path, "train", "train_targets_num.json"],
        target_train_data_num,
    )
    save(
        [args.output_path, "test", "test_targets_num.json"],
        target_test_data_num,
    )
    save(
        [args.output_path, "val", "val_targets_num.json"],
        target_val_data_num,
    )
    save([args.output_path, "train", "train_cases.txt"], train)
    save([args.output_path, "test", "test_cases.txt"], test)
    save([args.output_path, "val", "val_cases.txt"], val)
    save(
        [args.output_path, "train", "train_target_empty.txt"],
        target_empty_train,
    )

    save(
        [args.output_path, "test", "test_target_empty.txt"],
        target_empty_test,
    )
    save(
        [args.output_path, "val", "val_target_empty.txt"],
        target_empty_val,
    )


def update(
    segment: set[str], target_seg_data: dict[str, list[str]]
) -> dict[str, list[str]]:
    """Update target segment dictionary

    Parameters
    ----------
    segment : set[str]
       Updated segment to update target dictionary
    target_seg_data : dict[str, list[str]]
        Dictionary target segment to update

    Returns
    -------
    dict[str, list[str]]
        Updated dictionary target segment
    """
    for k, v in target_seg_data.items():
        target_seg_data[k] = list(v.intersection(segment))
    return target_seg_data


def checkandremove(
    datapoints: list[str],
    segment: set[str],
    data_targets: dict[str, list[str]],
    min_count: int,
) -> (list[str], set[str]):
    """Check and remove potential leakage points

    Parameters
    ----------
    datapoints : list[str]
        Points to check for leakage
    segment : set[str]
        Segment against which to check leakage
    data_targets : dict[str, list[str]]
        Targets for each datapoint (used for selecting points to remove/add)
    min_count : int
        Minimum count to ensure for datapoints

    Returns
    -------
    (list[str], set[str])
        Updated datapoints and segment
    """
    datap_seg_overlap = datapoints.intersection(segment)
    if len(datap_seg_overlap) != 0:
        datapoints = datapoints.difference(datap_seg_overlap)
        if len(datapoints) < min_count:
            ordered = sorted(
                datap_seg_overlap, key=lambda x: len(data_targets[x])
            )
            to_add = ordered[: min_count - len(datapoints)]
            datapoints.update(to_add)
            segment = segment.difference(to_add)
    return datapoints, segment


def save(path: list, obj: object) -> None:
    """Utility to save generated information

    Parameters
    ----------
    path : list
        Path to create from list to save data to
    obj : object
        Object to save
    """
    savepath = os.path.join(*path)
    if type(obj) in [list, set]:
        with open(savepath, "w") as f:
            for line in obj:
                print(line, file=f, end="\n")
    elif type(obj) == dict:
        with open(savepath, "w") as f:
            json.dump(obj, f, indent=4)
    else:
        logging.error(f"Unrecognised format {type(obj)} for saving>")


if __name__ == "__main__":
    main()
