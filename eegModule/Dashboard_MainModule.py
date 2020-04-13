from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap

from pylsl import StreamInlet, resolve_stream
from EEGScatterWidget_main import *

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
		layout.addWidget(EEGmodule_main(), 0, 0, 10, 4)
		layout.addWidget(pg.GraphicsLayoutWidget(), 0, 4, 10, 8)

		# add layout to window Widget
		widget.setLayout(layout)

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