#!/home/workboots/workEnv/bin/python3

"""select_advocates.py: Select advocates based on minimum number of cases.
"""

import argparse
import json
import logging
import os

from utils import set_logger, time_logger

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_path",
                    help="Path to load data from.")
parser.add_argument("-o", "--output_path", default=None,
                    help="Path to save generated data.")
parser.add_argument("-l", "--least", type=int, default=100,
                    help="Least number of cases for advocates.")


@time_logger
def main():
    args = parser.parse_args()
    if (args.output_path is None):
        args.output_path = args.input_path

    set_logger(os.path.join(args.output_path, "select_advocates.log"))

    with open(os.path.join(args.input_path, "adv_cases.json"), 'r') as f:
        adv_cases = json.load(f)

    adv_list = []
    for adv, cases in adv_cases.items():
        # Skipping advocates that do not meet the minimum case requirement
        if(len(cases) < args.least):
            logging.info((f"Advocate {adv} has {len(cases)}"
                          f"(<{args.least}) cases. Skipping."))
            continue
        adv_list.append(adv)

    logging.info(f"A total of {len(adv_list)} advocates were retained.")

    adv_dict = {
        (i + 1): adv for i, adv in enumerate(adv_list)}

    with open(os.path.join(args.output_path, "selected_advs.json"), 'w') as f:
        json.dump(adv_dict, f, indent=4)


if __name__ == "__main__":
    main()
