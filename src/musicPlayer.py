# !/usr/bin/python
import sys
import os

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

# Logging configuration
import logging
logging.basicConfig(filename="errlog.log",
                    filemode="a",
                    format="(%(asctime)s)  | %(name)s | %(levelname)s:%(message)s",
                    datefmt="%d  %B  %Y , %H:%M:%S",
                    level=os.environ.get("LOGLEVEL", "INFO"))

class Player(pg.GraphicsLayoutWidget):
    """Main Plot."""
    def __init__(self,title=""):
        
        """Initializer."""
        super().__init__()
        self.plot = self.addPlot()
        self.playerPlay = False
        self.y = [0,0]
        self.x = [0,0]
        
        self.plot.setTitle(title, size="13pt")
        self.plot.setLabel('bottom', 'Time', 's')
        
        self.setBackground(f'{COLOR1}')
        self.plot.getAxis('left').setPen(f"{COLOR4}")
        self.plot.getAxis('bottom').setPen(f"{COLOR4}")

        self.region = pg.LinearRegionItem()
        self.region.setEnabled(0)
        self.region.setMovable(False)

        self.plotSignal(0, self.y)
        
        self.changeRegion(0)

        self.plot.addItem(self.region, ignoreBounds=True)
    

    def plotSignal(self, length, y):
    
        # Plot
        self.plotLine = self.plot.plot(self.x, self.y)

        # Change region
        self.changeRegion(0)
        self.region.setClipItem(self.plotLine)


    def changeRegion(self, current):
        # Current variable represent current time in seconds
        self.region.setRegion([current-0.001, current+0.001])

    def updateLimits(self):
        self.plot.setLimits(xMin=0, xMax=np.int(max(self.x)), 
                                 yMin=np.int(min(self.y)), yMax=np.int(max(self.y)))
        self.plot.setYRange(np.int(min(self.y)), np.int(max(self.y)), padding=None, update=True)

    def updateData(self, length, y):        
        if length == 0 :
            length = 1
            
        # Set data
        self.y = y
        self.x = np.linspace(0, length, len(y))

        self.plotLine.setData(self.x, self.y)

        # Change limits
        self.updateLimits()

    def clearPlot(self):
        self.plot.clear()
