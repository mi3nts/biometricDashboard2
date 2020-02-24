from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np
import pyqtgraph.ptime as ptime
import random
import time
import datetime

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # set title of application window
        self.setWindowTitle("Respitory Module")

        # # resize main window
        self.resize(1600, 1200)

        # create a window widget for main window
        widget = QWidget()

        # define a layout for window
        layout = QGridLayout()

        # add all modules to MainWindow
        # HR Module: Top Left (Row:0, Column 0; Span 1 Row, Span 1 Column)
        # SpO2 Module: Bottom Left (Row:1, Column 0; Span 1 Row, Span 1 Column)
        # ECG Module: Top Right(Row:0, Column 1; Span 1 Row, Span 2 Columns)
        # PPG Module: Botton Right(Row:1, Column 1; Span 1 Row, Span 2 Columns)

        layout.addWidget(HR_Module(), 0, 0, 1, 1)  # HR
        layout.addWidget(ECG_Module(), 0, 1, 1, 2)  # ECG
        layout.addWidget(SpO2_Module(), 1, 0, 1, 1)  # SPo2
        layout.addWidget(PPG_Module(), 1, 1, 1, 2)  # PPG

        # add layout to window Widget
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand to take up all the space in the window by default.
        self.setCentralWidget(widget)

        # change window style to dark mode
        darkMode()


# create class to contain HR module
class HR_Module(QGroupBox, QWidget):
    def __init__(self, *args, **kwargs):
        super(QGroupBox, self).__init__()

        self.setTitle("Heart Rate Module")
        self.setStyleSheet("HR_Module{font-size:25px;}")

        hrWindow = QWidget()

        self.layout = QVBoxLayout()

        self.loading_lbl = QtGui.QLabel(hrWindow)
        self.loading_lbl.setAlignment(Qt.AlignBaseline)

        loading_movie = QtGui.QMovie("./images/hr.gif")
        self.loading_lbl.setMovie(loading_movie)
        loading_movie.start()

        self.setGeometry(
            hrWindow.height(), hrWindow.width(), hrWindow.height(), hrWindow.width()
        )
        self.setMinimumSize(10, 10)

        self.hr_Num = "98"
        # /2 is a number which you have to change
        self.labelB = QLabel(hrWindow)
        self.labelB.setGeometry(
            int(hrWindow.width() / 4), int(hrWindow.height() / 3), 50, 50
        )

        timer = QTimer(self)
        timer.timeout.connect(self.update_HR)
        timer.start(1000)

        self.layout.addWidget(hrWindow)
        # self.layout.
        self.setLayout(self.layout)

    def update_HR(self):
        self.rand_text = str(random.randint(60, 100))
        self.labelB.setText(self.rand_text)
        self.labelB.setFont(QtGui.QFont("Times", 50, QtGui.QFont.Bold))

    def resizeEvent(self, event):
        rect = self.geometry()
        size = QtCore.QSize(
            min(rect.width(), rect.height()), min(rect.width(), rect.height())
        )

        movie = self.loading_lbl.movie()
        movie.setScaledSize(size)


class ECG_Module(QGroupBox):
    # initialize attributes of ECGmodule class
    def __init__(self, *args, **kwargs):
        # have EEGmodule inherit attributes of QGroupBox
        super(QGroupBox, self).__init__(*args, **kwargs)

        # set title
        self.setTitle("ECG Module")
        self.setStyleSheet("ECG_Module{font-size:25px;}")

        # create layout for ECG Module
        self.layout = QHBoxLayout()

        self.layout.addWidget(ECG_GraphObject())  # add ECG Graph Object as Widget

        # set layout for module
        self.setLayout(self.layout)


class SpO2_Module(QGroupBox, QWidget):
    def __init__(self, *args, **kwargs):
        super(QGroupBox, self).__init__()

        self.setTitle("Sp02 Module")
        self.setStyleSheet("SpO2_Module{font-size:25px;}")
        self.layout = QVBoxLayout()

        spWindow = QWidget()

        self.loading_lbl = QtGui.QLabel(spWindow)
        self.loading_lbl.setAlignment(Qt.AlignBaseline)
        loading_movie = QtGui.QMovie("./images/bub4.gif")
        self.loading_lbl.setMovie(loading_movie)
        loading_movie.start()

        self.setGeometry(
            spWindow.height(), spWindow.width(), spWindow.height(), spWindow.width()
        )
        self.setMinimumSize(10, 10)

        self.rand_text = "96"
        # Label B -- Number
        self.labelB = QLabel(spWindow)
        # self.labelB.setAlignment(Qt.AlignHCenter
        self.labelB.setGeometry(
            int(spWindow.width() / 4), int(spWindow.height() / 3), 50, 50
        )

        timer = QTimer(self)
        timer.timeout.connect(self.update_label)
        timer.start(1000)

        self.layout.addWidget(spWindow)
        # self.layout.
        self.setLayout(self.layout)

    def update_label(self):
        self.rand_text = str(random.randint(84, 100))
        self.labelB.setText(self.rand_text)
        self.labelB.setFont(QtGui.QFont("Times", 50, QtGui.QFont.Bold))
        # self.labelB.move(130, 130)
        # self.labelB.setFont(QtGui.QFont("Times", 50, QtGui.QFont.Bold))

    def resizeEvent(self, event):
        rect = self.geometry()
        size = QtCore.QSize(
            min(rect.width(), rect.height()), min(rect.width(), rect.height()),
        )
        movie = self.loading_lbl.movie()
        movie.setScaledSize(size)


