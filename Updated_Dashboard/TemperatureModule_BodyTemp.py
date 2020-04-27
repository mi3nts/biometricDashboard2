from PyQt5 import *
import pyqtgraph as pg
import numpy as np


class TemperatureModule_BodyTemp:
    def __init__(self, Thermometer, inlet):

        pg.setConfigOption("background", "k")  # graph background color
        pg.setConfigOption("foreground", "w")  # graph foreground color
        pg.setConfigOption("antialias", True)

        self.thermometer = Thermometer  # Initilize Thermometer

        self.graphWidget = pg.PlotWidget()  # pyqtgraph PlotWidget Class
        self.graphWidget.setTitle(
            '<span style="font-size: 20px;"> Body Temperature</span>'
        )  # Set Title
        self.graphWidget.setLabel("left", "Temperature", units="Celsius")  # left label
        self.graphWidget.setLabel("bottom", "Number of samples")  # Bottom label

        self.text_box = pg.TextItem(html="<span></span>", anchor=(0, 0))
        self.text_box.setPos(0, 41.0)
        self.graphWidget.addItem(self.text_box)

        # Get initial data
        self.seconds = []  # seconds data array, x value
        self.temperature = []  # temperature data array, y value

        self.curve = self.graphWidget.plot()  # plot initialization
        self.graphWidget.setRange(
            yRange=(25.0, 41.0)
        )  # change the visible x range of the graph
        self.graphWidget.showGrid(x=True, y=True, alpha=0.3)  # Create a Grid
        self.graphWidget.enableAutoRange(axis="y")
        self.graphWidget.setAutoVisible(y=True)

        self.tempNumLabel = QtGui.QLabel()  # Body Temperature Number Display
        self.label = QtGui.QLabel()
        self.inlet = inlet

        # self.timer = pg.QtCore.QTimer()
        # self.timer.timeout.connect(self.getBodyTemp)
        # self.timer.start(20)

    def getBodyTemp(self, sample):
        # sample, timestamp = self.inlet.pull_sample()
        temp = sample[0][74]
        # print('BODY TEMP: ', temp)
        self.update(temp)

    def update(self, temp):
        if len(self.temperature) < 200:  # First ten seconds
            self.temperature.append(temp)

        else:  # after ten seconds
            self.temperature.pop(0)  # Pop one data to shift plot
            self.temperature.append(temp)  # updating the temperature
            # self.graphWidget.setRange(xRange=(self.seconds[0], self.seconds[99])) #change the visible x range of the graph

        if temp >= 38.0:
            self.curve.setData(
                self.temperature, pen=pg.mkPen("r",width=2)
            )  # if temperature is high, set line color red
            self.tempNumLabel.setText(
                "Body Temperature (C°):\n "
                + str(np.round(temp, 2))
                + "\n High - Hyperthermia"
            )
        elif 35.0 <= temp and temp < 38.0:
            self.curve.setData(
                self.temperature, pen=pg.mkPen("#0ffe1d", width=2)
            )  # if temperature is normal, set line color green
            self.tempNumLabel.setText(
                "Body Temperature (C°):\n "
                + str(np.round(temp, 2))
                + "\n Normal - Healthy"
            )

        else:
            self.curve.setData(
                self.temperature, pen=pg.mkPen("#03ffff",width=2)
            )  # if temperatre is too low, set line color blue
            self.tempNumLabel.setText(
                "<span style='color: white; font-weight: bold; font-size: 23px;'>Body Temperature</span><br><br> <span style='font-size: 16px; color: white;'>"
                + str(np.round(temp, 2))
                + " C°<br>Low - Hypothermia</span>"
            )

        # Update Thermometer Value
        self.thermometer.value = temp
        self.thermometer.repaint()
