#!/home/workboots/workEnv/bin/python3
"""create_splits.py: Create N-Fold cross-validation splits for cases of a
given list of advocates.
"""

import argparse
import json
import logging
import os
import pickle
from pathlib import Path

#  import numpy as np
from sklearn.model_selection import KFold, train_test_split

from utils import set_logger, time_logger

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = ""
__email__ = "upal.bhattacharya@gmail.com"

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_path",
                    help="Directory to load required data from.")
parser.add_argument("-o", "--output_path", default=None,
                    help="Directory to save splits.")
parser.add_argument("-n", "--nfold", type=int, default=20,
                    help="Number of folds.")


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
    args = parser.parse_args()
    if(args.output_path is None):
        args.output_path = args.input_path

    set_logger(os.path.join(args.output_path, "create_splits.log"))
    logging.info(f"Loading data from {args.input_path}.")
    logging.info(f"Saving data to {args.output_path}.")

    # Loading the json file with all advocates and their cases
    with open(os.path.join(args.input_path, "adv_cases.json"), 'r') as f:
        adv_cases = json.load(f)

    with open(os.path.join(args.input_path, "case_advs.json"), 'r') as f:
        case_advs = json.load(f)

    with open(os.path.join(args.input_path, "selected_advs.json"), 'r') as f:
        adv_list = json.load(f)

    adv_list = list(adv_list.values())

    logging.info(f"Creating {args.nfold} cross validation splits.")

    kf = KFold(n_splits=args.nfold, random_state=47)

    high_count = [{} for _ in range(args.nfold)]
    db_list = [[] for _ in range(args.nfold)]
    train_list = [[] for _ in range(args.nfold)]
    test_list = [[] for _ in range(args.nfold)]
    val_list = [[] for _ in range(args.nfold)]
    split_a = [[] for _ in range(args.nfold)]
    split_b = [[] for _ in range(args.nfold)]

    for i in range(args.nfold):
        high_count[i] = {adv: {"db": [],
                               "train": [],
                               "test": [],
                               "val": []}
                         for adv in adv_list}

    for adv in adv_list:
        cases = adv_cases[adv]

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

    for case, advs in case_advs.items():
        logging.info(f"Assigning case {case} to the correct segments.")
        for i in range(args.nfold):
            if (case in train_list[i]):
                _ = [high_count[i][adv]["train"].append(case)
                     for adv in advs if adv in adv_list]

            elif (case in db_list[i]):
                _ = [high_count[i][adv]["db"].append(case)
                     for adv in advs if adv in adv_list]

            elif (case in test_list[i]):
                _ = [high_count[i][adv]["test"].append(case)
                     for adv in advs if adv in adv_list]

            else:
                _ = [high_count[i][adv]["val"].append(case)
                     for adv in advs if adv in adv_list]

    output_path = os.path.join(args.output_path,
                               Path(f"cross_val/{args.nfold}_fold/"))

    if not(os.path.exists(output_path)):
        os.makedirs(output_path)

    #  with open(os.path.join(output_path, "adv_list.csv"), 'w') as f:
        #  wr = csv.writer(f, delimiter='\n')
        #  wr.writerow(adv_list)

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

        save_as_pickle(train_list[i], fold_path, "train.pkl")
        save_as_pickle(db_list[i], fold_path, "db.pkl")
        save_as_pickle(test_list[i], fold_path, "test.pkl")
        save_as_pickle(val_list[i], fold_path, "val.pkl")

        with open(os.path.join(fold_path, "adv_case_splits.json"),
                  'w+') as f:
            json.dump(high_count[i], f, indent=4)


if __name__ == "__main__":
    main()
