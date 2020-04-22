from PyQt5 import *
import pyqtgraph as pg
import time
import numpy as np


class TemperatureModule_GSR:
    def __init__(self, inlet):
        pg.setConfigOption("background", "k")  # Graph background color
        pg.setConfigOption("foreground", "w")  # Graph foreground color

        self.graphWidget = pg.PlotWidget()  # pyqtgraph PlotWidget Class
        self.graphWidget.setTitle(
            '<span style="font-size: 20px;">Galvanic Skin Response</span>'
        )  # Set Title

        self.graphWidget.setLabel(
            "left", '<span style="font-size:13px">GSR amplitude (uS)</span>',
        )  # Left label
        # self.graphWidget.setLabel(
        #     "bottom",
        #     '<span style="color:red;font-size:20px">"Number of samples"</span>',
        # )  # Bottom label

        self.graphWidget.showGrid(x=True, y=True, alpha=0.3)  # Create a Grid

        # Get initial data
        self.seconds = []  # seconds data array, x value
        self.gsrData = []  # temperature data array, y value

        self.graphWidget.plot(y=self.gsrData, clear=True)  # plot initial value
        self.graphWidget.setRange(
            yRange=(44400, 56000)
        )  # change the visible x range of the graph
        text_box = pg.TextItem(
            text="TEST",
            color=(200, 200, 200),
            html=None,
            anchor=(0, 0),
            border=None,
            fill=None,
            angle=0,
            rotateAxis=None,
        )
        self.graphWidget.addItem(text_box)

        self.count = 0  # Counter for downsampling
        self.sum = 0  # Sum for downsampling

        self.gsrNumLabel = QtGui.QLabel()  # Body Temperature Number Display

        self.inlet = inlet
        self.start_time = time.time()

        # self.timer = pg.QtCore.QTimer()
        # self.timer.timeout.connect(self.getGsrSignal)  # get GSR signal every 20 ms
        # self.timer.start(20)

    def getGsrSignal(self):  # downsample to output every 100ms
        # elapsed_time = time.time() - self.start_time
        # print('Elapsed Time: ', elapsed_time)
        # self.start_time = time.time()
        sample, timestamp = self.inlet.pull_sample()
        data = sample[73]
        # print('GSR: ', data)
        self.update(data)

    def update(self, data):
        # print("update")

        if len(self.gsrData) < 200:  # first 500 data
            self.gsrData.append(data)

        else:  # after ten seconds
            self.gsrData.pop(0)
            self.gsrData.append(data)  # updating GSR signal

            # self.seconds.pop(0)
            # self.seconds.append(self.seconds[len(self.seconds) - 1] + 0.1)

            # self.graphWidget.setRange(xRange=(0, 500)) #change the visible x range of the graph

        self.graphWidget.plot(
            y=self.gsrData, pen=(255, 165, 0), clear=True
        )  # update plot

        gsrLabel = str(np.round(data, 2))  # Type casting from float to string
        self.gsrNumLabel.setText(
            "GSR AMPLITUDE:\n" + gsrLabel
        )  # Update the temperature numbering label
        self.gsrNumLabel.setStyleSheet(
            "font-weight: bold; font-size:10pt; color: black"
        )
