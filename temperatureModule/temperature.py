from PyQt5 import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np
import sys  

OFFSET = 10
SCALE_HEIGHT = 224

class Thermometer(QtWidgets.QWidget):
    def __init__(self, parent):
        super(Thermometer, self).__init__()
        self.value = 35

    def changeValue(self, val):
        self.value = val
        self.paintEvent(self)
        

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.initDrawing(painter)
        self.drawTemperature(painter)
        self.drawBackground(painter)
        painter.end()

    def initDrawing(self, painter):
        self.normal = 25.0
        self.critical = 75.0
        self.m_min = 0.0
        self.m_max = 80.0
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(self.width()/2.0, 0.0)
        painter.scale(self.height()/300.0, self.height()/300.0)

    def drawBackground(self, painter):
        path = QtGui.QPainterPath()
        path.moveTo(-7.5, 257.0)
        path.quadTo(-12.5, 263.0, -12.5, 267.5)
        path.quadTo(-12.5, 278.0, 0.0, 280.0)
        path.quadTo(12.5, 278.0, 12.5, 267.5)
        path.moveTo(12.5, 267.5)
        path.quadTo(12.5, 263.0, 7.5, 257.0)
        path.lineTo(7.5, 25.0)
        path.quadTo(7.5, 12.5, 0, 12.5)
        path.quadTo(-7.5, 12.5, -7.5, 25.0)
        path.lineTo(-7.5, 257.0)
        p1 = QtCore.QPointF(-2.0, 0.0)
        p2 = QtCore.QPointF(12.5, 0.0)
        linearGrad = QtGui.QLinearGradient(p1, p2)
        linearGrad.setSpread(QtGui.QGradient.ReflectSpread)
        linearGrad.setColorAt(1.0, QtGui.QColor(0, 150, 255, 170))
        linearGrad.setColorAt(0.0, QtGui.QColor(255, 255, 255, 0))
        painter.setBrush(QtGui.QBrush(linearGrad))
        painter.setPen(QtCore.Qt.black)
        painter.drawPath(path)
        pen = QtGui.QPen()
        length = 12
        for i in range(33):
            pen.setWidthF(1.0)
            length = 12
            if i % 4 != 0:
                length = 8
                pen.setWidthF(0.8)
            if i % 2 != 0:
                length = 5
                pen.setWidthF(0.6)
            painter.setPen(pen)
            painter.drawLine(-7, 28+i*7, -7+length, 28+i*7)
        for i in range(9):
            num = self.m_min + i*(self.m_max-self.m_min)/8.0
            val = "{0}".format(num)
            fm = painter.fontMetrics()
            size = fm.size(QtCore.Qt.TextSingleLine, val)
            point = QtCore.QPointF(OFFSET, 252-i*28+size.width()/4.0)
            painter.drawText(point, val)

    def drawTemperature(self, painter):
        if self.value >= self.critical:
            color = QtGui.QColor(255, 0, 0)
        elif self.value >= self.normal:
            color = QtGui.QColor(0, 200, 0)
        else:
            color = QtGui.QColor(0, 0, 255)
        scale = QtGui.QLinearGradient(0.0, 0.0, 5.0, 0.0)
        bulb = QtGui.QRadialGradient(0.0, 267.0, 10.0, -5.0, 262.0)
        scale.setSpread(QtGui.QGradient.ReflectSpread)
        bulb.setSpread(QtGui.QGradient.ReflectSpread)
        color.setHsv(color.hue(), color.saturation(), color.value())
        scale.setColorAt(1.0, color)
        bulb.setColorAt(1.0, color)
        color.setHsv(color.hue(), color.saturation() - 200, color.value())
        scale.setColorAt(0.0, color)
        bulb.setColorAt(0.0, color)
        factor = self.value - self.m_min
        factor = (factor/self.m_max)-self.m_min
        temp = SCALE_HEIGHT * factor
        height = temp + OFFSET
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(scale)
        painter.drawRect(-5, 252+OFFSET-height, 10, height)
        painter.setBrush(bulb)
        rect = QtCore.QRectF(-10.0, 258, 20.0, 20.0)
        painter.drawEllipse(rect)


class TemperatureModule():
    def __init__(self):
        app = QApplication([]) # PyQT application starts
        window = QWidget() # create a window

        # left group box, body temperature label
        leftGroupBox = QGroupBox('Body Temperature Label') #label
        layout1 = QVBoxLayout()
        thermometer = Thermometer(layout1)
        layout1.addWidget(thermometer)
        leftGroupBox.setLayout(layout1)
        
        # right group box, body temperature graph
        rightGroupBox = QGroupBox('Body Temperature Graph')
        layout2 = QVBoxLayout() # create a box
        tempGraph = BodyTemperature(thermometer) # instantiate BodyTemperature Class
    
        layout2.addWidget(tempGraph.label)
        layout2.addWidget(tempGraph.graphWidget) # add graphwidget into a box
        rightGroupBox.setLayout(layout2)


        # GSR Label
        gsrLabel = QGroupBox('GSR Label') #label
        gsrLabel.setLayout(QVBoxLayout())

        # GSR graph
        gsrGraph = QGroupBox('GSR Graph')
        gsr = GSR()
        layout3 = QVBoxLayout()
        layout3.addWidget(gsr.graphWidget)
        gsrGraph.setLayout(layout3) 


        mainLayout = QGridLayout()
        mainLayout.addWidget(leftGroupBox, 0, 0)
        mainLayout.addWidget(rightGroupBox, 0, 1)

        mainLayout.addWidget(gsrLabel, 1, 0)
        mainLayout.addWidget(gsrGraph, 1, 1)

        darkMode()

        window.setLayout(mainLayout) # set layout inside a window
        window.show() # show window
        app.exec_()


