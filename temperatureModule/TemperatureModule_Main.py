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

class TemperatureModule():
    def __init__(self):
        app = QApplication([]) # PyQT application starts
        window = QWidget() # create a window

        streams = resolve_stream() # pylsl Data Stream Initialization
        inlet = StreamInlet(streams[0])

        # Thermometer Box
        leftGroupBox = QGroupBox('Body Temperature') #label
        leftGroupBox.setStyleSheet("color: white;")
        layout1 = QVBoxLayout()
        thermometer = Thermometer(layout1)
        layout1.addWidget(thermometer)
        leftGroupBox.setLayout(layout1)


        # Instantiate BodyTemperature Class
        bt = BodyTemperature(thermometer, streams, inlet) 
        # Instantiate GSR Class
        gsr = GSR(streams, inlet)
        # Instantiate Accelerometer Class
        acc = Accelerometer(streams, inlet)
        
        # Body temperature plot
        rightGroupBox = QGroupBox('Body Temperature Plot')
        rightGroupBox.setStyleSheet("color: white;")
        layout2 = QVBoxLayout() # create a box
        layout2.addWidget(bt.label)
        layout2.addWidget(bt.graphWidget) # add graphwidget into a box
        rightGroupBox.setLayout(layout2)

        # Body Temperature / GSR Numbering Label
        gsrLabel = QGroupBox('Body Temperature / GSR') 
        gsrLabel.setStyleSheet("color: white;")
        numLabelBox = QVBoxLayout()
        numLabelBox.addWidget(bt.tempNumLabel)
        numLabelBox.addWidget(gsr.gsrNumLabel)
        gsrLabel.setLayout(numLabelBox)
       

        # GSR graph
        gsrGraph = QGroupBox('GSR Plot')
        gsrGraph.setStyleSheet("color: white;")
        layout3 = QVBoxLayout()
        layout3.addWidget(gsr.graphWidget)
        gsrGraph.setLayout(layout3) 


        # Accelerometer 3D Visualization
        acc3d = QGroupBox('Accelerometer 3D Visualization')
        acc3d.setStyleSheet("color: white;")
        acc3dLayout = QVBoxLayout()
        acc3d.setLayout(acc3dLayout)
        

        # Accelerometer Plot
        accPlot = QGroupBox('Accelerometer Plot')
        accPlot.setStyleSheet("color: white;")
        accPlotLayout = QVBoxLayout()
        accPlotLayout.addWidget(acc.graphWidget)
        accPlot.setLayout(accPlotLayout)

        # Grid Layout
        mainLayout = QGridLayout()
        mainLayout.addWidget(leftGroupBox, 0, 0)
        mainLayout.addWidget(rightGroupBox, 0, 1)

        mainLayout.addWidget(gsrLabel, 1, 0)
        mainLayout.addWidget(gsrGraph, 1, 1)

        # Accelerometer
        mainLayout.addWidget(acc3d, 2, 0)
        mainLayout.addWidget(accPlot, 2, 1)

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


# Main Function
if __name__ == '__main__':
    TemperatureModule()