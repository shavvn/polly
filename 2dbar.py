"""
generate 2d bar graphs..
Still not sure if I should do it in OOP, but fuck it... do this first
"""
import csv
import sys
import polly

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
    file_list, out_dir = polly.parse_argv(sys.argv[1:])  # first element is this file...
    print file_list
