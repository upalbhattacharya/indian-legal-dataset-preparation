#!/usr/bin/env sh

./create_per_target_balanced_splits.py --target_data ~/Datasets/DHC/variations/v5/adv_info/overall/adv_cases.json \
    --data_targets ~/Datasets/DHC/variations/v5/targets/case_advs.json \
    --train_size 0.7 \
    --test_size 0.2 \
    --val_size 0.1 \
    --output_path ~/Datasets/DHC/variations/v5/split_info
