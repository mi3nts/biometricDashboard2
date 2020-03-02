from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Imports for Pyqt Graphs
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import time

# Import for PYLSL
from pylsl import StreamInlet, resolve_stream


# The Applications MainWindow
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Application Window Title
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


# HR Module Class
class HR_Module(QGroupBox, QWidget):
    def __init__(self, *args, **kwargs):
        super(QGroupBox, self).__init__()

        self.setTitle("Heart Rate Module")
        self.setStyleSheet("HR_Module{font-size:25px;}")  # Set Title Font

        hrWidget = QWidget()  # Create hrWidget

        self.layout = QVBoxLayout()

        self.HR_Gif_Label = QtGui.QLabel(hrWidget)  # Create a Label For the HR Gif
        self.HR_Gif_Label.setAlignment(Qt.AlignBaseline)  # Set Allignment

        # Add the Gif
        HR_GIF = QtGui.QMovie("./images/hr.gif")
        self.HR_Gif_Label.setMovie(HR_GIF)
        HR_GIF.start()

        self.setGeometry(
            hrWidget.height(), hrWidget.width(), hrWidget.height(), hrWidget.width()
        )
        self.setMinimumSize(10, 10)

        # Initial value
        self.hr_Num = "98"

        # Create a QLabel for Displaying the HR Value
        self.HR_Value_Label = QLabel(hrWidget)

        # Dynamically Set the Position & size of the Label
        self.HR_Value_Label.setGeometry(
            int(hrWidget.width() / 4), int(hrWidget.height() / 3), 50, 50
        )

        # Read the Data Using PyLSL
        print("looking for an HR stream...")
        streams = resolve_stream()
        self.inlet = StreamInlet(streams[0])

        # Update the HR Value every 20 ms
        timer = QTimer(self)
        timer.timeout.connect(self.update_HR)
        timer.start(20)

        # Add Widget
        self.layout.addWidget(hrWidget)
        self.setLayout(self.layout)

    def update_HR(self):
        self.sample2 = self.inlet.pull_sample()  # Get Sample
        print(self.sample2[0][72], "\n")  # Print values for Debuging
        self.rand_text = str(
            self.sample2[0][72]
        )  # Specifically Get the HR Data and Convert to String
        self.HR_Value_Label.setText(self.rand_text)  # Display Value
        self.HR_Value_Label.setFont(
            QtGui.QFont("Times", 50, QtGui.QFont.Bold)
        )  # Change Font

    # Resize the Gif based on the Window Size
    def resizeEvent(self, event):
        rect = self.geometry()
        size = QtCore.QSize(
            min(rect.width(), rect.height()), min(rect.width(), rect.height())
        )
        movie = self.HR_Gif_Label.movie()
        movie.setScaledSize(size)


# SpO2 Module Class
class SpO2_Module(QGroupBox, QWidget):
    def __init__(self, *args, **kwargs):
        super(QGroupBox, self).__init__()

        self.setTitle("Sp02 Module")  # Set Title
        self.setStyleSheet("SpO2_Module{font-size:25px;color:blue;}")  # Set Title Font
        self.layout = QVBoxLayout()

        SpO2_Widget = QWidget()  # Create a SpO2 Widget

        self.SpO2_Gif_Label = QtGui.QLabel(
            SpO2_Widget
        )  # Create a Label for the SpO2 Gif
        self.SpO2_Gif_Label.setAlignment(Qt.AlignBaseline)

        # add Gif
        SpO2_Gif = QtGui.QMovie("./images/bub7.1.gif")
        self.SpO2_Gif_Label.setMovie(SpO2_Gif)
        SpO2_Gif.start()

        self.setGeometry(
            SpO2_Widget.height(),
            SpO2_Widget.width(),
            SpO2_Widget.height(),
            SpO2_Widget.width(),
        )
        self.setMinimumSize(10, 10)

        # Initial Value
        self.rand_text = "000.0"

        # Create a QLabel for Displaying the Value
        self.SpO2_Value_Label = QLabel(SpO2_Widget)

        # Dynamically Set the Position & size of the Label
        self.SpO2_Value_Label.setGeometry(
            int(SpO2_Widget.width() / 4.5), int(SpO2_Widget.height() / 3), 125, 50
        )

        # Read the Data Using PyLSL
        print("looking for an SpO2 stream...")
        streams = resolve_stream()
        self.inlet = StreamInlet(streams[0])

        # Update the SpO2 Value every 20 ms
        timer = QTimer(self)
        timer.timeout.connect(self.update_SpO2)
        timer.start(20)

        self.layout.addWidget(SpO2_Widget)
        self.setLayout(self.layout)

    def update_SpO2(self):
        self.sample2 = self.inlet.pull_sample()  # Get Sample
        print(self.sample2[0][71], "\n")  # For Debugging
        self.rand_text = str(
            self.sample2[0][71]
        )  # Specifically Get the Sp)2 Data and Convert to String
        self.SpO2_Value_Label.setText(self.rand_text)  # Display Updated Value
        self.SpO2_Value_Label.setFont(
            QtGui.QFont("Times", 50, QtGui.QFont.Bold)
        )  # Set Font

    # Resize the Gif based on the Window Size
    def resizeEvent(self, event):
        rect = self.geometry()
        size = QtCore.QSize(
            min(rect.width(), rect.height()), min(rect.width(), rect.height()),
        )
        movie = self.SpO2_Gif_Label.movie()
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


