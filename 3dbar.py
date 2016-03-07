import csv
import sys
import numpy as np
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import polly

__author__ = "Shang Li"


def parse_csv(csv_name):
    """
    There are something fundamentally different about 3d graph...
    xpos, ypos, zpos are starting point of a bar
    dx, dy, dz are the dimension of a bar
    :param csv_name:
    :return:
    """
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
        params.update({"yticks": y_meta[1:]})
        z_meta = csv_reader.next()
        params.update({"zlabel": z_meta[0]})
        data = []
        for line in csv_reader:
            data.append(map(float, line))  # Convert to float instead of int
            # TODO maybe throw an exception if cannot convert?
        params.update({"data": data})
    return params


def plot(ax, params):
    x_len = len(params["xticks"])
    y_len = len(params["yticks"])
    xpos = y_len*range(x_len)  # It's not elegant but easy to repeat
    ypos = x_len*range(y_len)
    xpos = np.array(xpos)
    ypos = np.array(ypos)
    zpos = np.zeros(x_len*y_len)
    # ax.spines["top"].set_visible(False)
    # ax.spines["right"].set_visible(False)
    # ax.xaxis.set_label_position('bottom')
    # ax.xaxis.set_ticks_position('bottom')
    # ax.yaxis.set_label_position('left')
    # ax.yaxis.set_ticks_position('left')
    data = params["data"]
    data = np.array(data)
    data = data.flatten()
    dx = 0.5*np.ones_like(zpos)
    dy = dx.copy()
    ax.bar3d(xpos, ypos, zpos, dx, dy, data, color=polly.color_base[1])
    ax.set_title(params["title"])
    ax.set_xlabel(params["xlabel"])
    ax.set_xticks(xpos)
    ax.set_xticklabels(params["xticks"], ha="center")
    ax.set_ylabel(params["ylabel"])
    ax.set_yticks(ypos)
    ax.set_yticklabels(params["yticks"], ha="center")
    return


def parse_plot_save(f_name, out_dir):
    params = parse_csv(f_name)
    fig = pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')
    plot(ax, params)
    fig.savefig(out_dir+params["title"]+".pdf", format="pdf", dpi=1000)
    fig.clear()


if __name__ == "__main__":
    file_list, out_dir = polly.parse_argv(sys.argv[1:])  # first element is this file...
    for each_file in file_list:
        parse_plot_save(each_file, out_dir)
    print file_list