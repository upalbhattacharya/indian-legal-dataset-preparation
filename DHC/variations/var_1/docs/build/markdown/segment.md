# segment module

segment.py: Segments documents into sentences.


### segment.custom_sentencizer(doc: str)
Custom sentencizer to ignore brackets as sentence boundaries.

doc

    Text to process.

doc

    spacy document with sentence boundaries.


### segment.fix_sentence_boundaries(sentence_dict: dict)
Fix sentence boundaries to account for extra spaces ignored by spacy.

sentence_dict: dict

    Dictionary containing sentence text and spans.

sent_dict: dict

    Dictionary containing sentence texts and rectified spans.


### segment.main()

### segment.segment(text: str, nlp)
Segment sentences by boundary.

text

    Text to process.

nlp

    Spacy object to use for segmentation.

sent_dict

    Dictionary containing each sentence and their span.
