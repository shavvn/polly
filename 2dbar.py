"""
generate 2d bar graphs..
Still not sure if I should do it in OOP, but fuck it... do this first
"""
import csv
import sys
import numpy as np
from matplotlib import pyplot
import polly

__author__ = "Shang Li"


def parse_csv(csv_name):
    params = {}
    with open(csv_name) as f:
        csv_reader = csv.reader(f)
        meta_info = csv_reader.next()
        if meta_info:
            params.update({"title": meta_info[0]})
        x_meta = csv_reader.next()
        params.update({"xlabel": x_meta[0]})
        params.update({"xticks": x_meta[1:]})
        y_meta = csv_reader.next()
        params.update({"ylabel": y_meta[0]})
        params.update({"data": y_meta[1:]})
    return params


# def center_xtick(x_axis):
#    for tick in x_axis.get_ticks():


def plot(ax, params):
    width = 0.4
    if "width" in params:
        width = float(params["width"])
    data = map(int, params["data"])  # TODO what if float...?
    ind = np.arange(len(params["xticks"]))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.set_label_position('bottom')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_label_position('left')
    ax.yaxis.set_ticks_position('left')
    ax.bar(ind, height=data, color=polly.color_base[1], align="center", edgecolor="none")
    ax.set_title(params["title"])
    ax.set_xlabel(params["xlabel"])
    ax.set_xticks(ind)
    ax.set_xticklabels(params["xticks"], ha="center")
    ax.set_ylabel(params["ylabel"])

    return


def parse_plot_save(f_name, out_dir):
    params = parse_csv(f_name)
    fig, ax = pyplot.subplots(1, 1)
    plot(ax, params)
    fig.savefig(out_dir+params["title"]+".pdf", format="pdf", dpi=1000)
    fig.clear()
    
if __name__ == "__main__":
    file_list, out_dir = polly.parse_argv(sys.argv[1:])  # first element is this file...
    for each_file in file_list:
        parse_plot_save(each_file, out_dir)
    print file_list
