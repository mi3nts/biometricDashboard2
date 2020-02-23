from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *

from EEGArray import EEGArray

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pyqtgraph.ptime as ptime

import random as r
import numpy as np



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
        #layout.addWidget(respirationModule(), 1, 0)
        #layout.addWidget(temperatureModule(), 1, 1)

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

        # create layout for EEG Module
        self.layout = QHBoxLayout()
        # add a simple label widget to layout
        self.layout.addWidget(QLabel("EEG Module goes here"))
        #self.layout.addWidget(EEGmontage())
        self.layout.addWidget(QLabel(""))
        self.layout.addWidget(PyQtGraphObject())

        # set layout for module
        self.setLayout(self.layout)

# create class to contain a widget created using pyqtgraph

class PyQtGraphObject(QGroupBox):

    # initialize attributes of EEGmodule class
	def __init__(self, *args, **kwargs):
        # have EEGmodule inherit attributes of QGroupBox
		super(QGroupBox, self).__init__(*args, **kwargs)
		
		
		#making a view to show scatter plot item in
		self.view = pg.GraphicsLayoutWidget()
		self.layout = QHBoxLayout()
		#setting up so that a plotITEM can be added
		self.widget1 = self.view.addPlot()
		#creating the plot
		self.scatter1 = pg.ScatterPlotItem(pxMode=False)
		
		#get the node positions
		x,y,nodeList = EEGArray()
		#create spots
		self.spots = []
		for i in range(len(x)):
			self.spots.append({'pos' : (x[i], y[i]), 'size': .1,  'brush':pg.mkBrush(self.setNodeColor())})
		self.scatter1.addPoints(self.spots)
		self.widget1.addItem(self.scatter1)
		
		#setting up timer
		self.timer = QTimer(self)
		self.timer.setInterval(50)
		self.timer.timeout.connect(self.update_nodes)
		self.timer.start()
		
        # create layout for EEG Module
		self.layout.addWidget(self.view)
		#self.layout.resize(400,200)

        # set layout for module
		self.setLayout(self.layout)
		
	def update_nodes(self):
		for i in range(len(self.spots)):
			self.spots[i]['brush'] = pg.mkBrush(r.randint(0,254),r.randint(0,254),r.randint(0,254))
			self.scatter1.setData(self.spots)
			
	def setNodeColor(self):
		return QColor(r.randint(0,254),r.randint(0,254),r.randint(0,254))
		

# create a class to contain image of eeg montage

			


	
	
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
