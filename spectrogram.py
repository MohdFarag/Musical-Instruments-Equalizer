import sys
import os

# matplotlib
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np

# Logging configuration
import logging
logging.basicConfig(filename="errlog.log",
                    filemode="a",
                    format="(%(asctime)s)  | %(name)s | %(levelname)s:%(message)s",
                    datefmt="%d  %B  %Y , %H:%M:%S",
                    level=os.environ.get("LOGLEVEL", "INFO"))

class MplCanvas(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title("Spectrogram", fontweight ="bold")
        self.axes.set_xlabel("Time")
        self.axes.set_ylabel("Frequency")
        super(MplCanvas, self).__init__(self.fig)
    
    data_channel = [np.random.randint(-10,10) for i in range(500)]
    colorPalette = "rainbow"
    
    def addColorBar(self):
        try:
            colormap = plt.cm.get_cmap(self.colorPalette)
            sm = plt.cm.ScalarMappable(cmap=colormap)
            self.colorBarSpectrogram = self.fig.colorbar(sm)
            self.colorBarSpectrogram.solids.set_edgecolor("face")
        except:
            logging.error("Failed to add color bar.")

    def updateColorBar(self):
        colormap = plt.cm.get_cmap(self.colorPalette + "_r")
        sm = plt.cm.ScalarMappable(cmap=colormap)
        self.colorBarSpectrogram.update_normal(sm)

    def set_color(self, colorPalette):
        self.colorPalette = colorPalette

    def set_data_channel(self, data_channel):
        self.data_channel = data_channel

    def plotSignal(self, fs):
        # try:
            self.data_channel = np.array(self.data_channel)
            pxx,  freq, t, self.cax = self.axes.specgram(self.data_channel, Fs=fs, cmap=self.colorPalette, mode="psd")
            self.draw()
        # except:
        #     logging.error("Failed to plot Spectrogram.")  
        #     print("Error:  failed to plot spectrogram")         
        
    def clearSignal(self):
        self.axes.clear()