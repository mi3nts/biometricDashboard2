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
from EEGScatter_submodule_graph import EEGGraph
from MatPlotLibCmapToPyQtColorMap import cmapToColormap

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
        layout.addWidget(EEGmodule_main(), 0, 0, 1, 2)
        layout.addWidget(pg.GraphicsLayoutWidget(), 1, 0)
        layout.addWidget(CmapImage(), 1, 1)

        #layout.addWidget(DeltaFrequencyPG(), 1, 1)

        # add layout to window Widget
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

        # change window style to dark mode
        darkMode()


class CmapImage(QWidget):

    def __init__(self):
        super().__init__()

        self.im = QPixmap("./jet.png")

        self.label = QLabel()
        self.im = self.im.scaled(
            300, 350, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label.setPixmap(self.im)
        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 0, 1)
        self.setLayout(self.grid)

        # self.setGeometry(100, 100, 800, 300)

        # self.setWindowTitle("PyQT show image")
        self.show()


# create class to contain EEG module
class EEGmodule_main(QGroupBox):
    # initialize attributes of EEGmodule class
    def __init__(self, *args, **kwargs):
        # have EEGmodule inherit attributes of QGroupBox
        super(QGroupBox, self).__init__(*args, **kwargs)

        # set title of EEGmodule
        self.setTitle("EEG Module")
        # create layout for EEG Module
        self.layout = QGridLayout()
        # set layout for module
        self.setLayout(self.layout)

        # Creating graphs
        self.alphaGraph = EEGGraph()
        self.alphaGraph.setGraphTitle("Alpha Band")
        self.alphaBand = -3
        ######################################
        self.thetaGraph = EEGGraph()
        self.thetaGraph.setGraphTitle("Theta Band")
        self.thetaBand = -2
        ######################################
        self.deltaGraph = EEGGraph()
        self.deltaGraph.setGraphTitle("Delta Band")
        self.deltaBand = -1
        #######################################

        # checkbox for alphaGraph
        alphabox = QCheckBox("alphaGraph band", self)
        alphabox.setChecked(True)
        alphabox.stateChanged.connect(lambda: self.hideGraph(button=alphabox))

        thetaBox = QCheckBox("Theta Band", self)
        thetaBox.setChecked(True)
        thetaBox.stateChanged.connect(lambda: self.hideGraph(button=thetaBox))
        thetaBox.move(100, 0)

        deltaBox = QCheckBox("Delta band", self)
        deltaBox.setChecked(True)
        deltaBox.stateChanged.connect(lambda: self.hideGraph(button=deltaBox))
        deltaBox.move(200, 0)

        # add a simple label widget to layout
        # self.layout.addWidget(self.deltaGraph)
        # self.layout.addWidget(self.thetaGraph)
        # self.layout.addWidget(self.alphaGraph)
        # grid
        self.layout.addWidget(self.deltaGraph, 0, 1, 1, 1)
        self.layout.addWidget(self.thetaGraph, 0, 2, 1, 1)
        self.layout.addWidget(self.alphaGraph, 0, 0, 1, 1)

        # get the node positions
        x, y, nodeList = EEGArray()

        # set cmap
        cmap = getattr(matplotlib.cm, 'jet')
        self.color_list = cmapToColormap(cmap)
        ticks = []
        colors = []
        for item in self.color_list:
            ticks.append(item[0])
            colors.append(item[1])

        self.pgCM = pg.ColorMap(pos=ticks, color=colors)
        print(type(self.pgCM))
        # define number of electrodes
        self.n = 64
        # initialize newdata
        self.newdata = np.zeros(self.n)

        # initialize 64 by 64 data array
        self.data = np.zeros((self.n, self.n))

        # get global max for normalization
        self.aglobalMax = -(sys.maxsize)-1
        self.tglobalMax = -(sys.maxsize)-1
        self.dglobalMax = -(sys.maxsize)-1

        # Open StreamInlet
        print("looking for an EEG stream...")
        self.streams = resolve_stream()

        self.inlet = StreamInlet(self.streams[0])

        # self.view = pg.GraphicsItem()
        # gradientItem = pg.GradientItemEditor()
        # self.view.addItem(self.Colormap.getGradient().setOrientation('right'))
        # self.layout.addWidget(self.view)

        # create timer
        self.timer = QTimer(self)
        # self.timer.setInterval(10000)
        self.timer.timeout.connect(self.PullData)
        self.timer.start(20)

        self.count = 0

    def PullData(self):

        starttime = time.time()

        self.count = self.count+1
        # if self.count == 50:
        # self.inlet = StreamInlet(self.streams[0])

        # pull data
        sample = self.inlet.pull_sample()
        self.newdata = np.asarray(sample[0][:self.n])
        # print(timestamp)

        for i in range(4):
            if i == 1:
                temp, self.dglobalMax, self.data = getCmapByFreqVal(
                    self.data, self.newdata, self.deltaBand, self.dglobalMax)
                # set colors
                acolors = self.pgCM.map(temp)
                self.deltaGraph.update_nodes(colors=acolors)

            if i == 2:
                temp, self.tglobalMax, self.data = getCmapByFreqVal(
                    self.data, self.newdata, self.thetaBand, self.tglobalMax)
                # set colors
                bcolors = self.pgCM.map(temp)
                self.thetaGraph.update_nodes(colors=bcolors)

            if i == 3:
                temp, self.aglobalMax, self.data = getCmapByFreqVal(
                    self.data, self.newdata, self.alphaBand, self.aglobalMax)
                # set colors
                ccolors = self.pgCM.map(temp)
                self.alphaGraph.update_nodes(colors=ccolors)

        elapsed = time.time()-starttime
        self.timer.setInterval(elapsed*100)
        # set onlclickhover to show power and node label

    def hideGraph(self, button=None):
        if button.isChecked() == False:
            if button.text() == "alphaGraph band" and button.isChecked() == False:
                self.layout.removeWidget(self.alphaGraph)
                self.alphaGraph.setParent(None)

            if button.text() == 'Delta band' and button.isChecked() == False:
                self.layout.removeWidget(self.deltaGraph)
                self.deltaGraph.setParent(None)

            if button.text() == 'Theta Band' and button.isChecked() == False:
                self.layout.removeWidget(self.thetaGraph)
                self.thetaGraph.setParent(None)
        else:
            if button.text() == "alphaGraph band":
                self.layout.addWidget(self.alphaGraph, 0, 0, 1, 1)
                # self.layout.addWidget(self.alphaGraph)
            if button.text() == 'Delta band':
                self.layout.addWidget(self.deltaGraph, 0, 1, 1, 1)
                # self.layout.addWidget(self.deltaGraph)
            if button.text() == 'Theta Band':
                self.layout.addWidget(self.thetaGraph, 0, 2, 1, 1)
                # self.layout.addWidget(self.thetaGraph)


class checkboxes(QGroupBox):
    def __init__(self, *args, **kwargs):
        # have EEGmodule inherit attributes of QGroupBox
        super(QGroupBox, self).__init__(*args, **kwargs)

        # creating 3 boxes by default.


# create class to contain a widget created using pyqtgraph
class gradientW(QGroupBox):
    def __init__(self, *args, **kwargs):
        # have EEGmodule inherit attributes of QGroupBox
        super(QGroupBox, self).__init__(*args, **kwargs)
        # gradient widget
        self.gradient = QLinearGradient(0, 0, 1, 0)
        # set area to fill
        # self.painter = QPainter(self)
        # self.rect = QRect(0, 0, 100, 200)

    def setCofG(self, C=None, P=None):
        length = len(P)
        #gradient.addStop(P[0], C[0])
        for i in range(length):
            self.gradient.setColorAt(
                P[i], QColor.fromRgb(C[i][0], C[i][1], C[i][2]))
        #brush = QBrush(self.gradient)
        #self.painter.fillRect(self.rect, brush)

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
