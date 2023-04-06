#!/usr/bin/sh

FOLDS=1
SPLITS="train test val"

for fold in $(seq 0 $(($FOLDS - 1)))
do
    for split in $SPLITS
    do
        ./select_advocates.py -ac ~/Datasets/DHC/common_new/adv_info/adv_cases.json \
            -n  0 \
            -p ~/Datasets/DHC/variations/new/var_6/adv_info/overall/pet_cases.json \
            -d ~/Datasets/DHC/variations/new/var_6/adv_info/overall/res_cases.json \
            -o ~/Datasets/DHC/variations/new/var_6/adv_info/${FOLDS}_fold/fold_${fold}/${split}/ \
            -s ~/Datasets/DHC/variations/new/var_6/cross_val/${FOLDS}_fold/fold_${fold}_${split}_cases.txt \
            -sa ~/Datasets/DHC/variations/new/var_6/adv_info/overall/selected_advs.txt
    done
done

