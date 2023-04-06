#!/usr/bin/env sh

./create_splits_multilabel.py --input /DATA/upal/Datasets/DHC/common_new/preprocess/fact_selected_cases.txt \
    --targets /DATA/upal/Datasets/DHC/common_new/targets/case_advs.json \
    --folds 1 \
    --train_size 0.7 \
    --test_size 0.2 \
    --val_size 0.1 \
    --output_path .
