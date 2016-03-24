"""
This file saves some public APIs that the submodules may use.
I once considered to do it in OOP way, back then it looked unnecessary so I just stopped doing
it but instead tried to implement it in a very basic, function way. That's why you see the
Polly class here and the bar.py in the project.
But after I complete the 3rd submodule I realized I might switch back to OOP sometime...
For the development of new submodules, I'll keep doing traditional way, but I'll also have
another OOP branch trying to refector it to OOP...
"""
import os
import argparse
from abc import abstractmethod


class Polly(object):
    """
    A base class specify interfaces and do basic stuff such as init/set params
    """

    def __init__(self, **kwargs):
        """
        set default params and user defined ones
        """
        # have a list of default params, change them if necessary
        self.params = {
            "title": "Default Title",
            "data": None,
        }
        self.plot_type = "Default"
        self.set_params(**kwargs)
        self.output_dpi = 600

    def get_params(self):
        return self.params

    def set_params(self, **kwargs):
        # process kwargs
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

    @abstractmethod
    def save_fig(self, output_name, output_format):
        """
        save fig as specified output name and format, should be different for 2d and 3d
        :param output_name: output name, should include path
        :param output_format: output format, pdf or png
        :return: none for now...
        """
        raise NotImplementedError("Subclass must implement abstract method")

    def set_x_axis(self, ticks):
        self.ax.xaxis.set_label_position('bottom')
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.set_xlabel(self.params["xlabel"])
        self.ax.set_xticks(ticks)
        self.ax.set_xticklabels(self.params["xticks"], ha="center")

    def set_y_axis(self):
        self.ax.yaxis.set_label_position('left')
        self.ax.yaxis.set_ticks_position('left')
        self.ax.set_ylabel(self.params["ylabel"])
        # TODO maybe y and x should be handled differently but it's better to be consistent for 3d purposes...


color_base = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7']


def get_args(argv):
    args_parser = argparse.ArgumentParser(description="take input to plot, either a file, or something else...")
    args_parser.add_argument("--output_dir", help="output directory of all shit", default="./examples/")
    args_parser.add_argument("--input_dir", help="input dir contains all csv files to be processed",
                             default="./input/")
    args_parser.add_argument("--list_file", help="input file contains list of file dir + names",
                             default="all_csv_files.txt")
    args_parser.add_argument("--csv", nargs="*", help="the name(s) of the input csv file, needs to have same format as "
                                                      "sample", default="2d_bar_sample.csv")
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
