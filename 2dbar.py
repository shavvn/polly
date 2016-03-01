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


def set_params(**kwargs):
    params = {}
    for key, value in kwargs.iteritems():
        params.update({key: value})
    return params


def add_params(param, **kwargs):
    for key, value in kwargs.iteritems():
        param.update({key: value})


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

    
def plot(params):
    width = 0.4
    if "width" in params:
        width = float(params["width"])
    data = map(int, params["data"])  # TODO what if float...?
    y_max = max(data)
    y_ticks = range(0, y_max, y_max/10),
    ind = np.arange(len(params["xticks"]))
    pyplot.bar(ind, height=data, color="blue")
    pyplot.title(params["title"])
    pyplot.xlabel(params["xlabel"])
    pyplot.xticks(ind+width/2, params["xticks"])
    pyplot.ylabel(params["ylabel"])
    pyplot.yticks(y_ticks)
    # pyplot.savefig("sample.png")  #TODO cannot save?
    pyplot.close()
    return


def parse_and_plot(f_name):
    params = parse_csv(f_name)
    plot(params)

    
if __name__ == "__main__":
    file_list, out_dir = polly.parse_argv(sys.argv[1:])  # first element is this file...
    for each_file in file_list:
        parse_and_plot(each_file)
    print file_list
