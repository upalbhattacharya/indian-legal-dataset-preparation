#!/usr/bin/env sh

./create_splits_multilabel.py --input /home/workboots/Datatsets/DHC/common/preprocess/fact_selected_texts.txt \
    --targets /home/workboots/Datasets/DHC/common/targets/case_advs.json \
    --folds 1 \
    --train_size 0.7 \
    --test_size 0.2 \
    --val_size 0.1 \
    --output_path .
