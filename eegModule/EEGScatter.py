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

#setting up timer
		# self.timer = QTimer(self)
		# self.timer.setInterval(100)
		# self.timer.timeout.connect(self.update_nodes)
		# self.timer.start()

class EEGGraph(QGroupBox):
    # initialize attributes of EEGmodule class
	def __init__(self, *args, **kwargs):
		# have EEGmodule inherit attributes of QGroupBox
		super(QGroupBox, self).__init__(*args, **kwargs)
		
		#neded variable
		
		#making a view to show scatter plot item in
		self.view = pg.PlotWidget()
		self.layout = QHBoxLayout()
		
		#setting up so that a plotITEM can be added
		pg.setConfigOption('leftButtonPan', False)
		
		#creating the plot
		self.scatter1 = pg.ScatterPlotItem(pxMode=False)
		self.view.addItem(self.scatter1)
		#self.view.sigClicked.connect(self.clicked)
		#get the node positions
		x,y,nodeList = EEGArray()
		
		self.setGeometry(0,0, 100,100)
		
		self.spots = []
		for i in range(len(x)):
			self.spots.append({'pos' : (x[i], y[i]), 'size': .35,  'pen':{'width':-1},'brush':pg.mkBrush(0,0,255)})
		self.scatter1.addPoints(self.spots)
		
		#hide axis
		self.view.getPlotItem().hideAxis('bottom')
		self.view.getPlotItem().hideAxis('left')
		
		# #setting up timer
		# self.timer = QTimer(self)
		# self.timer.setInterval(100)
		# self.timer.timeout.connect(self.update_nodes)
		# self.timer.start()
		
		# create layout for EEG Module
		self.layout.addWidget(self.view)
		#self.layout.resize(400,200)

		# set layout for module
		self.setLayout(self.layout)
		
	def update_nodes(self, colors=None):
				
		# elapsed_time = time.time() - start_time
		#print(colors)
		for i in range(len(self.spots)):
			self.spots[i]['brush'] = pg.mkBrush(colors[i]*255)
		self.scatter1.clear()
		self.scatter1.setData(self.spots)
		
		
		
	def setGraphTitle(self, title):
		self.view.setTitle(title)
		

	def clicked(self, pts):
		print("clicked: %s" % pts)