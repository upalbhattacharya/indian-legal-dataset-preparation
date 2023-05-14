#!/usr/bin/env python
# coding: utf-8

from skmultilearn.model_selection import iterative_train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from itertools import chain
import json

datapoints_path = "/home/workboots/Datasets/DHC/common_new/preprocess/fact_selected_cases.txt"
case_advs_path = "/home/workboots/Datasets/DHC/common_new/targets/case_advs.json"

with open(datapoints_path, 'r') as f:
    cases = f.readlines()
cases = list(filter(None, map(lambda x: x.strip("\n"), cases)))

with open(case_advs_path, 'r') as f:
    case_advs = json.load(f)
cases = list(set(cases).intersection(set(case_advs)))
advs = list(set(chain.from_iterable(case_advs.values())))

mlb = MultiLabelBinarizer()
case_targets = [set(v) for k, v in case_advs.items() if k in cases]
y_binarized = mlb.fit_transform(case_targets)
print(y_binarized.shape)

X_train, y_train, X_test, y_test = iterative_train_test_split(
        cases, y_binarized, test_size=0.2)

with open("train_cases.txt", 'w') as f:
    for c in X_train:
        print(c, file=f, end="\n")

with open("test_cases.txt", 'w') as f:
    for c in X_test:
        print(c, file=f, end="\n")
