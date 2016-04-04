"""
This file saves some public APIs that the submodules may use.
There should be 2 fundamentally different base classes: Polly and Polly 3D
All sub-classes should all inherit from these 2 base classes
"""
import logging
import os
import csv
import sys
import argparse
import numpy as np
from abc import abstractmethod
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D


class Polly(object):
    """
    A base class specify interfaces and do basic stuff such as init/set params
    and fig ax handlers
    """
    color_base = ['#E69F00', '#56B4E9', '#009E73',
                  '#F0E442', '#0072B2', '#D55E00', '#CC79A7']
    more_markers = {  # this is a "hard copy" from matplotlib.markers.py ...
                      # a total of 23 markers
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
        self._dimension = 2
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

    @classmethod
    def get_data_dimension(cls, data):
        """
        get # of dimensions of data
        :param data: data
        :return: dimension, or 0 if not normal
        """
        if isinstance(data, list):
            if isinstance(data[0], list):
                if isinstance(data[0][0], list):
                    logging.error("sorry, no more than 2 dimensional data!")
                    return 3
                else:  # 2d
                    return 2
            else:  # 1d
                return 1
        else:
            logging.error("data must be a list object")
            return 0

    @classmethod
    def map_list_to_float(cls, data_in):
        """
        map a List into a float type, put a nan if cannot convert
        :param data_in: must be list type
        :return: list of float data
        """
        data = []
        for d in data_in:
            try:
                data.append(float(d))
            except ValueError:
                logging.warning("Data point cannot be converted to float!")
                data.append(np.nan)
        return data

    @classmethod
    def get_data(cls, data_in):
        """
        get data from params, figure out the dimension of the data and
        TODO: get rid of units like 6ms->6
        :param data_in: should be a list object
        :return: "pure" data
        """
        data_dim = cls.get_data_dimension(data_in)
        data = []
        if data_dim == 1:
            data = cls.map_list_to_float(data_in)
        elif data_dim == 2:
            for dd in data_in:
                data_1d = cls.map_list_to_float(dd)
                data.append(data_1d)
        else:
            logging.error("Wrong data format! Refer examples to get correct data format!")
            sys.exit()
        return data

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
            dim = self.get_data_dimension(data)
            if dim == 2:
                ticks = range(len(data[0]))
                ticklabels = map(str, ticks)
            elif dim == 1:
                ticks = range(len(data))
                ticklabels = map(str, ticks)
            else:
                logging.error("Input data dimension not supported!")
                sys.exit()
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
            logging.info("user didn't input yticks, creating from data...")
            if self._dimension == 3:
                data = self.params["data"]
                dim = self.get_data_dimension(data)
                if dim == 2:
                    ticks = range(len(data))
                    ticklabels = map(str, ticks)
                    self.ax.set_yticks(ticks)
                    self.ax.set_yticklabels(ticklabels, va="center")
                else:  # passed a 1d data to a 3d plot? no!
                    logging.error("Please don't pass 1D data to 3D graph..")
            elif self._dimension == 2:  # matplotlib will figure it out for you...
                pass
            else:
                logging.error("Input data dimension not supported!")
                sys.exit()

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
        logging.info("saving figure as "+path_and_name)
        self.fig.savefig(path_and_name, format=self.output_format, dpi=self.output_dpi)

    def plot(self):
        """
        This use to be an abstract function but then I decide to merge the line plotting
        into the base class so it's easier. idk if it's good design practice...
        """
        data = self.get_data(self.params["data"])
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
                y_data.append(self.map_list_to_float(row[1:]))
            self.params.update({"labels": labels})
            self.params.update({"data": y_data})
        return self.params

    def plot_and_save(self, **kwargs):
        self.plot()
        self.save_fig(**kwargs)
        self.fig.clear()
        pyplot.close(self.fig)

    def parse_plot_save(self, f_name, **kwargs):
        self.parse_csv(f_name)
        self.plot_and_save(**kwargs)
        pyplot.close(self.fig)


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
        # close figure generate by 2d, this looks dump to me, is there a better way?
        self.fig.clear()
        pyplot.close(self.fig)
        self.fig = pyplot.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self._dimension = 3

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
            elif key in "output_dir":
                self.output_dir = value
            else:
                pass
        path_and_name = self.output_dir + "/" + self.output_name + "." + self.output_format
        self.ax.view_init(30, 120)
        self.fig.savefig(path_and_name, format=self.output_format, dpi=self.output_dpi)
        path_and_name = self.output_dir + "/" + self.output_name + "_2." + self.output_format
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


def get_output_name_from_input_file(input_name, out_dir):
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


def add_argv_parser():
    args_parser = argparse.ArgumentParser(description="take input to plot, "
                                                      "either a file, or something else...")
    args_parser.add_argument("--output_dir",
                             help="output directory of all shit",
                             default="./examples/")
    args_parser.add_argument("--input_dir",
                             help="input dir contains all csv files to be processed",
                             default="./input/")
    args_parser.add_argument("--list_file",
                             help="input file contains list of file dir + names",
                             default="all_csv_files.txt")
    args_parser.add_argument("--csv", nargs="*",
                             help="the names of the input csv files, "
                                  "needs to have same format as example")
    args_parser.add_argument("--format",
                             help="The output format of the graph, either pdf or png",
                             default="png", type=str, choices=["pdf", "png"])
    args_parser.add_argument("-pdf", help="set output format to pdf",
                             action="store_true")
    args_parser.add_argument("-png", help="set output format to png",
                             action="store_true")
    args_parser.add_argument("-v", "--verbose", help="output verbose",
                             action="store_true")
    args_parser.add_argument("-d", "--debug", help="whether to turn on debug",
                             action="store_true")
    return args_parser


def get_file_list(args):
    """
    get input files to be processing from args, either csv file(s),
    or a file containing a list of file names to be processed
    or an input dir containing all files to be processed
    :param args: should use the parser add_argv_parser generated
    :return: a list of file names to be processed
    """
    f_list = []
    if len(args.csv) > 0:
        f_list = args.csv
    elif args.input_dir:
        if os.path.exists(args.input_dir):
            all_files = os.listdir(args.input_dir)
            for one_file in all_files:
                if ".csv" in one_file:
                    f_list.append(one_file)
        else:
            logging.error("Input dir doesn't exist!")
            sys.exit()
    elif args.list_file:
        if os.path.isfile(args.list_file):
            for line in open(args.list_file, "r"):
                f_list.append(line.rstrip())  # rstrip get rids of end of line
        else:
            logging.error("Input file doesn't exist!")
            sys.exit()
    else:
        logging.error("Must have some input...")
        sys.exit()
    return f_list


def parse_argv(argv):
    """
    take argv as input, parse it and return usable data structures
    :param argv:
    :return: file_list a list of files need to be parsed, output dir is where they
            need to be stored, and format is in what format they neeed to be stored.
    """
    argv_parser = add_argv_parser()
    args = argv_parser.parse_args(argv)
    if args.debug:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
    if args.verbose:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)
    f_list = get_file_list(args)
    kwargs = {}
    if args.output_dir:
        kwargs["output_dir"] = args.output_dir
        if not os.path.exists(args.output_dir):
            logging.info("output dir not exist, creating one for you...")
            os.mkdir(args.output_dir)
    if args.pdf:
        kwargs["output_format"] = "pdf"
    elif args.png:
        kwargs["output_format"] = "png"
    else:
        kwargs["output_format"] = args.format
    return f_list, kwargs


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


def parse_plot_save(f_name, **kwargs):
    line = Polly()
    line.parse_plot_save(f_name, **kwargs)

if __name__ == "__main__":
    file_list, kwargs = parse_argv(sys.argv[1:])
    for each_file in file_list:
        parse_plot_save(each_file, **kwargs)
