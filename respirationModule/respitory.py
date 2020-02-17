from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pyqtgraph.ptime as ptime

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
class HR_Module(QGroupBox):

    # initialize attributes of HR module class
    def __init__(self, *args, **kwargs):
        # have EEGmodule inherit attributes of QGroupBox
        super(QGroupBox, self).__init__(*args, **kwargs)

        # set title
        self.setTitle("Heart Rate Module")

        # create layout for EEG Module
        self.layout = QHBoxLayout()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)

        hr = "98"

        qp.setPen(QPen(Qt.red, 10, Qt.SolidLine))
        qp.drawEllipse(40, 30, 350, 350)
        painter = QPainter(self)
        painter.setFont(QFont("times", 40))
        # /2 is a number which you have to change
        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.drawText(200, 210, hr)

        qp.end()

        # add a simple label widget to layout
        # self.layout.addWidget(QLabel("HR Module goes here"))

        # set layout for module
        self.setLayout(self.layout)


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
        # have EEGmodule inherit attributes of QGroupBox
        super(QGroupBox, self).__init__(*args, **kwargs)
        self.setTitle("SpO2 Visualization")

        # create layout for SpO2 Module
        self.layout = QHBoxLayout()

        # Create Widget to add labels
        spWindow = QWidget()
        # spWindow.setGeometry(0, 600, 450, 600)

        # Label A -- GIF
        labelA = QLabel(spWindow)
        spo2Image = QMovie("./images/bub2.gif")
        labelA.setMovie(spo2Image)
        spo2Image.start()
        # labelA.resize(900, 900)

        # Label B -- Number
        labelB = QLabel(spWindow)
        labelB.setText("96.9%")
        labelB.setFont(QtGui.QFont("Times", 50, QtGui.QFont.Bold))
        labelB.move(150, 130)

        # add Widget to Layout
        self.layout.addWidget(spWindow)

        self.setLayout(self.layout)
        # self.show()


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
