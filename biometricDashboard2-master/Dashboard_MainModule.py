from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap

import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import matplotlib.cm
import matplotlib.colors as colors
import csv
import random as r
import numpy as np
import scipy.signal as sps
import socketserver
import sys
import time
import os

from TemperatureModule_BodyTemp import * # Body Temperature Class
from TemperatureModule_GSR import *             # GSR Class
from Thermometer import *     # Thermometer Class
from TemperatureModule_Accelerometer import *   # Accelerometer Class
from pylsl import StreamInlet, resolve_stream
from EEGScatterWidget_main import *
from RM_Graphs import *
from RM_SPO2Widget import *
from RM_HRWidget import *
# Subclass QMainWindow to customise your application's main window


class MainWindow(QMainWindow):
	def __init__(self, inlet):
		super(MainWindow, self).__init__()

		# set title of application window
		self.setWindowTitle("Biometric Dashboard")
		# # resize main window
		self.resize(1600, 1200)
		# create a window widget for main window
		widget = QWidget()

		# define a layout for window
		layout_window = QGridLayout()
		layout_eeg = QVBoxLayout()
		layout_numbers = QGridLayout()
		layout_graphs = QGridLayout()

		#setting up widgets
		spo2 = SpO2_Mod(inlet)	#spo2 widget
		ppg = PPG_Graph(inlet)  # PPG Graph
		hrw = HR_Module(inlet)  # HR Widget
		ecgraph = ECG_Graph(inlet)  # ECG Graph
		rgraph = Resp_Graph(inlet)  # Respiratory Graph
		eegModule = EEGmodule_main(inlet) #EEG module
		thermometer = Thermometer()
		bt = TemperatureModule_BodyTemp(thermometer, inlet) 
		gsr = TemperatureModule_GSR(inlet)
		acc = TemperatureModule_Accelerometer(inlet)

		#add the layout widget into the window
		layout_eeg.addWidget(eegModule)
		#the non-graph widgets, HR, temperature, SP02
		layout_numbers.addWidget(spo2.SpO2_Widget, 0, 0)
		layout_numbers.addWidget(hrw.HR_Widget, 0, 1)
		##Add the temperature

		#Adding graphs to layout
		layout_graphs.addWidget(ecgraph.ECG_Graph,0,0)
		layout_graphs.addWidget(ppg.PPG_Graph,1,0)
		layout_graphs.addWidget(rgraph.Resp_Graph, 2, 0)
		layout_graphs.addWidget(bt.graphWidget, 3,0)
		layout_graphs.addWidget(gsr.graphWidget, 4, 0)

		# add all modules to MainWindow where EEG module takes up 1 row and 2
		# columns and sits in the top left grid box. The respiration module sits
		# in the bottom left grid box. The temperature module sits in the bottom
		# right grid box.
		layout_window.addLayout(layout_eeg,0, 0, 10, 1)
		layout_window.addLayout(layout_numbers,0,1,4,3)
		layout_window.addLayout(layout_graphs, 1,1,6,3)

		# add layout to window Widget
		widget.setLayout(layout_window)
		# Set the central widget of the Window. Widget will expand
		# to take up all the space in the window by default.
		self.setCentralWidget(widget)

		# change window style to dark mode
		darkMode()
		

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

def getStream():
	print("looking for an EEG stream...")
	streams = resolve_stream()
	inlet = StreamInlet(streams[0])
	return inlet
	
	
# run application
if __name__ == '__main__':
	import sys
	inlet = getStream()
	# You need one (and only one) QApplication instance per application.
	# Pass in sys.argv to allow command line arguments for your app.
	# If you know you won't use command line arguments QApplication([]) works too.
	app = QApplication(sys.argv)
	# create a window from the MainWindow class defined above
	window = MainWindow(inlet)
	# show the window
	window.show()
	# Start the event loop.
	sys.exit(app.exec_())