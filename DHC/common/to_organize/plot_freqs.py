#!/home/workboots/VirtualEnvs/aiml/bin/python3
# -*- encoding: utf8 -*-
# Birth: 2022-01-06 11:51:29.568250615 +0530
# Modify: 2022-01-06 21:32:03.069177719 +0530

"""
Plot frequency-based bar plots from a dictionary.
"""

import argparse
import json
import os

#  import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

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
                        help="Label of X axis.")
    parser.add_argument("-y", "--ylabel",
                        help="Label of Y axis.")

    args = parser.parse_args()

    # Loading the data
    with open(args.input_path, 'r') as f:
        data = json.load(f)

    df = pd.DataFrame.from_dict(data, orient="index", columns=["Frequency"])
    fig = px.bar(df, log_y=True)
    fig.update_layout(showlegend=False,
                      title=args.title,
                      xaxis_title=args.xlabel,
                      yaxis_title=args.ylabel,
                      xaxis=dict(
                          rangeslider=dict(
                              visible=True)))

    fig.update_traces(marker_color='maroon')
    fig.update_xaxes(visible=True, showticklabels=False)
    flname = args.title.lower().replace(" ", "_")
    fig.write_html(os.path.join(args.output_path, f"{flname}.html"))


if __name__ == "__main__":
    main()
