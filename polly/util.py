import logging
import os
import sys
import argparse


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
