import csv
import sys
import numpy as np
from matplotlib import pyplot
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
    xpos = y_len*range(x_len)  # It's not elegant but easy to repeat
    ypos = x_len*range(y_len)
    xpos = np.array(xpos)+0.25
    ypos = np.array(ypos)+0.25
    zpos = np.zeros(x_len*y_len)
    data = params["data"]
    data = np.array(data)
    data = data.flatten()
    dx = 0.5*np.ones_like(zpos)
    dy = dx.copy()
    colors = polly.color_base[0:x_len]
    colors *= y_len
    X, Y = np.meshgrid(xpos, ypos)
    ax.plot_surface(xpos, ypos, zpos, dx, dy, data, color=colors, edgecolor="none", alpha=0.65)
    ax.set_title(params["title"])
    ax.set_xlabel(params["xlabel"])
    ax.set_xticks(xpos+0.25)
    ax.set_xticklabels(params["xticks"], ha="center")
    ax.set_ylabel(params["ylabel"])
    ax.set_yticks(ypos+0.25)
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
