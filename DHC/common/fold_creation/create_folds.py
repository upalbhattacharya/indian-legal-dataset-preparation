#!/usr/bin/env python

"""Create train-test folds for given data"""

import argparse
import json
import logging
import os
import shutil

from sklearn.model_selection import KFold
from utils import set_logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_list",
                        help="List of files/documents to splits")
    parser.add_argument("-n", "--nfold", type=int, default=5,
                        help="Number of folds to create")
    parser.add_argument("-d", "--data_dir", type=str, default=None,
                        help="Directory with data to use to copy files")
    parser.add_argument("-e", "--ext", default=None,
                        help=("Document extensions for files to move. "
                              "Specify extension without leading dot"))
    parser.add_argument("-o", "--output_dir",
                        help="Path to save generated split information")

    args = parser.parse_args()

    set_logger(os.path.join(args.output_dir, "create_folds"))
    logging.info("Inputs:")
    for name, value in vars(args).items():
        logging.info(f"{name}: {value}")

    # Raise error if data_dir provided but not ext
    try:
        if args.data_dir is not None and args.ext is None:
            raise ValueError(("Argument '--ext' has to be specified when "
                              "specifying argument '--data_dir'"))
    except ValueError as e:
        logging.error(repr(e))
        return

    # Load file list
    with open(args.file_list, 'r') as f:
        docs = f.readlines()
    items = list(filter(None, map(lambda x: x.strip(), docs)))
    logging.info(f"Will carry out {args.nfold} cross-validation with "
                 f"{len(items)} items")

    kfold = KFold(n_splits=args.nfold, shuffle=True, random_state=47)

    for i, (train_idx, test_idx) in enumerate(kfold.split(items)):
        logging.info(f"Fold {i+1} has {len(train_idx)} training items and "
                     f"{len(test_idx)} testing items")
        train_items = [items[idx] for idx in list(train_idx)]
        test_items = [items[idx] for idx in list(test_idx)]
        split_info = {
                "train": train_items,
                "test": test_items
                }
        save_path = os.path.join(args.output_dir, f"{args.nfold}_fold",
                                 f"fold_{i}")
        # Create directory for split
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        # Copy data if required
        if args.output_dir is not None and args.ext is not None:
            logging.info("Copying files")
            train_path = os.path.join(save_path, "train")
            test_path = os.path.join(save_path, "test")
            if not os.path.exists(train_path):
                os.makedirs(train_path)
            if not os.path.exists(test_path):
                os.makedirs(test_path)

            for item in train_items:
                fl = item + f".{args.ext}"
                logging.info(f"Copying training item {fl}")
                shutil.copy(os.path.join(args.data_dir, fl),
                            os.path.join(train_path, fl))

            for item in test_items:
                fl = item + f".{args.ext}"
                logging.info(f"Copying testing item {fl}")
                shutil.copy(os.path.join(args.data_dir, fl),
                            os.path.join(test_path, fl))

        with open(os.path.join(save_path, "split_info.json"), 'w') as f:
            json.dump(split_info, f, indent=4)


if __name__ == "__main__":
    main()
