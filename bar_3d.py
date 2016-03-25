import csv
import sys
import numpy as np
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import polly

__author__ = "Shang Li"


class Bar3D(polly.Polly3D):

    def parse_csv(self, csv_name):
        """
        There are something fundamentally different about 3d graph...
        xpos, ypos, zpos are starting point of a bar
        dx, dy, dz are the dimension of a bar
        :param csv_name:
        :return:
        """
        with open(csv_name) as f:
            csv_reader = csv.reader(f)
            meta_info = csv_reader.next()
            if meta_info:
                self.params.update({"title": meta_info[0]})
            x_meta = csv_reader.next()
            self.params.update({"xlabel": x_meta[0]})
            self.params.update({"xticks": x_meta[1:]})
            y_meta = csv_reader.next()
            self.params.update({"ylabel": y_meta[0]})
            self.params.update({"yticks": y_meta[1:]})
            z_meta = csv_reader.next()
            self.params.update({"zlabel": z_meta[0]})
            data = []
            for line in csv_reader:
                data.append(map(float, line))  # Convert to float instead of int
                # TODO maybe throw an exception if cannot convert?
            self.params.update({"data": data})

    def plot(self):
        x_pos = self.set_x_axis()
        x_pos = np.array(x_pos)
        y_pos = self.set_y_axis()
        y_pos = np.array(y_pos)
        X, Y = np.meshgrid(x_pos, y_pos)
        X = X.flatten() + 0.25
        Y = Y.flatten() + 0.25
        z_pos = np.zeros(len(x_pos)*len(y_pos))
        data = self.params["data"]
        data = np.array(data)
        data = data.flatten()
        dx = 0.5*np.ones_like(z_pos)
        dy = dx.copy()
        colors = self.color_base[0:len(x_pos)]
        colors *= len(y_pos)
        self.ax.bar3d(X, Y, z_pos, dx, dy, data, color=colors, edgecolor="none", alpha=0.8)
        self.ax.set_xticks(x_pos+0.25)
        self.ax.set_yticks(y_pos+0.25)
        self.ax.set_zlabel(self.params["zlabel"])
        return


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
    X, Y = np.meshgrid(np.arange(x_len), np.arange(y_len))
    X = X.flatten() + 0.25
    Y = Y.flatten() + 0.25
    x_pos = np.arange(x_len)
    y_pos = np.arange(y_len)
    zpos = np.zeros(x_len*y_len)
    data = params["data"]
    data = np.array(data)
    data = data.flatten()
    dx = 0.5*np.ones_like(zpos)
    dy = dx.copy()
    colors = polly.color_base[0:x_len]
    colors *= y_len
    ax.bar3d(X, Y, zpos, dx, dy, data, color=colors, edgecolor="none", alpha=0.7)
    ax.set_title(params["title"])
    ax.set_xlabel(params["xlabel"])
    ax.set_xticks(x_pos+0.25)
    ax.set_xticklabels(params["xticks"], ha="center")
    ax.set_ylabel(params["ylabel"])
    ax.set_yticks(y_pos+0.25)
    ax.set_yticklabels(params["yticks"], ha="center")
    ax.set_zlabel(params["zlabel"])
    return


def parse_plot_save(f_name, out_dir, graph_format):
    params = parse_csv(f_name)
    plot_save(f_name, params, out_dir, graph_format)


def plot_save(f_name, params, out_dir, graph_format):
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
