from PyQt5 import *
import pyqtgraph as pg

class BodyTemperature():
    def __init__(self, Thermometer, streams, inlet):
        
        pg.setConfigOption('background', 'w') #graph background color
        pg.setConfigOption('foreground', 'k') #graph foreground color

        self.thermometer = Thermometer # Initilize Thermometer
        
        self.graphWidget = pg.PlotWidget() #pyqtgraph PlotWidget Class
        self.graphWidget.setTitle('<span style="font-size: 20px;"> Body Temperature</span>') # Set Title

     
        self.graphWidget.setLabel('left', "Temerature", units='Celsius') # left label
        #self.graphWidget.setLabel('bottom', "Number of Samples", units='') # bottom label

      
        # Get initial data
        self.seconds = [] # seconds data array, x value
        self.temperature = [] # temperature data array, y value

        self.graphWidget.plot(y=self.temperature, clear=True) # plot initial value
        self.graphWidget.setRange(yRange=(34.0, 41.0)) # change the visible x range of the graph

        self.label = QtGui.QLabel()
        self.label.setStyleSheet("background-color: white")

        self.tempNumLabel = QtGui.QLabel() # Body Temperature Number Display
        
        #Timer Setup, every second update the data
        self.streams = streams
        self.inlet = inlet
       
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.getBodyTemp)
        self.timer.start(20)
    
    def getBodyTemp(self):
        sample, timestamp = self.inlet.pull_sample()
        temp = sample[74] + 6
        #print('BODY TEMP: ', temp)
        self.update(temp)
        

    def update(self, temp):
        if len(self.temperature) < 500: # First ten seconds
            # if len(self.seconds) == 0: # Initialization
            #     self.seconds.append(-80)
            # else:
                #self.seconds.append(self.seconds[len(self.seconds) - 1] + 20)
            self.temperature.append(temp)
            
        else: # after ten seconds
            self.temperature.pop(0) # Pop one data to shift plot
            self.temperature.append(temp) #updating the temperature
            #self.graphWidget.setRange(xRange=(self.seconds[0], self.seconds[99])) #change the visible x range of the graph

        if temp >= 38.0:
            self.graphWidget.plot(y=self.temperature, pen='r', clear=True) # if temperature is high, set line color red
            self.label.setText('<span style="font-size: 15px;"> Body Temperature is too high! <span>')
            self.label.setStyleSheet('color: red; background-color: white;')

        elif temp >= 35.0 and temp < 38.0:
            self.graphWidget.plot(y=self.temperature, pen='g', clear=True) # if temperature is normal, set line color green
            self.label.setText('<span style="font-size: 15px;">Body Temperature is normal</span>')
            self.label.setStyleSheet('color: green; background-color: white;')

        else:
            self.graphWidget.plot(y=self.temperature, pen='b', clear=True) # if temperatre is too low, set line color blue
            self.label.setText('<span style="font-size: 15px;"Body Temperature is too low</span>')
            self.label.setStyleSheet('color: blue; background-color: white;')
        self.graphWidget.plot(y=self.temperature, pen='g', clear=True) # if temperature is normal, set line color green
        
        # Update Thermometer Value
        self.thermometer.value = temp 
        self.thermometer.repaint()

        tempLabel = str(temp) # Type casting from float to string
        
        self.tempNumLabel.setText("Temp(C): " + tempLabel) # Update the temperature numbering label
        self.tempNumLabel.setStyleSheet('font-weight: bold; font-size:10pt; color: white')
