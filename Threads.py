import os

from PyQt5.QtCore import QObject, QThread, pyqtSignal
import numpy as np
# Logging configuration
import logging
logging.basicConfig(filename="errlog.log",
                    filemode="a",
                    format="(%(asctime)s)  | %(name)s | %(levelname)s:%(message)s",
                    datefmt="%d  %B  %Y , %H:%M:%S",
                    level=logging.INFO)


class equalizeWorker(QObject):
    fftData = pyqtSignal(np.ndarray)
    freqFftData = pyqtSignal(np.ndarray)
    equalizedData = pyqtSignal(np.ndarray)
    finished = pyqtSignal()

    def run(self, status, data, samplerate=0):
        """Long-running task."""
        # data can be data in real time or fftData
        if status:
            self.fourierTransform(data, samplerate)
        else:
            self.inverseFourierTransform(data)
        self.finished.emit()

    def fourierTransform(self, data, samplerate):
        try:
            self.fftData.emit(np.copy(np.fft.rfft(data)))
            self.freqFftData.emit(np.fft.rfftfreq(n=len(data), d=1./samplerate))
        except:
            logging.error(f"Failed to make DFT on array with {np.ndim(data)} dimension and shape = {np.shape(data)}.")

    def inverseFourierTransform(self, fftData):
        try:
            equalizedData = np.fft.irfft(fftData)
            if np.ndim(equalizedData) == 1:
                equalizedData = np.asanyarray(equalizedData, dtype=np.int16)
            self.equalizedData.emit(equalizedData)
        except:
            logging.error(f"Failed to make Inverse DFT on array with {np.ndim(fftData)} dimension and shape = {np.shape(fftData)}.")