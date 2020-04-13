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




class TemperatureModule_Main():
    def __init__(self, inlet):
        app = QApplication([]) # PyQT application starts
        window = QWidget() # create a window


        # Thermometer Box
        self.ThermometerBox = QGroupBox('Body Temperature') #label
        self.ThermometerBox.setStyleSheet("color: white;")
        layout1 = QVBoxLayout()
        thermometer = Thermometer(layout1)
        layout1.addWidget(thermometer)
        self.ThermometerBox.setLayout(layout1)


        # Instantiate BodyTemperature Class
        bt = TemperatureModule_BodyTemp(thermometer, inlet) 
        # Instantiate GSR Class
        gsr = TemperatureModule_GSR(inlet)
        # Instantiate Accelerometer Class
        acc = TemperatureModule_Accelerometer(inlet)
        
        # Body Temperature Plot Box
        self.BodyTempBox = QGroupBox('Body Temperature Plot')
        self.BodyTempBox.setStyleSheet("color: white;")
        layout2 = QVBoxLayout() # create a box
        #layout2.addWidget(bt.label)
        layout2.addWidget(bt.graphWidget) # add graphwidget into a box
        self.BodyTempBox.setLayout(layout2)

        # Body Temperature / GSR Numbering Label Box
        self.NumberingLabelBox = QGroupBox('Body Temperature / GSR') 
        self.NumberingLabelBox.setStyleSheet("color: white;")
        numLabelBox = QVBoxLayout()
        numLabelBox.addWidget(bt.tempNumLabel)
        numLabelBox.addWidget(gsr.gsrNumLabel)
        self.NumberingLabelBox.setLayout(numLabelBox)
       

        # GSR Plot Box
        self.GSRPlotBox = QGroupBox('GSR Plot')
        self.GSRPlotBox.setStyleSheet("color: white;")
        layout3 = QVBoxLayout()
        layout3.addWidget(gsr.graphWidget)
        self.GSRPlotBox.setLayout(layout3) 


        # Accelerometer 3D Visualization
        self.Accelerometer_3D_Box = QGroupBox('Accelerometer 3D Visualization')
        self.Accelerometer_3D_Box.setStyleSheet("color: white;")
        layout5 = QVBoxLayout()
        layout5.addWidget(acc.visualization)
        self.Accelerometer_3D_Box.setLayout(layout5)
        

        # Accelerometer Plot
        self.AcceleromterPlotBox = QGroupBox('Accelerometer Plot')
        self.AcceleromterPlotBox.setStyleSheet("color: white;")
        layout6 = QVBoxLayout()
        layout6.addWidget(acc.graphWidget)
        self.AcceleromterPlotBox.setLayout(layout6)

        # Grid Layout
        mainLayout = QGridLayout()

        # First Row = Body Temperature Module
        mainLayout.addWidget(self.ThermometerBox, 0, 0, 1, 2)
        mainLayout.addWidget(self.BodyTempBox, 0, 2, 1, 2)

        # Second Row = GSR Module
        mainLayout.addWidget(self.NumberingLabelBox, 1, 0, 1, 2)
        mainLayout.addWidget(self.GSRPlotBox, 1, 2, 1, 2)

        # Accelerometer
        mainLayout.addWidget(self.Accelerometer_3D_Box, 2, 0, 1, 2)
        mainLayout.addWidget(self.AcceleromterPlotBox, 2, 2, 1, 2)

        darkMode() # Apply Dark Mode
    
        window.setLayout(mainLayout) # set layout inside a window
        window.show() # show window
        app.exec_() # Run PyQt application
    
        
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
    TemperatureModule_Main(inlet)
