from PyQt5 import *
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np


class TemperatureModule_Accelerometer:
	def __init__(self, inlet):
		pg.setConfigOption("background", "k")  # graph background color
		pg.setConfigOption("foreground", "w")  # graph foreground color
		pg.setConfigOption("antialias", True)
		self.graphWidget = pg.PlotWidget()  # pyqtgraph PlotWidget Class
		self.graphWidget.setTitle(
			'<span style="font-size: 15px;"> Accelerometer </span>'
		)  # Set Title
		self.graphWidget.setLabel("left", "Acceleration")  # left label
		self.graphWidget.setLabel("bottom", "Number of samples")  # Bottom label
		self.graphWidget.showGrid(x=True, y=True, alpha=0.3)  # Create a Grid

		# Get initial data
		self.seconds = []  # seconds data array, x value
		self.accel = [[], [], []]  # Holds acceleration value,

		self.x_curve = self.graphWidget.plot()  # plot initialization, x value
		self.y_curve = self.graphWidget.plot()  # plot initialization, y value
		self.z_curve = self.graphWidget.plot()  # plot initialization, z value

		self.graphWidget.setRange(
			yRange=(-5000, 5000)
		)  # change the visible x range of the graph
		text_box = pg.TextItem(
			html='<span style="color: #FF0000;">- X value </span><span style="color: #008000;">- Y value </span><span style="color: #0000ff;"> - Z value </span> ',
			anchor=(0, 0),
			border=None,
			fill=None,
			angle=0,
			rotateAxis=None,
		)
		text_box.setPos(0, 5000)
		self.graphWidget.addItem(text_box)

		self.visualization = gl.GLViewWidget()
		# xgrid = gl.GLGridItem()
		# xgrid.scale(1, 1, 1)
		# ygrid = gl.GLGridItem()
		# ygrid.rotate(90, 1, 0, 0)
		# ygrid.scale(1, 1, 1)
		# self.visualization.addItem(xgrid)
		# self.visualization.addItem(ygrid)

		# create human face-looking object
		md = gl.MeshData.sphere(rows=10, cols=20)
		faceCount = md.faceCount()
		colors = np.ones((faceCount, 4), dtype=float)
		colors[0:60] = [0, 0, 0, 0]  # hair
		colors[102] = [0, 0, 1, 0.3]  # left eye
		colors[104] = [0, 0, 1, 0.3]  # right eye
		colors[182] = [0, 0, 1, 0.3]  # mouth
		md.setFaceColors(colors)

		self.head = gl.GLMeshItem(meshdata=md, smooth=False)  # , shader='balloon')
		self.rotation = 0
		self.head.rotate(10, 0, 1, 0)
		self.visualization.addItem(self.head)

		# Previous x, y, z point value, initialized to 0
		self.preXval = 0
		self.preYval = 0
		self.preZval = 0
		# Timer Setup, every second update the data
		self.inlet = inlet
		# self.timer = pg.QtCore.QTimer()
		# self.timer.timeout.connect(self.getValues)
		# self.timer.start(20)

	def getValues(self,sample ):
		# 78,AccelX
		# 79,AccelY
		# 80,AccelZ
		#sample, timestamp = self.inlet.pull_sample()
		xVal = sample[0][77]
		yVal = sample[0][78]
		zVal = sample[0][79]
		# print('ACCEL X: ', xVal)
		# print('ACCEL Y: ', yVal)
		# print('ACCEL Z: ', zVal)
		self.update(xVal, yVal, zVal)

	def update(self, xVal, yVal, zVal):
		if len(self.accel[0]) < 200:  # First 500 samples
			self.accel[0].append(xVal)
			self.accel[1].append(yVal)
			self.accel[2].append(zVal)
		else:  # after ten seconds
			self.accel[0].pop(0)  # Pop one data to shift plot
			self.accel[1].pop(0)  # Pop one data to shift plot
			self.accel[2].pop(0)  # Pop one data to shift plot

			self.accel[0].append(xVal)
			self.accel[1].append(yVal)
			self.accel[2].append(zVal)

		self.x_curve.setData(self.accel[0], pen="r")
		self.y_curve.setData(self.accel[1], pen="g")
		self.z_curve.setData(self.accel[2], pen="b")

		# x, y, z value move to amount
		# It is calulcated by subtracting current value from previous value
		xMoveTo = (xVal / 1000) - self.preXval
		yMoveTo = (yVal / 1000) - self.preYval
		zMoveTo = (zVal / 1000) - self.preZval
		# print('X: ', xMoveTo)
		# print('Y: ', yMoveTo)
		# print('Z: ', zMoveTo)
		self.head.translate(
			xMoveTo, yMoveTo, zMoveTo
		)  # x, y, z moves from previous point to current point
		self.preXval = xVal / 1000
		self.preYval = yVal / 1000
		self.preZval = zVal / 1000
