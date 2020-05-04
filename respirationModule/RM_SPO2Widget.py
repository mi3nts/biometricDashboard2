from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class SpO2_Mod(QGroupBox):
	def __init__(self, inlet):
		super(QGroupBox, self).__init__()
		
		#self.layout = QHBoxLayout()
		self.setTitle("Sp02 Module")  # Set Title

		self.SpO2_Widget = QWidget()  # Create a SpO2 Widget

		self.SpO2_Gif_Label = QtGui.QLabel(
			self.SpO2_Widget
		)  # Create a Label for the SpO2 Gif
		self.SpO2_Gif_Label.setAlignment(Qt.AlignBaseline)

		# add Gif
		SpO2_Gif = QtGui.QMovie("./images/bub7.1.gif")
		self.SpO2_Gif_Label.setMovie(SpO2_Gif)
		SpO2_Gif.start()

		self.setGeometry(
			self.SpO2_Widget.height(),
			self.SpO2_Widget.width(),
			self.SpO2_Widget.height(),
			self.SpO2_Widget.width(),
		)

		# Initial Value
		self.rand_text = "000"

		# Create a QLabel for Displaying the Value
		self.SpO2_Value_Label = QLabel(self.SpO2_Widget)
		self.SpO2_Value_Label.setStyleSheet("background-color: none; color:blue;font-size:50px;")

		# Dynamically Set the Position & size of the Labelp
		self.SpO2_Value_Label.setGeometry(
			int(self.SpO2_Widget.width() / 6),
			int(self.SpO2_Widget.height() / 4),
			125,
			50,
		)

		# SpO2 Condition Label
		self.SpO2_Condition_Label = QLabel()
		self.SpO2_Condition_Label.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
		self.SpO2_Condition_Label.setAlignment(Qt.AlignCenter)

		self.inlet = inlet

	def update_SpO2(self, sample):
		num = sample[0][71]
		data = str(int(num))  # Get the SpO2 Data and Convert to String
		self.SpO2_Value_Label.setText(data)  # Display Updated Value

		if num >= 95:
			self.SpO2_Condition_Label.setText("Normal -- Healthy")
			self.SpO2_Condition_Label.setStyleSheet("color: #0ffe1d")

		elif num > 85 and num <= 94:
			self.SpO2_Condition_Label.setText("Hypoxic")
			self.SpO2_Condition_Label.setStyleSheet("color: yellow")

		else:
			self.SpO2_Condition_Label.setText("Severely Hypoxic")
			self.SpO2_Condition_Label.setStyleSheet("color: red")

	# Resize the Gif based on the Window Size
	def resizeEvent(self, event):
		rect = self.geometry()
		size = QtCore.QSize(
			min(rect.width(), rect.height()), min(rect.width(), rect.height()),
		)
		movie = self.SpO2_Gif_Label.movie()
		movie.setScaledSize(size)
