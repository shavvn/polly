import polly
import csv
import sys


class Bar2D(polly.Polly):
    """
    Feel like don't even need an init
    """
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
            data = self.map_list_to_float(y_meta[1:])
            self.params.update({"data": data})
        return self.params

    def plot(self):
        data = self.get_data(self.params["data"])
        x_ticks = self.set_x_axis()
        self.set_y_axis()
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.bar(x_ticks, height=data, color=self.color_base[1], align="center", edgecolor="none")
        self.ax.set_title(self.params["title"])


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


def plot_and_save(params, **kwargs):
    """
    :param params: params
    :param kwargs: output kwargs
    :return:
    """
    bar_2d = Bar2D(**params)
    bar_2d.plot_and_save(**kwargs)


def parse_plot_save(csv_file, **kwargs):
    bar_2d = Bar2D()
    bar_2d.parse_plot_save(csv_file, **kwargs)


if __name__ == "__main__":
    file_list, kwargs = polly.parse_argv(sys.argv[1:])
    for each_file in file_list:
        parse_plot_save(each_file, **kwargs)
