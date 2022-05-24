#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding:utf8 -*-

# Birth: 2021-12-28 11:22:20.084643339 +0530
# Modify: 2022-05-16 13:21:28.955362035 +0530

"""create_splits.py: Create N-Fold cross-validation splits for cases of a
given list of itemocates.
"""

import argparse
import json
import logging
import os
import pickle
from pathlib import Path
from collections import defaultdict

#  import numpy as np
from sklearn.model_selection import KFold, train_test_split

from utils import set_logger, time_logger

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = "1.1"
__email__ = "upal.bhattacharya@gmail.com"


def recursive_defaultdict():
    return defaultdict(recursive_defaultdict)


def print_list_overlap(train: list, db: list, test: list, val: list) -> None:
    """Print overlap between given lists.

    Parameters
    ----------
    train : list
        train
    db : list
        db
    test : list
        test
    val : list
        val

    Returns
    -------
    None

    """

    db_train = set(train).intersection(set(db))
    db_val = set(db).intersection(set(val))
    db_test = set(db).intersection(set(test))
    train_val = set(train).intersection(set(val))
    train_test = set(train).intersection(set(test))
    val_test = set(val).intersection(set(test))

    logging.info(f"db train: {db_train}")
    logging.info(f"db val: {db_val}")
    logging.info(f"db test: {db_test}")
    logging.info(f"train val: {train_val}")
    logging.info(f"train test: {train_test}")
    logging.info(f"val test: {val_test}")


def remove_overlap(sublist_a: list, sublist_b: list,
                   list_obj: list, extend_obj: list, least: int = 4) -> list:
    """Remove overlaps between sublists to be appended to two lists.

    Parameters
    ----------
    sublist_a : list
        sublist_a
    sublist_b : list
        sublist_b
    list_obj : list
        list_obj
    extend_obj : list
        extend_obj
    least : int
        least

    Returns
    -------
    list

    """

    extend_obj_pruned = list(set(extend_obj) - set(list_obj))
    list_obj_pruned = list(set(list_obj))

    if(len(extend_obj_pruned) < least):
        list_obj_pruned = list(set(list_obj) - set(extend_obj))
        sublist_a = list(set(sublist_a) - set(extend_obj))
        sublist_b = list(set(sublist_b) - set(extend_obj))
        extend_obj_pruned = list(set(extend_obj))

    return sublist_a, sublist_b, list_obj_pruned, extend_obj_pruned


def save_as_pickle(list_obj: list, path: str, flname: str) -> None:
    """Save a given object as a pickle object in the specified path.

    Parameters
    ----------
    list_obj : list
        list_obj
    path : str
        path
    flname : str
        flname

    Returns
    -------
    None

    """

    with open(os.path.join(path, flname), 'wb') as f:
        pickle.dump(list_obj, f)


