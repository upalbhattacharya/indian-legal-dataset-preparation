#!/usr/bin/env sh

./get_area_act_chapter_section_info.py  --input_path ~/Datasets/DHC/common/preprocess/statutes/  \
    --area_info ~/Datasets/DHC/raw/area_survey/act_areas.json \
    --chapter_info ~/Datasets/IndiaCode/new/CentralActs/section_chapters_alt.json \
    --selected_cases ~/Datasets/DHC/variations/v5/split_info/test/test_cases.txt \
    --output_path ~/Datasets/DHC/variations/v5/area_act_chapter_section_info/test
