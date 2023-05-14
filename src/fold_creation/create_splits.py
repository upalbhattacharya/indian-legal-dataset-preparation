#!/usr/bin/env python
# Birth: 2023-03-23 10:59:53.571586426 +0530
# Modify: 2023-03-28 12:02:21.146340679 +0530

"""Create train, test, validation splits along with cross-validation
variants."""

import argparse
import logging
import os
import random

from sklearn.model_selection import KFold, train_test_split

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

    # For Single Fold
    if args.folds == 1:
        train, test = train_test_split(
                data,
                test_size=args.test_size,
                train_size=args.train_size + args.val_size,
                shuffle=True)
        val = []
        if args.val_size != 0.0:
            args.val_size = (data_size * args.val_size *
                             1./(data_size *
                                 (args.train_size + args.val_size)))
            train, val = train_test_split(
                    train,
                    test_size=args.val_size,
                    shuffle=False)

        # Save data
        save_data(
                path=args.output_path,
                train=train,
                test=test,
                val=val,
                fold=0)

    else:
        kf = KFold(
                n_splits=args.folds,
                shuffle=False)
        args.test_size = 1./args.folds
        args.train_size = 1.0 - args.test_size - args.val_size
        args.val_size = (data_size * args.val_size *
                         1./(data_size *
                             (args.train_size + args.val_size)))
        for i, (train_idx, test_idx) in enumerate(kf.split(data)):
            train = list(map(lambda x: data[x], train_idx))
            test = list(map(lambda x: data[x], test_idx))

            if args.val_size != 0.0:
                train, val = train_test_split(
                        train,
                        test_size=args.val_size,
                        shuffle=False)

            save_data(
                    path=args.output_path,
                    train=train,
                    test=test,
                    val=val,
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
