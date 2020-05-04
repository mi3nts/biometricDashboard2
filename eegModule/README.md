# EEG Module
The EEG Module uses scatter plots to dipsplay the array of electrodes of the EEG device. 
## EEGScatterWidget_Main
Within the EEGScatterWidget_main, the 3 graphs for the Alpha, Delta, and Theta bands are created, using EEGScatter_submodule_graph as the base of the graphs. The Main module also creates the colormap and gradient used for the coloring of the nodes.
## GetCmapValues.py
getCmapByFreqVal: For a given frequency value, the function calls the fourier transform on the current sample of data and computes the cmap value for that sample of data based on the power value. getCmapForZscores: Exactly the same as getCmapByFreqVal but computes the zscore value and uses that in the cmap.
