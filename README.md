# Polly
Polly is built on top of Matplotlib that can easily generate plots charts and graphs. It could be used by academic writing and data visualization. 

## User Guide


### Plot a 2D bar graph

To plot a 2D bar graph from a csv file, simply do
```
python bar_2d.py --csv examples/2d_bar.csv
```

or you can do it in your program as easy as:
```
bar_2d.plot([58, 4, 1, 5, 13])
```

to get a quick preview and do whatever you want next.
 
The result looks like:
![2D Bar Sample](examples/2d_bar.png)

### Plot a 2D Stacked bar graph

To plot a 2D bar graph from a csv file, simply do
```
python 2d_stacked_bar.py --csv examples/2d_stacked_bar.csv
```

or you can do it in your program as easy as:
```
2d_stacked_bar.plot([[58, 70, 86, 115, 169],
					  20, 50, 60, 70, 120],
					  10, 10, 20, 30, 40]])
```

The result is as follows:
![2D Stacked Bar Sample](examples/2d_stacked_bar.png)

### Plot a 3D Bar Graph

To plot a 3D bar graph from a csv file, simply do
```
python 3dbar.py --csv examples/3d_bar.csv
```

or you if you have your *axes* object and params ready in your program, you can use
```
3dbar.plot(params)
```

The result is as follows: (2 graphs of different angles will be generated so that you have the best view.
![3D Bar Sample](examples/3d_bar_2.png)

### Plot a 3D Surface Graph

To plot a 3D surface graph from a csv file, simply do
```
python surface_3d.py --csv examples/3d_surface_sample.csv
```

or you if you have your *axes* object and params ready in your program, you can use
```
surface_3d.plot(data)
```

The result looks like: 
![3D Surface Sample](examples/3d_surface_2.png)

### Others

For more options for above commands, simply use *-h* or *--help* option when running the commands.

**TODO**: 

- complete a param list with default values.
- put output format in args
- figure out what should be put in args, what should be in params
    - For now I think graph-type-specific parameters should be kept in params, e.g. the data 
    - Other general stuff should be in args, e.g. the output format, location, etc.
- need support for 3d surface, heatmap, etc

