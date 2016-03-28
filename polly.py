"""
This file saves some public APIs that the submodules may use.
There should be 2 fundamentally different base classes: Polly and Polly 3D
All sub-classes should all inherit from these 2 base classes
"""
import os
import csv
import sys
import argparse
import numpy as np
from abc import abstractmethod
from matplotlib import pyplot
from matplotlib import markers
from mpl_toolkits.mplot3d import Axes3D


class Polly(object):
    """
    A base class specify interfaces and do basic stuff such as init/set params
    and fig ax handlers
    """
    color_base = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7']
    more_markers = {  # this is a "hard copy" from matplotlib.markers.py ... a total of 23 markers
        '.': 'point',
        ',': 'pixel',
        'o': 'circle',
        'v': 'triangle_down',
        '^': 'triangle_up',
        '<': 'triangle_left',
        '>': 'triangle_right',
        '1': 'tri_down',
        '2': 'tri_up',
        '3': 'tri_left',
        '4': 'tri_right',
        '8': 'octagon',
        's': 'square',
        'p': 'pentagon',
        '*': 'star',
        'h': 'hexagon1',
        'H': 'hexagon2',
        '+': 'plus',
        'x': 'x',
        'D': 'diamond',
        'd': 'thin_diamond',
        '|': 'vline',
        '_': 'hline',
        }.keys()

    def __init__(self, **kwargs):
        """
        set default params and user defined ones
        """
        # have a list of default params, change them if necessary
        self.fig, self.ax = pyplot.subplots(1, 1)
        self.params = {
            "title": "Default Title",
            "xlabel": "X Label",
            "xticks": [],
            "ylabel": "Y Label",
            "yticks": [],
            "data": [],
        }
        self.set_params(**kwargs)
        self.plot_type = "Default"
        self.output_dpi = 300
        self.output_dir = "examples/"
        self.output_name = get_out_name_from_title(self.params["title"])
        self.output_format = "png"

    def get_params(self):
        return self.params

    def set_params(self, **kwargs):
        for key, value in kwargs.items():
            self.params.update({key: value})

    def add_params(self, **kwargs):
        """
        add new parameters from a dict structure
        :param kwargs: key and value pairs
        :return: nothing... params should be updated
        """
        for key, value in kwargs.items():
            self.params[key] = value

    def set_x_axis(self):
        """
        see if params[xticks] are set, if set, use it
        if not, then infer xticks from data
        TODO when there're many ticks it's hard to read
        :return: indices
        """
        self.ax.xaxis.set_label_position('bottom')
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.set_xlabel(self.params["xlabel"])
        ticks = self.params["xticks"]
        if ticks:
            ticks = range(len(ticks))
            self.ax.set_xticks(ticks)
            self.ax.set_xticklabels(self.params["xticks"], ha="center")
        else:
            data = self.params["data"]
            if isinstance(data[0], list):  # 2d data
                if len(data[0]) > 0:
                    ticks = range(len(data[0]))
                    ticklabels = map(str, ticks)
                    self.ax.ax.set_xticks(ticks)
                    self.ax.set_xticklabels(ticklabels, ha="center")
                else:
                    print "wtf..?"
            else:  # 1d data
                ticks = range(len(data))
                ticklabels = map(str, ticks)
                self.ax.set_xticks(ticks)
                self.ax.set_xticklabels(ticklabels, ha="center")
        return ticks

    def set_y_axis(self):
        """
        had to use 2 try/except to handle this since for 2d and 3d situations y axis
        should be handled differently... but I'm just being lazy lol
        """
        ticks = self.params["yticks"]
        try:
            self.ax.yaxis.set_label_position('left')
        except AssertionError:
            self.ax.yaxis.set_label_position('bottom')
        try:
            self.ax.yaxis.set_ticks_position('left')
        except ValueError:
            self.ax.yaxis.set_ticks_position('bottom')
        self.ax.set_ylabel(self.params["ylabel"])
        if ticks:
            ticks = range(len(ticks))
            self.ax.set_yticks(ticks)
            self.ax.set_yticklabels(self.params["yticks"], va="center")
        else:
            data = self.params["data"]
            if isinstance(data[0], list):  # 2d data, then only need to get len(data)
                if len(data) > 0:
                    ticks = range(len(data))
                    ticklabels = map(str, ticks)
                    self.ax.set_yticks(ticks)
                    self.ax.set_yticklabels(ticklabels, va="center")
                else:
                    print "wtf..?"
            else:  # for 1d data, then you can ignore this since matplotlib will handle that for you
                pass
        return ticks

    def save_fig(self, **kwargs):
        """
        Save fig with specified name and format (post fix)
        :param kwargs: overwirte default values
        :return: nothing for now..
        """
        self.output_name = get_out_name_from_title(self.params["title"])
        for key, value in kwargs.items():
            if key in "output_format":
                if value in "pdf":
                    self.output_format = "pdf"
            elif key in "output_dpi":
                self.output_dpi = value
            elif key in "output_name":
                self.output_name = value
            else:
                pass
        path_and_name = self.output_dir + "/" + self.output_name + "." + self.output_format
        self.fig.savefig(path_and_name, format=self.output_format, dpi=self.output_dpi)

    def plot(self):
        """
        This use to be an abstract function but then I decide to merge the line plotting
        into the base class so it's easier. idk if it's good design practice...
        """
        data = self.params["data"]
        xticks = self.set_x_axis()
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        cnt = 0
        for row in data:
            self.ax.plot(xticks, row, linewidth=2, marker=self.more_markers[cnt])
            cnt += 1
        self.ax.legend(self.params["labels"], loc="best")
        self.ax.set_title(self.params["title"])

    def parse_csv(self, csv_name):
        with open(csv_name) as f:
            csv_reader = csv.reader(f)
            meta_info = csv_reader.next()
            if meta_info:
                self.params.update({"title": meta_info[0]})
            x_meta = csv_reader.next()
            self.params.update({"xlabel": x_meta[0]})
            self.params.update({"xticks": x_meta[1:]})
            labels = []
            y_data = []
            for row in csv_reader:
                labels.append(row[0])
                y_data.append(map(float, row[1:]))
            self.params.update({"labels": labels})
            self.params.update({"data": y_data})
        return self.params

    def plot_and_save(self, **kwargs):
        self.plot()
        self.save_fig(**kwargs)
        self.fig.clear()

    def parse_plot_save(self, f_name, **kwargs):
        self.parse_csv(f_name)
        self.plot_and_save(**kwargs)


