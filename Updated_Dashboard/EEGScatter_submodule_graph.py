from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
from EEGArray import EEGArray
import random as r
import numpy as np
from GetCmapValues import getCmapByFreqVal

class EEG_Graph_Submodule():
    # initialize attributes of EEGmodule class
	#def __init__(self, *args, **kwargs):
	def __init__(self):
		pg.setConfigOption("background", "k")  # graph background color
		pg.setConfigOption("foreground", "w")  # graph foreground color
		pg.setConfigOption("antialias", True)
		# have EEGmodule inherit attributes of QGroupBox
		#super(QGroupBox, self).__init__(*args, **kwargs)

		#making a plotWidgetMain to show scatter plot item in
		self.plotWidgetMain = pg.PlotWidget()
		#self.layout = QHBoxLayout()
		
		#self.plotWidgetMain.getViewBox().setGeometry(0,0,300,300)
		#self.setGeometry(0,0,300,300)
		#self.resize(300,300)
		#setting up so that a plotITEM can be added
		pg.setConfigOption('leftButtonPan', False)

		#creating the plot
		self.node_scatter_graph = pg.ScatterPlotItem(pxMode=False)
		self.plotWidgetMain.addItem(self.node_scatter_graph)
		#self.plotWidgetMain.sigClicked.connect(self.clicked)
		#get the node positions
		x,y,nodeList = EEGArray()
		self.spots = []
		self.value = []
		#initialize the spots as blue
		for i in range(len(x)):
			self.spots.append({'pos' : (x[i], y[i]), 'size': .35,  'pen':{'width':-1},'brush':pg.mkBrush(0,0,255)})
			self.value.append(0)
		self.node_scatter_graph.addPoints(self.spots)
		print(len(x))
		#hide axis
		self.plotWidgetMain.getPlotItem().hideAxis('bottom')
		self.plotWidgetMain.getPlotItem().hideAxis('left')
		
		# create layout for EEG Module
		#self.layout.addWidget(self.plotWidgetMain)

		# set layout for module
		#self.setLayout(self.layout)
		
		
		
	def update_nodes(self, colors=None, data=None):
				
		# elapsed_time = time.time() - start_time
		#print(colors)
		for i in range(len(self.spots)):
			self.spots[i]['brush'] = pg.mkBrush(colors[i]*255)
		
		
		self.value = data
		self.node_scatter_graph.clear()
		self.node_scatter_graph.setData(self.spots)
		
		
	def setGraphTitle(self, title):
		self.plotWidgetMain.setTitle(title)
		#self.setTitle(title)
		#self.setStyleSheet("EEG_Graph_Submodule{font-size:25px;}")
		

	def clicked(self, pts):
		print("clicked: %s" % pts)


		