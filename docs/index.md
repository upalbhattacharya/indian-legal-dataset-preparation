# Indian Legal Dataset Preparation's Documentation

Welcome to the documentation for the [Indian Legal Dataset Preparation
Repo](https://github.com/upalbhattacharya/indian-legal-dataset-preparation).
This repository consists of various scripts to process Indian legal case data.
The scripts have been written to work with the HTML structure of documents as
provided by [Indian Kanoon](https://indiankanoon.org) but should work with minor
tweaking for other formats. The functionalities provided are:

- Basic text cleanup.
- Extraction of textual portions of case documents.
- Crude identification and removal preamble sections of documents.
- Extraction of statutes: (Areas, Acts, Chapters and Sections)
- Identification of rhetorical roles of sentences (utilised a modified version
  of [Semantic Segmentation](https://github.com/Law-AI/semantic-segmentation).
- Extraction of names of advocates (as petitioners or respondents).
