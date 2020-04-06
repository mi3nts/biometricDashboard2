from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class HR_Module(QGroupBox):
    def __init__(self, streams, inlet):
        super(QGroupBox, self).__init__()

        self.setTitle("Heart Rate Widget")
        self.setStyleSheet("HR_Module{font-size:25px;}")  # Set Title Font

        self.HR_Widget = QWidget()  # Create hrWidget
        # self.HR_Widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.HR_Gif_Label = QtGui.QLabel(
            self.HR_Widget
        )  # Create a Label For the HR Gif
        self.HR_Gif_Label.setAlignment(Qt.AlignCenter)  # Set Allignment

        # Add the Gif
        HR_GIF = QtGui.QMovie("./images/hr3.gif")
        self.HR_Gif_Label.setMovie(HR_GIF)
        HR_GIF.start()

        self.setGeometry(
            self.HR_Widget.height(),
            self.HR_Widget.width(),
            self.HR_Widget.height(),
            self.HR_Widget.width(),
        )

        self.setMinimumSize(400, 100)

        # Initial value
        self.hr_Num = "98"

        # Create a QLabel for Displaying the HR Value
        self.HR_Value_Label = QLabel(self.HR_Widget)

        # Dynamically Set the Position & size of the Label
        self.HR_Value_Label.setGeometry(
            int(self.HR_Widget.width() / 4.5), int(self.HR_Widget.height() / 3), 125, 50
        )

        self.inlet = inlet

        # Update the HR Value every 20 ms
        timer = QTimer(self)
        timer.timeout.connect(self.update_HR)
        timer.start(20)

    def update_HR(self):
        # print(self.sample2[0][72], "\n")  # Print values for Debuging
        sample = self.inlet.pull_sample()
        data = str(sample[0][72])  # Get the HR Data and Convert to String
        self.HR_Value_Label.setText(data)  # Display Value
        self.HR_Value_Label.setFont(
            QtGui.QFont("Times", 50, QtGui.QFont.Bold)
        )  # Change Font

    # Resize the Gif based on the Window Size
    def resizeEvent(self, event):
        rect = self.geometry()
        size = QtCore.QSize(
            min(rect.width(), rect.height()), min(rect.width(), rect.height())
        )
        movie = self.HR_Gif_Label.movie()
        movie.setScaledSize(size)