class Polly3D(Polly):
    def __init__(self, **kwargs):
        super(Polly3D, self).__init__(**kwargs)
        default_3d_params = {
            "zlabel": "Z Label",
            "zticks": [],
        }
        for key, value in default_3d_params.iteritems():
            if key not in self.params:
                self.params.update({key: value})
        # this looks dump to me, is there a better way?
        self.fig.clear()
        pyplot.close(self.fig)
        self.fig = pyplot.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

    def save_fig(self, **kwargs):
        """
        for 3D it's different, since it might block the view so by default I'll save 2 graphs
        from 2 different angles
        :param kwargs: overwirte default values
        :return: nothing for now..
        """
        self.output_name = get_out_name_from_title(self.params["title"])
        for key, value in kwargs.items():
            if key in "output_format":
                if value in "pdf":
                    self.output_format = "pdf"
            elif key in "output_dpi":
                self.output_dpi = value
            elif key in "output_name":
                self.output_name = value
            else:
                pass
        path_and_name = self.output_dir + "/" + self.output_name + "." + self.output_format
        self.ax.view_init(30, 120)
        self.fig.savefig(path_and_name, format=self.output_format, dpi=self.output_dpi)
        path_and_name = self.output_dir + "/" + self.output_name + "_2" + "." + self.output_format
        self.ax.view_init(30, 240)
        self.fig.savefig(path_and_name, format=self.output_format, dpi=self.output_dpi)

    @abstractmethod
    def plot(self):
        """
        Abstract method, Subclass must implement this
        :return: None
        """
        raise NotImplementedError("Subclass must implement abstract method")

    @abstractmethod
    def parse_csv(self, file_name):
        """
        :param file_name: the csv name to be parsed
        :return: params that could be used to plot
        """
        raise NotImplementedError("Subclass must implement abstract method")


def get_out_name_from_title(title):
    """
    replace weird chars with _
    :param title: title string
    :return: legit output name string
    """
    out_name = title.lower()
    out_name = out_name.replace("/", "_")
    out_name = out_name.replace(" ", "_")
    out_name = out_name.replace(":", "_")
    out_name = out_name.replace("\"", "_")
    out_name = out_name.replace("*", "_")
    return out_name


