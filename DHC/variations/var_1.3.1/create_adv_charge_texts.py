#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-04-04 13:16:37.437543197 +0530
# Modify: 2022-04-08 15:47:20.777663762 +0530

"""Generate advocate representation texts from their IPC charges."""

import argparse
import json
import os
import re
from itertools import repeat
from random import shuffle

from collections import defaultdict
from nltk.corpus import stopwords

stopwords = stopwords.words("english")
stopwords_re = "|".join([rf"\b{word}\b" for word in stopwords])

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__license__ = ""
__version__ = "1.1"
__email__ = "upal.bhattacharya@gmail.com"


def remove_punctuation(adv_charges: dict[list[str]]) -> dict[list[str]]:
    """Naive generation of advocate representations by only punctuation
    removal.

    Parameters
    ----------
    adv_charges : dict[list]
        Charges of advocates.

    Returns
    -------
    rep : dict[list[str]]
        Representations of advocates with punctuations removed.

    """
    rep = {}

    # Generating representatives
    for adv, charges in adv_charges.items():
        adv_rep = []
        for charge in charges:
            # Removing unwanted characters
            charge_text = re.sub(r",|\.", " ", charge)
            adv_rep.append(charge_text)

        rep[adv] = adv_rep

    return rep


def lowercase(adv_charges: dict[list[str]]) -> dict[list[str]]:
    """Naive generation of advocate representations by lowercasing.

    Parameters
    ----------
    adv_charges : dict[list[str]]
        Charges of advocates concatenated.

    Returns
    -------
    rep : dict[list[str]]
        Representations of advocates after lowercasing.

    """

    rep = {}

    # Generating representatives
    for adv, charges in adv_charges.items():
        adv_rep = []
        for charge in charges:
            # Removing unwanted characters
            adv_rep.append(charge.lower())

        rep[adv] = adv_rep

    return rep


def stopword_removal(adv_charges: dict[list[str]]) -> dict[list[str]]:
    """Naive generation of advocate representations by removing stopwords.

    Parameters
    ----------
    adv_charges : dict[list[str]]
        Charges of advocates concatenated.

    Returns
    -------
    rep : dict[list[str]]
        Representations of advocates after stopword removal.

    """

    rep = {}

    # Generating representatives
    for adv, charges in adv_charges.items():
        adv_rep = []
        for charge in charges:
            # Removing unwanted characters
            adv_rep.append(re.sub(r"\s+", " ",
                                  re.sub(stopwords_re, "", charge)).strip())
            # Removing extra blankspaces

        rep[adv] = adv_rep

    return rep


def repeat_charges(adv_charges: dict,
                   reorder: bool = False) -> dict[list[str]]:
    """Create advocate representations that repeats the charges

    Parameters
    ----------
    adv_charges : dict
        Charges of advocates.
    shuffle : bool, default False
        Whether to shuffle the charges after repetition.

    Returns
    -------
    dict[list[str]]

    """

    adv_charges_rep = defaultdict(lambda: list())
    for adv, charges in adv_charges.items():
        adv_charges_rep[adv].extend(item for charge, r in charges.items()
                                    for item in list(repeat(charge, r))
                                    )
        if reorder:
            shuffle(adv_charges_rep[adv])

    return adv_charges_rep


def generate_document(adv_charge_list: list, sent_len: int):
    """Generate the representation document

    Parameters
    ----------
    adv_charge_list : list
        adv_charge_list
    sent_len : int
        sent_len
    """
    print(len(adv_charge_list))
    rep = ""
    present_sent_len = 0
    for charge in adv_charge_list:
        if len(charge.split(" ")) + present_sent_len > sent_len:
            rep = rep + "\n" + charge
            present_sent_len = len(charge.split(" "))
        else:
            rep = rep + " " + charge
            present_sent_len += len(charge.split(" "))

    return re.sub(r" +", " ", rep).strip()


def main():
    parser = argparse.ArgumentParser(
                description=("Generate advocate representations from their IPC"
                             " charges. Three strategies are used:\n"
                             "- no_repeat (default)\n"
                             "- repeat_randomized\n"
                             "- with_stopwords"))
    parser.add_argument("-c", "--charges_path",
                        help="Path to charges.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated charges.")
    parser.add_argument("-m", "--method", type=str, default="no_repeat",
                        help=("What kind of procedure to follow to generate"
                              " texts."))
    parser.add_argument("-l", "--sent_len", type=int, default=100,
                        help="Length of each pseudo sentence generated")

    args = parser.parse_args()

    # Loading charges

    with open(args.charges_path, 'r') as f:
        adv_charges = json.load(f)

    # Bringing it to the correct format for usage
    if args.method != "repeat_randomized":
        adv_charges = {
                k: list(v.keys()) for k, v in adv_charges.items()}
    else:
        adv_charges = repeat_charges(adv_charges, reorder=True)

    adv_charge_rep = remove_punctuation(adv_charges)
    adv_charge_rep = lowercase(adv_charge_rep)
    if args.method != "with_stopwords":
        adv_charge_rep = stopword_removal(adv_charge_rep)

    # Saving
    for adv, adv_charge in adv_charge_rep.items():
        doc = generate_document(adv_charge, args.sent_len)
        with open(os.path.join(args.output_path, args.method,
                               f"{adv}.txt"), 'w') as f:
            f.write(doc)


if __name__ == "__main__":
    main()
