from PyQt5 import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg 
from BodyTemperature import * # Body Temperature Class
from Gsr import *             # GSR Class
from Thermometer import *     # Thermometer Class
from Accelerometer import *   # Accelerometer Class
from pylsl import StreamInlet, resolve_stream # Data Stream
import time
import sys 

class TemperatureModule():
    def __init__(self):
        app = QApplication([]) # PyQT application starts
        window = QWidget() # create a window

        streams = resolve_stream() # pylsl Data Stream Initialization
        inlet = StreamInlet(streams[0])
        
        # Body temperature label (Thermometer)
        leftGroupBox = QGroupBox('Body Temperature') #label
        layout1 = QVBoxLayout()
        thermometer = Thermometer(layout1)
        layout1.addWidget(thermometer)
        leftGroupBox.setLayout(layout1)
        
        # Body temperature plot
        rightGroupBox = QGroupBox('Body Temperature Plot')
        layout2 = QVBoxLayout() # create a box
        tempGraph = BodyTemperature(thermometer, streams, inlet) # instantiate BodyTemperature Class
        layout2.addWidget(tempGraph.label)
        layout2.addWidget(tempGraph.graphWidget) # add graphwidget into a box
        rightGroupBox.setLayout(layout2)

        # Body Temperature / GSR Numbering Label
        gsrLabel = QGroupBox('Body Temperature / GSR') 
        numLabelBox = QVBoxLayout()
        bodyTempNum = QtGui.QLabel()
        gsrNum = QtGui.QLabel()
        bodyTempNum.setText('Body Temperature Numbering Display')
        gsrNum.setText('GSR Numbering Display')
        numLabelBox.addWidget(bodyTempNum)
        numLabelBox.addWidget(gsrNum)
        gsrLabel.setLayout(numLabelBox)
       

        # GSR graph
        gsrGraph = QGroupBox('GSR')
        gsr = GSR(streams, inlet)
        layout3 = QVBoxLayout()
        layout3.addWidget(gsr.graphWidget)
        gsrGraph.setLayout(layout3) 


        # Accelerometer 3D Visualization
        acc3d = QGroupBox('Accelerometer 3D Visualization')
        acc3dLayout = QVBoxLayout()
        acc3d.setLayout(acc3dLayout)
        

        # Accelerometer Plot
        accPlot = QGroupBox('Accelerometer Plot')
        accPlotLayout = QVBoxLayout()
        accPlot.setLayout(accPlotLayout)

        mainLayout = QGridLayout()
        mainLayout.addWidget(leftGroupBox, 0, 0)
        mainLayout.addWidget(rightGroupBox, 0, 1)

        mainLayout.addWidget(gsrLabel, 1, 0)
        mainLayout.addWidget(gsrGraph, 1, 1)

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


if __name__ == '__main__':
    TemperatureModule()