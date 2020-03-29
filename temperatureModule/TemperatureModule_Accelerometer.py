from PyQt5 import *
import pyqtgraph as pg

class Accelerometer():
    def __init__(self, streams, inlet):
            
        pg.setConfigOption('background', 'w') #graph background color
        pg.setConfigOption('foreground', 'k') #graph foreground color
        
        
        self.graphWidget = pg.PlotWidget() #pyqtgraph PlotWidget Class
        self.graphWidget.setTitle('<span style="font-size: 20px;"> Accelerometer </span>') # Set Title

    
        self.graphWidget.setLabel('left', "Acceleration") # left label
        #self.graphWidget.setLabel('bottom', "Time", units='Mili Seconds') # bottom label
    
        # Get initial data
        self.seconds = [] # seconds data array, x value
        self.accel = [[], [], []] # Holds acceleration value, 

        self.graphWidget.plot(y=self.accel[0], pen='r') # plot initial value
        self.graphWidget.plot(y=self.accel[1], pen='g') # plot initial value
        self.graphWidget.plot(y=self.accel[2], pen='b') # plot initial value

        self.graphWidget.setRange(yRange=(-5000, 5000)) # change the visible x range of the graph

        #Timer Setup, every second update the data
        self.streams = streams
        self.inlet = inlet
    
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.getValues)
        self.timer.start(20)
    
    def getValues(self):
        # 78,AccelX
        # 79,AccelY
        # 80,AccelZ
        sample, timestamp = self.inlet.pull_sample()
        xVal = sample[77] 
        yVal = sample[78]
        zVal = sample[79]
        # print('ACCEL X: ', xVal)
        # print('ACCEL Y: ', yVal)
        # print('ACCEL Z: ', zVal)

        self.update(xVal, yVal, zVal)
            

    def update(self, xVal, yVal, zVal):
        if len(self.accel[0]) < 500: # First 500 samples
            # if len(self.seconds) == 0: # Initialization
            #     self.seconds.append(-80)
            # else:
                #self.seconds.append(self.seconds[len(self.seconds) - 1] + 20)
            self.accel[0].append(xVal)
            self.accel[1].append(yVal)
            self.accel[2].append(zVal)
            
            
        else: # after ten seconds
            self.accel[0].pop(0) # Pop one data to shift plot
            self.accel[1].pop(0) # Pop one data to shift plot
            self.accel[2].pop(0) # Pop one data to shift plot

        
            self.accel[0].append(xVal)
            self.accel[1].append(yVal)
            self.accel[2].append(zVal)
            

        self.graphWidget.plot(y=self.accel[0], pen='r') # plot initial value
        self.graphWidget.plot(y=self.accel[1], pen='g') # plot initial value
        self.graphWidget.plot(y=self.accel[2], pen='b') # plot initial value


