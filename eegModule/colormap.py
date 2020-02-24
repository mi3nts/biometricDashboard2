
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import matplotlib.pyplot as plt
import pyqtgraph as pg
import numpy as np
import collections
from matplotlib import cm
from pyqtgraph.Qt import QtCore, QtGui

import numpy as np
import pyqtgraph

# additional imports for this to work ...
import collections
import matplotlib.cm

# cmap to colormap: this functoin converts the matplotlib colormaps to integrate into pyqtgraph colormaps


def cmapToColormap(cmap, nTicks=1):
    """
    Converts a Matplotlib cmap to pyqtgraphs colormaps. No dependency on matplotlib.

    Parameters:
    *cmap*: Cmap object. Imported from matplotlib.cm.*
    *nTicks*: Number of ticks to create when dict of functions is used. Otherwise unused.
    """

    # Case #1: a dictionary with 'red'/'green'/'blue' values as list of ranges (e.g. 'jet')
    # The parameter 'cmap' is a 'matplotlib.colors.LinearSegmentedColormap' instance ...
    if hasattr(cmap, '_segmentdata'):
        colordata = getattr(cmap, '_segmentdata')
        if ('red' in colordata) and isinstance(colordata['red'], collections.Sequence):
            # print("[cmapToColormap] RGB dicts with ranges")

            # collect the color ranges from all channels into one dict to get unique indices
            posDict = {}
            for idx, channel in enumerate(('red', 'green', 'blue')):
                for colorRange in colordata[channel]:
                    posDict.setdefault(
                        colorRange[0], [-1, -1, -1])[idx] = colorRange[2]

            indexList = list(posDict.keys())
            indexList.sort()
            # interpolate missing values (== -1)
            for channel in range(3):  # R,G,B
                startIdx = indexList[0]
                emptyIdx = []
                for curIdx in indexList:
                    if posDict[curIdx][channel] == -1:
                        emptyIdx.append(curIdx)
                    elif curIdx != indexList[0]:
                        for eIdx in emptyIdx:
                            rPos = (eIdx - startIdx) / (curIdx - startIdx)
                            vStart = posDict[startIdx][channel]
                            vRange = (posDict[curIdx][channel] -
                                      posDict[startIdx][channel])
                            posDict[eIdx][channel] = rPos * vRange + vStart
                        startIdx = curIdx
                        del emptyIdx[:]

            for channel in range(3):  # R,G,B
                for curIdx in indexList:
                    posDict[curIdx][channel] *= 255

            posList = [[i, posDict[i]] for i in indexList]
            return posList

        # Case #2: a dictionary with 'red'/'green'/'blue' values as functions (e.g. 'gnuplot')
        elif ('red' in colordata) and isinstance(colordata['red'], collections.Callable):
            # print("[cmapToColormap] RGB dict with functions")
            indices = np.linspace(0., 1., nTicks)
            luts = [np.clip(np.array(colordata[rgb](indices), dtype=np.float), 0, 1) * 255
                    for rgb in ('red', 'green', 'blue')]
            return list(zip(indices, list(zip(*luts))))

    # If the parameter 'cmap' is a 'matplotlib.colors.ListedColormap' instance, with the attributes 'colors' and 'N'
    elif hasattr(cmap, 'colors') and hasattr(cmap, 'N'):
        colordata = getattr(cmap, 'colors')
        # Case #3: a list with RGB values (e.g. 'seismic')
        if len(colordata[0]) == 3:
            # print("[cmapToColormap] list with RGB values")
            indices = np.linspace(0., 1., len(colordata))
            scaledRgbTuples = [(rgbTuple[0] * 255, rgbTuple[1]
                                * 255, rgbTuple[2] * 255) for rgbTuple in colordata]
            return list(zip(indices, scaledRgbTuples))

        # Case #3: a list of tuples with positions and RGB-values (e.g. 'terrain')
        # -> this section is probably not needed anymore!?
        elif len(colordata[0]) == 2:
            # print("[cmapToColormap] list with positions and RGB-values. Just scale the values.")
            scaledCmap = [(idx, (vals[0] * 255, vals[1] * 255, vals[2] * 255))
                          for idx, vals in colordata]
            return scaledCmap

    # Case #X: unknown format or datatype was the wrong object type
    else:
        raise ValueError("[cmapToColormap] Unknown cmap format or not a cmap!")

    # start the event loop


