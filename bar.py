"""
This file is used to generate graphs
First I'll build up the basics and then figure out a general way to do it...
"""
import polly
import csv
import numpy as np
from matplotlib import pyplot


class Plot2DBar(polly.Polly):
    def __init__(self, *args, **kwargs):
        self.params = super(Plot2DBar, self).__init__(args, kwargs)
        self.params = {
            "xlabel": None,
            "xticks": None,
            "ylabel": None,
            "yticks": None,
        }
        self.set_params(self, args, kwargs)
        return self.params

    def parse_csv(self, fname):
        f = open(fname, "r")
        reader = csv.reader(f)
        header = next(reader)
        line = next(reader)
        data = map(int, line[1:])
        y_max = max(data)
        params = {
            "xlabel": line[0],
            "xticks": header[1:],
            "yticks": range(0, y_max, y_max/10),
            "data": data,
        }
        f.close()
        return params

    def plot(self):
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

def plot_2d_stacked_bar(params):
    ind = np.arange(len(params["xticks"]))
    width = 0.4
    offset = [0]*len(params["data"][0])
    colors = pyplot.cm.BuPu(np.linspace(0, 0.5, len(params["data"])))
    ax = pyplot.subplot(111)
    legends = []
    index = 0
    for data_row in params["data"]:
        p = pyplot.bar(ind, height=data_row, bottom=offset, color=colors[index])
        offset = map(sum, zip(data_row, offset))
        legends.append(p[0])
        index += 1
    box = ax.get_position()
    ymax = max(offset)
    ax.set_position([box.x0, box.y0, box.width*0.8, box.height])
    pyplot.title(params["title"])
    pyplot.xlabel(params["xlabel"])
    pyplot.xticks(ind+width/2, params["xticks"])
    pyplot.ylabel(params["ylabel"])
    pyplot.yticks(range(0, ymax, ymax/10))
    pyplot.legend(legends, params["breakdowns"],loc='center left', bbox_to_anchor=(1,0.5))
    pyplot.savefig("sample.png")
    pyplot.close()
    return


# ultimate goal...
def plot_3d_stacked_bar():
    return 0


if __name__ == "__main__":
    f = open("2d_stacked_sample.csv", "r")
    reader = csv.reader(f)
    header = next(reader)
    print(header)
    data = []
    breakdowns = []
    for row in reader:
        breakdowns.append(row[0])
        data.append(map(int, row[1:]))
    params = {
        "title": "Execution Time",
        "xlabel": "Shape",
        "xticks": header[1:],
        "ylabel": "Exe Time (us)",
        "yticks": None,
        "zlabel": None,
        "zticks": None,
        "breakdowns": breakdowns,
        "data": data,
    }
    plot_2d_stacked_bar(params)
