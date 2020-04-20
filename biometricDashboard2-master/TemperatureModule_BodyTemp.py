from PyQt5 import *
import pyqtgraph as pg


class TemperatureModule_BodyTemp:
    def __init__(self, Thermometer, inlet):

        pg.setConfigOption("background", "k")  # graph background color
        pg.setConfigOption("foreground", "w")  # graph foreground color

        self.thermometer = Thermometer  # Initilize Thermometer

        self.graphWidget = pg.PlotWidget()  # pyqtgraph PlotWidget Class
        self.graphWidget.setTitle(
            '<span style="font-size: 15px;"> Body Temperature</span>'
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
        self.graphWidget.showGrid(x=True, y=True, alpha=0.5)  # Create a Grid
        self.tempNumLabel = QtGui.QLabel()  # Body Temperature Number Display

        self.label = QtGui.QLabel()

        self.inlet = inlet

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.getBodyTemp)
        self.timer.start(20)

    def getBodyTemp(self):
        sample, timestamp = self.inlet.pull_sample()
        temp = sample[74]
        # print('BODY TEMP: ', temp)
        self.update(temp)

    def update(self, temp):
        if len(self.temperature) < 500:  # First ten seconds
            self.temperature.append(temp)

        else:  # after ten seconds
            self.temperature.pop(0)  # Pop one data to shift plot
            self.temperature.append(temp)  # updating the temperature
            # self.graphWidget.setRange(xRange=(self.seconds[0], self.seconds[99])) #change the visible x range of the graph

        if temp >= 38.0:
            self.curve.setData(
                self.temperature, pen="r"
            )  # if temperature is high, set line color red
            self.label.setText("Too High")
            self.label.setStyleSheet("font-weight: bold; font-size:10pt; color: red;")
            # self.text_box.setHtml('<span style="color: #FF0000;">Temperature is high</span>') # color = red

        elif 35.0 <= temp and temp < 38.0:
            self.curve.setData(
                self.temperature, pen="g"
            )  # if temperature is normal, set line color green
            self.label.setText("Normal")
            self.label.setStyleSheet("font-weight: bold; font-size:10pt; color: green;")
            # self.text_box.setHtml('<span style="color: #008000;">Temperature is normal</span>') # color = green

        else:
            self.curve.setData(
                self.temperature, pen="b"
            )  # if temperatre is too low, set line color blue
            self.label.setText("Too Low")
            self.label.setStyleSheet("font-weight: bold; font-size:10pt; color: blue;")
            # self.text_box.setHtml('<span style="color: #0000ff;">Temperature is low</span>') # color = blue

        # Update Thermometer Value
        self.thermometer.value = temp
        self.thermometer.repaint()

        tempLabel = str(temp)
        self.tempNumLabel.setText("TEMPERATURE:\n " + tempLabel + " C°")
        # Update the temperature numbering label
        self.tempNumLabel.setStyleSheet(
            "font-weight: bold; font-size:10pt; color: black"
        )
