#!/usr/bin/env sh

./get_area_act_chapter_section_info.py  --input_path ~/Datasets/SC_50k/common/preprocess/statutes/  \
    --area_info ~/Datasets/DHC/raw/area_survey/act_areas.json \
    --chapter_info ~/Datasets/IndiaCode/new/CentralActs/section_chapters_alt.json \
    --output_path ~/Datasets/SC_50k/common/area_act_chapter_section_info/
