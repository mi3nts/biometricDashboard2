from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap

import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import matplotlib.cm
import matplotlib.colors as colors
import csv
import random as r
import numpy as np
import scipy.signal as sps
import socketserver
import sys
import time
import os

from TemperatureModule_BodyTemp import *  # Body Temperature Class
from TemperatureModule_GSR import *  # GSR Class
from Thermometer import *  # Thermometer Class
from TemperatureModule_Accelerometer import *  # Accelerometer Class
from pylsl import StreamInlet, resolve_stream
from EEGScatterWidget_main import *
from RM_Graphs import *
from RM_SPO2Widget import *
from RM_HRWidget import *

# from RM_Main import *
from TemperatureModule_Main import *

# Subclass QMainWindow to customise your application's main window


class MainWindow(QMainWindow):
    def __init__(self, inlet):
        super(MainWindow, self).__init__()

        # set title of application window
        self.setWindowTitle("Biometric Dashboard")
        # # resize main window
        self.resize(1600, 1200)
        # create a window widget for main window
        widget = QWidget()

        # Initializing Tab Screen
        self.bm_tabs = QTabWidget()
        self.main_tab = QWidget()
        self.eeg_tab = QWidget()
        self.resp_tab = QWidget()
        self.temp_tab = QWidget()

        self.bm_tabs.setStyleSheet("color:black;")

        # Adding tabs to the Screen
        self.bm_tabs.addTab(self.main_tab, "Main Tab")
        self.bm_tabs.addTab(self.eeg_tab, "EEG Tab")
        self.bm_tabs.addTab(self.resp_tab, "Resp Tab")
        self.bm_tabs.addTab(self.temp_tab, "Temp Tab")

        # Setting up Widgets
        self.spo2 = SpO2_Mod(inlet)  # spo2 widget
        self.spo22 = SpO2_Mod(inlet)  # spo2 widget
        self.ppg = PPG_Graph(inlet)  # PPG Graph
        self.ppg2 = PPG_Graph(inlet)
        self.hrw = HR_Module(inlet)  # HR Widget
        self.hrw2 = HR_Module(inlet)  # HR Widget
        self.ecgraph = ECG_Graph(inlet)  # ECG Graph
        self.ecgraph2 = ECG_Graph(inlet)  # ECG Graph
        self.rgraph = Resp_Graph(inlet)
        self.rgraph2 = Resp_Graph(inlet)  # Respiratory Graph
        self.eegModule = EEGmodule_main(inlet)  # EEG module
        self.eegModule2 = EEGmodule_main(inlet)
        self.cmap = CmapImage()

        # Thermometer Box
        self.ThermometerBox = QGroupBox("Body Temperature")  # label
        self.ThermometerBox.setStyleSheet("color: white;")
        layout6 = QVBoxLayout()
        self.thermometer = Thermometer(layout6)
        layout6.addWidget(self.thermometer)
        self.ThermometerBox.setLayout(layout6)

        self.ThermometerBox2 = QGroupBox("Body Temperature")  # label
        self.ThermometerBox.setStyleSheet("color: white;")
        layout16 = QVBoxLayout()
        self.thermometer2 = Thermometer(layout16)
        layout16.addWidget(self.thermometer2)
        self.ThermometerBox2.setLayout(layout16)

        self.bt = TemperatureModule_BodyTemp(self.thermometer, inlet)
        self.bt2 = TemperatureModule_BodyTemp(self.thermometer2, inlet)

        # Instantiate GSR Class
        self.gsr = TemperatureModule_GSR(inlet)
        self.gsr2 = TemperatureModule_GSR(inlet)
        # Instantiate Accelerometer Class
        self.acc = TemperatureModule_Accelerometer(inlet)

        ######################################################

        biometricWidgets(self)

        mainTabUI(self)
        respTabUI(self)
        tempTabUI(self)
        eegTabUI(self)

        # self.bm_tabs.currentChanged.connect(lambda: onChange(self))

        self.setCentralWidget(self.bm_tabs)

        # change window style to dark mode
        darkMode()


