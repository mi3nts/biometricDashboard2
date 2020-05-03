from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class HR_Module(QGroupBox):
	def __init__(self, inlet):
		super(QGroupBox, self).__init__()
		
		self.setTitle("Heart Rate Widget")

		self.HR_Widget = QWidget()  # Create hrWidget

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

		# Initial value
		self.hr_Num = "98"

		# Create a QLabel for Displaying the HR Value
		self.HR_Value_Label = QLabel(self.HR_Widget)
		self.HR_Value_Label.setStyleSheet("color:red;font-size:50px")

		# Dynamically Set the Position & size of the Label
		self.HR_Value_Label.setGeometry(
			int(self.HR_Widget.width() / 5.5), int(self.HR_Widget.height() / 4), 125, 50
		)

		# Heart Rate -- Condition label
		self.HR_Condition_Label = QLabel()
		self.HR_Condition_Label.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
		self.HR_Condition_Label.setAlignment(Qt.AlignCenter)

		self.inlet = inlet

	def update_HR(self, sample):
		num = sample[0][72]  # Get the HR Data and Convert to String
		data = str(int(num))
		self.HR_Value_Label.setText(data)  # Display Value
		# Change Font
		if num > 60 and num <= 80:
			self.HR_Condition_Label.setText("Condition White! - Normal HR")
			self.HR_Condition_Label.setStyleSheet("color: white")

		elif num > 80 and num <= 114:
			self.HR_Condition_Label.setText("Condition Yellow! - Normal but High HR")
			self.HR_Condition_Label.setStyleSheet("color: yellow")

		elif num > 114 and num <= 145:
			self.HR_Condition_Label.setText(
				"Condition Red! - Motor Skills Deteriorates"
			)
			self.HR_Condition_Label.setStyleSheet("color: red")

		elif num > 145 and num <= 175:
			self.HR_Condition_Label.setText(
				"Condition Grey! - Cognitivie Processing Deteriorates"
			)
			self.HR_Condition_Label.setStyleSheet("color: grey")

		elif num > 175 and num <= 220:
			self.HR_Condition_Label.setText(
				"Condition Black! -- Irational Flight or Flee"
			)
			self.HR_Condition_Label.setStyleSheet("color: black")

	# Resize the Gif based on the Window Size
	def resizeEvent(self, event):
		rect = self.geometry()
		size = QtCore.QSize(
			min(rect.width(), rect.height()), min(rect.width(), rect.height())
		)
		movie = self.HR_Gif_Label.movie()
		movie.setScaledSize(size)
