# Polly
Polly is a wrapper package of matplotlib that can easily generate plots charts and graphs. It could be used by academic writing and data visualization. 

## How to use it?

(currently only 2D bar and 2d stacked bar plot works, see examples)

### Plot a 2D bar graph

To plot a 2D bar graph from a csv file, simply do
```
python 2dbar.py --csv 2d_bar_sample.csv
```

or you if you have your *axes* object and params ready in your program, you can use
```
2dbar.plot(ax, params)
```

The result is as follows:
![2D Bar Sample](examples/2D_Bar.pdf)

### Plot a 2D Stacked bar graph

To plot a 2D bar graph from a csv file, simply do
```
python 2d_stacked_bar.py --csv 2d_stacked_sample.csv
```

or you if you have your *axes* object and params ready in your program, you can use
```
2d_stacked_bar.plot(ax, params)
```

To be finished...

**TODO**: 

- complete a param list with default values.
- put output format in args
- figure out what should be put in args, what should be in params
- need support for 3d surface, heatmap, etc

