#!/usr/bin/env sh

./get_silver_targets.py --data_targets ~/Datasets/DHC/variations/v5/targets/case_advs.json \
  --attribute_targets ~/Datasets/DHC/variations/v5/adv_info/overall/area_act_chapter_section_info/area_adv_info.json \
  --target_attribute_info ~/Datasets/DHC/variations/v5/adv_info/overall/area_act_chapter_section_info/adv_area_act_chapter_section_info.json \
  --data_attribute_info ~/Datasets/DHC/variations/v5/area_act_chapter_section_info/overall/case_area_act_chapter_section_info.json \
  --similarity 1.0 \
  --key "areas" \
  --output_dir ~/Datasets/DHC/variations/v5/targets
