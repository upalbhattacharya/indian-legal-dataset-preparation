#!/usr/bin/env python

"""Get sentences of particular rhetorical roles"""

import json
import argparse
import os
import logging

from utils import set_logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to input data")
    parser.add_argument("-o", "--output_path",
                        help="Path to save extracted sentences")
    parser.add_argument("-r", "--roles", nargs="+", type=str,
                        default=["Facts"],
                        help="Rhetorical roles to consider")

    args = parser.parse_args()
    set_logger(os.path.join(args.output_path, "get_roles_sentences"))
    logging.info("Inputs:")
    for name, value in vars(args).items():
        logging.info(f"{name}: {value}")

    role_lengths = {}

    for fl in os.listdir(args.input_path):
        logging.info(f"Getting sentences from {fl}")
        flname = os.path.splitext(fl)[0]
        path = os.path.join(args.input_path, fl)
        with open(path, 'r') as f:
            sent_data = json.load(f)
        sents = [sent["text"] for idx, sent in sent_data.items()
                 if sent["role"] in args.roles]

        if sents == []:
            logging.info(f"No relevant sentences found for {flname}")
            continue

        role_lengths[flname] = len(sents)
        with open(os.path.join(args.output_path, f"{flname}.txt"), 'w') as f:
            for sent in sents:
                print(sent, file=f, end="\n")

    role_lengths = {k: v for k, v in sorted(
                                    role_lengths.items(),
                                    key=lambda x: len(x[1]),
                                    reverse=True)}

    logging.info(f"Relevant sentences found for {len(role_lengths)} documents")
    with open(os.path.join(args.output_path, "role_sentences_num.json"),
              'w') as f:
        json.dump(role_lengths, f, indent=4)

    with open(os.path.join(args.output_path, "role_selected_cases.txt"),
              'w') as f:
        for case in role_lengths:
            print(case, file=f, end="\n")


if __name__ == "__main__":
    main()
