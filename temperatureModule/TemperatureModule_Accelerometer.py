from PyQt5 import *
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np

class TemperatureModule_Accelerometer():
    def __init__(self, inlet):
        pg.setConfigOption('background', 'w') #graph background color
        pg.setConfigOption('foreground', 'k') #graph foreground color
        self.graphWidget = pg.PlotWidget() #pyqtgraph PlotWidget Class
        self.graphWidget.setTitle('<span style="font-size: 15px;"> Accelerometer </span>') # Set Title
        self.graphWidget.setLabel('left', "Acceleration") # left label
        self.graphWidget.setLabel('bottom', "Number of samples")   # Bottom label

        # Get initial data
        self.seconds = [] # seconds data array, x value
        self.accel = [[], [], []] # Holds acceleration value, 

        self.x_curve = self.graphWidget.plot() # plot initialization, x value
        self.y_curve = self.graphWidget.plot() # plot initialization, y value
        self.z_curve = self.graphWidget.plot() # plot initialization, z value
        
        self.graphWidget.setRange(yRange=(-5000, 5000)) # change the visible x range of the graph
        text_box = pg.TextItem(html='<span style="color: #FF0000;">- X value </span><span style="color: #008000;">- Y value </span><span style="color: #0000ff;"> - Z value </span> ', anchor=(0, 0), border=None, fill=None, angle=0, rotateAxis=None)
        text_box.setPos(0, 5000)
        self.graphWidget.addItem(text_box)

        self.test = gl.GLViewWidget()
        g = gl.GLGridItem()
        g.scale(2,2,1)
        xgrid = gl.GLGridItem()
        xgrid.rotate(90, 0, 1, 0)
        xgrid.scale(2, 2, 1)
        self.test.addItem(xgrid)
        self.test.addItem(g)
        md = gl.MeshData.sphere(rows=10, cols=20)
        faceCount = md.faceCount()
        colors = np.ones((faceCount, 4), dtype=float)
        colors[::2,0] = 0
        colors[:,1] = np.linspace(0, 1, colors.shape[0])
        md.setFaceColors(colors)
        m3 = gl.GLMeshItem(meshdata=md, smooth=False)#, shader='balloon')
        m3.translate(0, 0, 0)
        self.test.addItem(m3)
        
    
        #Timer Setup, every second update the data
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
            
        self.x_curve.setData(self.accel[0], pen='r')
        self.y_curve.setData(self.accel[1], pen='g')
        self.z_curve.setData(self.accel[2], pen='b')

