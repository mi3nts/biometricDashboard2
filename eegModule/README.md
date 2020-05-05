# EEG Module
The EEG Module uses scatter plots to dipsplay the array of electrodes of the EEG device.  
## Prerequisites
Needed packages:
- PyQt5
- pyqtgraph
- pylsl
- numpy

## Execution
Run this module with
```
py 
```

## EEGScatterWidget_Main.py
Within the EEGScatterWidget_main, the 3 graphs for the Alpha, Delta, and Theta bands are created, using EEGScatter_submodule_graph as the base of the graphs. The Main module also creates the colormap and gradient used for the coloring of the nodes. This file sets up the display for the submodule and allows for each graph individually be added or the whole premade layout to be added.

This file also pulls data from the pylsl data stream to update the plots.
## EEGScatter_submodule_graph.py
Using pyqtgraph, the file creates a scatter plot plot widget and creates each node, with each node being independent within the graph. The axis are hidden. The update nodes fucntion takes a colorlist array (numpy array) and sets the colors in the array to the corresponding node.
## GetCmapValues.py
getCmapByFreqVal: For a given frequency value, the function calls the fourier transform on the current sample of data and computes the cmap value for that sample of data based on the power value. getCmapForZscores: Exactly the same as getCmapByFreqVal but computes the zscore value and uses that in the cmap.
## SelectFrequency.py
Returns a numpy array of values that correspond to the selected frequency band.
## GradientBox.py
A pyqtgraph GradientWidget is passed to this class, and returns a groupbox that contains 4 text QLabels and a QLabel that has the gradient as a pixmap.


#### On the list
- Add hover events to display node name and z_score value