class BodyTemperature():
    def __init__(self, Thermometer):
        pg.setConfigOption('background', 'w') #graph background color
        pg.setConfigOption('foreground', 'k') #graph foreground color


        #thermometer
        self.thermometer = Thermometer
        
        self.graphWidget = pg.PlotWidget(title='Body Temperature') #pyqtgraph PlotWidget Class
     
        self.graphWidget.setLabel('left', "Temerature", units='Celsius') # left label
        self.graphWidget.setLabel('bottom', "Time", units='Mili Seconds') # bottom label

      
        # Get initial data
        self.seconds = [-80] # seconds data array, x value
        self.temperature = [self.getBodyTemp()] # temperature data array, y value

        self.graphWidget.plot(self.seconds, self.temperature, clear=True) # plot initial value
        self.graphWidget.setRange(yRange=(34.0, 41.0)) # change the visible x range of the graph

        self.label = QtGui.QLabel()
        #self.label.setText('Temperature is normal')
        #self.label.setStyleSheet('color: green')
        
        #Timer Setup, every second update the data
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(20)
    
    def getBodyTemp(self):
        return np.random.uniform(36.0, 36.3)

    def update(self):
        temp = 0 # initialize 
        if len(self.seconds) < 10: # first ten seconds
            self.seconds.append(self.seconds[len(self.seconds) - 1] + 20)
            temp = self.getBodyTemp()
            self.temperature.append(temp)
            
        else: # after ten seconds
            #self.seconds.pop(0) 
            #self.seconds.append(self.seconds[8]+1) #updating the seconds
            self.temperature.pop(0)
            temp = self.getBodyTemp()
            self.temperature.append(temp) #updating the temperature
            self.graphWidget.setRange(xRange=(self.seconds[0], self.seconds[9])) #change the visible x range of the graph

        if temp >= 38.0:
            self.graphWidget.plot(self.seconds, self.temperature, pen='r', clear=True) # if temperature is high, set line color red
            self.label.setText('Body Temperature is too high')
            self.label.setStyleSheet('color: red')
        elif temp >= 35.0 and temp < 38.0:
            self.graphWidget.plot(self.seconds, self.temperature, pen='g', clear=True) # if temperature is normal, set line color green
            self.label.setText('Body Temperature is normal')
            self.label.setStyleSheet('color: green')
        else:
            self.graphWidget.plot(self.seconds, self.temperature, pen='b', clear=True) # if temperatre is too low, set line color blue
            self.label.setText('Body Temperature is too low')
            self.label.setStyleSheet('color: blue')
        
        self.thermometer.value = temp
        self.thermometer.repaint()

class GSR():
    def __init__(self):
        pg.setConfigOption('background', 'w') #graph background color
        pg.setConfigOption('foreground', 'k') #graph foreground color
        self.graphWidget = pg.PlotWidget(title='Galvanic Skin Response') #pyqtgraph PlotWidget Class

        self.graphWidget.setLabel('left', "GSR amplitude", units='uS') # left label
        self.graphWidget.setLabel('bottom', "Time", units='Seconds') # bottom label

        # Get initial data
        self.seconds = [0] # seconds data array, x value
        self.gsrData = [self.getGsrSignal()] # temperature data array, y value

        self.graphWidget.plot(self.seconds, self.gsrData, clear=True) # plot initial value
        self.graphWidget.setRange(yRange=(0, 1.5)) # change the visible x range of the graph
        self.graphWidget.setDownsampling(mode='peak') # down sampling

        #Timer Setup, every second update the data
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)
    
    def getGsrSignal(self):
        return np.random.uniform(0.3, 1.3)

    def update(self):
        if len(self.gsrData) < 100: # first ten seconds
            gsrSignal = self.getGsrSignal()
            self.gsrData.append(gsrSignal)
            self.seconds.append(self.seconds[len(self.seconds) - 1] + 0.1)
            self.graphWidget.plot(self.seconds, self.gsrData, pen=(255,165,0), clear=True) # update plot
        
        else: # after ten seconds
            self.gsrData.pop(0)
            gsrSignal = self.getGsrSignal()
            self.gsrData.append(gsrSignal) #updating GSR signal

            self.graphWidget.plot(self.seconds, self.gsrData, pen=(255,165,0), clear=True) # update plot
    
        
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