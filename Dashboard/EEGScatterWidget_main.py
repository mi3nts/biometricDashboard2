from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap

from EEGArray import EEGArray
from GetCmapValues import getCmapByFreqVal, getCmapForZscores
from pylsl import StreamInlet, resolve_stream
from pyqtgraph import PlotWidget, plot
# from PyQtAlphaFrequency import AlphaFrequencyPG
# from PyQtThetaFrequency import ThetaFrequencyPG
from EEGScatter_submodule_graph import EEG_Graph_Submodule
from MatPlotLibCmapToPyQtColorMap import cmapToColormap
from GradientBox import gradientLayout

import pyqtgraph as pg
import pyqtgraph.ptime as ptime
from matplotlib import cm
import matplotlib.colors as colors

import random as r
import numpy as np
import scipy.signal as sps
import socketserver
import sys
import time


class CmapImage(QWidget):
	def __init__(self):
		super().__init__()

		self.im = QPixmap("./jet.png")
		self.rotation = 90
		self.im = self.im.transformed(
			QTransform().rotate(self.rotation), Qt.SmoothTransformation
		)
		self.label = QLabel("Frequencies")
		self.title = QLabel("Power (Normalized Frequencies)")
		self.title.setAlignment(Qt.AlignCenter)
		self.im = self.im.scaled(300, 350, Qt.KeepAspectRatio, Qt.FastTransformation)
		self.label.setPixmap(self.im)
		self.label.setScaledContents(True)
		self.grid = QGridLayout()
		self.grid.addWidget(self.label, 0, 1)
		self.setLayout(self.grid)

		# self.setGeometry(100, 100, 800, 300)

		# self.setWindowTitle("PyQT show image")
		self.show()


