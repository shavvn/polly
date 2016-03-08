import os
import argparse
from abc import abstractmethod


class Polly(object):
    """
    A base class specify interfaces and do basic stuff such as init/set params
    """

    def __init__(self, *args, **kwargs):
        """
        set default params and user defined ones
        :return: self.params
        """
        # have a list of default params, change them if necessary
        self.params = {
            "title": "Default Title",
            "width": 0.4,
            "data": None,
        }
        self.plot_type = "Default"
        self.set_params(args, kwargs)

    def get_params(self):
        return self.params

    def set_params(self, *args, **kwargs):
        if len(args) == 1:  # pass a file or data structure
            if ".csv" in args:  # a csv file
                self.parse_csv(args)
            else:
                if isinstance(args, dict):  # a dict instance
                    for key, value in args.items():
                        if key in self.params:
                            self.params[key] = value
        elif len(args) == 0:
            pass
        else:
            print ("shouldn't have more than 1 args")
            exit(1)
        # process kwargs
        for key, value in kwargs.items():
            if key in self.params:
                self.params[key] = value

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


color_base = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7']


def argv_parser(argv):
    args_parser = argparse.ArgumentParser(description="take input to plot, either a file, or something else...")
    args_parser.add_argument("--output_dir", help="output directory of all shit", default="./output/")
    args_parser.add_argument("--input_dir", help="input dir contains all csv files to be processed",
                             default="./input/")
    args_parser.add_argument("--list_file", help="input file contains list of file dir + names",
                             default="all_csv_files.txt")
    args_parser.add_argument("--csv", nargs="*", help="the name(s) of the input csv file, needs to have same format as "
                                                      "sample", default="2d_bar_sample.csv")
    args_parser.add_argument("--format", help="The output format of the graph, either pdf or png",
                             default="png")
    args_parser.add_argument("-pdf", help="set output format to pdf", action="store_true")
    args_parser.add_argument("-png", help="set output format to png", action="store_true")
    # TODO figure out if we can merge the above 3 together
    args = args_parser.parse_args(argv)
    return args


def parse_argv(argv):
    f_list = []
    out_dir = "./output/"
    args = argv_parser(argv)
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
