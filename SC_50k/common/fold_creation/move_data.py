#!/usr/bin/env python

"""Copy data from location to another location based on given list"""

import argparse
import os
from shutil import copy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source_path",
                        help="Path to copy from")
    parser.add_argument("-d", "--destination_path",
                        help="Path to copy to")
    parser.add_argument("-f", "--file_list",
                        help="Path to list of files to copy")

    args = parser.parse_args()

    with open(args.file_list, 'r') as f:
        docs = f.readlines()

    docs = list(filter(None, map(lambda x: x.strip(), docs)))

    for doc in docs:
        copy(os.path.join(args.source_path, f"{doc}.txt"),
             args.destination_path)


if __name__ == "__main__":
    main()
