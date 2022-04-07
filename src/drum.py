from PyQt5 import QtCore, QtGui, QtWidgets

from threading import Thread # This will support us for multithreading
from functools import partial
import sounddevice as sd
import numpy as np

class Drum(QtWidgets.QWidget):
    def __init__(self):
        
        """Initializer."""
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("centralwidget")
        self.frequency_tons = {"1": 30, "2": 40}
        self.waveAmp = 0.5
    
        # Add image of drums
        drumphoto = QtWidgets.QLabel(self)
        drumImg = QtGui.QPixmap('images/drum.png').scaled(500,300)
        drumphoto.setPixmap(drumImg)
        drumphoto.setGeometry(QtCore.QRect(0, 0, 500, 300))

        # Buttons
        self.rightBtn = QtWidgets.QPushButton(self)
        self.rightBtn.setGeometry(350, 5, 30, 30)
        self.rightBtn.setStyleSheet("""QPushButton {
                                        background: transparent;border-radius: 8px; padding: 6px;
                                    }
                                    QPushButton:hover {
                                        background-color: #a27741;
                                    }
                                    QPushButton:pressed {
                                        background-color: #9c733f;
                                    }""")
        self.rightBtn.setText("R")
        self.rightBtn.setObjectName("rightBtn")

        self.leftBtn = QtWidgets.QPushButton(self)
        self.leftBtn.setGeometry(105, 25, 30, 30)
        self.leftBtn.setStyleSheet("""QPushButton {
                                        background: transparent;border-radius: 8px; padding: 6px;
                                    }
                                    QPushButton:hover {
                                        background-color: #a27741;
                                    }
                                    QPushButton:pressed {
                                        background-color: #9c733f;
                                    }""")
        self.leftBtn.setText("L")
        self.leftBtn.setObjectName("leftBtn")
        
        self.rightBtn.raise_()
        self.leftBtn.raise_()

        self.connect()
        self.retranslateUi()

    def editFreq(self, value, labelText):
        self.frequency_tons["1"] = int(3/4 * value)
        self.frequency_tons["2"] = int(value)
        self.waveAmp = int(value) / 100
        labelText.setText(str(value))

    def connect(self):        
        self.rightBtn.clicked.connect(partial(self.generateDrum, self.frequency_tons["1"])) 
        self.leftBtn.clicked.connect(partial(self.generateDrum, self.frequency_tons["2"]))

    def karplus_strong_drum(self, wavetable, n_samples, prob):
        samples = []
        current_sample = 0
        previous_value = 0
        while len(samples) < n_samples:
            r = np.random.binomial(1, prob)
            sign = float(r == 1) * 2 - 1
            wavetable[current_sample] = sign * self.waveAmp * (wavetable[current_sample] + previous_value)
            samples.append(wavetable[current_sample])
            previous_value = samples[-1]
            current_sample += 1
            current_sample = current_sample % wavetable.size
        return np.array(samples)

    def generateDrum(self, freq):
        fs = 8000
        wavetable_size = fs // freq
        wavetable = np.ones(wavetable_size)

        sample = self.karplus_strong_drum(wavetable, 1 * fs, 0.3)
        sd.play(sample, fs)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.rightBtn.setShortcut(_translate("MainWindow", "]"))
        self.leftBtn.setShortcut(_translate("MainWindow", "["))