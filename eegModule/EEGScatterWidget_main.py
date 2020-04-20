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


class CmapImage(QWidget):

    def __init__(self):
        super().__init__()

        self.im = QPixmap("./jet.png")
        self.rotation = 90
        self.im = self.im.transformed(QTransform().rotate(
            self.rotation), Qt.SmoothTransformation)
        self.label = QLabel(" Frequencies")
        self.title = QLabel("Normalized Amplitude")
        # self.title.setMinimumHeight(self.grid.height())
        self.title.setAlignment(Qt.AlignCenter)
        self.im = self.im.scaled(
            300, 500, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label.setPixmap(self.im)

        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 0, 1)
        self.grid.addWidget(self.title, 0, 1)
        self.setLayout(self.grid)

        # self.setGeometry(100, 100, 800, 300)

        # self.setWindowTitle("PyQT show image")
        self.show()


# create class to contain EEG module
class EEGmodule_main(QGroupBox):
    # initialize attributes of EEGmodule class
    def __init__(self,  inlet):
        # have EEGmodule inherit attributes of QGroupBox
        super(QGroupBox, self).__init__()
        self.inlet = inlet
        # set title of EEGmodule
        self.setTitle("EEG Module")
        # create layout for EEG Module
        self.layout = QGridLayout()
        # set layout for module
        self.setLayout(self.layout)

        # Creating graphs
        self.alphaGraph = EEG_Graph_Submodule()
        self.alphaGraph.setGraphTitle("Alpha Band (8-12Hz)")
        self.alphaBand = -3
        ######################################
        self.thetaGraph = EEG_Graph_Submodule()
        self.thetaGraph.setGraphTitle("Theta Band (4-7Hz)")
        self.thetaBand = -2
        ######################################
        self.deltaGraph = EEG_Graph_Submodule()
        self.deltaGraph.setGraphTitle("Delta Band (0-4Hz)")
        self.deltaBand = -1
        # self.deltaGraph.plotWidgetMain.resize(300,300)
        #######################################

        print(self.alphaGraph.geometry())

        # checkbox for alphaGraph
        alphabox = QCheckBox("Alpha Band", self)
        alphabox.setChecked(True)
        alphabox.stateChanged.connect(lambda: self.hideGraph(button=alphabox))
        ###################################################
        thetaBox = QCheckBox("Theta Band", self)
        thetaBox.setChecked(True)
        thetaBox.stateChanged.connect(lambda: self.hideGraph(button=thetaBox))
        thetaBox.move(100, 0)
        ###################################################
        deltaBox = QCheckBox("Delta Band", self)
        deltaBox.setChecked(True)
        deltaBox.stateChanged.connect(lambda: self.hideGraph(button=deltaBox))
        deltaBox.move(200, 0)
        ###################################################

        # add graphs to widget
        self.layout.addWidget(self.deltaGraph, 0, 0)
        self.layout.addWidget(self.thetaGraph, 1, 0)
        self.layout.addWidget(self.alphaGraph, 2, 0)
        self.layout.addWidget(CmapImage(), 3, 0)
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
        fill_1 = pg.PlotWidget()
        fill_1.getPlotItem().hideAxis('bottom')
        fill_1.getPlotItem().hideAxis('left')
        fill_2 = pg.PlotWidget()
        fill_2.getPlotItem().hideAxis('bottom')
        fill_2.getPlotItem().hideAxis('left')
        fill_3 = pg.PlotWidget()
        fill_3.getPlotItem().hideAxis('left')
        fill_3.getPlotItem().hideAxis('bottom')

        if button.isChecked() == False:
            if button.text() == "Alpha Band":
                self.alphaGraph.setParent(None)
                self.layout.removeWidget(self.alphaGraph)
                self.layout.addWidget(fill_1, 2, 0)

            if button.text() == 'Theta Band':
                self.thetaGraph.setParent(None)
                self.layout.removeWidget(self.thetaGraph)
                self.layout.addWidget(fill_2, 1, 0)

            if button.text() == "Delta Band":
                self.deltaGraph.setParent(None)
                self.layout.removeWidget(self.deltaGraph)
                self.layout.addWidget(fill_3, 0, 0)
        else:
            if button.text() == "Alpha Band":
                self.layout.addWidget(self.alphaGraph, 2, 0)
                fill_1.setParent(None)
            if button.text() == 'Theta Band':
                self.layout.addWidget(self.thetaGraph, 1, 0)
                # self.layout.removeWidget(fill_2)
                fill_2.setParent(None)
                # self.layout.addWidget(self.thetaGraph)
            if button.text() == 'Delta Band':
                self.layout.addWidget(self.deltaGraph, 0, 0)
                # self.layout.removeWidget(fill_3)
                fill_3.setParent(None)
