import csv
import sys
import numpy as np
from matplotlib import cm
import polly

__author__ = "Shang Li"


class Surface3D(polly.Polly3D):
    def parse_csv(self, csv_name):
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
            self.params.update({"data": data})
        return self.params

    def plot(self):
        xticks = self.set_x_axis()
        yticks = self.set_y_axis()
        x_pos, y_pos = np.meshgrid(xticks, yticks)
        data = self.get_data(self.params["data"])
        data = np.array(data)
        data = data.flatten()
        z = data.reshape(x_pos.shape)  # this is different from 3d bar, should have the same shape.
        self.ax.plot_surface(x_pos, y_pos, z, cmap=cm.coolwarm, rstride=1, cstride=1, linewidth=1)
        self.ax.set_title(self.params["title"])
        self.ax.set_zlabel(self.params["zlabel"])
        return


def plot(*args, **params):
    if len(args) == 1:  # only support data for now
        if isinstance(args[0], list):
            surface_3d = Surface3D(data=args[0])
            surface_3d.plot()
            surface_3d.fig.show()
    else:
        surface_3d = Surface3D(**params)
        surface_3d.plot()
        surface_3d.fig.show()


def plot_and_save(params, **kwargs):
    surface_3d = Surface3D(**params)
    surface_3d.plot_and_save(**kwargs)


def parse_plot_save(f_name, **kwargs):
    surface_3d = Surface3D()
    surface_3d.parse_plot_save(f_name, **kwargs)


if __name__ == "__main__":
    file_list, kwargs = polly.parse_argv(sys.argv[1:])
    for each_file in file_list:
        parse_plot_save(each_file, **kwargs)