def mainTabUI(self):
    layout_eeg = QGridLayout()
    # layout_eeg.addWidget(self.eegModule.deltaGraph, 1, 0)
    # layout_eeg.addWidget(self.eegModule.thetaGraph, 2, 0)
    # layout_eeg.addWidget(self.eegModule.alphaGraph, 3, 0)
    layout_eeg.addWidget(self.eegModule.deltaG, 1, 0)
    layout_eeg.addWidget(self.eegModule.thetaG, 2, 0)
    layout_eeg.addWidget(self.eegModule.alphaG, 3, 0)
    layout_eeg.addWidget(self.cmap, 4, 0)
    # print(self.eegModule.alphaG.parentWidget())
    self.eegGroupBox = QGroupBox()
    self.eegGroupBox.setLayout(layout_eeg)

    layout_numbers = QGridLayout()
    layout_numbers.addWidget(self.SpO2GroupBox, 0, 0)
    layout_numbers.addWidget(self.HRGroupBox, 0, 1)
    layout_numbers.addWidget(self.ThermometerBox, 0, 2)
    self.numGroup = QGroupBox()
    self.numGroup.setLayout(layout_numbers)

    layout_graphs = QGridLayout()

    # Adding graphs to layout
    layout_graphs.addWidget(self.EcgGroupBox, 0, 0)
    layout_graphs.addWidget(self.PpgGroupBox, 0, 1)
    layout_graphs.addWidget(self.RespGroupBox, 1, 0)
    layout_graphs.addWidget(self.GSRPlotBox, 1, 1)
    self.graphsGroup = QGroupBox()
    self.graphsGroup.setLayout(layout_graphs)

    mainTabLayout = QGridLayout()
    mainTabLayout.addWidget(self.eegGroupBox, 0, 0, 22, 1)
    mainTabLayout.addWidget(self.numGroup, 0, 1, 20, 1)
    mainTabLayout.addWidget(self.graphsGroup, 20, 1, 2, 1)
    self.main_tab.setLayout(mainTabLayout)


def respTabUI(self):
    mlay = QGridLayout()
    mlay.addWidget(self.HRGroupBox2, 0, 0, 3, 1)
    mlay.addWidget(self.SpO2GroupBox2, 3, 0, 3, 1)
    mlay.addWidget(self.RespGroupBox2, 0, 1, 2, 3)
    mlay.addWidget(self.EcgGroupBox2, 2, 1, 2, 3)
    mlay.addWidget(self.PpgGroupBox2, 4, 1, 2, 3)
    self.resp_tab.setLayout(mlay)


def eegTabUI(self):
    layout_eeg2 = QGridLayout()
    layout_eeg2.addWidget(self.eegModule2)
    self.eeg_tab.setLayout(layout_eeg2)


def tempTabUI(self):
    # Grid Layout
    self.mainLayout = QGridLayout()

    # First Row = Body Temperature Module
    self.mainLayout.addWidget(self.ThermometerBox2, 0, 0, 1, 1)
    self.mainLayout.addWidget(self.BodyTempBox, 0, 2, 1, 3)

    # Second Row = GSR Module
    self.mainLayout.addWidget(self.NumberingLabelBox, 1, 0, 1, 1)
    self.mainLayout.addWidget(self.GSRPlotBox2, 1, 2, 1, 3)

    # Accelerometer
    self.mainLayout.addWidget(self.Accelerometer_3D_Box, 2, 0, 1, 1)
    self.mainLayout.addWidget(self.AcceleromterPlotBox, 2, 2, 1, 3)
    self.temp_tab.setLayout(self.mainLayout)


