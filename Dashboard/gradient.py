from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap

from EEGArray import EEGArray
from GetCmapValues import getCmapByFreqVal
from pylsl import StreamInlet, resolve_stream
from pyqtgraph import PlotWidget, plot

# from PyQtAlphaFrequency import AlphaFrequencyPG
# from PyQtThetaFrequency import ThetaFrequencyPG
from EEGScatter_submodule_graph import EEG_Graph_Submodule
from MatPlotLibCmapToPyQtColorMap import cmapToColormap

import pyqtgraph as pg
# from pyqtgraph import *
import pyqtgraph.ptime as ptime
from matplotlib import cm
import matplotlib.colors as colors


class Gradient():
	def __init__(self, colors, ticks):
		self.gradient = pg.GradientEditorItem()
		for pos in range(len(ticks)):
			self.gradient.addTick(x=ticks[pos],color=colors[pos], movable=False)
	