# create class to contain EEG module
class EEGmodule_main(QGroupBox):
    # initialize attributes of EEGmodule class
	def __init__(self, inlet):
		# have EEGmodule inherit attributes of QGroupBox
		pg.setConfigOptions(antialias=True)
		super(QGroupBox, self).__init__()
		self.inlet = inlet
		# set title of EEGmodule
		# self.setTitle("EEG Module")
		# create layout for EEG Module
		self.layout = QGridLayout()
		# set layout for module
		self.setLayout(self.layout)
		

		# Creating graphs
		self.alphaGraph = EEG_Graph_Submodule()
		self.alphaGraph.setGraphTitle(
			'<span style="color:white;font-size:20px">Alpha Band (8-12Hz)</span>'
		)
		self.alphaBand = -3
		self.alphaG = self.alphaGraph.plotWidgetMain
		
		######################################
		self.thetaGraph = EEG_Graph_Submodule()
		self.thetaGraph.setGraphTitle(
			'<span style="color:white;font-size:20px">Theta Band (4-7Hz)</span>'
		)
		self.thetaBand = -2
		self.thetaG = self.thetaGraph.plotWidgetMain
		
		######################################
		self.deltaGraph = EEG_Graph_Submodule()
		self.deltaGraph.setGraphTitle(
			'<span style="color:white;font-size:20px">Delta Band (0-4Hz)</span>'
		)
		self.deltaG = self.deltaGraph.plotWidgetMain
		self.deltaBand = -1
		
		#######################################

		# checkbox for alphaGraph
		self.alphaBox = QCheckBox("Alpha Band", self)
		self.alphaBox.setStyleSheet("QCheckBox{color:white;}")
		self.alphaBox.setChecked(True)
		self.alphaBox.stateChanged.connect(lambda: self.hideGraph(button=self.alphaBox))
		###################################################
		self.thetaBox = QCheckBox("Theta Band", self)
		self.thetaBox.setStyleSheet("QCheckBox{color:white;}")
		self.thetaBox.setChecked(True)
		self.thetaBox.stateChanged.connect(lambda: self.hideGraph(button=self.thetaBox))
		self.thetaBox.move(100, 0)
		###################################################
		self.deltaBox = QCheckBox("Delta Band", self)
		self.deltaBox.setStyleSheet("QCheckBox{color:white;}")
		self.deltaBox.setChecked(True)
		self.deltaBox.stateChanged.connect(lambda: self.hideGraph(button=self.deltaBox))
		self.deltaBox.move(200, 0)
		###################################################	
		
		
		#######################################################
		#add check boxes to layout
		self.layout.addWidget(self.alphaBox,1,4)
		self.layout.addWidget(self.deltaBox,1,0)
		self.layout.addWidget(self.thetaBox,1,2)
		# add graphs to widget
		self.layout.addWidget(self.deltaG, 2, 0, 1, 2)
		self.layout.addWidget(self.thetaG, 2, 2, 1, 2)
		self.layout.addWidget(self.alphaG, 2, 4, 1, 2)
		
		#self.layout.addWidget(CmapImage(), 3, 2, 1, 2)
		# = QLabel("Normalized Power")
		#label.setStyleSheet("QLabel{color:white; font:20px;}")
		#self.layout.addWidget(label, 3, 1, 1,1)
		
		fill = pg.PlotWidget()
		fill.getPlotItem().hideAxis("bottom")
		fill.getPlotItem().hideAxis("left")
		fill.setBackground(background=None)
		self.layout.addWidget(fill, 4,0,1,6)
		
		# get the node positions
		x, y, nodeList = EEGArray()

		# set cmap
		colormap = cm.get_cmap("jet") #getting colormap from matplotlib
		colormap._init()
		lut = (colormap._lut * 255).view(np.ndarray) #convert to numpy array
		ticks = []
		colors = []
		# pos = []
		# mapColors = []
		self.gradient = pg.GradientWidget(allowAdd=False)	
		for i in range(len(lut)-3):	#adding colors to a gradient
			r=int(lut[i][0])
			g=int(lut[i][1])
			b=int(lut[i][2])
			a=255
			ticks.append(i/255)
			colors.append((r,g,b,a))
			# pos.append(i/255)
			# mapColors.append((r,g,b,a))
			if i%15 == 0:
				self.gradient.addTick(x=ticks[i], color=QColor(r,g,b,a), movable=False)
			
				if i == 0:
					self.gradient.setTickColor(0,QColor(r,g,b,a))
				elif i == 255:
					self.gradient.addTick(1,QColor(r,g,b,a))
		
		
		
		#self.pgCM = pg.ColorMap(np.array(ticks), colors)
		self.pgCM = self.gradient.colorMap()
		# self.layout.addWidget(self.gradient, 3, 4, 1, 2)
		##########################################################################
		#creating a groupbox for the gradient and labels
		self.gradientBox = gradientLayout(self.gradient)
		#####################################
		self.layout.addWidget(self.gradientBox, 3,0,1,8)
		##########################################################################
		
		
		
		self.n = 64
		# initialize newdata
		self.newdata = np.zeros(self.n)
		# initialize 64 by 64 data array
		self.data = np.zeros((self.n, self.n))
		# get global max for normalization
		self.aglobalMax = -(sys.maxsize) - 1
		self.tglobalMax = -(sys.maxsize) - 1
		self.dglobalMax = -(sys.maxsize) - 1

		# Open StreamInlet
		self.setLayout(self.layout)
		# create timer
		# self.timer = QTimer(self)
		# # self.timer.setInterval(10000)
		# self.timer.timeout.connect(self.UpdateNodes)
		# self.timer.start(20)
		output = open('output.txt', 'w')
		output.close()
		

	def UpdateNodes(self, sample ):
		output = open('output.txt', 'a')
		# pull data
		# sample = self.inlet.pull_sample()
		self.newdata = np.asarray(sample[0][: self.n])
		# print(timestamp)
		
		for i in range(4):
			if i == 1:
				temp, self.data = getCmapForZscores(
					self.data, self.newdata, self.deltaBand
				)
				# set colors
				acolors = self.pgCM.map(temp)
				#print(temp)
				self.deltaGraph.update_nodes(colors=acolors)
				
			if i == 2:
				temp,  self.data = getCmapForZscores(
					self.data, self.newdata, self.thetaBand
				)
				# set colors
				bcolors = self.pgCM.map(temp)
				self.thetaGraph.update_nodes(colors=bcolors)
				

			if i == 3:
				temp,  self.data = getCmapForZscores(
					self.data, self.newdata, self.alphaBand
				)
				# set colors
				ccolors = self.pgCM.map(temp)
				self.alphaGraph.update_nodes(colors=ccolors)
				print(ccolors[1], " alpha color", file = output)
				print(temp[1], file = output)
			#print(acolors[30], " " , bcolors[10], " ", ccolors[60], file = output)
		output.close()
		# elapsed = time.time()-starttime
		# self.timer.setInterval(elapsed*100)
		# set onlclickhover to show power and node label

	def hideGraph(self, button=None):
		#fill widgets
		fill_1 = pg.PlotWidget()
		fill_1.setBackground(None)
		fill_1.getPlotItem().hideAxis("bottom")
		fill_1.getPlotItem().hideAxis("left")
		fill_2 = pg.PlotWidget()
		fill_2.setBackground(None)
		fill_2.getPlotItem().hideAxis("bottom")
		fill_2.getPlotItem().hideAxis("left")
		fill_3 = pg.PlotWidget()
		fill_3.getPlotItem().hideAxis("left")
		fill_3.getPlotItem().hideAxis("bottom")
		fill_3.setBackground(None)

		if button.isChecked() == False:
			if button.text() == "Alpha Band":
				self.layout.addWidget(fill_1, 2, 4, 1, 2)
				self.layout.removeWidget(self.alphaG)
				self.alphaG.setParent(None)
				

			if button.text() == "Theta Band":
				self.layout.addWidget(fill_2, 2, 2, 1, 2)
				self.layout.removeWidget(self.thetaG)
				self.thetaG.setParent(None)
				

			if button.text() == "Delta Band":
				self.layout.addWidget(fill_3, 2, 0, 1, 2)
				self.layout.removeWidget(self.deltaG)
				self.deltaG.setParent(None)
				
		else:
			if button.text() == "Alpha Band":
				self.layout.addWidget(self.alphaG, 2, 4, 1, 2)
				self.layout.removeWidget(fill_1)
				fill_1.setParent(None)
				
			if button.text() == "Theta Band":
				self.layout.addWidget(self.thetaG, 2, 2, 1, 2)
				self.layout.removeWidget(fill_2)
				fill_2.setParent(None)
				
			if button.text() == "Delta Band":
				self.layout.addWidget(self.deltaG, 2, 0, 1, 2)
				self.layout.removeWidget(fill_3)
				fill_3.setParent(None)
				
