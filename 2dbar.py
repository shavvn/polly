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
    ind = np.arange(len(self.params["xticks"]))
    ax = pyplot.subplot(111)
    pyplot.bar(ind, height=self.params["data"], color="blue")
    pyplot.title(self.params["title"])
    pyplot.xlabel(self.params["xlabel"])
    pyplot.xticks(ind+self.params["width"]/2, self.params["xticks"])
    pyplot.ylabel(self.params["ylabel"])
    pyplot.yticks(self.params["yticks"])
    pyplot.savefig("sample.png")
    pyplot.close()
    return
    
    
if __name__ == "__main__":
    # TODO this argparsing process should be general
    args_parser = argparse.ArgumentParser(description="take input to plot")
    args_parser.add_argument("--interval_file", help="the name of the interval output csv file, ignore if not desired",
                             default="intervals.csv")
    args_parser.add_argument("--output", help="output directory of all shit", default="./output/")
    args_parser.add_argument("--input_dir", help="input dir contains all tsv files to be processed",
                             default="../Play_Store_100k/")
    args_parser.add_argument("--list_file", help="input file contains list of file dir + names",
                             default="badapps_google.txt")
    args_parser.add_argument("--input_name", help="single input tsv file")
    
    