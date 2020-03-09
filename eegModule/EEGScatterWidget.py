from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *

from EEGArray import EEGArray
from GetCmapValues import getCmapByFreqVal
from pylsl import StreamInlet, resolve_stream
from pyqtgraph import PlotWidget, plot
# from PyQtAlphaFrequency import AlphaFrequencyPG
# from PyQtThetaFrequency import ThetaFrequencyPG
from EEGScatter import EEGGraph

import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import matplotlib.cm as cm
import matplotlib.colors as colors

import csv
import random as r
import numpy as np
import scipy.signal as sps
import socketserver
import sys
import time

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # set title of application window
        self.setWindowTitle("Biometric Dashboard")
		
        # # resize main window
        self.resize(1600, 1200)

        # create a window widget for main window
        widget = QWidget()

        # define a layout for window
        layout = QGridLayout()

        # add all modules to MainWindow where EEG module takes up 1 row and 2
        # columns and sits in the top left grid box. The respiration module sits
        # in the bottom left grid box. The temperature module sits in the bottom
        # right grid box.
        layout.addWidget(EEGmodule(), 0, 0, 1, 2)
        layout.addWidget(pg.GraphicsLayoutWidget(), 1, 0)
        #layout.addWidget(DeltaFrequencyPG(), 1, 1)

        # add layout to window Widget
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

        # change window style to dark mode
        darkMode()

# create class to contain EEG module

class EEGmodule(QGroupBox):
    # initialize attributes of EEGmodule class
	def __init__(self, *args, **kwargs):
		# have EEGmodule inherit attributes of QGroupBox
		super(QGroupBox, self).__init__(*args, **kwargs)

		# set title of EEGmodule
		self.setTitle("EEG Module")


		self.test = 5
		# create layout for EEG Module
		self.layout = QHBoxLayout()
		
		#Creating graphs 
		self.alpha=EEGGraph()
		self.alpha.setGraphTitle("Alpha Band")
		self.alphaBand = -3
		
		self.theta=EEGGraph()
		self.theta.setGraphTitle("Theta Band")
		self.thetaBand = -2
		
		self.delta=EEGGraph()
		self.delta.setGraphTitle("Delta Band")
		self.deltaBand = -1
		
		# add a simple label widget to layout
		self.layout.addWidget(self.delta)
		self.layout.addWidget(self.theta)
		self.layout.addWidget(self.alpha)
	
		# set layout for module
		self.setLayout(self.layout)
		
		
		#get the node positions
		x,y,nodeList = EEGArray()
		#set cmap
		self.cmap = cm.get_cmap("jet")		
		colormap = []
		posi=[]
		
		for  i in range(self.cmap.N):
			colormap.append( self.cmap(i))
			posi.append(i/self.cmap.N)
			if i == self.cmap.N-1:
				posi[i-1]=1
				
		for i in range(len(colormap)):
			lst = list(colormap[i])
			lst[0] = lst[0]*255
			lst[1] = lst[1]*255
			lst[2] = lst[2]*255
			lst[3] = lst[3]*255
			colormap[i] = tuple(lst)
		print(colormap)
		self.pgCM = pg.ColorMap(pos = posi, color = colormap, mode='float')
		# define number of electrodes
		self.n = 64		
		#initialize newdata
		self.newdata = np.zeros(self.n)		
		
		#initialize 64 by 64 data array
		self.data = np.zeros((self.n,self.n))
		
		#get global max for normalization
		self.aglobalMax = -(sys.maxsize)-1
		self.tglobalMax = -(sys.maxsize)-1
		self.dglobalMax = -(sys.maxsize)-1
		
		#Open StreamInlet
		print("looking for an EEG stream...")
		self.streams = resolve_stream()
		
		self.inlet = StreamInlet(self.streams[0])
		
		
		# self.view = pg.GraphicsItem()
		# gradientItem = pg.GradientItemEditor()
		# self.view.addItem(self.Colormap.getGradient().setOrientation('right'))
		# self.layout.addWidget(self.view)
		
		
		
		#create timer
		self.timer = QTimer(self)
		#self.timer.setInterval(10000)
		self.timer.timeout.connect(self.PullData)
		self.timer.start(20)
		
		self.count = 0
		
	
		
		
	def PullData(self):
		
		
		starttime=time.time()
		
		self.count= self.count+1
		# if self.count == 50:
			# self.inlet = StreamInlet(self.streams[0])
		
		#pull data
		sample = self.inlet.pull_sample()
		self.newdata = np.asarray(sample[0][:self.n])
		#print(timestamp)
		
		for i in range(4):
			if i == 1:
				temp, self.dglobalMax, self.data = getCmapByFreqVal(self.data, self.newdata, self.deltaBand, self.dglobalMax)
				#set colors
				
				acolors = self.pgCM.map(temp)#self.CM.map(temp, mode='byte')
				self.delta.update_nodes(colors=acolors)
				
			if i == 2:
				temp, self.tglobalMax, self.data = getCmapByFreqVal(self.data, self.newdata, self.thetaBand, self.tglobalMax)
				#set colors
				bcolors = self.pgCM.map(temp)#self.CM.map(temp, mode='byte')
				self.theta.update_nodes(colors=bcolors)
			
			if i == 3:
				temp, self.aglobalMax, self.data = getCmapByFreqVal(self.data, self.newdata, self.alphaBand, self.aglobalMax)
				#set colors
				ccolors =self.pgCM.map(temp)#self.CM.map(temp, mode='byte')
				self.alpha.update_nodes(colors=ccolors)				
			
		elapsed = time.time()-starttime	
		self.timer.setInterval(elapsed*100)
		#set onlclickhover to show power and node label
			
		
		
				
		
# create class to contain a widget created using pyqtgraph

	
# function to change application style to dark mode
def darkMode():
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.black)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    QApplication.setPalette(dark_palette)

# run application
if __name__ == '__main__':
    import sys

    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication(sys.argv)
    # create a window from the MainWindow class defined above
    window = MainWindow()
    # show the window
    window.show()
    # Start the event loop.
    sys.exit(app.exec_())
	