class PPG_Module(QGroupBox):
    # initialize attributes of PPG module class
    def __init__(self, *args, **kwargs):
        # have PPG module inherit attributes of QGroupBox
        super(QGroupBox, self).__init__(*args, **kwargs)

        # set title
        self.setTitle("PPG Module")
        self.setStyleSheet("PPG_Module{font-size:25px;}")

        # create layout for EEG Module
        self.layout = QHBoxLayout()

        # Need to add PPG Graph Object
        self.layout.addWidget(SpO2_GraphObject())
        # set layout for module
        self.setLayout(self.layout)


class SpO2_GraphObject(QGroupBox):
    # initialize attributes of SpO2 Graph class
    def __init__(self, *args, **kwargs):
        # have EEGmodule inherit attributes of QGroupBox
        super(QGroupBox, self).__init__(*args, **kwargs)

        self.sampleGraph = pg.PlotWidget()
        self.sampleGraph.setTitle(
            '<span style="color:red;font-size:25px">PPG Graph</span>'
        )
        # Axis Labels
        self.sampleGraph.setLabel(
            "left", '<span style="color:red;font-size:25px">Voltage</span>'
        )
        self.sampleGraph.setLabel(
            "bottom", '<span style="color:red;font-size:25px">Time (Sec)</span>'
        )

        self.sampleGraph.setRange(yRange=(-500, 500))

        self.sampleGraph.showGrid(x=True, y=True, alpha=0.3)

        # setting Line Colour, Width, Style
        self.pen = pg.mkPen(color="b", width=5, style=QtCore.Qt.DotLine)

        # Data

        self.yData = []
        self.xData = []

        # plot data: x, y values
        self.sampleGraph.plot(
            pen=self.pen, symbol="+", symbolSize=15, symbolBrush=("w"),
        )

        self.graphLable = QLabel()

        # Graph Title

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_oxySat)
        self.timer.start(1000)

        # create layout for EEG Module
        self.layout = QHBoxLayout()

        # self.layout.addWidget(self.graphLable)
        self.layout.addWidget(self.sampleGraph)

        # set layout for module
        self.setLayout(self.layout)

    def getOxySat(self):
        return np.random.uniform(-400, 400)

    def timestamp(self):
        return int(time.mktime(datetime.datetime.now().timetuple()))

    def update_oxySat(self):
        oxySatData = 0

        if len(self.xData) < 10:  # first ten seconds
            self.xData.append(self.timestamp())
            oxySatData = self.getOxySat()
            self.yData.append(oxySatData)
        else:  # after ten seconds
            self.yData.pop(0)
            oxySatData = self.getOxySat()
            self.yData.append(oxySatData)
            self.sampleGraph.setRange(
                xRange=(self.xData[0], self.xData[9])
            )  # change the visible x range of the graph

        if oxySatData <= 0:
            self.sampleGraph.plot(self.xData, self.yData, pen="r", clear=True)
        elif oxySatData > 0 and oxySatData <= 100:
            self.sampleGraph.plot(self.xData, self.yData, pen="y", clear=True)
        else:
            self.sampleGraph.plot(self.xData, self.yData, pen="g", clear=True)


class ECG_GraphObject(QGroupBox):
    # initialize attributes of SpO2 Graph class
    def __init__(self, *args, **kwargs):
        # have EEGmodule inherit attributes of QGroupBox
        super(QGroupBox, self).__init__(*args, **kwargs)

        self.sampleGraph = pg.PlotWidget()
        self.sampleGraph.setTitle(
            '<span style="color:red;font-size:25px">ECG Graph</span>'
        )
        # Axis Labels
        self.sampleGraph.setLabel("left", "Voltage (V)", color="red", size=30)
        self.sampleGraph.setLabel("bottom", "Time (Sec)", color="red", size=30)

        self.sampleGraph.setRange(yRange=(-500, 500))

        self.sampleGraph.showGrid(x=True, y=True, alpha=0.3)

        # setting Line Colour, Width, Style
        self.pen = pg.mkPen(color="b", width=5, style=QtCore.Qt.DotLine)

        # Data

        self.yData = []
        self.xData = []

        # plot data: x, y values
        self.sampleGraph.plot(
            pen=self.pen, symbol="+", symbolSize=15, symbolBrush=("w"),
        )

        self.graphLable = QLabel()

        # Graph Title

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_oxySat)
        self.timer.start(1000)

        # create layout for EEG Module
        self.layout = QHBoxLayout()

        # self.layout.addWidget(self.graphLable)
        self.layout.addWidget(self.sampleGraph)

        # set layout for module
        self.setLayout(self.layout)

    def getOxySat(self):
        return np.random.uniform(-400, 400)

    def timestamp(self):
        return int(time.mktime(datetime.datetime.now().timetuple()))

    def update_oxySat(self):
        oxySatData = 0

        if len(self.xData) < 10:  # first ten seconds
            self.xData.append(self.timestamp())
            oxySatData = self.getOxySat()
            self.yData.append(oxySatData)
        else:  # after ten seconds
            self.yData.pop(0)
            oxySatData = self.getOxySat()
            self.yData.append(oxySatData)
            self.sampleGraph.setRange(
                xRange=(self.xData[0], self.xData[9])
            )  # change the visible x range of the graph

        if oxySatData <= 0:
            self.sampleGraph.plot(self.xData, self.yData, pen="r", clear=True)
        elif oxySatData > 0 and oxySatData <= 100:
            self.sampleGraph.plot(self.xData, self.yData, pen="y", clear=True)
        else:
            self.sampleGraph.plot(self.xData, self.yData, pen="g", clear=True)


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text="Time", units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        return [
            datetime.datetime.fromtimestamp(value).strftime("%H:%M") for value in values
        ]


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
if __name__ == "__main__":
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
