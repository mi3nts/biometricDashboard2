from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import time
import sys

# Import for PYLSL
from pylsl import StreamInlet, resolve_stream
from RM_Graphs import *
from RM_SPO2Widget import *
from RM_HRWidget import *


class RespiratoryModule(QMainWindow):
    def __init__(self, inlet):
        super(RespiratoryModule, self).__init__()
        window = QWidget()
        window.setWindowTitle("Respiratory Dashboard")
        window.resize(1600, 1400)

        self.inlet = inlet

        self.spo2 = SpO2_Mod(inlet)  # SpO2 Widget
        self.ppg = PPG_Graph(inlet)  # PPG Graph
        self.hrw = HR_Module(inlet)  # HR Widget
        self.ecgraph = ECG_Graph(inlet)  # ECG Graph
        self.rgraph = Resp_Graph(inlet)  # Respiratory Graph

        self.SpO2GroupBox = QGroupBox("Oxygen Saturation (%)")
        self.SpO2GroupBox.setStyleSheet(
            "color: white; background-color: black;font-size:25px"
        )
        layout1 = QGridLayout()
        layout1.addWidget(self.spo2.SpO2_Widget, 0, 0)
        self.SpO2GroupBox.setLayout(layout1)

        self.HRGroupBox = QGroupBox("Heart Rate (Beats/min)")
        self.HRGroupBox.setStyleSheet(
            "color: white; background-color: black;font-size:25px"
        )
        layout2 = QGridLayout()
        layout2.addWidget(self.hrw.HR_Widget, 0, 0)
        self.HRGroupBox.setLayout(layout2)

        self.EcgGroupBox = QGroupBox()
        self.EcgGroupBox.setStyleSheet("background-color: black;")
        layout3 = QHBoxLayout()
        layout3.addWidget(self.ecgraph.ECG_Graph)
        self.EcgGroupBox.setLayout(layout3)

        self.PpgGroupBox = QGroupBox()
        self.PpgGroupBox.setStyleSheet("background-color: black;")
        layout4 = QHBoxLayout()
        layout4.addWidget(self.ppg.PPG_Graph)
        self.PpgGroupBox.setLayout(layout4)

        self.RespGroupBox = QGroupBox()
        self.RespGroupBox.setStyleSheet("background-color: black;")
        layout5 = QHBoxLayout()
        layout5.addWidget(self.rgraph.Resp_Graph)
        self.RespGroupBox.setLayout(layout5)

        mlay = QGridLayout()
        mlay.addWidget(self.HRGroupBox, 0, 0, 3, 1)
        mlay.addWidget(self.SpO2GroupBox, 3, 0, 3, 1)
        mlay.addWidget(self.RespGroupBox, 0, 1, 2, 3)
        mlay.addWidget(self.EcgGroupBox, 2, 1, 2, 3)
        mlay.addWidget(self.PpgGroupBox, 4, 1, 2, 3)
        window.setLayout(mlay)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.UpdateModules)
        self.timer.start(20)

        self.setCentralWidget(window)

        # Set the central widget of the Window. Widget will expand to take up all the space in the window by default.
        darkMode()

    def UpdateModules(self):
        sample = self.inlet.pull_sample()
        # updating all widgets
        self.ppg.update_ppgData(sample)
        self.ecgraph.update_ecgData(sample)
        self.hrw.update_HR(sample)
        self.spo2.update_SpO2(sample)
        self.rgraph.update_RespData(sample)


# function to change application style to dark mode
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
    inlet = getStream()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = RespiratoryModule(inlet)
    window.show()
    sys.exit(app.exec_())
