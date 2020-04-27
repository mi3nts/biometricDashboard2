from PyQt5 import *
import pyqtgraph as pg
import time
import numpy as np


class TemperatureModule_GSR:
    def __init__(self, inlet):
        pg.setConfigOption("background", "k")  # Graph background color
        pg.setConfigOption("foreground", "w")  # Graph foreground color
        pg.setConfigOption("antialias", True)
        self.graphWidget = pg.PlotWidget()  # pyqtgraph PlotWidget Class
        self.graphWidget.setTitle(
            '<span style="font-size: 20px;">Galvanic Skin Response</span>'
        )  # Set Title

        self.graphWidget.setLabel(
            "left", '<span style="font-size:13px">GSR amplitude (uS)</span>',
        )  # Left label
        self.graphWidget.setLabel(
            "bottom",
            '<span style="color:red;font-size:20px">"Number of samples"</span>',
        )  # Bottom label

        self.graphWidget.showGrid(x=True, y=True, alpha=0.3)  # Create a Grid

        # Get initial data
        self.seconds = []  # seconds data array, x value
        self.gsrData = []  # temperature data array, y value

        self.graphWidget.plot(y=self.gsrData, clear=True)  # plot initial value
        self.graphWidget.setRange(
            yRange=(44400, 56000)
        )  # change the visible x range of the graph
        self.graphWidget.enableAutoRange(axis="y")
        self.graphWidget.setAutoVisible(y=True)
        self.graphWidget.setLimits(minYRange=200)

        self.count = 0  # Counter for downsampling
        self.sum = 0  # Sum for downsampling

        self.gsrNumLabel = QtGui.QLabel()  # Body Temperature Number Display

        self.inlet = inlet
        self.start_time = time.time()

        # self.timer = pg.QtCore.QTimer()
        # self.timer.timeout.connect(self.getGsrSignal)  # get GSR signal every 20 ms
        # self.timer.start(20)

    def getGsrSignal(self, sample):
        data = sample[0][73]
        # print('GSR: ', data)
        self.update(data)

    def update(self, data):

        if len(self.gsrData) < 200:  # first 500 data
            self.gsrData.append(data)

        else:  # after ten seconds
            self.gsrData.pop(0)
            self.gsrData.append(data)  # updating GSR signal

        self.graphWidget.plot(
            y=self.gsrData, pen=pg.mkPen((255, 165, 0),width=2), clear=True
        )  # update plot

        self.gsrNumLabel.setText(
            "<span style='color: white; font-weight: bold; font-size: 23px;'>GSR Amplitude </span> <br><br> <span style='font-size: 16px; color: white;'>"
            + str(np.round(data, 2))
            + " µs</span>"
        )
