import numpy as np
import pyqtgraph
from matplotlib import cm
from PySide2 import QtWidgets

QtWidgets.QApplication([])
glw = pyqtgraph.GraphicsLayoutWidget()
glw.show()
p = glw.addPlot(0, 0)
img = pyqtgraph.ImageItem()
p.addItem(img)


# Get the colormap
def colormap_conversion(cm_name):
    colormap = cm.get_cmap(cm_name)  # cm.get_cmap("CMRmap")
    colormap = cm.get_cmap(str)
    colormap._init()
    # Convert matplotlib colormap from 0-1 to 0 -255 for Qt
    lut = (colormap._lut * 255).view(np.ndarray)
    # Apply the colormap
    img.setLookupTable(lut)


# dummy data
d = np.random.random_sample((1, 2))
type(d)
img.updateImage(image=d, levels=(1, 1))

QtWidgets.qApp.exec_()
