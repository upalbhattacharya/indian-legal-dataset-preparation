#!/usr/bin/env python

"""Create dictionary of sections for section extraction"""

import os
import argparse
import json
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--meta_info",
                        help="Document containing meta information")
    parser.add_argument("-d", "--data_path",
                        help="Path to directory with all information")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data")

    args = parser.parse_args()

    with open(args.meta_info, 'r') as f:
        meta_info = json.load(f)

    sections = {}
    chapters = {}

    r = re.compile(r"The", flags=re.I)

    for title, content in meta_info.items():
        path = os.path.join(args.data_path, content["Act ID"] + ".json")
        if not os.path.exists(path):
            continue
        with open(path, 'r') as f:
            secs = json.load(f)

        # Handle 'Article' for Constitution
        secs = {re.sub("Article ", "", k): v 
                for k, v in secs.items()}

        title = r.sub('', title).strip()

        sections.update({
            f"{title}_{sec}": f"{title}_{sec}" for sec in secs})

        chapters.update({
            f"{title}_{sec}": f"{title}_" + secs[sec]["chapter"] if
            secs[sec]["chapter"] != "" else f"{title}_" + "NO CHAPTER"
            for sec in secs})

    with open(os.path.join(args.output_path, "section_names.json"), 'w') as f:
        json.dump(sections, f, indent=4)

    with open(os.path.join(args.output_path, "section_chapters.json"),
              'w') as f:
        json.dump(chapters, f, indent=4)


if __name__ == "__main__":
    main()
