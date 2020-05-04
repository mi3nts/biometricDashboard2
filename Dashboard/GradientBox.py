from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyqtgraph as pg

class gradientLayout(QGroupBox):
	def __init__(self, gradient):
		super(QGroupBox, self).__init__()
		boxLayout = QGridLayout()
		#########################
		px = QPixmap(self.width(), 40)
		p = QPainter(px)
		grad = gradient.getGradient()
		brush = QBrush(grad)
		p.fillRect(QRect(0, 0, self.width(), 40), brush)
		p.end()
		label = QLabel()
		label.setPixmap(px)
		label.setContentsMargins(1, 1, 1, 1)
		label.setScaledContents(True)
		##############
		title = QLabel("Power (Normalized Z-scores)")
		title.setStyleSheet("QLabel { color:white; font:16px;}")
		title.setAlignment(Qt.AlignHCenter)
		title.setScaledContents(True)
		##############
		zero = QLabel("0")
		zero.setAlignment(Qt.AlignHCenter)
		zero.setStyleSheet("QLabel { color:white; font:14px;}")
		##############
		one = QLabel("1")
		one.setAlignment(Qt.AlignRight)
		one.setStyleSheet("QLabel { color:white; font:14px;}")
		##############
		negOne = QLabel("-1")
		negOne.setStyleSheet("QLabel { color:white; font:14px;}")
		##############
		boxLayout.addWidget(title, 0,0,1,3)
		boxLayout.addWidget(negOne, 1,0,1,1)
		boxLayout.addWidget(zero, 1,1)
		boxLayout.addWidget(one, 1,2)
		boxLayout.addWidget(label,2,0,1,3)
		self.setLayout(boxLayout)