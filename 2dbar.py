"""
generate 2d bar graphs..
Still not sure if I should do it in OOP, but fuck it... do this first
"""
import csv
import sys
import numpy as np
from matplotlib import pyplot
import matplotlib
import polly

__author__ = "Shang Li"

# matplotlib.rcParams['figure.figsize'] = 1.68, 1.5
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
font = {
    'family': 'serif',
    'weight': 'normal',
    # 'size': 12
}
matplotlib.rc('font', **font)
# matplotlib.rc('text', usetex=True)


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

    
def plot(ax, params):
    width = 0.4
    if "width" in params:
        width = float(params["width"])
    data = map(int, params["data"])  # TODO what if float...?
    ind = np.arange(len(params["xticks"]))
    ax.bar(ind, height=data, color=polly.color_base[1], edgecolor="none")
    ax.set_title(params["title"])
    ax.set_xlabel(params["xlabel"])
    ax.set_xticks(ind+width/2, params["xticks"])
    ax.set_ylabel(params["ylabel"])
    return


def parse_and_plot(f_name, out_dir):
    params = parse_csv(f_name)
    fig, ax = pyplot.subplots(1, 1)
    plot(ax, params)
    fig.savefig(out_dir+params["title"]+".pdf", format="pdf", dpi=1000)
    fig.clear()
    
if __name__ == "__main__":
    file_list, out_dir = polly.parse_argv(sys.argv[1:])  # first element is this file...
    for each_file in file_list:
        parse_and_plot(each_file, out_dir)
    print file_list
