"""
generate 2d bar graphs..
Still not sure if I should do it in OOP, but fuck it... do this first
"""
import os
import csv
import argparse

__author__ = "Shang Li"


def set_params(**kwargs):
    params = {}
    for key, value in kwargs.iteritems():
        params.update({key: value})
    return params


def add_params(param, **kwargs):
    for key, value in kwargs.iteritems():
        param.update({key: value})


def parse_csv(csv_name):
    params = {}
    with open(csv_name) as f:
        csv_reader = csv.reader(f)
        meta_info = csv_reader.next()
        if not meta_info[0]:
            params.update({"title": meta_info[0]})
        # got title so far.
    return params

    
def plot(params):
    ind = np.arange(len(params["xticks"]))
    ax = pyplot.subplot(111)
    pyplot.bar(ind, height=params["data"], color="blue")
    pyplot.title(params["title"])
    pyplot.xlabel(params["xlabel"])
    pyplot.xticks(ind+params["width"]/2, params["xticks"])
    pyplot.ylabel(params["ylabel"])
    pyplot.yticks(params["yticks"])
    pyplot.savefig("sample.png")
    pyplot.close()
    return
    
    
if __name__ == "__main__":
    # TODO this argparsing process should be general
    # So do it here, then move it to polly maybe..
    args_parser = argparse.ArgumentParser(description="take input to plot, either a file, or something else...")
    args_parser.add_argument("--output_dir", help="output directory of all shit", default="./output/")
    args_parser.add_argument("--input_dir", help="input dir contains all csv files to be processed",
                             default="./input/")
    args_parser.add_argument("--list_file", help="input file contains list of file dir + names",
                             default="all_csv_files.txt")
    args_parser.add_argument("--csv", nargs="*", help="the name(s) of the input csv file, needs to have same format as "
                                                      "sample", default="2d_bar_sample.csv")
    # Need to have some priority here since you don't want to do all of these at once
    f_list = []
    out_dir = "./output/"
    args = args_parser.parse_args()
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
