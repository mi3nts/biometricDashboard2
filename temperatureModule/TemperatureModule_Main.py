from PyQt5 import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg 
from TemperatureModule_BodyTemp import * # Body Temperature Class
from TemperatureModule_GSR import *             # GSR Class
from Thermometer import *     # Thermometer Class
from TemperatureModule_Accelerometer import *   # Accelerometer Class
from pylsl import StreamInlet, resolve_stream # Data Stream
import time
import sys 

class TemperatureModule_Main(QMainWindow):
    def __init__(self, inlet):
        super(TemperatureModule_Main, self).__init__()
        window = QWidget()
        window.setWindowTitle("Respiratory Dashboard")
        self.inlet = inlet

        # Thermometer Box
        self.ThermometerBox = QGroupBox('Body Temperature') #label
        self.ThermometerBox.setStyleSheet("color: white; background-color: black; font-size:25px;")
        layout1 = QVBoxLayout()
        thermometer = Thermometer(layout1)
        thermometer.setStyleSheet('font-size: 10px;')
        layout1.addWidget(thermometer)
        self.ThermometerBox.setLayout(layout1)


        self.bt = TemperatureModule_BodyTemp(thermometer, inlet) 
        self.gsr = TemperatureModule_GSR(inlet)
        self.acc = TemperatureModule_Accelerometer(inlet)
        
        # Body Temperature Plot Box
        self.BodyTempBox = QGroupBox()
        self.BodyTempBox.setStyleSheet("color: white; background-color: black;")
        layout2 = QVBoxLayout() 
        layout2.addWidget(self.bt.graphWidget)
        self.BodyTempBox.setLayout(layout2)

        # Numbering Label Box
        self.NumberingLabelBox = QGroupBox() 
        self.NumberingLabelBox.setStyleSheet("color: white; background-color: black;")
        numLabelBox = QVBoxLayout()
        numLabelBox.addWidget(self.bt.tempNumLabel)
        numLabelBox.addWidget(self.gsr.gsrNumLabel)
        numLabelBox.addWidget(self.acc.label)
        self.NumberingLabelBox.setLayout(numLabelBox)
       
        # GSR Plot Box
        self.GSRPlotBox = QGroupBox()
        self.GSRPlotBox.setStyleSheet("color: white; background-color: black;")
        layout3 = QVBoxLayout() 
        layout3.addWidget(self.gsr.graphWidget)
        self.GSRPlotBox.setLayout(layout3) 


        # Accelerometer Plot
        self.AcceleromterPlotBox = QGroupBox()
        self.AcceleromterPlotBox.setStyleSheet("color: white; background-color: black;")
        layout6 = QVBoxLayout()
        layout6.addWidget(self.acc.graphWidget)
        self.AcceleromterPlotBox.setLayout(layout6)

        # Grid Layout
        mainLayout = QGridLayout()

        # First Column = Body Temperature Module row, column, rowSpan, columnSpan
        mainLayout.addWidget(self.ThermometerBox, 0, 0, 3, 1)
        mainLayout.addWidget(self.NumberingLabelBox, 3, 0, 3, 1)

        # Second Column
        mainLayout.addWidget(self.BodyTempBox, 0, 1, 2, 4)
        mainLayout.addWidget(self.GSRPlotBox, 2, 1, 2, 4)
        mainLayout.addWidget(self.AcceleromterPlotBox, 4, 1, 2, 4)
        window.setLayout(mainLayout)

    

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.UpdateModules)
        self.timer.start(20)

        self.setCentralWidget(window)

        # Set the central widget of the Window. Widget will expand to take up all the space in the window by default.
        darkMode()
        

    def UpdateModules(self):
        # pulling data
        sample = self.inlet.pull_sample()
        # updating all widgets
        self.acc.getValues(sample)
        self.bt.getBodyTemp(sample)
        self.gsr.getGsrSignal(sample)

    
        
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


# function to grab data stream
def getStream():
    print("looking for data stream...")
    streams = resolve_stream()
    inlet = StreamInlet(streams[0])
    return inlet

# Main Function
if __name__ == '__main__':
    inlet = getStream()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window =  TemperatureModule_Main(inlet)
    # show the window
    window.show()
    # Start the event loop.
    sys.exit(app.exec_())
