#!/usr/bin/env sh

# Selection of advocates based on optional minimum and maximum criteria


# For Folds
# FOLDS=1
SPLITS="train test val"
#
# for fold in $(seq 0 $(($FOLDS - 1)))
# do
#     for split in $SPLITS
#     do
#         ./select_advocates.py -ac /DATA/upal/Datasets/DHC/common_new/adv_info/adv_cases.json \
#             -n  0 \
#             -p /DATA/upal/Datasets/DHC/variations/new/var_6/adv_info/overall/pet_cases.json \
#             -d /DATA/upal/Datasets/DHC/variations/new/var_6/adv_info/overall/res_cases.json \
#             -o /DATA/upal/Datasets/DHC/variations/new/var_6/adv_info/${FOLDS}_fold/fold_${fold}/${split}/ \
#             -s /DATA/upal/Datasets/DHC/variations/new/var_6/cross_val/${FOLDS}_fold/fold_${fold}_${split}_cases.txt \
#             -sa /DATA/upal/Datasets/DHC/variations/new/var_6/adv_info/overall/selected_advs.txt
#     done
# done

# For overall

# ./select_advocates.py -ac ~/Datasets/DHC/common/adv_info/adv_cases.json \
#     -p ~/Datasets/DHC/common/adv_info/pet_cases.json \
#     -d ~/Datasets/DHC/common/adv_info/res_cases.json \
#     -s ~/Datasets/DHC/common/preprocess/fact_selected_cases.txt \
#     -n 10 \
#     -o ~/Datasets/DHC/variations/v5/adv_info/overall

# For one split

for split in $SPLITS
do
    ./select_advocates.py -ac ~/Datasets/DHC/variations/v5/adv_info/overall/adv_cases.json \
        -n  0 \
        -p ~/Datasets/DHC/variations/v5/adv_info/overall/pet_cases.json \
        -d ~/Datasets/DHC/variations/v5/adv_info/overall/res_cases.json \
        -o ~/Datasets/DHC/variations/v5/adv_info/${split}/ \
        -s ~/Datasets/DHC/variations/v5/split_info/${split}/${split}_cases.txt \
        -sa ~/Datasets/DHC/variations/v5/adv_info/overall/selected_advs.txt
done

exit 0
