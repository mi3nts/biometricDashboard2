from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import random

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

        # create layout for ECG Module
        self.layout = QHBoxLayout()

        self.layout.addWidget(SpO2_GraphObject())  # add ECG Graph Object as Widget

        # set layout for module
        self.setLayout(self.layout)


class SpO2_Module(QGroupBox, QWidget):
    def __init__(self, *args, **kwargs):
        super(QGroupBox, self).__init__()

        self.setTitle("Sp02 Module")
        self.layout = QVBoxLayout()

        spWindow = QWidget()

        self.loading_lbl = QtGui.QLabel(spWindow)
        self.loading_lbl.setAlignment(Qt.AlignBaseline)
        loading_movie = QtGui.QMovie("./images/bub2.gif")
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
        self.rand_text = str(random.randint(90, 96))
        self.labelB.setText(self.rand_text)
        self.labelB.setFont(QtGui.QFont("Times", 50, QtGui.QFont.Bold))
        # self.labelB.move(130, 130)
        # self.labelB.setFont(QtGui.QFont("Times", 50, QtGui.QFont.Bold))

    def resizeEvent(self, event):
        rect = self.geometry()
        size = QtCore.QSize(
            min(rect.width(), rect.height()), min(rect.width(), rect.height())
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

        sampleGraph = pg.PlotWidget()

        # Data
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        SO = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        # setting Line Colour, Width, Style
        pen = pg.mkPen(color="b", width=5, style=QtCore.Qt.DotLine)

        # Graph Title
        sampleGraph.setTitle('<span style="color:red;font-size:25px">SpO2 Graph</span>')
        # Axis Labels
        sampleGraph.setLabel("left", "Oxygen Saturation (°C)", color="red", size=30)
        sampleGraph.setLabel("bottom", "Time (Sec)", color="red", size=30)

        # plot data: x, y values
        sampleGraph.plot(
            time, SO, pen=pen, symbol="+", symbolSize=15, symbolBrush=("w")
        )

        # create layout for EEG Module
        self.layout = QHBoxLayout()

        self.layout.addWidget(sampleGraph)

        # set layout for module
        self.setLayout(self.layout)


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