class MplCmapImageView(pyqtgraph.ImageView):

    def __init__(self, additionalCmaps=[], setColormap=None, **kargs):
        super(MplCmapImageView, self).__init__(**kargs)

        self.gradientEditorItem = self.ui.histogram.item.gradient

        self.activeCm = "white"
        self.mplCmaps = {}

        if len(additionalCmaps) > 0:
            self.registerCmap(additionalCmaps)

        # if setColormap is not None:
        #     self.gradientEditorItem.restoreState(setColormap)

    def registerCmap(self, cmapNames):
        """ Add matplotlib cmaps to the GradientEditors context menu"""
        # self.gradientEditorItem.menu.addSeparator()
        # savedLength = self.gradientEditorItem.length
        # self.gradientEditorItem.length = 100

        # iterate over the list of cmap names and check if they're avaible in MPL
        for cmapName in cmapNames:
            if not hasattr(matplotlib.cm, cmapName):
                print('[extendedimageview] Unknown cmap name: \'{}\'. Your Matplotlib installation might be outdated.'.format(
                    cmapName))
            else:
                # create a Dictionary just as the one at the top of GradientEditorItem.py
                cmap = getattr(matplotlib.cm, cmapName)
                self.mplCmaps[cmapName] = {
                    'ticks': cmapToColormap(cmap), 'mode': 'rgb'}

                # Create the menu entries
                # The following code is copied from pyqtgraph.ImageView.__init__() ...
                px = QtGui.QPixmap(100, 15)
                p = QtGui.QPainter(px)
                self.gradientEditorItem.restoreState(
                    self.mplCmaps[cmapName])

                grad = self.gradientEditorItem.getGradient()
                brush = QtGui.QBrush(grad)
                p.fillRect(QtCore.QRect(200, 200, 200, 30), brush)
                p.end()
                label = QtGui.QLabel()
                label.setPixmap(px)
                label.setContentsMargins(1, 1, 1, 1)
                act = QtGui.QWidgetAction(self.gradientEditorItem)
                act.setDefaultWidget(label)

                # act.triggered.connect(self.cmapClicked)
                act.name = cmapName
                self.gradientEditorItem.menu.addAction(act)
        # self.gradientEditorItem.length = savedLength

    def cmapClicked(self, b=None):
        """onclick handler for our custom entries in the GradientEditorItem's context menu"""
        act = self.sender()
        self.gradientEditorItem.restoreState(self.mplCmaps[act.name])
        self.activeCm = act.name


if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app = QtGui.QApplication([])

    # Create window with ImageView widget
    win = QtGui.QMainWindow()
    win.resize(800, 800)

    imv = MplCmapImageView(
        additionalCmaps=['jet'])
    win.setCentralWidget(imv)
    win.show()
    win.setWindowTitle('pyqtgraph example: ImageView')

    # Create random 3D data set with noisy signals
    img = pyqtgraph.gaussianFilter(
        np.random.normal(size=(200, 200)), (5, 5)) * 20 + 100
    img = img[np.newaxis, :, :]
    decay = np.exp(-np.linspace(0, 0.3, 100))[:, np.newaxis, np.newaxis]
    data = np.random.normal(size=(2, 2, 2))
    # data += img * decay
    # data += 2

    imv.setImage(data, xvals=np.linspace(1., 3., data.shape[0]))

    QtGui.QApplication.instance().exec_()
