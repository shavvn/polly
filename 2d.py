import polly
import csv
import numpy as np
from matplotlib import pyplot


class Bar2D(polly.Polly):
    def __init__(self, **kwargs):
        super(Bar2D, self).__init__(**kwargs)
        default_params = {
            "xlabel": "X Label",
            "xticks": None,
            "ylabel": "Y Label",
            "yticks": None,
        }
        for key in default_params:
            if key not in self.params:
                self.params.update({key: default_params[key]})
        self.fig, self.ax = pyplot.subplots(1, 1)

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
        x_ticks = np.arange(len(self.params["xticks"]))
        self.set_x_axis(x_ticks)
        self.set_y_axis()
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.bar(x_ticks, height=data, color=polly.color_base[1], align="center", edgecolor="none")
        self.ax.set_title(self.params["title"])


    def save_fig(self, output_name, output_format):
        """
        Save fig with specified name and format (post fix)
        :param output_name: output name, should include path if not sure
        :param output_format: output format, will be shown as a post fix
        :return: nothing for now..
        """
        if output_format == "pdf":
            pass
        elif output_format == "png":
            self.output_dpi = 300
        else:
            output_format = "png"
        self.fig.savefig(output_name+"."+output_format, format=output_format, dpi=self.output_dpi)

    def parse_plot_save(self, f_name, out_dir, graph_format):
        self.parse_csv(f_name)
        self.plot()
        self.save_fig(polly.gen_output_name(f_name, out_dir), graph_format)
        self.fig.clear()


if __name__ == "__main__":
    bar_2d = Bar2D()
    bar_2d.parse_plot_save("examples/2d_bar_sample.csv", "examples/", "png")
