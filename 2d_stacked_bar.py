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
        data = []
        breakdowns = []
        for line in csv_reader:
            breakdowns.append(line[0])
            data.append(map(float, line[1:]))  # Convert to float instead of int
            # TODO maybe throw an exception if cannot convert?
        params.update({"data": data})
        params.update({"breakdowns": breakdowns})
    return params


def plot(ax, params):
    ind = np.arange(len(params["xticks"]))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.set_label_position('bottom')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_label_position('left')
    ax.yaxis.set_ticks_position('left')
    data = params["data"]
    offset = [0]*len(data[0])
    handles = []
    index = 0  # have to do it in not a pythonic way, but whatever...
    for data_row in data:
        bars = ax.bar(ind, height=data_row, bottom=offset, color=polly.color_base[index], align="center", edgecolor="none")
        offset = map(sum, zip(data_row, offset))  # Add this row to prepare the offset for next row
        handles.append(bars[0])
        index += 1
    for each_bar, height in zip(bars, offset):
        ax.text(each_bar.get_x()+each_bar.get_width()/2, 1.05*height, '%.1f' % float(height), ha='center', va='bottom')
    ax.set_title(params["title"])
    ax.set_xlabel(params["xlabel"])
    ax.set_xticks(ind)
    ax.set_xticklabels(params["xticks"], ha="center")
    ax.set_ylabel(params["ylabel"])
    ax.legend(handles, params["breakdowns"], loc="best")
    return


def parse_plot_save(f_name, out_dir, graph_format):
    params = parse_csv(f_name)
    fig, ax = pyplot.subplots(1, 1)
    plot(ax, params)
    polly.save_fig(fig, polly.gen_output_name(f_name, out_dir), graph_format)
    fig.clear()


if __name__ == "__main__":
    file_list, out_dir, graph_format = polly.parse_argv(sys.argv[1:])  # first element is this file...
    for each_file in file_list:
        parse_plot_save(each_file, out_dir, graph_format)
    print file_list
