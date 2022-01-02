#!/home/workboots/workEnv/bin/python3

"""parse_json.py: Extract 'doc' element of raw data (contains required
information).
"""

import argparse
import json
import logging
import os

from bs4 import BeautifulSoup

from utils import set_logger, time_logger

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


parser = argparse.ArgumentParser()

parser.add_argument("-d", "--input_path",
                    help="Source path to load files from.")
parser.add_argument("-o", "--output_path",
                    help="Output path to store cleaned data.")


@time_logger
def main():

    args = parser.parse_args()

    set_logger(os.path.join(args.output_path, "parse_json.log"))
    logging.info(f"Parsing json files from {args.input_path}.")
    logging.info(f"Saving parsed html documents to {args.output_path}.")

    for flname in os.listdir(args.input_path):

        # Only getting json files
        if not(flname.endswith(".json")):
            logging.info(f"File {flname} is not a json file. Skipping.")
            continue

        filepath = os.path.join(args.input_path, flname)
        filename = os.path.splitext(flname)[0]

        # Only working with json case files that have actual data
        if(os.stat(filepath).st_size == 0):
            logging.info(
                f"File {flname} does not contain any data. Skipping.")
            continue

        logging.info(f"Loading and converting {flname}")

        with open(filepath, 'r') as f:
            json_data = json.load(f)

        # Extracting the 'doc' section from the json file
        html_data = json_data['doc']

        # Using BeautifulSoup to save it in a human-readable format
        soup = BeautifulSoup(html_data, 'html.parser')

        with open(os.path.join(args.output_path,
                               f"{filename}.html"), 'w') as f:
            f.write(soup.prettify())


if __name__ == "__main__":
    main()
