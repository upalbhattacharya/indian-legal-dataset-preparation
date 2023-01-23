#!/usr/bin/env sh

./select_cases_from_groups.py -i ~/Datasets/SC_50k/variations/var_2/area_act_chapter_section_info/overall/case_area_act_chapter_section_info.json \
    -s ~/Datasets/IndiaCode/new/CentralActs/section_chapters.json \
    -a ~/Datasets/DHC/variations/var_1/surveys/areas/Mitali/act_to_area_mapping.json \
    -o ~/Datasets/SC_50k/variations/var_3/area_act_chapter_section_info \
    -sm 150
