import csv
import sys
import numpy as np
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
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
        # different from 3d bar, the xpos and ypos for 3d surface seemed to be an 2d array..
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
    # this is more difficult than I anticipated... you first need to triangulate the data to 3D
    # so that the data you pass to the plot_surface X, Y, Z are 2D arrays
    # and it turns out that the triangulation process is not trivial... wtf..
    # http://stackoverflow.com/questions/9170838/surface-plots-in-matplotlib
    # the above link should help on this issue
    x = np.arange(0, x_len, 1)
    y = np.arange(0, y_len, 1)
    X, Y = np.meshgrid(x, y)
    data = params["data"]
    data = np.array(data)
    data = data.flatten()
    Z = data.reshape(X.shape)
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, rstride=1, cstride=1, linewidth=1)
    ax.set_title(params["title"])
    ax.set_xlabel(params["xlabel"])
    ax.set_xticks(x)
    ax.set_xticklabels(params["xticks"], ha="center")
    ax.set_ylabel(params["ylabel"])
    ax.set_yticks(y)
    ax.set_yticklabels(params["yticks"], ha="center")
    ax.set_zlabel(params["zlabel"])
    return


def parse_plot_save(f_name, out_dir, graph_format):
    params = parse_csv(f_name)
    fig = pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')
    plot(ax, params)
    # for 3d plots, save 2 figures from 120 and 240 angle to make sure everything is visible
    ax.view_init(30, 120)
    polly.save_fig(fig, polly.gen_output_name(f_name, out_dir), graph_format)
    ax.view_init(30, 240)
    out_name = polly.gen_output_name(f_name, out_dir) + "_2"
    polly.save_fig(fig, out_name, graph_format)
    fig.clear()


if __name__ == "__main__":
    file_list, out_dir, graph_format = polly.parse_argv(sys.argv[1:])  # first element is this file...
    for each_file in file_list:
        parse_plot_save(each_file, out_dir, graph_format)
