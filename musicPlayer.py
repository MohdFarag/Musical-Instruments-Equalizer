# !/usr/bin/python

# importing Qt widgets
from pickle import TRUE
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
        self.plot = self.addPlot()
        self.playerPause = True
        
        #self.setMaximumHeight(400)
        self.plot.setTitle(title, size="13pt")
        self.plot.setLabel('bottom', 'Time', 's')
        
        self.setBackground(f'{COLOR1}')
        self.plot.getAxis('left').setPen(f"{COLOR4}")
        self.plot.getAxis('bottom').setPen(f"{COLOR4}")
        self.plot.setMouseEnabled(False)

        self.region = pg.LinearRegionItem()
        self.region.setEnabled(0)
        self.region.setMovable(False)
        
        self.changeRegion(0)

        self.plot.addItem(self.region, ignoreBounds=True)
    
        self.y = [0]
        self.x = [0]

    def plotSignal(self, length, y):        
        if length == 0 :
            length = 1
            
        # Set data
        self.x = np.linspace(0, length, len(y))
        self.y = y

        # Plot
        plotLine = self.plot.plot(self.x, self.y)
        plotLine.setData(self.x, self.y)  # Update the data.
        
        self.changeRegion(0)
        self.region.setClipItem(plotLine)
        self.updateLimits()

    def changeRegion(self, current):
        # Current variable represent current time in seconds
        self.region.setRegion([current-0.001, current+0.001])

    def updateLimits(self):
        self.plot.setLimits(xMin=min(self.x), xMax=max(self.x), 
                                yMin=min(self.y), yMax=max(self.y))
        self.plot.setXRange(min=0, max=max(self.x), padding=0)

        self.plot.enableAutoRange(axis='y')
        self.plot.setAutoVisible(y=True)


    def clearPlot(self):
        self.plot.clear()
