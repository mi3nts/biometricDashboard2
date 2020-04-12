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


class RespiratoryModule:
    def __init__(self, inlet):
        window = QWidget()
        window.setWindowTitle("Respiratory Dashboard")
        window.resize(1600, 1400)

        spo2 = SpO2_Mod(inlet)  # SpO2 Widget
        ppg = PPG_Graph(inlet)  # PPG Graph
        hrw = HR_Module(inlet)  # HR Widget
        ecgraph = ECG_Graph(inlet)  # ECG Graph
        rgraph = Resp_Graph(inlet)  # Respiratory Graph

        SpO2GroupBox = QGroupBox("SpO2")
        SpO2GroupBox.setStyleSheet("color: Green;")
        layout1 = QVBoxLayout()  # create a box
        layout1.addWidget(spo2.SpO2_Widget)
        SpO2GroupBox.setLayout(layout1)

        HRGroupBox = QGroupBox("HR")
        HRGroupBox.setStyleSheet("color: Green;")
        layout2 = QVBoxLayout()  # create a box
        layout2.addWidget(hrw.HR_Widget)
        HRGroupBox.setLayout(layout2)

        EcgGroupBox = QGroupBox("ECG")
        EcgGroupBox.setStyleSheet("color: Green;")
        layout3 = QHBoxLayout()  # create a box
        layout3.addWidget(ecgraph.ECG_Graph)
        EcgGroupBox.setLayout(layout3)

        PpgGroupBox = QGroupBox("PPG")
        PpgGroupBox.setStyleSheet("color: Green;")
        layout4 = QHBoxLayout()
        layout4.addWidget(ppg.PPG_Graph)
        PpgGroupBox.setLayout(layout4)

        RespGroupBox = QGroupBox("Resp")
        RespGroupBox.setStyleSheet("color: Green;")
        layout5 = QHBoxLayout()
        layout5.addWidget(rgraph.Resp_Graph)
        RespGroupBox.setLayout(layout5)

        mlay = QGridLayout()
        mlay.addWidget(HRGroupBox, 0, 0, 3, 1)
        mlay.addWidget(SpO2GroupBox, 3, 0, 3, 1)
        mlay.addWidget(RespGroupBox, 0, 1, 2, 3)
        mlay.addWidget(EcgGroupBox, 2, 1, 2, 3)
        mlay.addWidget(PpgGroupBox, 4, 1, 2, 3)

        # Set the central widget of the Window. Widget will expand to take up all the space in the window by default.
        darkMode()

        window.setLayout(mlay)
        window.show()
        app.exec_()


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
    app = QApplication(sys.argv)
    inlet = getStream()
    RespiratoryModule(inlet)
