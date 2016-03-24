import polly
import csv
import sys


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

    def plot_and_save(self, **kwargs):
        self.plot()
        self.save_fig(**kwargs)
        self.fig.clear()

    def parse_plot_save(self, f_name, **kwargs):
        self.parse_csv(f_name)
        self.plot_and_save(**kwargs)


def plot(*args, **params):
    """
    This is different from the plot in class, you only need to pass "data" in here, the program will figure
    out the rest. (of course you can also pass more than just data)
    :param params: params, should have at least "data" set
    :return: should return the object or just (fig, ax)?
    """
    if len(args) == 1:  # only support data for now
        if isinstance(args[0], list):
            bar_2d = Bar2D(data=args[0])
            bar_2d.plot()
            bar_2d.fig.show()
    else:
        bar_2d = Bar2D(**params)
        bar_2d.plot()
        bar_2d.fig.show()
        

def plot_save(params, **kwargs):
    """
    :param params: params
    :param kwargs: output kwargs
    :return:
    """
    bar_2d = Bar2D(**params)
    bar_2d.plot_and_save(**kwargs)


def parse_plot_save(csv_file, out_dir, format):
    """
    TODO only this needs to be changed along with the parse_argv function
    """
    bar_2d = Bar2D()
    kwargs = {"output_dir": out_dir,
              "output_format": format}
    bar_2d.parse_plot_save(csv_file, **kwargs)


if __name__ == "__main__":
    file_list, out_dir, graph_format = polly.parse_argv(sys.argv[1:])
    for each_file in file_list:
        parse_plot_save(each_file, out_dir, graph_format)
