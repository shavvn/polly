import polly
import csv
import sys
import numpy as np



class Bar2D(polly.Polly):
    def __init__(self, **kwargs):
        super(Bar2D, self).__init__(**kwargs)
        default_params = {
            "xlabel": "X Label",
            "xticks": "",
            "ylabel": "Y Label",
            "yticks": "",
        }
        for key in default_params:
            if key not in self.params:
                self.params.update({key: default_params[key]})

    def parse_csv(self, csv_name):
        with open(csv_name, "r") as f:
            csv_reader = csv.reader(f)
            meta_info = csv_reader.next()
            if meta_info:
                self.params.update({"title": meta_info[0]})
            x_meta = csv_reader.next()
            self.params.update({"xlabel": x_meta[0]})
            self.params.update({"xticks": x_meta[1:]})
            y_meta = csv_reader.next()
            self.params.update({"ylabel": y_meta[0]})
            self.params.update({"data": map(float, y_meta[1:])})
        return self.params

    def plot(self):
        data = map(int, self.params["data"])
        x_ticks = self.set_x_axis()
        self.set_y_axis()
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.bar(x_ticks, height=data, color=polly.color_base[1], align="center", edgecolor="none")
        self.ax.set_title(self.params["title"])

    def plot_save(self, output_name, **kwargs):
        self.plot()
        self.save_fig(output_name, **kwargs)
        self.fig.clear()

    def parse_plot_save(self, f_name, out_dir, graph_format):
        output_name = polly.gen_output_name(f_name, out_dir)
        self.parse_csv(f_name)
        self.plot_save(output_name, output_format=graph_format)


def plot(params):
    """
    TODO: this still could be simplified by just passing data, let the program figure
    out x and y
    :param params: params, should have at least "data" set
    :return:
    """
    bar_2d = Bar2D(**params)
    bar_2d.plot()
    bar_2d.fig.show()


def plot_save(f_name, params, out_dir, format):
    """
    TODO for those out_dir, format which have default values, could pack it to **kwarg
    :param f_name: name to be saved
    :param params: params
    :param out_dir: where to be saved
    :param format: format to be saved
    :return:
    """
    bar_2d = Bar2D(**params)
    bar_2d.plot_save(f_name, out_dir, format)


def parse_plot_save(csv_file, out_dir, format):
    bar_2d = Bar2D()
    bar_2d.parse_plot_save(csv_file, out_dir, format)


if __name__ == "__main__":
    file_list, out_dir, graph_format = polly.parse_argv(sys.argv[1:])
    for each_file in file_list:
        parse_plot_save(each_file, out_dir, graph_format)
