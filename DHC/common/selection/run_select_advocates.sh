#!/usr/bin/sh

FOLDS=1
SPLITS="train test val"

for fold in $(seq 0 $(($FOLDS - 1)))
do
    for split in $SPLITS
    do
        ./select_advocates.py -ac /DATA/upal/Datasets/DHC/common_new/adv_info/adv_cases.json \
            -n  0 \
            -p /DATA/upal/Datasets/DHC/variations/new/var_6/adv_info/overall/pet_cases.json \
            -d /DATA/upal/Datasets/DHC/variations/new/var_6/adv_info/overall/res_cases.json \
            -o /DATA/upal/Datasets/DHC/variations/new/var_6/adv_info/${FOLDS}_fold/fold_${fold}/${split}/ \
            -s /DATA/upal/Datasets/DHC/variations/new/var_6/cross_val/${FOLDS}_fold/fold_${fold}_${split}_cases.txt \
            -sa /DATA/upal/Datasets/DHC/variations/new/var_6/adv_info/overall/selected_advs.txt
    done
done

