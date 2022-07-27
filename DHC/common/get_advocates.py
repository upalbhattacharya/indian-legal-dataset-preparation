#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf-8 -*-
# Birth: 2022-07-04 17:13:03.696110411 +0530
# Modify: 2022-07-05 13:40:27.869188525 +0530

"""
Finds names of advocates in a given set of files and creates an advocate-case
mapping.
"""
import argparse
import json
import logging
import os
import regex as re
from difflib import get_close_matches

from bs4 import BeautifulSoup

from utils import set_logger, clean_names, update_dict

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = ""
__email__ = "upal.bhattacharya@gmail.com"

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--data_path",
                    help="Source data path.")
parser.add_argument("-o", "--output_path",
                    help="Path to save data.")


def main():

    args = parser.parse_args()
    set_logger(os.path.join(args.output_path, "get_advocates.log"))

    # Regex to extract names
    regex = r'(?:D|M)(?:r|s|rs)\.\s*[A-Za-z.]+\s+[A-Za-z.]+(?:\s*[A-Za-z]+)?,?'

    # Terms to be used to split the text into sections for petitioner and
    # plaintiff extraction
    petitioner_terms = ['Petitioner', 'Apellant', 'Appellant', 'Plaintiff']
    respondent_terms = ['Respondent']
    petitioner_term_regex = "|".join(petitioner_terms)
    respondent_term_regex = "|".join(respondent_terms)

    adv_cases = {}
    pet_cases = {}
    res_cases = {}

    # Iterating through the files to find advocate names of each case
    for fl in os.listdir(args.data_path):

        filepath = os.path.join(args.data_path, fl)
        flname = os.path.splitext(fl)[0]

        logging.info(f"Processing {flname}")
        with open(filepath, 'r') as f:
            raw = f.read()

        soup = BeautifulSoup(raw, 'html.parser')

        # For some documents, the name of the advocates(especially for the
        # respondents, is given in the first few paragraphs as opposed to the
        # pre div

        try:
            filtered = soup.pre.text
        except Exception:
            logging.info(
                (f"Case {flname} does not have a pre section."
                 "May not have advocate information"))
        for i in range(1, 4):
            try:
                para = soup.find("p", {"id": f"p_{i}"})
                filtered = filtered + para.text
            except Exception:
                # In the event the document is short and a certain paragraph
                # does not exist
                continue

        # For getting the text containing petitioners' advocates
        petitioner_text = set()
        respondent_text = set()

        # Works with petitioners. Best to extract respondents as set difference
        petitioner_regex = (rf"(?<={petitioner_term_regex}s?)(?P<pet>.*?)"
                            rf"versus.*?(?={respondent_term_regex}s?)"
                            rf"(?P<res>.*?)")
        r = re.compile(petitioner_regex, flags=re.I | re.DOTALL)
        segs = [m.groupdict() for m in r.finditer(filtered)]
        for el in segs:
            for k, v in el.items():
                if k == 'res':
                    respondent_text.update([v])
                else:
                    petitioner_text.update([v])

        # Alternate pattern
        petitioner_regex_alt = (rf"(?<=For the {petitioner_term_regex}s?)"
                                rf"(?P<pet>.*?)"
                                rf"(?=For the {respondent_term_regex}s?)"
                                rf"(?P<res>.*?)")
        r_alt = re.compile(petitioner_regex_alt, flags=re.I | re.DOTALL)
        segs = [m.groupdict() for m in r_alt.finditer(filtered)]
        for el in segs:
            for k, v in el.items():
                if k == 'res':
                    respondent_text.update([v])
                else:
                    petitioner_text.update([v])

        # Pruning
        petitioner_text = " ".join(petitioner_text)

        # Using regexes to find all names for a particular case
        all_names = re.findall(regex, filtered)
        advocates = set(all_names)  # Eliminating any repetitions

        # Getting text that holds names of petitioners' advocates
        petitioner_names = re.findall(regex, petitioner_text)
        petitioners = set(petitioner_names)

        # Getting the respondents' advocate names as the set difference between
        # the total names extracted and those found as petitioners
        respondents = advocates.difference(petitioners)

        petitioners = list(petitioners)
        respondents = list(respondents)

        # Running the clean_names(...) method first for petitioners and then
        # for respondents
        petitioners = clean_names(petitioners)
        respondents = clean_names(respondents, check=petitioners)

        logging.info(f"Found advocates: {clean_names(all_names)}.")
        logging.info(f"Found petitioners: {petitioners}.")
        logging.info(f"Found respondents: {respondents}.")

        adv_cases = update_dict(adv_cases,
                                [*petitioners, *respondents], flname)
        pet_cases = update_dict(pet_cases, petitioners, flname)
        res_cases = update_dict(res_cases, respondents, flname)

    # Forcefully adding any missed advocates
    for adv in adv_cases:
        if pet_cases.get(adv, -1) == -1:
            pet_cases[adv] = []

        if res_cases.get(adv, -1) == -1:
            res_cases[adv] = []

    i = 0
    advs = list(adv_cases.keys())
    logging.info(f"A total of {len(advs)} advocates were found.")
    logging.info(f"A total of {len(pet_cases.keys())} petitioners were found.")
    logging.info(f"A total of {len(res_cases.keys())} respondents were found.")
    logging.info("Removing and merging duplicates.")

    # Iterates through the dictionary to find duplicate advocate names
    # Forced to use a while loop with a manual iterating variable as variable
    # deletion takes place
    while(i < len(advs)):
        # Cleaning up the names of the advocates by removing punctutations and
        # spaces for easier similarity checking to remove redundancies by
        # gesalt pattern matching
        adv = advs[i]

        # get_close_matches uses gesalt pattern matching
        similar_advs = get_close_matches(
            adv, advs, n=10, cutoff=0.92)[1:]

        logging.info(f"Advocates {similar_advs} found similar to {adv}.")

        # Checking that similar matches are found
        if(len(similar_advs) == 0):
            i += 1
            continue

        shorter = adv
        for s_adv in similar_advs:
            # If one of the matches have already been removed from the
            # dictionary, skip it
            if(adv_cases.get(s_adv, -1) == -1):
                logging.info(f"{s_adv} not found. Possibly removed.")
                continue

            # Merge two advocates if they have overlaps
            if (set(adv_cases[shorter]).intersection(
                    set(adv_cases[s_adv])) == set()):
                logging.info(f"{adv} and {s_adv} have no cases in common.")
                continue

            # Retaining the shorter name
            if(len(shorter) <= len(s_adv)):
                adv_cases[shorter].extend(adv_cases[s_adv])

                if(pet_cases.get(shorter, -1) != -1 and
                        pet_cases.get(s_adv, -1) != -1):
                    pet_cases[shorter].extend(pet_cases[s_adv])
                    del pet_cases[s_adv]
                    assert pet_cases.get(s_adv, -1) == -1, "Deleted but found"

                if(res_cases.get(shorter, -1) != -1 and
                        res_cases.get(s_adv, -1) != -1):
                    res_cases[shorter].extend(res_cases[s_adv])
                    del res_cases[s_adv]
                    assert res_cases.get(s_adv, -1) == -1, "Deleted but found"

                logging.info(f"Merged {s_adv} with {shorter}.")
                del adv_cases[s_adv]

            else:
                adv_cases[s_adv].extend(adv_cases[shorter])

                if(pet_cases.get(shorter, -1) != -1 and
                        pet_cases.get(s_adv, -1) != -1):
                    pet_cases[s_adv].extend(pet_cases[shorter])
                    del pet_cases[shorter]
                    assert pet_cases.get(shorter, -1) == -1, "Deleted but found"

                if(res_cases.get(shorter, -1) != -1 and
                        res_cases.get(s_adv, -1) != -1):
                    res_cases[s_adv].extend(res_cases[shorter])
                    del res_cases[shorter]
                    assert pet_cases.get(shorter, -1) == -1, "Deleted but found"

                logging.info(f"Merged {shorter} with {s_adv}.")
                del adv_cases[shorter]

                shorter = s_adv

        # If the present index dictionary value is removed, do not update
        # the iterating variable
        if(adv_cases.get(adv, -1) == -1):
            i -= 1
        i += 1

        # Reconfiguring the list of keys after deletion
        advs = list(adv_cases.keys())

    adv_cases = {k: list(set(v)) for k, v in adv_cases.items()}
    adv_cases_len = {k: len(v) for k, v in sorted(adv_cases.items(),
                                                  key=lambda x: len(x[1]),
                                                  reverse=True)}

    pet_cases_len = {k: len(v) for k, v in sorted(pet_cases.items(),
                                                  key=lambda x: len(x[1]),
                                                  reverse=True)}

    res_cases_len = {k: len(v) for k, v in sorted(res_cases.items(),
                                                  key=lambda x: len(x[1]),
                                                  reverse=True)}

    logging.info(f"{len(adv_cases.keys())} cleaned advocate names retained.")
    logging.info(f"{sum(list(adv_cases_len.values()))} cases were found.")

    # Saving the data
    with open(os.path.join(args.output_path, "adv_cases_new.json"), 'w+') as f:
        json.dump(adv_cases, f, indent=4)

    with open(os.path.join(args.output_path, "pet_cases_new.json"), 'w+') as f:
        json.dump(pet_cases, f, indent=4)

    with open(os.path.join(args.output_path, "res_cases_new.json"), 'w+') as f:
        json.dump(res_cases, f, indent=4)

    with open(os.path.join(args.output_path,
                           "adv_cases_num_new.json"), 'w+') as f:
        json.dump(adv_cases_len, f, indent=4)

    with open(os.path.join(args.output_path,
                           "pet_cases_num_new.json"), 'w+') as f:
        json.dump(pet_cases_len, f, indent=4)

    with open(os.path.join(args.output_path,
                           "res_cases_num_new.json"), 'w+') as f:
        json.dump(res_cases_len, f, indent=4)


if __name__ == "__main__":
    main()
