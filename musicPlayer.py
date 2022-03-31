# !/usr/bin/python

# importing Qt widgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Definition of Main Color Palette
from Defs import COLOR1, COLOR2, COLOR3, COLOR4, COLOR5

# importing numpy and pandas
import numpy as np
import pandas as pd

# importing pyqtgraph as pg
import pyqtgraph as pg

class Player(pg.GraphicsLayoutWidget):
    """Main Plot."""
    def __init__(self,title=""):
        
        """Initializer."""
        super().__init__()
        self.setMaximumHeight(400)
        self.plot = self.addPlot()

        self.plot.setTitle(title, size="15pt")
        self.plot.setLabel('bottom', 'Time', 's')
        
        self.setBackground(f'{COLOR1}')
        self.plot.getAxis('left').setPen(f"{COLOR4}")
        self.plot.getAxis('bottom').setPen(f"{COLOR4}")

        self.region = pg.LinearRegionItem()
        self.region.setRegion([0.2, 0.21])
        
        self.plot.addItem(self.region, ignoreBounds=True)

        self.y = [0]
        self.x = [0]

    def plotSignal(self, x, y):
        # Clear prev plot
        self.clearPlot()
        
        # Set data
        self.x = x
        self.y = y

        # Plot
        plotLine = self.plot.plot(x,y)
        self.region.setClipItem(plotLine)
        self.changeRegion(self, 0)


    def changeRegion(self, current):
        # Current variable represent current time in seconds
        self.region.setRegion([current, current+5])

    def clearPlot(self):
        self.plot.clear()
