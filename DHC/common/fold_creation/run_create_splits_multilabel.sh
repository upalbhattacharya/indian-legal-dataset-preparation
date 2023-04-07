#!/usr/bin/env sh

./create_splits_multilabel.py --input /DATA/upal/Datasets/DHC/variations/new/var_6/adv_info/overall/selected_cases.txt \
    --targets /DATA/upal/Datasets/DHC/variations/new/var_6/targets/case_advs.json \
    --folds 1 \
    --train_size 0.7 \
    --test_size 0.2 \
    --val_size 0.1 \
    --output_path /DATA/upal/Datasets/DHC/variations/new/var_6/cross_val/1_fold/
