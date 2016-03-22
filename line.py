import csv
import sys
import numpy as np
from matplotlib import pyplot
import polly

y_1 = [[0.0003, 0.0053, 0.0863, 1.9041],
       [0.0001, 0.0014, 0.0230, 0.3702],
       [0.0001, 0.0006, 0.0054, 0.0713],
       [0.0014, 0.0062, 0.0360, 0.3750],
       [0.0000, 0.0000, 0.0004, 0.0109]]
y_5 = [
    [0, 0.1, 0.5, 3.4, 23.7, 210.2, 1673.3, 12420.3],
    [0.0,  0.1,  1.0,  7.4, 58.8,  497.4, 3926.2, 30844.9],
    [0.0,  0.1,  0.7,  4.8, 38.5,  305.6, 2451.5, 19303.4],
    [0.0,  0.1,  0.5,  3.5, 28.8,  226.8, 1793.1, 14104.8],
    [0.0,  0.1,  0.4,  3.2, 25.6,  199.9, 1543.1, 11913.1],
    [0.0,  0.1,  0.4,  3.1, 25.1,  196.2, 1508.6, 11450.8],
    [0.0,  0.1,  0.4,  3.0, 24.4,  190.3, 1503.2, 11308.4],
    [0.0,  0.1,  0.3,  3.0, 24.1,  200.2, 1596.9, 11506.2],
    [0.0,  0.1,  0.3,  2.3, 24.0,  203.7, 1621.1, 11917.6],
]

fig, ax = pyplot.subplots(1, 1)
markers = [".", "s", "o", "x", "+", "d", ",", "v", "h"]
x_ticks = np.arange(len(y_1[0]))
x_tick_labels = ["64", "256", "1024", "4096"]
x_title = "Matrix Size"
y_title = "log10(Time)"
legend_list = ["Access by rows",
               "Access by columns",
               "Vectorial colunm",
               "Vectorial row",
               "Matlab BLAS"]
legend_list_5 = ["no block",
                 "block=2",
                 "block=4",
                 "block=8",
                 "block=16",
                 "block=32",
                 "block=64",
                 "block=128",
                 "block=256",]
x_ticks_5 = np.arange(len(y_5[0]))
x_tick_labels_5 = ["16", "32", "64", "128", "256", "512", "1024", "2048"]
ax.set_xlabel(x_title)
ax.set_xticks(x_ticks_5)
ax.set_xticklabels(x_tick_labels_5)
ax.set_ylabel(y_title)
cnt = 0
for y in y_5:
    ax.plot(x_ticks_5, np.log10(y), linewidth=2, marker=markers[cnt])
    cnt += 1
ax.legend(legend_list_5, loc='best')
fig.show()
fig.clear()
