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
    def __init__(self, *args, **kwargs):
        super(RespiratoryModule, self).__init__(*args, **kwargs)

        tabLayout = QHBoxLayout()
        window = QWidget()
        window.setWindowTitle("Respiratory Dashboard")
        window.resize(1600, 1400)

        self.tabs = QTabWidget()

        print("looking for an Data stream...")
        streams = resolve_stream()  # Data Stream Initialization
        inlet = StreamInlet(streams[0])  # Creating an inlet

        # rep = MainWindow()
        spo2 = SpO2_Mod(streams, inlet)
        ppg = PPG_Graph(inlet)
        ppg2 = PPG_Graph(inlet)
        spgraph = SpO2_Graph(inlet)
        hrw = HR_Module(streams, inlet)
        hrgraph = HR_Graph(inlet)
        ecgraph = ECG_Graph(inlet)
        ecgraph2 = ECG_Graph(inlet)
        rgraph = Resp_Graph(inlet)

        GraphsGroupBox = QGroupBox("Respiratory Module Graphs")
        GraphsGroupBox.setStyleSheet("color: Green;")
        layout1 = QGridLayout()  # create a box
        layout1.addWidget(rgraph.Resp_Graph, 0, 0)
        layout1.addWidget(ecgraph2.ECG_Graph, 1, 0)  # add graphwidget into a box
        layout1.addWidget(ppg.PPG_Graph, 2, 0)
        layout1.addWidget(hrgraph.HR_Graph, 3, 0)
        GraphsGroupBox.setLayout(layout1)

        SpO2GroupBox = QGroupBox("SpO2")
        SpO2GroupBox.setStyleSheet("color: Green;")
        layout3 = QGridLayout()  # create a box
        layout3.addWidget(spo2.SpO2_Widget, 0, 0)
        SpO2GroupBox.setLayout(layout3)

        HRGroupBox = QGroupBox("HR")
        HRGroupBox.setStyleSheet("color: Green;")
        layout2 = QVBoxLayout()  # create a box
        layout2.addWidget(hrw.HR_Widget)
        HRGroupBox.setLayout(layout2)

        MainGroupBox = QGroupBox("Main Outlet")
        MainGroupBox.setStyleSheet("color: Green;")
        mlay = QGridLayout()  # create a box
        mlay.addWidget(spo2.SpO2_Widget, 1, 0, 1, 1)
        mlay.addWidget(hrw.HR_Widget, 0, 0, 1, 1)
        mlay.addWidget(ppg2.PPG_Graph, 1, 1, 1, 3)
        mlay.addWidget(ecgraph.ECG_Graph, 0, 1, 1, 3)
        MainGroupBox.setLayout(mlay)

        self.tab1 = MainGroupBox
        self.tab2 = GraphsGroupBox
        self.tab3 = QWidget()

        self.tabs.resize(300, 200)

        # self.tab3.setLayout(layout1)

        tabLayout.addWidget(self.tabs)
        self.tabs.addTab(self.tab1, "Overall")
        self.tabs.addTab(self.tab2, "Graphs")
        self.tabs.addTab(self.tab3, "SPO2")

        # Set the central widget of the Window. Widget will expand to take up all the space in the window by default.
        darkMode()

        window.setLayout(tabLayout)
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


# run application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    RespiratoryModule()
