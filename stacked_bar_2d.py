import csv
import sys
import polly

__author__ = "Shang Li"


class StackedBar2D(polly.Polly):
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
            data = []
            stacks = []
            for line in csv_reader:
                stacks.append(line[0])
                data.append(self.map_data(line[1:]))  # Convert to float instead of int
            self.params.update({"data": data})
            self.params.update({"stacks": stacks})
            
    def plot(self):
        xticks = self.set_x_axis()
        self.set_y_axis()
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        data = self.get_data(self.params["data"])
        offset = [0]*len(data[0])
        handles = []  # TODO doesn't seem to need this handles?
        index = 0
        for data_row in data:
            bars = self.ax.bar(xticks, height=data_row, bottom=offset,
                               color=self.color_base[index], align="center", edgecolor="none")
            offset = map(sum, zip(data_row, offset))  # Add this row to prepare the offset for next row
            handles.append(bars[0])
            index += 1
        for each_bar, height in zip(bars, offset):
            self.ax.text(each_bar.get_x()+each_bar.get_width()/2,  # text x pos
                         1.05*height,                              # text y pos
                         '%.1f' % float(height),                   # 1 digit enough?
                         ha='center', va='bottom')
        self.ax.set_title(self.params["title"])
        self.ax.legend(handles, self.params["stacks"], loc="best")


def plot(*args, **params):
    if len(args) == 1:  # only support data for now
        if isinstance(args[0], list):
            stacked_bar = StackedBar2D(data=args[0])
            stacked_bar.plot()
            stacked_bar.fig.show()
    else:
        stacked_bar = StackedBar2D(**params)
        stacked_bar.plot()
        stacked_bar.fig.show()


def plot_and_save(params, **kwargs):
    stacked_bar = StackedBar2D(**params)
    stacked_bar.plot_and_save(**kwargs)


def parse_plot_save(f_name, **kwargs):
    stacked_bar = StackedBar2D()
    stacked_bar.parse_plot_save(f_name, **kwargs)

if __name__ == "__main__":
    file_list, kwargs = polly.parse_argv(sys.argv[1:])  # first element is this file...
    for each_file in file_list:
        parse_plot_save(each_file, **kwargs)