def get_args(argv):
    args_parser = argparse.ArgumentParser(description="take input to plot, either a file, or something else...")
    args_parser.add_argument("--output_dir", help="output directory of all shit", default="./examples/")
    args_parser.add_argument("--input_dir", help="input dir contains all csv files to be processed",
                             default="./input/")
    args_parser.add_argument("--list_file", help="input file contains list of file dir + names",
                             default="all_csv_files.txt")
    args_parser.add_argument("--csv", nargs="*", help="the name(s) of the input csv file, needs to have same format as "
                                                      "sample", default="2d_bar.csv")
    args_parser.add_argument("--format", help="The output format of the graph, either pdf or png",
                             default="png", type=str, choices=["pdf", "png"])
    args_parser.add_argument("-pdf", help="set output format to pdf", action="store_true")
    args_parser.add_argument("-png", help="set output format to png", action="store_true")
    args = args_parser.parse_args(argv)
    return args


def parse_argv(argv):
    """
    take argv as input, parse it and return usable data structures
    :param argv:
    :return: file_list a list of files need to be parsed, output dir is where they
            need to be stored, and format is in what format they neeed to be stored.
    """
    f_list = []
    out_dir = "./output/"
    args = get_args(argv)
    if len(args.csv) > 0:
        f_list = args.csv
    elif args.input_dir:
        if os.path.exists(args.input_dir):
            all_files = os.listdir(args.input_dir)
            for each_file in all_files:
                if ".csv" in each_file:
                    f_list.append(each_file)
        else:
            print "Input Dir doesn't exist!"
    elif args.list_file:
        if os.path.isfile(args.list_file):
            for line in open(args.list_file, "r"):
                f_list.append(line.rstrip())  # rstrip get rids of end of line
        else:
            print "Input List File doesn't exist!"
    else:
        print "really? nothing input?"
    if args.output_dir:
        out_dir = args.output_dir
        if not os.path.exists(args.output_dir):
            os.mkdir(args.output_dir)
    if args.pdf:
        graph_format = "pdf"
    elif args.png:
        graph_format = "png"
    else:
        graph_format = args.format
    return f_list, out_dir, graph_format


def gen_output_name(input_name, out_dir):
    """
    This is a helper function that take a input dir+file_name and a output dir name then
    generate a output name.
    e.g. if input_name= ../input/file.txt and out_dir= ../output/, you want the output to be
    ../output/file.something instead of ../input/..output/file.something...
    :param input_name: a mix of path and name
    :param out_dir: output dir
    :return: corrected output dir
    """
    base_name = os.path.basename(input_name)  # get rid of path
    base_name = os.path.splitext(base_name)[0]  # get rid of extension name
    out_name = out_dir + "/" + base_name
    return out_name


def save_fig(fig, output_name, output_format):
    """
    Save fig with specified name and format (post fix)
    :param fig: fig handler
    :param output_name: output name, should include path if not sure
    :param output_format: output format, will be shown as a post fix
    :return: nothing for now..
    """
    output_dpi = 600  # 600 should be enough for most cases, even for printing
    if output_format == "pdf":
        pass
    elif output_format == "png":
        output_dpi = 300
    else:
        output_format = "png"
    fig.savefig(output_name+"."+output_format, format=output_format, dpi=output_dpi)


def plot(*args, **params):
    if len(args) == 1:  # only support data for now
        if isinstance(args[0], list):
            line = Polly(data=args[0])
            line.plot()
            line.fig.show()
    else:
        line = Polly(**params)
        line.plot()
        line.fig.show()


def plot_and_save(params, **kwargs):
    line = Polly(**params)
    line.plot_and_save(**kwargs)


def parse_plot_save(f_name, out_dir, graph_format):
    line = Polly()
    kwargs = {
        "output_dir": out_dir,
        "output_format": graph_format
    }
    line.parse_plot_save(f_name, **kwargs)

if __name__ == "__main__":
    file_list, out_dir, graph_format = parse_argv(sys.argv[1:])  # first element is this file...
    for each_file in file_list:
        parse_plot_save(each_file, out_dir, graph_format)