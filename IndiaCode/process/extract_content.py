#!/usr/bin/env python3

"""Extracts all relevant information from converted texts"""

import argparse
import json
import os
import re

from joblib import Parallel, delayed
import logging

from utils import set_logger

__author__ = "Upal Bhattacharya"
__license__ = ""
__copyright__ = ""
__version__ = ""
__email__ = "upal.bhattacharya@gmail.com"

regexes = {
        "section": re.compile(r"SECTIONS?"),
        "nonwords": re.compile(r"[^\w./,\s-]"),
        "pagenum": re.compile(r"\n+\d+\s*\n+", flags=re.DOTALL),
        "chapter": re.compile(r"CHAPTER\s+[MCLXVI]+", flags=re.DOTALL),
        "chapname": re.compile(r"([A-Z\s]+)"),
        "section_parse": re.compile(
            r"(?P<num>[0-9]+)(?P<alpha>(?:[A-Z]+)?).?\s*(?P<title>.*)"),
        "ref": re.compile(r"\d+\[(.*?)\]", flags=re.DOTALL),
        "ref_2": re.compile(r"\s*(\d)*(\*)+\s*"),
        "numbrace": re.compile(r"\d+\["),
        "upperwords": re.compile(r"\b[A-Z]+\b"),
        "namedate": re.compile(r"(.*),?\s+(\d+)?$")
            }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--act_meta_info",
                        help="Path to file with all meta information")
    parser.add_argument("-d", "--data_path",
                        help="Path to directory with all texts")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated data")

    args = parser.parse_args()

    with open(args.act_meta_info, 'r') as f:
        meta_info = json.load(f)

    with Parallel(n_jobs=-1) as parallel:
        parallel([delayed(parallelize)(act_name=act,
                                       act_id=meta_info[act]["Act ID"],
                                       data_path=args.data_path,
                                       output_path=args.output_path)
                  for act in meta_info])

    #  _ = [parallelize(act_name=act,
                     #  act_id=meta_info[act]["Act ID"],
                     #  data_path=args.data_path,
                     #  output_path=args.output_path)
         #  for act in meta_info]


def parallelize(**kwargs):
    set_logger(os.path.join(kwargs["output_path"], "extract_content"))
    path = os.path.join(kwargs["data_path"], kwargs["act_id"] + ".txt")
    if not os.path.exists(path):
        logging.info(f"{path} not found.")
        return

    with open(path, 'r') as f:
        txt = f.read()
    txt = txt.strip()
    txt = bytes(txt, 'utf-8').decode('utf-8', 'ignore')
    txt = txt.replace('\x0c', '')

    # Get name and date of act
    title = kwargs["act_name"]
    date = ""
    name_parts = regexes["namedate"].match(
                                    kwargs["act_name"].strip(".").strip())
    if name_parts is not None:
        title, date = name_parts.groups()
        title = title.strip(",")

    title = r"\s+".join(title.split())
    title = title.replace("(", "\(")
    title = title.replace(")", "\)")
    #  title = re.sub(r"\Bs\b", "s?", title)

    r = re.compile(rf"{title},?\s*({date})?", flags=re.I | re.DOTALL)
    parts = r.split(txt, maxsplit=2)
    parts = list(filter(None, parts))

    if len(parts) < 2:
        logging.info(f"Insufficient parts for {title+date}. Skipping")
        return
    else:
        if len(parts) % 2 == 0:
            arrangement = " ".join(parts[:len(parts)//2])
            info = " ".join(parts[len(parts)//2:])
        else:
            arrangement = " ".join(parts[:len(parts)//2+1])
            info = " ".join(parts[len(parts)//2+1:])

    # Get section names and chapters
    logging.info(f"Finding sections and chapters for {title}.")
    section_info = get_section_titles_chapters(text=arrangement)
    section_info = get_section_texts(text=info, section_info=section_info)

    with open(os.path.join(kwargs["output_path"], kwargs["act_id"] + ".json"),
              'w') as f:
        json.dump(section_info, f, indent=4)


def get_section_titles_chapters(text):
    arrangement = regexes["section"].sub('', text)
    arrangement = regexes["nonwords"].sub('', arrangement)
    arrangement = regexes["pagenum"].sub('', arrangement)

    chapters = regexes["chapter"].split(arrangement)
    section_info = {}

    logging.info(f"Found {len(chapters)} chapters")

    for chap in chapters:
        chap_name = regexes["chapname"].search(chap)
        chap_text = ""
        if chap_name is not None:
            chap_text = chap_name.groups()[-1].replace(
                                "PREAMBLE", '').replace(r"\s+", ' ').strip()
        matches = regexes["section_parse"].finditer(chap)
        for match in matches:
            dct = dict(match.groupdict())
            if section_info.get(dct["num"]+dct["alpha"], -1) == -1:
                section_info[dct["num"]+dct["alpha"]] = {
                        "title": dct["title"].strip().strip("."),
                        "chapter": chap_text}

    if list(section_info.keys())[0] != "1":
        del section_info[list(section_info.keys())[0]]

    return section_info


def get_section_texts(text, section_info):
    info = regexes["ref"].sub(r"\1", text)
    info = regexes["numbrace"].sub("", info)
    info = regexes["ref_2"].sub("", info)
    info = regexes["upperwords"].sub("", info)
    info = regexes["nonwords"].sub("", info)
    info = regexes["pagenum"].sub("", info)

    titles = []
    for num in section_info:
        title_text = section_info[num]["title"].split()
        title_text = r"\s+".join(title_text).strip()
        titles.append(rf"{num}\.?\s*{title_text}")

    for i, t1, t2 in zip(section_info, titles, titles[1:]+['']):
        if t2 == '':
            if i == len(titles) - 1:
                t2 = r"\Z"
        r = re.compile(rf"{t1}(.*){t2}", flags=re.I | re.DOTALL)

        for m in r.finditer(info):
            t = str(m.groups()[0]).strip()
            if t == "":
                logging.info(f"Empty found between {t1}, {t2}")
            section_info[i]["text"] = re.sub(r"\s+", ' ',
                                        str(m.groups()[0])).strip().strip(".")

    return section_info


if __name__ == "__main__":
    main()
