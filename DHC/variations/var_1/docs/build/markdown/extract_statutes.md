# extract_statutes module

extract_statutes.py: Extract statutes from documents.


### extract_statutes.check_exists(actsec, statutes)
Return valid cited statutes.

actsec

    Set of statutes cited and their spans.

statutues: dict

    Dictionary of statutes to reference.

cleaned

    Valid set of statutes and their spans.


* **Return type**

    `set`



### extract_statutes.clean(act_sec)
Clean up given set of extracted sections to standard format.

actsec

    Set containing statutes and their spans.

actsec

    Set containing formatted statutes and their spans.


* **Return type**

    `set`



### extract_statutes.extract_statutes(text, per_sentence=True)
Finds all statutes mentioned in the given text.

text

    Text to extract statutes from.

per_sentence

    Whether to find the statutes for each sentence. (Only works when a
    dictionary is passed to text.)

secs

    Dictionary of cited statutes.


* **Return type**

    `dict`



### extract_statutes.get_statutes(text, actlist, unit)
Find all statutes cited in text.

text

    Text to find statutes from.

actlist

    List of acts to use for reference.

unit

    Article or section.

actsec

    Set containing cited statutes and spans.


* **Return type**

    `set`



### extract_statutes.main()

### extract_statutes.sentence_align(sentence_dict, orig)
Align citations to sentences.

sentence_dict

    Dictionary of statute citations.

orig

    Dictionary of sentences.

orig

    Dictionary with sections given for each sentence.


* **Return type**

    `dict`
