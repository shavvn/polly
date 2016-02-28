"""
generate 2d bar graphs..
Still not sure if I should do it in OOP, but fuck it... do this first
"""
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
    args_parser.add_argument("--csv_files", help="the name of the input csv file, needs to have same format as sample",
                             default="2d_bar_sample.csv")
    args_parser.add_argument("--output_dir", help="output directory of all shit", default="./output/")
    args_parser.add_argument("--input_dir", help="input dir contains all csv files to be processed",
                             default="./input/")
    args_parser.add_argument("--list_file", help="input file contains list of file dir + names",
                             default="all_csv_files.txt")
    args_parser.add_argument("--csv", nargs="*", help="csv file(s) to be processed")
    