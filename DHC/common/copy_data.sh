#!/usr/bin/env sh

SRC="/home/workboots/Datasets/DHC/common/preprocess/fact_sentences"
DEST="/home/workboots/Datasets/DHC/variations/v5/data/test"
FILE="/home/workboots/Datasets/DHC/variations/v5/split_info/test/test_cases.txt"

while read line
do
    cp "${SRC}/${line}.txt" "${DEST}/"
done < ${FILE}
