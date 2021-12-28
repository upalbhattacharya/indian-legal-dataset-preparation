#!/home/workboots/workEnv/bin/python3
"""
For each case, the script looks through certain sections of the document to
find the names of advocates based on regexes.

Location of the names of the advocates in the document:
    * Usually, the names of the advocates are found in the 'pre' div of the
    html document.
    * The Petitioner's advocates' names are usually found after a phrase like
    "Petitioner Through".
    * The Respondent's advocates' names are usally found after such a similar
    phrase.
    * IN SOME SITUATIONS, the required names of the advocates are not
    contained in the 'pre' div and can be usually found in the first few
    paragraphs of the document.

Points for the names:
    * Names of advocates always start with a salutation like Mr., Ms. or Mrs.
    * Names can be in full like 'Yogesh Sharma' or with initials
    'O.M. Prasad'.
    * Spacing in names also varies.
    * Names can have a middle name as well.
    * The surname/title is not abbreviated. Other parts of the name can appear
    abbreviated or as initials.

Considerations for the regex matching:
    * Names are USUALLY followed by a comma. In certain instances, this is not
    followed and needs to be handled separately.
    * The regex pattern matches for both names without a middle name and names
    with a middle name.
    * For names without a middle name, the regex can provide slightly
    erroneous results like "Yogesh Sharma and" that need to be handled.

Procedure followed: For each document:
    * Get the relevant text portions (pre and p_1 to p_3) from the document.
    * Use the regex pattern matching to get names/strings.
    * Remove any repititions found (the selected portion of text can have the
    names repeated several times.
    * Removing any trailing commas ','.
    * Remove titles like 'Mr.' and 'Mrs.' from the extracted and pruned
    strings.
    * Remove any non-name words by checking for non-capitalized words in the
    extracted strings and dropping everything after the first non-capitalized
    word.
    * Remove all spaces and punctuation marks '.'. (For convenience of
    checking similar names).
    * In a dictionary with the names as keys, add the case number to each of
    the advocates extracted(in a list) if it has not been added already.
    * For each advocate, get at most 10 of the advocate names with at least
    0.85 gesalt pattern matching score.
    * For each advocate, check whether any of the similar names have the same
    case list. If so, retain the shorter name and drop the larger one from the
    dictionary.

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__licencse__ = ""
__version__ = ""
__email__ = "upal.bhattacharya@gmail.com"
"""
import argparse
import json
import logging
import os
import re
from difflib import get_close_matches

from bs4 import BeautifulSoup

from utils import set_logger, time_logger, clean_names, update_dict

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--data_path",
                    help="Source data path.")
parser.add_argument("-o", "--output_path",
                    help="Path to save data.")


@time_logger
def main():

    args = parser.parse_args()
    set_logger(os.path.join(args.output_path, "get_advocates.log"))

    # Regex to extract names
    regex = r'(?:D|M)(?:r|s|rs)\.\s*[A-Za-z.]+\s+[A-Za-z.]+(?:\s+[A-Za-z]+)?,?'

    # Terms to be used to split the text into sections for petitioner and
    # plaintiff extraction
    petitioner_terms = ['Petitioner', 'Apellant', 'Appellant', 'Plaintiff']
    respondent_terms = ['Respondent']

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

        # Splitting the text to search through for Petitioners
        unique_combinations = [(pet, res)
                               for res in respondent_terms
                               for pet in petitioner_terms]

        # For getting the text containing petitioners' advocates
        petitioner_text = ""

        for pet, res in unique_combinations:  # TODO fix petitioner extraction
            petitioner_text = (petitioner_text + " ".join(re.findall(
                pet+r's?(.+?)'+res+r's?', filtered, re.I))).strip()

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
        respondents = clean_names(respondents)

        logging.info(f"Found petitioners: {petitioners}.")
        logging.info(f"Found respondents: {respondents}.")

        adv_cases = update_dict(adv_cases,
                                [*petitioners, *respondents], flname)
        pet_cases = update_dict(pet_cases, petitioners, flname)
        res_cases = update_dict(res_cases, respondents, flname)

    i = 0
    advs = list(adv_cases.keys())
    logging.info(f"A total of {len(advs)} advocates were found.")
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
                continue

            # Merge two advocates if they have overlaps
            if (set(adv_cases[shorter]).intersection(
                    set(adv_cases[s_adv])) == set()):
                continue

            # Retaining the shorter name
            if(len(shorter) <= len(s_adv)):
                adv_cases[shorter].extend(adv_cases[s_adv])

                if(pet_cases.get(shorter, -1) != -1 and
                        pet_cases.get(s_adv, -1) != -1):
                    pet_cases[shorter].extend(pet_cases[s_adv])
                    del pet_cases[s_adv]

                if(res_cases.get(shorter, -1) != -1 and
                        res_cases.get(s_adv, -1) != -1):
                    res_cases[shorter].extend(res_cases[s_adv])
                    del res_cases[s_adv]

                logging.info(f"Merged {s_adv} with {shorter}.")
                del adv_cases[s_adv]

            else:
                adv_cases[s_adv].extend(adv_cases[shorter])

                if(pet_cases.get(shorter, -1) != -1 and
                        pet_cases.get(s_adv, -1) != -1):
                    pet_cases[s_adv].extend(pet_cases[shorter])
                    del pet_cases[shorter]

                if(res_cases.get(shorter, -1) != -1 and
                        res_cases.get(s_adv, -1) != -1):
                    res_cases[s_adv].extend(res_cases[shorter])
                    del res_cases[shorter]

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

    logging.info(f"{len(adv_cases.keys())} cleaned advocate names retained.")
    logging.info(f"{sum(list(adv_cases_len.values()))} cases were found.")

    # Saving the data
    with open(os.path.join(args.output_path, "adv_cases.json"), 'w+') as f:
        json.dump(adv_cases, f, indent=4)

    #  with open(os.path.join(args.output_path, "pet_cases.json"), 'w+') as f:
        #  json.dump(pet_cases, f, indent=4)

    #  with open(os.path.join(args.output_path, "res_cases.json"), 'w+') as f:
        #  json.dump(res_cases, f, indent=4)

    with open(os.path.join(args.output_path, "adv_cases_num.json"), 'w+') as f:
        json.dump(adv_cases_len, f, indent=4)


if __name__ == "__main__":
    main()