def biometricWidgets(self):

    self.SpO2GroupBox = QGroupBox("Oxygent Saturation (%)")
    self.SpO2GroupBox.setStyleSheet("color: white;")
    layout1 = QGridLayout()  # create a box
    layout1.addWidget(self.spo2.SpO2_Widget, 0, 0)
    self.SpO2GroupBox.setLayout(layout1)

    self.SpO2GroupBox2 = QGroupBox("Oxygent Saturation (%)")
    self.SpO2GroupBox2.setStyleSheet("color: white;")
    layout21 = QGridLayout()  # create a box
    layout21.addWidget(self.spo22.SpO2_Widget, 0, 0, 9, 1)
    layout21.addWidget(self.spo22.SpO2_Condition_Label, 9, 0, 1, 1)
    self.SpO2GroupBox2.setLayout(layout21)

    self.HRGroupBox = QGroupBox("Heart Rate (Beats/min)")
    self.HRGroupBox.setStyleSheet("color: white;")
    layout2 = QGridLayout()  # create a box
    layout2.addWidget(self.hrw.HR_Widget, 0, 0)
    self.HRGroupBox.setLayout(layout2)

    self.HRGroupBox2 = QGroupBox("Heart Rate (Beats/min)")
    self.HRGroupBox2.setStyleSheet("color: white;")
    layout22 = QGridLayout()  # create a box
    layout22.addWidget(self.hrw2.HR_Widget, 0, 0, 9, 1)
    layout22.addWidget(self.hrw2.HR_Condition_Label, 9, 0, 1, 1)
    self.HRGroupBox2.setLayout(layout22)

    self.EcgGroupBox = QGroupBox()
    layout3 = QHBoxLayout()  # create a box
    layout3.addWidget(self.ecgraph.ECG_Graph)
    self.EcgGroupBox.setLayout(layout3)

    self.PpgGroupBox = QGroupBox()
    layout4 = QHBoxLayout()
    layout4.addWidget(self.ppg.PPG_Graph)
    self.PpgGroupBox.setLayout(layout4)

    self.RespGroupBox = QGroupBox()
    layout5 = QHBoxLayout()
    layout5.addWidget(self.rgraph.Resp_Graph)
    self.RespGroupBox.setLayout(layout5)

    self.EcgGroupBox2 = QGroupBox()
    layout14 = QHBoxLayout()  # create a box
    layout14.addWidget(self.ecgraph2.ECG_Graph)
    self.EcgGroupBox2.setLayout(layout14)

    self.PpgGroupBox2 = QGroupBox()
    layout13 = QHBoxLayout()
    layout13.addWidget(self.ppg2.PPG_Graph)
    self.PpgGroupBox2.setLayout(layout13)

    self.RespGroupBox2 = QGroupBox()
    layout12 = QHBoxLayout()
    layout12.addWidget(self.rgraph2.Resp_Graph)
    self.RespGroupBox2.setLayout(layout12)

    self.BodyTempBox = QGroupBox("Body Temperature")
    self.BodyTempBox.setStyleSheet("color: white;")
    layout8 = QVBoxLayout()  # create a box
    layout8.addWidget(self.bt.graphWidget)  # add graphwidget into a box
    self.BodyTempBox.setLayout(layout8)

    # Body Temperature / GSR Numbering Label Box
    self.NumberingLabelBox = QGroupBox()
    numLabelBox = QVBoxLayout()
    numLabelBox.addWidget(self.bt.tempNumLabel)
    numLabelBox.addWidget(self.gsr.gsrNumLabel)
    self.NumberingLabelBox.setLayout(numLabelBox)

    # GSR Plot Box
    self.GSRPlotBox = QGroupBox()
    layout9 = QVBoxLayout()
    layout9.addWidget(self.gsr.graphWidget)
    self.GSRPlotBox.setLayout(layout9)

    self.GSRPlotBox2 = QGroupBox()
    layout19 = QVBoxLayout()
    layout19.addWidget(self.gsr2.graphWidget)
    self.GSRPlotBox2.setLayout(layout19)

    # Accelerometer 3D Visualization
    self.Accelerometer_3D_Box = QGroupBox("Accelerometer 3D Visualization")
    self.Accelerometer_3D_Box.setStyleSheet("color: white;")
    layout10 = QVBoxLayout()
    layout10.addWidget(self.acc.visualization)
    self.Accelerometer_3D_Box.setLayout(layout10)

    # Accelerometer Plot
    self.AcceleromterPlotBox = QGroupBox()
    layout11 = QVBoxLayout()
    layout11.addWidget(self.acc.graphWidget)
    self.AcceleromterPlotBox.setLayout(layout11)


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


def getStream():
    print("looking for an EEG stream...")
    streams = resolve_stream()
    inlet = StreamInlet(streams[0])
    return inlet


# run application
if __name__ == "__main__":
    import sys

    inlet = getStream()
    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    # create a window from the MainWindow class defined above
    window = MainWindow(inlet)
    # show the window
    window.show()
    # Start the event loop.
    sys.exit(app.exec_())
