from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from pyqtgraph import *
import pyqtgraph as pg
import numpy as np
import sys  

class TemperatureModule():
    def __init__(self):
        app = QApplication([]) # PyQT application starts
        window = QWidget() # create a window

        # left group box, body temperature label
        leftGroupBox = QGroupBox('Body Temperature Label') #label
        layout1 = QVBoxLayout()
        layout1.addWidget(QPushButton('Label'))
        leftGroupBox.setLayout(layout1)
        
        # right group box, body temperature graph
        rightGroupBox = QGroupBox('Body Temperature Graph')
        layout2 = QVBoxLayout() # create a box
        tempGraph = BodyTemperature() # instantiate BodyTemperature Class
        layout2.addWidget(tempGraph.graphWidget) # add graphwidget into a box
        rightGroupBox.setLayout(layout2)

        mainLayout = QGridLayout()
        mainLayout.addWidget(leftGroupBox, 0, 0)
        mainLayout.addWidget(rightGroupBox, 0, 1)

        window.setLayout(mainLayout) # set layout inside a window
        window.show() # show window
        app.exec_()

class BodyTemperature():
    def __init__(self):
        pg.setConfigOption('background', 'w') #graph background color
        pg.setConfigOption('foreground', 'k') #graph foreground color

        self.graphWidget = pg.PlotWidget(title='Body Temperature') #pyqtgraph PlotWidget Class
     
        self.graphWidget.setLabel('left', "Temerature", units='Celsius') # left label
        self.graphWidget.setLabel('bottom', "Time Passed", units='Second') # bottom label

        # Get initial data
        self.seconds = [1] # seconds data array, x value
        self.temperature = [self.getBodyTemp()] # temperature data array, y value

        self.graphWidget.plot(self.seconds, self.temperature) # plot initial value
        self.graphWidget.setRange(yRange=(34.0, 41.0)) # change the visible x range of the graph
        
        #Timer Setup, every second update the data
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)
    
    def getBodyTemp(self):
        return np.random.uniform(36.0, 36.3)


    def update(self):
        if len(self.seconds) < 10: # first ten seconds
            self.seconds.append(self.seconds[len(self.seconds) - 1] + 1)
            temp = self.getBodyTemp()
            self.temperature.append(temp)
            
        else: # after ten seconds
            self.seconds.pop(0) 
            self.seconds.append(self.seconds[8]+1) #updating the seconds
            self.temperature.pop(0)
            temp = self.getBodyTemp()
            self.temperature.append(temp) #updating the temperature
            self.graphWidget.setRange(xRange=(self.seconds[0], self.seconds[9])) #change the visible x range of the graph

        if temp >= 38.0:
            self.graphWidget.plot(self.seconds, self.temperature, pen='r') # if temperature is high, set line color red
        elif temp >= 35.0 and temp < 38.0:
            self.graphWidget.plot(self.seconds, self.temperature, pen='g') # if temperature is normal, set line color green
        else:
            self.graphWidget.plot(self.seconds, self.temperature, pen='b') # if temperatre is too low, set line color blue

if __name__ == '__main__':
    TemperatureModule()