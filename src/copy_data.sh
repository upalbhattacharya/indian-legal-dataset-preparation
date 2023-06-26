#!/usr/bin/env sh

SRC="/home/workboots/Datasets/SC_50k/common/preprocess/fact_sentences"
DEST="/home/workboots/Datasets/LLPE/variations/v1/data/test"
FILE="/home/workboots/Datasets/LLPE/variations/v1/area_act_chapter_section_info/test_cases.txt"

while read line
do
    cp "${SRC}/${line}.txt" "${DEST}/"
done < ${FILE}
