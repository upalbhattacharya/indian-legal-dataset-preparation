#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf8 -*-
# Last Modified: Wed Jan 05, 2022  02:18PM

"""
Find the distribution of acts and sections for cases.
"""

import argparse
import json
import os
from collections import Counter

from utils import order


def get_distbn(dict_obj: dict, key: str = "acts") -> dict:
    """Return frequency of given key elements from dictionary.

    Parameters
    ----------
    dict_obj : dict
        Dictionary to get frequency information from.
    key : str, default "acts"
        Element class to obtain frequency information for.

    Returns
    -------
    dict

    """
    ele_freq = [ele for item in dict_obj.values()
                for ele in item[key].keys()]
    ele_freq = dict(Counter(ele_freq))
    ele_freq = order(ele_freq)
    return ele_freq


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load data from.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data.")

    args = parser.parse_args()

    with open(args.input_path, 'r') as f:
        case_statute_info = json.load(f)

    act_freq = get_distbn(case_statute_info, "acts")
    sec_freq = get_distbn(case_statute_info, "sections")

    with open(os.path.join(args.output_path, "act_freq.json"),
              'w') as f:
        json.dump(act_freq, f, indent=4)

    with open(os.path.join(args.output_path, "section_freq.json"),
              'w') as f:
        json.dump(sec_freq, f, indent=4)


if __name__ == "__main__":
    main()
