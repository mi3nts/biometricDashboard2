from PyQt5 import *
import pyqtgraph as pg

class GSR():
    def __init__(self, streams, inlet):
        pg.setConfigOption('background', 'w') # Graph background color
        pg.setConfigOption('foreground', 'k') # Graph foreground color

        self.graphWidget = pg.PlotWidget() #pyqtgraph PlotWidget Class
        self.graphWidget.setTitle('<span style="font-size: 20px;">Galvanic Skin Response</span>') # Set Title

        self.graphWidget.setLabel('left', "GSR amplitude", units='uS') # Left label
        self.graphWidget.setLabel('bottom', "Time", units='Seconds')   # Bottom label

        # Get initial data
        self.seconds = [] # seconds data array, x value
        self.gsrData = [] # temperature data array, y value

        self.graphWidget.plot(self.seconds, self.gsrData, clear=True) # plot initial value
        self.graphWidget.setRange(yRange=(0, 1.5))                    # change the visible x range of the graph
    
        self.count = 0  # Counter for downsampling
        self.sum = 0    # Sum for downsampling

        self.streams = streams
        self.inlet = inlet

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.getGsrSignal) # get GSR signal every 20 ms
        self.timer.start(20) 
    
    def getGsrSignal(self): # downsample to output every 100ms
        sample, timestamp = self.inlet.pull_sample()
        data = sample[73] * 0.00001
        print('GSR: ', data)

        if self.count > 5:     # After 100ms
            self.count = 0     # Reset counter
            avg = self.sum / 5 # Get the average to downsample
            self.sum = 0       # Reset Sum 
            self.update(avg)
        else:                  # If under 100ms, increment count and sum
            self.count += 1
            self.sum += data
        

    def update(self, data):
        if len(self.gsrData) < 100: # first ten seconds
            if len(self.seconds) == 0: # Initialization
                self.seconds.append(0)
            else:
                self.seconds.append(self.seconds[len(self.seconds) - 1] + 0.1)
            self.gsrData.append(data)
            self.graphWidget.plot(self.seconds, self.gsrData, pen=(255,165,0), clear=True) # update plot
        
        else: # after ten seconds
            self.gsrData.pop(0)
            #gsrSignal = self.getGsrSignal()
            self.gsrData.append(data) #updating GSR signal

            self.graphWidget.plot(self.seconds, self.gsrData, pen=(255,165,0), clear=True) # update plot
    