from PyQt5 import QtCore, QtGui, QtWidgets

from threading import Thread # This will support us for multithreading
from functools import partial
import sounddevice as sd
import simpleaudio as sa
import numpy as np

class Guitar(QtWidgets.QWidget):
    def __init__(self):

        """Initializer."""
        super().__init__()
        self.duration = 0.48
        self.setupUi()

    def setupUi(self):
        self.setObjectName("centralwidget")
        self.frequency_tons = {"E1": 82, "A": 110, "D": 147, "G": 196, "B": 247, "E2": 330}

        # Add image of drums
        drumphoto = QtWidgets.QLabel(self)
        drumImg = QtGui.QPixmap('images/guitar.png').scaled(650,265)
        drumphoto.setPixmap(drumImg)
        drumphoto.setGeometry(QtCore.QRect(0, 0, 650,265))

        # Buttons
        self.Btn1 = QtWidgets.QPushButton(self)
        self.Btn1.setGeometry(455, 114, 50, 5)
        self.Btn1.setStyleSheet("""QPushButton {
                                        background: transparent;border-radius: 8px; padding: 6px;
                                    }
                                    QPushButton:hover {
                                        background-color: #160063;
                                    }
                                    QPushButton:pressed {
                                        background-color: #070426;
                                    }""")

        self.Btn2 = QtWidgets.QPushButton(self)
        self.Btn2.setGeometry(455, 122, 50, 5)
        self.Btn2.setStyleSheet("""QPushButton {
                                        background: transparent;border-radius: 8px; padding: 6px;
                                    }
                                    QPushButton:hover {
                                        background-color: #160063;
                                    }
                                    QPushButton:pressed {
                                        background-color: #070426;
                                    }""")

        self.Btn3 = QtWidgets.QPushButton(self)
        self.Btn3.setGeometry(455, 129, 50, 5)
        self.Btn3.setStyleSheet("""QPushButton {
                                        background: transparent;border-radius: 8px; padding: 6px;
                                    }
                                    QPushButton:hover {
                                        background-color: #160063;
                                    }
                                    QPushButton:pressed {
                                        background-color: #070426;
                                    }""")

        self.Btn4 = QtWidgets.QPushButton(self)
        self.Btn4.setGeometry(455, 136, 50, 5)
        self.Btn4.setStyleSheet("border: 3px solid blue; border-radius: 40px;")
        self.Btn4.setStyleSheet("""QPushButton {
                                        background: transparent;border-radius: 8px; padding: 6px;
                                    }
                                    QPushButton:hover {
                                        background-color: #160063;
                                    }
                                    QPushButton:pressed {
                                        background-color: #070426;
                                    }""")
        
        self.Btn5 = QtWidgets.QPushButton(self)
        self.Btn5.setGeometry(455, 140, 50, 5)
        self.Btn5.setStyleSheet("border: 3px solid blue; border-radius: 40px;")
        self.Btn5.setStyleSheet("""QPushButton {
                                        background: transparent;border-radius: 8px; padding: 6px;
                                    }
                                    QPushButton:hover {
                                        background-color: #160063;
                                    }
                                    QPushButton:pressed {
                                        background-color: #070426;
                                    }""")

        self.Btn6 = QtWidgets.QPushButton(self)
        self.Btn6.setGeometry(455, 150, 50, 5)
        self.Btn6.setStyleSheet("border: 3px solid blue; border-radius: 40px;")
        self.Btn6.setStyleSheet("""QPushButton {
                                        background: transparent;border-radius: 8px; padding: 6px;
                                    }
                                    QPushButton:hover {
                                        background-color: #160063;
                                    }
                                    QPushButton:pressed {
                                        background-color: #070426;
                                    }""")

        self.Btn1.raise_()
        self.Btn2.raise_()
        self.Btn3.raise_()
        self.Btn4.raise_()
        self.Btn5.raise_()
        self.Btn6.raise_()

        self.connect()
        self.retranslateUi()

    def changeDuration(self):
        if self.duration == 0.50:
            self.duration = 0.48
        else :
            self.duration = 0.50

    def connect(self):
        self.Btn1.clicked.connect(partial(self.generateGuitar, self.frequency_tons["E1"]))
        self.Btn2.clicked.connect(partial(self.generateGuitar, self.frequency_tons["A"]))
        self.Btn3.clicked.connect(partial(self.generateGuitar, self.frequency_tons["D"]))
        self.Btn4.clicked.connect(partial(self.generateGuitar, self.frequency_tons["G"]))
        self.Btn5.clicked.connect(partial(self.generateGuitar, self.frequency_tons["B"]))
        self.Btn6.clicked.connect(partial(self.generateGuitar, self.frequency_tons["E2"]))

    def karplus_strong(self, wavetable, n_samples):
        """Synthesizes a new waveform from an existing wavetable, modifies last sample by averaging."""
        samples = []
        current_sample = 0
        previous_value = 0
        while len(samples) < n_samples:
            wavetable[current_sample] = self.duration * (wavetable[current_sample] + previous_value)
            samples.append(wavetable[current_sample])
            previous_value = samples[-1]
            current_sample += 1
            current_sample = current_sample % wavetable.size
        return np.array(samples)

    def generateGuitar(self, freq):
        fs = 44100
        wavetable_size = fs // freq

        wavetable = (3 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float64)
        sample = self.karplus_strong(wavetable, 2 * fs)
        sd.play(sample, fs)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Btn1.setShortcut(_translate("MainWindow", "1"))
        self.Btn2.setShortcut(_translate("MainWindow", "2"))
        self.Btn3.setShortcut(_translate("MainWindow", "3"))
        self.Btn4.setShortcut(_translate("MainWindow", "4"))
        self.Btn5.setShortcut(_translate("MainWindow", "5"))
        self.Btn6.setShortcut(_translate("MainWindow", "6"))