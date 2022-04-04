from PyQt5 import QtCore, QtGui, QtWidgets

from threading import Thread # This will support us for multithreading
from functools import partial
import simpleaudio as sa
import numpy as np

class Drum(QtWidgets.QWidget):
    def __init__(self):
        
        """Initializer."""
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("centralwidget")

        # Add image of drums
        drumphoto = QtWidgets.QLabel(self)
        drumImg = QtGui.QPixmap('images/drum.png').scaled(500,300)
        drumphoto.setPixmap(drumImg)
        drumphoto.setGeometry(QtCore.QRect(100, 100, 500, 300))

        # Buttons
        self.rightBtn = QtWidgets.QPushButton(self)
        self.rightBtn.setGeometry(450, 105, 30, 30)
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
        self.leftBtn.setGeometry(205, 125, 30, 30)
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

    def getOctave(self):
        return self.octave

    def get_instrument_notes(self, base_freq, denominator):
        note_freq = {self.getOctave()[note_index]: base_freq * pow(self.piano_mode, (note_index / denominator)) for note_index in
                     range(len(self.getOctave()))}
        note_freq[''] = 0.0  # silent freq
        return note_freq
    
    def amplifying_wave(self,data):
        data = data * (16300/np.max(data))  # amplifying the wave
        data = data.astype(np.int16)
        return data

    def get_wave(self, freq, duration=0.5):
        amplitude = 4096
        self.sample_rate = 44100  # Hz
        time = np.linspace(0, duration, int(44100 * duration))
        wave = amplitude * np.sin(2 * np.pi * freq * time)
        return wave

    def played_instrument_key(self, key_index, base_freq, den):
        notesFreqs = self.get_instrument_notes(base_freq, den)
        sound = self.getOctave()[key_index]
        song = [self.get_wave(notesFreqs[note]) for note in sound.split('-')]
        song = np.concatenate(song)
        data = song.astype(np.int16)
        data=self.amplifying_wave(data)
        sa.play_buffer(data, 1, 2, 44100)

    def connect(self):        
        self.rightBtn.clicked.connect(partial(self.played_instrument_key, 0, 523.25, 12)) 
        self.leftBtn.clicked.connect(partial(self.played_instrument_key, 0, 587.33, 12))

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.rightBtn.setShortcut(_translate("MainWindow", "]"))
        self.leftBtn.setShortcut(_translate("MainWindow", "["))