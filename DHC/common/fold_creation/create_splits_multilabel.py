#!/usr/bin/env python
# Birth: 2023-03-28 15:27:09.205409913 +0530
# Modify: 2023-04-06 15:35:15.134017324 +0530

"""Create train, test, validation splits along with cross-validation
variants."""

import argparse
import json
import logging
import os
import random
from itertools import chain

from sklearn.preprocessing import MultiLabelBinarizer
from skmultilearn.model_selection import IterativeStratification

from utils import set_logger

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__license__ = ""
__version__ = ""
__email__ = "upal.bhattacharya@gmail.com"

random.seed(42)


def main():

    # Command-line inputs:
    # Required data:
    #  - List of items
    #  - Number of Folds (optional), default:
    #  - Train, Test and Validation size

    parser = argparse.ArgumentParser(description=(
                "Create train, test, validation splits along with "
                "cross-validation variants with additional functionality to "
                "balance representations of targets in each split."))

    parser.add_argument("--input", type=str,
                        help="Path to file with total list of items")
    parser.add_argument("--targets", type=str,
                        help="Path to targets to use for balanced splits")
    parser.add_argument("--folds", type=int, default=5,
                        help="Number of folds for cross-validation")
    parser.add_argument("--train_size", type=float, default=0.7,
                        help="Size of training split (when folds = 1)")
    parser.add_argument("--test_size", type=float, default=0.2,
                        help="Size of test split (when folds = 1)")
    parser.add_argument("--val_size", type=float, default=0.1,
                        help="Size of validation split")
    parser.add_argument("--output_path", type=str,
                        help="Path to save generated split information.")

    args = parser.parse_args()
    set_logger(os.path.join(args.output_path, "create_splits"))

    # Verify that three splits add to 1.0 when using 1 fold
    if (args.folds == 1 and
            round(args.train_size + args.test_size + args.val_size) != 1.0):
        raise ValueError("The sum of three splits should be equal to 1.0")

    for k, v in vars(args).items():
        logging.info(f"{k}: {v}")

    # Load items
    with open(args.input, 'r') as f:
        data = f.readlines()
    data = list(filter(None, map(lambda x: x.strip("\n"), data)))

    # Redefining validation split value with respect to train_size
    data_size = len(data)

    # Load targets
    with open(args.targets, 'r') as f:
        targets = json.load(f)

    data = list(set(data).intersection(set(targets)))
    target_classes = list(set(chain.from_iterable(targets.values())))

    # Binarizing labels
    mlb = MultiLabelBinarizer()

    data_targets = [set(v) for k, v in targets.items() if k in data]
    y_binarized = mlb.fit_transform(data_targets)

    # For Single Fold
    if args.folds == 1:
        stratifier = IterativeStratification(
                n_splits=2,
                order=2,
                sample_distribution_per_fold=[args.test_size,
                                              args.train_size+args.val_size])

        train_idx, test_idx = next(stratifier.split(data, y_binarized))
        data_train = [data[idx] for idx in train_idx]
        data_test = [data[idx] for idx in test_idx]

        targets_train = y_binarized[train_idx, :]
        targets_test = y_binarized[test_idx, :]

        if args.val_size != 0.0:
            args.val_size = (data_size * args.val_size *
                             1./(data_size *
                                 (args.train_size + args.val_size)))
            stratifier = IterativeStratification(
                    n_splits=2,
                    order=2,
                    sample_distribution_per_fold=[args.val_size,
                                                  args.train_size])
            train_idx, val_idx = next(stratifier.split(
                                            data_train, targets_train))
            data_train = [data_train[idx] for idx in train_idx]
            data_val = [data_train[idx] for idx in val_idx]

            targets_train = targets_train[train_idx, :]
            targets_val = targets_train[val_idx, :]

        # Save data
        save_data(
                path=args.output_path,
                train=data_train,
                test=data_test,
                val=data_val,
                fold=0)

    else:
        stratifier = IterativeStratification(
                n_splits=args.folds,
                order=2,
                sample_distribution_per_fold=[args.test_size,
                                              args.train_size+args.val_size])
        args.test_size = 1./args.folds
        args.train_size = 1.0 - args.test_size - args.val_size
        args.val_size = (data_size * args.val_size *
                         1./(data_size *
                             (args.train_size + args.val_size)))

        for i, (train_idx, test_idx) in enumerate(
                stratifier.split(data, y_binarized)):
            data_train = [data_train[idx] for idx in train_idx]
            data_val = [data_train[idx] for idx in val_idx]

            targets_train = targets_train[train_idx, :]
            targets_val = targets_train[val_idx, :]

            if args.val_size != 0.0:
                val_stratifier = IterativeStratification(
                        n_splits=2,
                        order=2,
                        sample_distribution_per_fold=[args.val_size,
                                                      args.train_size])
                train_idx, val_idx = next(val_stratifier.split(
                                                data_train, targets_train))
                data_train = [data_train[idx] for idx in train_idx]
                data_val = [data_train[idx] for idx in val_idx]

                targets_train = targets_train[train_idx, :]
                targets_val = targets_train[val_idx, :]

            save_data(
                    path=args.output_path,
                    train=data_train,
                    test=data_test,
                    val=data_val,
                    fold=i)


def save_data(
        path: str,
        train: list,
        test: list,
        val: list,
        fold: int):
    with open(
            os.path.join(path, f"fold_{fold}_train_cases.txt"), 'w') as f:
        for item in train:
            print(item, file=f, end="\n")

    with open(
            os.path.join(path, f"fold_{fold}_test_cases.txt"), 'w') as f:
        for item in test:
            print(item, file=f, end="\n")

    if len(val) > 0:
        with open(
                os.path.join(path, f"fold_{fold}_val_cases.txt"),
                'w') as f:
            for item in val:
                print(item, file=f, end="\n")


if __name__ == "__main__":
    main()
