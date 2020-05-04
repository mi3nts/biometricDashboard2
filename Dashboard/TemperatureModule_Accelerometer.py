from PyQt5 import *
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
class TemperatureModule_Accelerometer:
    def __init__(self, inlet):
        pg.setConfigOption("background", "k")  # graph background color
        pg.setConfigOption("foreground", "w")  # graph foreground color
        pg.setConfigOption("antialias", True)
        self.graphWidget = pg.PlotWidget()  # pyqtgraph PlotWidget Class
        self.graphWidget.setTitle(
            '<span style="font-size: 25px;"> Accelerometer </span>'
        )  # Set Title
        self.graphWidget.setLabel(
            "left", '<span style="font-size: 20px;">Acceleration</span>'
        )  # left label
        self.graphWidget.setLabel(
            "bottom", '<span style="font-size: 20px;">Number of samples</span>'
        )  # Bottom label
        self.graphWidget.showGrid(x=True, y=True, alpha=0.3)  # Create a Grid

        # Get initial data
        self.seconds = []  # seconds data array, x value
        self.accel = [[], [], []]  # Holds acceleration value,

        self.x_curve = self.graphWidget.plot()  # plot initialization, x value
        self.y_curve = self.graphWidget.plot()  # plot initialization, y value
        self.z_curve = self.graphWidget.plot()  # plot initialization, z value

        self.graphWidget.setRange(
            yRange=(-5000, 5000)
        )  # change the visible x range of the graph
        text_box = pg.TextItem(
            html='<span style="color: #FFA500;">- X value </span><span style="color: #0ffe1d;">- Y value </span><span style="color: #03ffff;"> - Z value </span> ',
            anchor=(0, 0),
            border=None,
            fill=None,
            angle=0,
            rotateAxis=None,
        )
        text_box.setPos(0, 5000)
        self.graphWidget.addItem(text_box)
        self.label = QtGui.QLabel()  # Accelerometer Number Display

    def getValues(self, sample):
        # 78: AccelX, 79: AccelY. 80: AccelZ
        xVal = sample[0][77]
        yVal = sample[0][78]
        zVal = sample[0][79]
        self.update(xVal, yVal, zVal)

    def update(self, xVal, yVal, zVal):
        if len(self.accel[0]) < 200:  # First 500 samples
            self.accel[0].append(xVal)
            self.accel[1].append(yVal)
            self.accel[2].append(zVal)
        else:  # after ten seconds
            self.accel[0].pop(0)  # Pop one data to shift plot
            self.accel[1].pop(0)  # Pop one data to shift plot
            self.accel[2].pop(0)  # Pop one data to shift plot

            self.accel[0].append(xVal)
            self.accel[1].append(yVal)
            self.accel[2].append(zVal)

        self.x_curve.setData(self.accel[0], pen=pg.mkPen("#FFA500", width=2))
        self.y_curve.setData(self.accel[1], pen=pg.mkPen("#0ffe1d",width=2))
        self.z_curve.setData(self.accel[2], pen=pg.mkPen("#03ffff",width=2))

        self.label.setText(
            '<span style="font-size: 23px; font-weight: bold; color: white;">Accelerometer</span>  <br><br> <span style="font-size: 16px; color: white;">x: '
            + str(np.round(xVal, 2))
            + " m/s²<br> y: "
            + str(np.round(yVal, 2))
            + "  m/s²<br> z: "
            + str(np.round(zVal, 2))
            + "  m/s²</span>"
        )

