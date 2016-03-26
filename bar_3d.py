import csv
import sys
import numpy as np
import polly

__author__ = "Shang Li"


class Bar3D(polly.Polly3D):
    def parse_csv(self, csv_name):
        """
        There are something fundamentally different about 3d graph...
        xpos, ypos, zpos are starting point of a bar
        dx, dy, dz are the dimension of a bar
        :param csv_name:
        :return:
        """
        with open(csv_name) as f:
            csv_reader = csv.reader(f)
            meta_info = csv_reader.next()
            if meta_info:
                self.params.update({"title": meta_info[0]})
            x_meta = csv_reader.next()
            self.params.update({"xlabel": x_meta[0]})
            self.params.update({"xticks": x_meta[1:]})
            y_meta = csv_reader.next()
            self.params.update({"ylabel": y_meta[0]})
            self.params.update({"yticks": y_meta[1:]})
            z_meta = csv_reader.next()
            self.params.update({"zlabel": z_meta[0]})
            data = []
            for line in csv_reader:
                data.append(map(float, line))  # Convert to float instead of int
                # TODO maybe throw an exception if cannot convert?
            self.params.update({"data": data})

    def plot(self):
        xticks = self.set_x_axis()
        xticks = np.array(xticks)
        yticks = self.set_y_axis()
        yticks = np.array(yticks)
        x_pos, y_pos = np.meshgrid(xticks, yticks)
        x_pos = x_pos.flatten() - 0.25
        y_pos = y_pos.flatten() - 0.25
        z_pos = np.zeros(len(xticks)*len(yticks))
        data = self.params["data"]
        data = np.array(data)
        data = data.flatten()
        dx = 0.5*np.ones_like(z_pos)
        dy = dx.copy()
        colors = self.color_base[0:len(xticks)]
        colors *= len(yticks)
        self.ax.bar3d(x_pos, y_pos, z_pos, dx, dy, data, color=colors, edgecolor="none", alpha=0.8)
        self.ax.set_zlabel(self.params["zlabel"])
        return


def plot(*args, **params):
    if len(args) == 1:  # only support data for now
        if isinstance(args[0], list):
            bar_3d = Bar3D(data=args[0])
            bar_3d.plot()
            bar_3d.fig.show()
    else:
        bar_3d = Bar3D(**params)
        bar_3d.plot()
        bar_3d.fig.show()


def plot_and_save(params, **kwargs):
    bar_3d = Bar3D(**params)
    bar_3d.plot_and_save(**kwargs)


def parse_plot_save(f_name, out_dir, graph_format):
    bar_3d = Bar3D()
    kwargs = {
        "output_dir": out_dir,
        "output_format": graph_format
    }
    bar_3d.parse_plot_save(f_name, **kwargs)


if __name__ == "__main__":
    file_list, out_dir, graph_format = polly.parse_argv(sys.argv[1:])  # first element is this file...
    for each_file in file_list:
        parse_plot_save(each_file, out_dir, graph_format)
