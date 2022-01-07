#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf8 -*-
# Birth: 2022-01-07 09:48:45.942860937 +0530
# Modify: 2022-01-07 10:24:45.896251539 +0530

"""
Make HTML table of given data.
"""

import argparse
import json
import os

import plotly.graph_objects as go
import pandas as pd

__author__ = "Upal Bhattacharya"
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__email__ = "upal.bhattacharya@gmail.com"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path",
                        help="Path to load data to plot.")
    parser.add_argument("-o", "--output_path",
                        help="Path to save generated plot.")
    parser.add_argument("-t", "--title",
                        help="Title of plot.")
    parser.add_argument("-x", "--xlabel",
                        help="Label of rows.")
    parser.add_argument("-y", "--ylabel",
                        help="Label of columns.")

    args = parser.parse_args()

    # Loading the data
    with open(args.input_path, 'r') as f:
        data = json.load(f)

    df = pd.DataFrame.from_dict(data, orient="index", columns=[args.ylabel])
    cols = df.columns.tolist()
    cols = [args.xlabel, *cols]
    df[args.xlabel] = df.index
    df = df[cols]
    flname = args.title.lower().replace(" ", "_")

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    align='center'),
        cells=dict(values=df.transpose().values.tolist(),
                   align='center'))
        ])

    fig.write_html(os.path.join(args.output_path, f"{flname}.html"))


if __name__ == "__main__":
    main()