class PPG_Module(QGroupBox):
    # initialize attributes of PPG module class
    def __init__(self, *args, **kwargs):
        # have PPG module inherit attributes of QGroupBox
        super(QGroupBox, self).__init__(*args, **kwargs)

        # set title
        self.setTitle("PPG Module")
        self.setStyleSheet("PPG_Module{font-size:25px;}")

        # create layout for PPG Module
        self.layout = QHBoxLayout()

        # Need to add PPG Graph Object
        self.layout.addWidget(PPG_GraphObject())
        # set layout for module
        self.setLayout(self.layout)


class PPG_GraphObject(QGroupBox):
    def __init__(self, *args, **kwargs):
        super(QGroupBox, self).__init__(*args, **kwargs)

        self.PPG_Graph = pg.PlotWidget()  # Create a Plot Widget

        # Set Title
        self.PPG_Graph.setTitle(
            '<span style="color:red;font-size:25px">PPG Graph</span>'
        )

        # Axis Labels
        self.PPG_Graph.setLabel(
            "left", '<span style="color:red;font-size:25px">Voltage</span>'
        )
        self.PPG_Graph.setLabel(
            "bottom", '<span style="color:red;font-size:25px">Time (Sec)</span>'
        )

        self.PPG_Graph.setRange(yRange=(15000, 17000))  # Set Range of Y axis

        self.PPG_Graph.showGrid(x=True, y=True, alpha=0.3)  # Create a Grid

        # Initial Data
        self.yData = [0]
        self.xData = [0]

        # Read the Data Using PyLSL
        print("looking for an PPG stream...")
        streams = resolve_stream()
        self.inlet = StreamInlet(streams[0])

        # Update the PPG Data every 20 ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ppgData)
        self.timer.start(20)

        # create layout for PPG Module
        self.layout = QHBoxLayout()

        self.layout.addWidget(self.PPG_Graph)

        # set layout for module
        self.setLayout(self.layout)

    def getPPGData(self):
        # Get Next Data Points
        self.sample = self.inlet.pull_sample()
        print(self.sample[0][70], "\n")  # For Debugging

        return self.sample[0][70]

    def update_ppgData(self):
        ppgData = 0
        if len(self.xData) < 10:  # first ten seconds
            self.xData.append(self.xData[len(self.xData) - 1] + 20)
            ppgData = self.getPPGData()
            self.yData.append(ppgData)
        else:  # after ten seconds
            self.yData.pop(0)
            ppgData = self.getPPGData()
            self.yData.append(ppgData)
            self.PPG_Graph.setRange(
                xRange=(self.xData[0], self.xData[9])
            )  # change the visible x range of the graph

        self.PPG_Graph.plot(self.xData, self.yData, pen="r", clear=True)  # Update Plot


class ECG_GraphObject(QGroupBox):
    def __init__(self, *args, **kwargs):
        super(QGroupBox, self).__init__(*args, **kwargs)

        self.ECG_Graph = pg.PlotWidget()  # Create a Plot
        self.ECG_Graph.setTitle(
            '<span style="color:red;font-size:25px">ECG Graph</span>'
        )

        # Axis Labels
        self.ECG_Graph.setLabel(
            "left", '<span style="color:red;font-size:25px">Voltage</span>'
        )
        self.ECG_Graph.setLabel(
            "bottom", '<span style="color:red;font-size:25px">Time (Sec)</span>'
        )

        self.ECG_Graph.setRange(yRange=(1000, 14000))  # Set Range of Y axis

        self.ECG_Graph.showGrid(x=True, y=True, alpha=0.3)  # Create a Grid

        # Data
        self.yData = [0]
        self.xData = [0]

        # Read the Data Using PyLSL
        print("looking for an ECG stream...")
        streams = resolve_stream()
        self.inlet = StreamInlet(streams[0])

        # Update the ECG Data every 20 ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ecgData)
        self.timer.start(20)

        # create layout for EEG Module
        self.layout = QHBoxLayout()

        # self.layout.addWidget(self.graphLable)
        self.layout.addWidget(self.ECG_Graph)

        # set layout for module
        self.setLayout(self.layout)

    def getECGData(self):
        self.sample = self.inlet.pull_sample()
        print(self.sample[0][68], "\n")

        return self.sample[0][68]

    def update_ecgData(self):
        ecgData = 0

        if len(self.xData) < 10:  # first ten seconds
            self.xData.append(self.xData[len(self.xData) - 1] + 20)
            ecgData = self.getECGData()
            self.yData.append(ecgData)
        else:  # after ten seconds
            self.yData.pop(0)
            ecgData = self.getECGData()
            self.yData.append(ecgData)
            self.ECG_Graph.setRange(
                xRange=(self.xData[0], self.xData[9])
            )  # change the visible x range of the graph

        self.ECG_Graph.plot(self.xData, self.yData, pen="r", clear=True)  # Update Plot


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
