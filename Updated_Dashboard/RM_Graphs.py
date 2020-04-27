# Respiratory Module --- Graphs
# Author: Nikhil Nannapaneni

# Imports
from PyQt5 import *
import pyqtgraph as pg
pg.setConfigOption("background", "k")  # graph background color
pg.setConfigOption("foreground", "w")  # graph foreground color
pg.setConfigOption("antialias", True)
class PPG_Graph:
	def __init__(self, inlet):
	
		

		self.PPG_Graph = pg.PlotWidget()  # Create a Plot Widget

		# Set Title
		self.PPG_Graph.setTitle(
			'<span style="color:white;font-size:25px">PPG Graph</span>'
		)

		# Axis Labels
		self.PPG_Graph.setLabel(
			"left", '<span style="color:white;font-size:18px">Millivolts (mV)</span>'
		)

		# Initial Data
		self.yData = []

		self.PPG_Curve = self.PPG_Graph.plot()
		self.PPG_Graph.setRange(yRange=(15500, 17500))  # Set Range of Y axis
		self.PPG_Graph.setLimits(minYRange= 2000)
		self.PPG_Graph.showGrid(x=True, y=True, alpha=0.3)  # Create a Grid
		self.PPG_Graph.enableAutoRange(axis='y')
		self.PPG_Graph.setAutoVisible(y=True)
		self.inlet = inlet

        # Update the PPG Data every 20 ms
        # self.timer = pg.QtCore.QTimer()
        # self.timer.timeout.connect(self.update_ppgData)
        # self.timer.start(20)

	def getPPGData(self):
		# Get Next Data Points
		sample = self.inlet.pull_sample()
		return sample[0][70]

	def update_ppgData(self, sample):
		sample = sample[0][70]
		if len(self.yData) < 200:
			self.yData.append(sample)
		else:  # after ten seconds
			self.yData.pop(0)
			self.yData.append(sample)

		self.PPG_Curve.setData(self.yData, pen=pg.mkPen("r", width=2))  # Update Plot


class ECG_Graph:
	def __init__(self, inlet):
		self.ECG_Graph = pg.PlotWidget()  # Create a Plot
		self.ECG_Graph.setTitle(
			'<span style="color:white;font-size:25px">ECG Graph</span>'
		)

		# Axis Labels
		self.ECG_Graph.setLabel(
			"left", '<span style="color:white;font-size:18px">Millivolts (mV)</span>'
		)
		# initial data
		self.yData = []

		self.ECG_Curve = self.ECG_Graph.plot()
		self.ECG_Graph.setRange(yRange=(1400, 13050))  # Set Range of Y axis
		self.ECG_Graph.setLimits(minYRange=1000)  # Set miinmum span
		self.ECG_Graph.showGrid(x=True, y=True, alpha=0.3)  # Create a Grid
		self.ECG_Graph.enableAutoRange(axis='y')
		self.ECG_Graph.setAutoVisible(y=True)
		self.inlet = inlet

        # # Update the ECG Data every 20 ms
        # self.timer = pg.QtCore.QTimer()
        # self.timer.timeout.connect(self.update_ecgData)
        # self.timer.start(20)

	def update_ecgData(self, sample):
        #sample = self.inlet.pull_sample()
		if len(self.yData) < 200:  # first ten seconds
			self.yData.append(sample[0][68])  # get next data point
		else:  # after ten seconds
			self.yData.pop(0)
			self.yData.append(sample[0][68])

		self.ECG_Curve.setData(self.yData,  pen=pg.mkPen("w", width=2))  # Update Plot


class HR_Graph:
	def __init__(self, inlet):
		self.HR_Graph = pg.PlotWidget()  # Create a Plot
		self.HR_Graph.setTitle(
			'<span style="color:white;font-size:25px">HR Graph</span>'
		)

		# Axis Labels
		self.HR_Graph.setLabel(
			"left", '<span style="color:white;font-size:25px">Heart Rate</span>'
		)
		# initial data
		self.yData = []

		self.HR_Curve = self.HR_Graph.plot()
		self.HR_Graph.setRange(yRange=(70, 100))  # Set Range of Y axis
		self.HR_Graph.showGrid(x=True, y=True, alpha=0.3)  # Create a Grid

		self.inlet = inlet

        # Update the HR Data every 20 ms
        # self.timer = pg.QtCore.QTimer()
        # self.timer.timeout.connect(self.update_HRData)
        # self.timer.start(20)

	def update_HRData(self, sample):
        #sample = self.inlet.pull_sample()
		if len(self.yData) < 200:  # first ten seconds
			self.yData.append(sample[0][72])  # get next data point
		else:  # after ten seconds
			self.yData.pop(0)
			self.yData.append(sample[0][72])

		self.HR_Curve.setData(self.yData,  pen=pg.mkPen("b", width=2))  # Update Plot


class SpO2_Graph:
	def __init__(self, inlet):
		self.SpO2_Graph = pg.PlotWidget()  # Create a Plot
		self.SpO2_Graph.setTitle(
			'<span style="color:white;font-size:25px">SpO2 Graph</span>'
		)

		# Axis Labels
		self.SpO2_Graph.setLabel(
			"left",
			'<span style="color:white;font-size:25px">Oxygen Saturation (%) </span>',
		)
		# initial data
		self.yData = []

		self.SpO2_Curve = self.SpO2_Graph.plot()
		self.SpO2_Graph.setRange(yRange=(95, 100))  # Set Range of Y axis
		self.SpO2_Graph.showGrid(x=True, y=True, alpha=0.3)  # Create a Grid

		self.inlet = inlet

        # Update the SpO2 Data every 20 ms
        # self.timer = pg.QtCore.QTimer()
        # self.timer.timeout.connect(self.update_SpO2Data)
        # self.timer.start(20)

	def update_SpO2Data(self, sample):
        #sample = self.inlet.pull_sample()
		if len(self.yData) < 200:  # first ten seconds
			self.yData.append(sample[0][71])  # get next data point
		else:  # after ten seconds
			self.yData.pop(0)
			self.yData.append(sample[0][71])

		self.SpO2_Curve.setData(self.yData, pen="b")  # Update Plot


class Resp_Graph:
	def __init__(self, inlet):
		self.Resp_Graph = pg.PlotWidget()  # Create a Plot
		self.Resp_Graph.setTitle(
			'<span style="color:white;font-size:25px">Resp Graph</span>'
		)

		# Axis Labels
		self.Resp_Graph.setLabel(
			"left", '<span style="color:white;font-size:20px">Breaths/min</span>',
		)
		# initial data
		self.yData = []

		self.Resp_Curve = self.Resp_Graph.plot()
		self.Resp_Graph.setRange(yRange=(33, 39))  # Set Range of Y axis
		self.Resp_Graph.setLimits(minYRange=10)  # Set Range of Y axis
		self.Resp_Graph.showGrid(x=True, y=True, alpha=0.3)  # Create a Grid
		self.Resp_Graph.enableAutoRange(axis='y')
		self.Resp_Graph.setAutoVisible(y=True)
		self.inlet = inlet

        # Update the Resp Data every 20 ms
        # self.timer = pg.QtCore.QTimer()
        # self.timer.timeout.connect(self.update_RespData)
        # self.timer.start(20)

	def update_RespData(self,sample):
		#sample = self.inlet.pull_sample()
		if len(self.yData) < 200:  # first ten seconds
			self.yData.append(sample[0][69])  # get next data point
		else:  # after ten seconds
			self.yData.pop(0)
			self.yData.append(sample[0][69])

		self.Resp_Curve.setData(self.yData,  pen=pg.mkPen("y", width=2))  # Update Plot