@time_logger
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--case_items_path",
                        help="Case to item mapping.")
    parser.add_argument("-i", "--items_cases_path",
                        help="Item to case mapping.")
    parser.add_argument("-it", "--items_list_path",
                        help="Path to items list")
    parser.add_argument("-o", "--output_path", default=None,
                        help="Directory to save splits.")
    parser.add_argument("-n", "--nfold", type=int, default=20,
                        help="Number of folds.")
    parser.add_argument("-m", "--min_count", type=int, default=25,
                        help="Least number of cases for an item.")

    args = parser.parse_args()

    set_logger(os.path.join(args.output_path, "create_splits.log"))
    logging.info(f"Saving data to {args.output_path}.")

    # Loading the json file with all itemocates and their cases
    with open(args.items_cases_path, 'r') as f:
        item_cases = json.load(f)

    with open(args.case_items_path, 'r') as f:
        case_items = json.load(f)

    with open(args.items_list_path, 'r') as f:
        item_list = json.load(f)

    item_list = list(item_list.values())

    logging.info(f"Creating {args.nfold} cross validation splits.")

    kf = KFold(n_splits=args.nfold, random_state=47, shuffle=True)

    #  item_case_split = [defaultdict(lambda: defaultdict(list))
                       #  for _ in range(args.nfold)]
    db_list = [[] for _ in range(args.nfold)]
    train_list = [[] for _ in range(args.nfold)]
    test_list = [[] for _ in range(args.nfold)]
    val_list = [[] for _ in range(args.nfold)]
    split_a = [[] for _ in range(args.nfold)]
    split_b = [[] for _ in range(args.nfold)]

    item_case_split = [{} for _ in range(args.nfold)]

    for i in range(args.nfold):
        item_case_split[i] = {item: {"db": [],
                                     "train": [],
                                     "test": [],
                                     "val": []}
                              for item in item_list
                              if (item_cases.get(item, -1) != -1 and
                                  len(item_cases[item]) >= args.min_count)}

    for item in item_list:
        if item_cases.get(item, -1) == -1:
            logging.info(f"No cases for {item}.")
            #  item_case_split[i].pop(item, "Does not exist")
            continue
        cases = item_cases[item]
        if len(cases) < args.min_count:
            logging.info(f"Insufficient cases for {item}.")
            #  item_case_split[i].pop(item, "Does not exist")
            continue

        for i, (split_a_idx, split_b_idx) in enumerate(
                kf.split(cases)):
            extend_a = [cases[idx] for idx in split_a_idx]
            extend_b = [cases[idx] for idx in split_b_idx]

            extend_a = list(set(extend_a) - set(extend_b))

            # TODO Fix hardcoding of least attribute
            train_list[i], db_list[i], split_a[i], extend_b = remove_overlap(
                train_list[i], db_list[i], split_a[i], extend_b, least=2)

            test_list[i], val_list[i], split_b[i], extend_a = remove_overlap(
                test_list[i], val_list[i], split_b[i], extend_a, least=12)

            split_b[i].extend(extend_b)
            split_a[i].extend(extend_a)

            # TODO Fix train size percentage to be automatically calculated
            train, db = train_test_split(extend_a, train_size=0.5556)
            if len(extend_b) < 2:
                test = extend_b
                val = []
            else:
                test, val = train_test_split(extend_b, train_size=0.5)

            _, _, train_list[i], db = remove_overlap([], [], train_list[i],
                                                     db, least=9)
            _, _, db_list[i], train = remove_overlap([], [], db_list[i],
                                                     train, least=7)
            _, _, test_list[i], val = remove_overlap([], [], test_list[i],
                                                     val, least=1)
            _, _, val_list[i], test = remove_overlap([], [], val_list[i],
                                                     test, least=1)

            train_list[i].extend(train)
            db_list[i].extend(db)
            test_list[i].extend(test)
            val_list[i].extend(val)

    item_list = list(item_case_split[0].keys())

    for case, items in case_items.items():
        logging.info(f"Assigning case {case} to the correct segments.")
        for i in range(args.nfold):
            if (case in train_list[i]):
                _ = [item_case_split[i][item]["train"].append(case)
                     for item in items if item in item_list]

            elif (case in db_list[i]):
                _ = [item_case_split[i][item]["db"].append(case)
                     for item in items if item in item_list]

            elif (case in test_list[i]):
                _ = [item_case_split[i][item]["test"].append(case)
                     for item in items if item in item_list]

            else:
                _ = [item_case_split[i][item]["val"].append(case)
                     for item in items if item in item_list]

    output_path = os.path.join(args.output_path,
                               Path(f"cross_val/{args.nfold}_fold/"))

    if not(os.path.exists(output_path)):
        os.makedirs(output_path)

    for i in range(args.nfold):
        total_cases = (len(train_list[i]) + len(test_list[i])
                       + len(val_list[i]) + len(db_list[i]))
        logging.info(f"Fold {i} has {len(train_list[i])} training cases.")
        logging.info(f"Fold {i} has {len(db_list[i])} databank cases.")
        logging.info(f"Fold {i} has {len(test_list[i])} test cases.")
        logging.info(f"Fold {i} has {len(val_list[i])} validation cases.")
        logging.info(f"Fold {i} has a total of {total_cases} cases.")

        print_list_overlap(train_list[i], db_list[i], test_list[i],
                           val_list[i])

        fold_path = os.path.join(output_path, f"fold_{i}")
        if not(os.path.exists(fold_path)):
            logging.info(f"Making directory/directories {fold_path}")
            os.makedirs(fold_path)

        #  save_as_pickle(train_list[i], fold_path, "train.pkl")
        #  save_as_pickle(db_list[i], fold_path, "db.pkl")
        #  save_as_pickle(test_list[i], fold_path, "test.pkl")
        #  save_as_pickle(val_list[i], fold_path, "val.pkl")

        with open(os.path.join(fold_path, "item_case_splits.json"),
                  'w+') as f:
            json.dump(item_case_split[i], f, indent=4)


if __name__ == "__main__":
    main()
