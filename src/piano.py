from PyQt5 import QtCore, QtGui, QtWidgets

from threading import Thread # This will support us for multithreading
from functools import partial
import simpleaudio as sa
import numpy as np
import winsound
from scipy.io.wavfile import *

class Piano(QtWidgets.QWidget):
    def __init__(self):
        
        """Initializer."""
        super().__init__()
        
        self.pianoModes = { 0: 0.1,
                            1: 0.2,
                            2: 0.3, 
                            3: 0.4, 
                            4: 0.5, 
                            5: 0.6, 
                            6: 0.7 }
        
        self.allkeysInput = None
        self.lastkeyInput = None
        
        self.samplerate = 44100
        self.base_freq = 261.63
        
        self.duration = 0.5

        self.setupUi()
 
    def setMode(self, index):
        self.duration = self.pianoModes.get(index)

    def setInputs(self, allkeysInput, lastkeyInput):
        self.allkeysInput = allkeysInput
        self.lastkeyInput = lastkeyInput


    def setEnteredKey(self, key, allKeysInput, lastKeyInput):
        lastKeyInput.setText(key)
        allKeysInput.setText(allKeysInput.text() + " " + key)

    def setupUi(self):
        self.setObjectName("centralwidget")
    
        # Buttons
        self.c4 = QtWidgets.QPushButton(self)
        self.c4.setGeometry(QtCore.QRect(20, 30, 41, 181))
        self.c4.setStyleSheet("""#c4 {
            color: #000;
            padding-top:65px;
            background-color: rgb(242, 242, 242);
            background-color: qlineargradient(spread:pad, x1:1, y1:0.711, x2:0.903455, y2:0.711, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));
        }
        #c4:pressed {
            background-color: rgb(250, 250, 250);
        }""")

        self.c4.setText("A")
        self.c4.setObjectName("c4")
        self.d4 = QtWidgets.QPushButton(self)
        self.d4.setGeometry(QtCore.QRect(60, 30, 41, 181))
        self.d4.setStyleSheet("#d4{\n"
    "color: #000;"
    "padding-top:65px;"
    "background-color: rgb(242, 242, 242);\n"
    "background-color: qlineargradient(spread:pad, x1:1, y1:0.711, x2:0.903455, y2:0.711, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "#d4:pressed{\n"
    "background-color: rgb(250, 250, 250);\n"
    "\n"
    "}")
        self.d4.setText("S")
        self.d4.setObjectName("d4")
        self.c40 = QtWidgets.QPushButton(self)
        self.c40.setGeometry(QtCore.QRect(40, 30, 31, 111))
        self.c40.setStyleSheet("#c40{\n"
    "color: #fff;"
    "padding-top:65px;"
    "background-color: rgb(0, 0, 0);\n"
    "background-color: qlineargradient(spread:pad, x1:0.028, y1:0.619, x2:1, y2:0.494, stop:0.852273 rgba(0, 0, 0, 250), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "#c40:pressed{\n"
    "background-color: rgb(0, 0, 0);\n"
    "\n"
    "    background-color: qlineargradient(spread:pad, x1:0.857955, y1:0.0170455, x2:1, y2:0, stop:0.125 rgba(0, 0, 0, 255), stop:0.977273 rgba(255, 255, 255, 255));\n"
    "\n"
    "}\n"
    "")
        self.c40.setText("Q")
        self.c40.setObjectName("c40")
        self.d40 = QtWidgets.QPushButton(self)
        self.d40.setGeometry(QtCore.QRect(80, 30, 31, 111))
        self.d40.setStyleSheet("#d40{\n"
    "color: #fff;"
    "padding-top:65px;"
    "background-color: rgb(0, 0, 0);\n"
    "background-color: qlineargradient(spread:pad, x1:0.028, y1:0.619, x2:1, y2:0.494, stop:0.852273 rgba(0, 0, 0, 250), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "#d40:pressed{\n"
    "background-color: rgb(0, 0, 0);\n"
    "\n"
    "    background-color: qlineargradient(spread:pad, x1:0.857955, y1:0.0170455, x2:1, y2:0, stop:0.125 rgba(0, 0, 0, 255), stop:0.977273 rgba(255, 255, 255, 255));\n"
    "\n"
    "}\n"
    "")
        self.d40.setText("W")
        self.d40.setObjectName("d40")
        self.e4 = QtWidgets.QPushButton(self)
        self.e4.setGeometry(QtCore.QRect(100, 30, 41, 181))
        self.e4.setStyleSheet("#e4{\n"
    "color: #000;"
    "padding-top:65px;"
    "background-color: rgb(242, 242, 242);\n"
    "background-color: qlineargradient(spread:pad, x1:1, y1:0.711, x2:0.903455, y2:0.711, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "\n"
    "\n"
    "#e4:pressed{\n"
    "background-color: rgb(250, 250, 250);\n"
    "\n"
    "}")
        self.e4.setText("D")
        self.e4.setObjectName("e4")
        self.f4 = QtWidgets.QPushButton(self)
        self.f4.setGeometry(QtCore.QRect(140, 30, 41, 181))
        self.f4.setStyleSheet("#f4{\n"
    "color: #000;"
    "padding-top:65px;"
    "background-color: rgb(242, 242, 242);\n"
    "background-color: qlineargradient(spread:pad, x1:1, y1:0.711, x2:0.903455, y2:0.711, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "\n"
    "\n"
    "#f4:pressed{\n"
    "background-color: rgb(250, 250, 250);\n"
    "\n"
    "}")
        self.f4.setText("F")
        self.f4.setObjectName("f4")
        self.g4 = QtWidgets.QPushButton(self)
        self.g4.setGeometry(QtCore.QRect(180, 30, 41, 181))
        self.g4.setStyleSheet("#g4{\n"
    "color: #000;"
    "padding-top:65px;"
    "background-color: rgb(242, 242, 242);\n"
    "background-color: qlineargradient(spread:pad, x1:1, y1:0.711, x2:0.903455, y2:0.711, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "\n"
    "\n"
    "#g4:pressed{\n"
    "background-color: rgb(250, 250, 250);\n"
    "\n"
    "}")
        self.g4.setText("G")
        self.g4.setObjectName("g4")
        self.a4 = QtWidgets.QPushButton(self)
        self.a4.setGeometry(QtCore.QRect(220, 30, 41, 181))
        self.a4.setStyleSheet("#a4{\n"
    "color: #000;"
    "padding-top:65px;"
    "background-color: rgb(242, 242, 242);\n"
    "background-color: qlineargradient(spread:pad, x1:1, y1:0.711, x2:0.903455, y2:0.711, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "\n"
    "\n"
    "#a4:pressed{\n"
    "background-color: rgb(250, 250, 250);\n"
    "\n"
    "}")
        self.a4.setText("H")
        self.a4.setObjectName("a4")
        self.b4 = QtWidgets.QPushButton(self)
        self.b4.setGeometry(QtCore.QRect(260, 30, 41, 181))
        self.b4.setStyleSheet("#b4{\n"
    "color: #000;"
    "padding-top:65px;"
    "background-color: rgb(242, 242, 242);\n"
    "background-color: qlineargradient(spread:pad, x1:1, y1:0.711, x2:0.903455, y2:0.711, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "\n"
    "\n"
    "#b4:pressed{\n"
    "background-color: rgb(250, 250, 250);\n"
    "\n"
    "}")
        self.b4.setText("J")
        self.b4.setObjectName("b4")
        self.c5 = QtWidgets.QPushButton(self)
        self.c5.setGeometry(QtCore.QRect(300, 30, 41, 181))
        self.c5.setStyleSheet("#c5{\n"
    "color: #000;"
    "padding-top:65px;"
    "background-color: rgb(242, 242, 242);\n"
    "background-color: qlineargradient(spread:pad, x1:1, y1:0.711, x2:0.903455, y2:0.711, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "\n"
    "\n"
    "#c5:pressed{\n"
    "background-color: rgb(250, 250, 250);\n"
    "\n"
    "}")
        self.c5.setText("K")
        self.c5.setObjectName("c5")
        self.d5 = QtWidgets.QPushButton(self)
        self.d5.setGeometry(QtCore.QRect(340, 30, 41, 181))
        self.d5.setStyleSheet("#d5{\n"
    "color: #000;"
    "padding-top:65px;"
    "background-color: rgb(242, 242, 242);\n"
    "background-color: qlineargradient(spread:pad, x1:1, y1:0.711, x2:0.903455, y2:0.711, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "\n"
    "\n"
    "#d5:pressed{\n"
    "background-color: rgb(250, 250, 250);\n"
    "\n"
    "}")
        self.d5.setText("L")
        self.d5.setObjectName("d5")
        self.a5 = QtWidgets.QPushButton(self)
        self.a5.setGeometry(QtCore.QRect(500, 30, 41, 181))
        self.a5.setStyleSheet("#a5{\n"
    "color: #000;"
    "padding-top:65px;"
    "background-color: rgb(242, 242, 242);\n"
    "background-color: qlineargradient(spread:pad, x1:1, y1:0.711, x2:0.903455, y2:0.711, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "\n"
    "\n"
    "#a5:pressed{\n"
    "background-color: rgb(250, 250, 250);\n"
    "\n"
    "}")
        self.a5.setText("V")
        self.a5.setObjectName("a5")
        self.e5 = QtWidgets.QPushButton(self)
        self.e5.setGeometry(QtCore.QRect(380, 30, 41, 181))
        self.e5.setStyleSheet("#e5{\n"
    "color: #000;"
    "padding-top:65px;"
    "background-color: rgb(242, 242, 242);\n"
    "background-color: qlineargradient(spread:pad, x1:1, y1:0.711, x2:0.903455, y2:0.711, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "\n"
    "\n"
    "#e5:pressed{\n"
    "background-color: rgb(250, 250, 250);\n"
    "\n"
    "}")
        self.e5.setText("Z")
        self.e5.setObjectName("e5")
        self.g5 = QtWidgets.QPushButton(self)
        self.g5.setGeometry(QtCore.QRect(460, 30, 41, 181))
        self.g5.setStyleSheet("#g5{\n"
    "color: #000;"
    "padding-top:65px;"
    "background-color: rgb(242, 242, 242);\n"
    "background-color: qlineargradient(spread:pad, x1:1, y1:0.711, x2:0.903455, y2:0.711, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "\n"
    "\n"
    "#g5:pressed{\n"
    "background-color: rgb(250, 250, 250);\n"
    "\n"
    "}")
        self.g5.setText("C")
        self.g5.setObjectName("g5")
        self.f5 = QtWidgets.QPushButton(self)
        self.f5.setGeometry(QtCore.QRect(420, 30, 41, 181))
        self.f5.setStyleSheet("#f5{\n"
    "color: #000;"
    "padding-top:65px;"
    "background-color: rgb(242, 242, 242);\n"
    "background-color: qlineargradient(spread:pad, x1:1, y1:0.711, x2:0.903455, y2:0.711, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "\n"
    "\n"
    "#f5:pressed{\n"
    "background-color: rgb(250, 250, 250);\n"
    "\n"
    "}")
        self.f5.setText("X")
        self.f5.setObjectName("f5")
        self.b5 = QtWidgets.QPushButton(self)
        self.b5.setGeometry(QtCore.QRect(540, 30, 41, 181))
        self.b5.setStyleSheet("#b5{\n"
    "color: #000;"
    "padding-top:65px;"
    "background-color: rgb(242, 242, 242);\n"
    "background-color: qlineargradient(spread:pad, x1:1, y1:0.711, x2:0.903455, y2:0.711, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "\n"
    "\n"
    "#b5:pressed{\n"
    "background-color: rgb(250, 250, 250);\n"
    "\n"
    "}")
        self.b5.setText("B")
        self.b5.setObjectName("b5")
        self.c6 = QtWidgets.QPushButton(self)
        self.c6.setGeometry(QtCore.QRect(580, 30, 41, 181))
        self.c6.setStyleSheet("#c6{\n"
    "color: #000;"
    "padding-top:65px;"
    "background-color: rgb(242, 242, 242);\n"
    "background-color: qlineargradient(spread:pad, x1:1, y1:0.711, x2:0.903455, y2:0.711, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "\n"
    "\n"
    "#c6:pressed{\n"
    "background-color: rgb(250, 250, 250);\n"
    "\n"
    "}")
        self.c6.setText("N")
        self.c6.setObjectName("c6")
        self.f40 = QtWidgets.QPushButton(self)
        self.f40.setGeometry(QtCore.QRect(160, 30, 31, 111))
        self.f40.setStyleSheet("#f40{\n"
    "color: #fff;"
    "padding-top:65px;"
    "background-color: rgb(0, 0, 0);\n"
    "background-color: qlineargradient(spread:pad, x1:0.028, y1:0.619, x2:1, y2:0.494, stop:0.852273 rgba(0, 0, 0, 250), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "#f40:pressed{\n"
    "background-color: rgb(0, 0, 0);\n"
    "\n"
    "    background-color: qlineargradient(spread:pad, x1:0.857955, y1:0.0170455, x2:1, y2:0, stop:0.125 rgba(0, 0, 0, 255), stop:0.977273 rgba(255, 255, 255, 255));\n"
    "\n"
    "}\n"
    "")
        self.f40.setText("E")
        self.f40.setObjectName("f40")
        self.g40 = QtWidgets.QPushButton(self)
        self.g40.setGeometry(QtCore.QRect(200, 30, 31, 111))
        self.g40.setStyleSheet("#g40{\n"
    "color: #fff;"
    "padding-top:65px;"
    "background-color: rgb(0, 0, 0);\n"
    "background-color: qlineargradient(spread:pad, x1:0.028, y1:0.619, x2:1, y2:0.494, stop:0.852273 rgba(0, 0, 0, 250), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "#g40:pressed{\n"
    "background-color: rgb(0, 0, 0);\n"
    "\n"
    "    background-color: qlineargradient(spread:pad, x1:0.857955, y1:0.0170455, x2:1, y2:0, stop:0.125 rgba(0, 0, 0, 255), stop:0.977273 rgba(255, 255, 255, 255));\n"
    "\n"
    "}\n"
    "")
        self.g40.setText("R")
        self.g40.setObjectName("g40")
        self.a40 = QtWidgets.QPushButton(self)
        self.a40.setGeometry(QtCore.QRect(240, 30, 31, 111))
        self.a40.setStyleSheet("#a40{\n"
    "color: #fff;"
    "padding-top:65px;"
    "background-color: rgb(0, 0, 0);\n"
    "background-color: qlineargradient(spread:pad, x1:0.028, y1:0.619, x2:1, y2:0.494, stop:0.852273 rgba(0, 0, 0, 250), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "#a40:pressed{\n"
    "background-color: rgb(0, 0, 0);\n"
    "\n"
    "    background-color: qlineargradient(spread:pad, x1:0.857955, y1:0.0170455, x2:1, y2:0, stop:0.125 rgba(0, 0, 0, 255), stop:0.977273 rgba(255, 255, 255, 255));\n"
    "\n"
    "}\n"
    "")
        self.a40.setText("T")
        self.a40.setObjectName("a40")
        self.c50 = QtWidgets.QPushButton(self)
        self.c50.setGeometry(QtCore.QRect(320, 30, 31, 111))
        self.c50.setStyleSheet("#c50{\n"
    "color: #fff;"
    "padding-top:65px;"
    "background-color: rgb(0, 0, 0);\n"
    "background-color: qlineargradient(spread:pad, x1:0.028, y1:0.619, x2:1, y2:0.494, stop:0.852273 rgba(0, 0, 0, 250), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "#c50:pressed{\n"
    "background-color: rgb(0, 0, 0);\n"
    "\n"
    "    background-color: qlineargradient(spread:pad, x1:0.857955, y1:0.0170455, x2:1, y2:0, stop:0.125 rgba(0, 0, 0, 255), stop:0.977273 rgba(255, 255, 255, 255));\n"
    "\n"
    "}\n"
    "")
        self.c50.setText("Y")
        self.c50.setObjectName("c50")
        self.d50 = QtWidgets.QPushButton(self)
        self.d50.setGeometry(QtCore.QRect(360, 30, 31, 111))
        self.d50.setStyleSheet("""
                            #d50{
                                color: #fff;
                                padding-top:65px;
                                background-color: rgb(0, 0, 0);
                                background-color: qlineargradient(spread:pad, x1:0.028, y1:0.619, x2:1, y2:0.494, stop:0.852273 rgba(0, 0, 0, 250), stop:1 rgba(255, 255, 255, 255));
                            }
                            #d50:pressed {
                                background-color: rgb(0, 0, 0);
                                background-color: qlineargradient(spread:pad, x1:0.857955, y1:0.0170455, x2:1, y2:0, stop:0.125 rgba(0, 0, 0, 255), stop:0.977273 rgba(255, 255, 255, 255));
                            }
                            """)
        self.d50.setText("U")
        self.d50.setObjectName("d50")
        self.f50 = QtWidgets.QPushButton(self)
        self.f50.setGeometry(QtCore.QRect(440, 30, 31, 111))
        self.f50.setStyleSheet("#f50{\n"
    "color: #fff;"
    "padding-top:65px;"
    "background-color: rgb(0, 0, 0);\n"
    "background-color: qlineargradient(spread:pad, x1:0.028, y1:0.619, x2:1, y2:0.494, stop:0.852273 rgba(0, 0, 0, 250), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "#f50:pressed{\n"
    "background-color: rgb(0, 0, 0);\n"
    "\n"
    "    background-color: qlineargradient(spread:pad, x1:0.857955, y1:0.0170455, x2:1, y2:0, stop:0.125 rgba(0, 0, 0, 255), stop:0.977273 rgba(255, 255, 255, 255));\n"
    "\n"
    "}\n"
    "")
        self.f50.setText("I")
        self.f50.setObjectName("f50")

        self.g50 = QtWidgets.QPushButton(self)
        self.g50.setGeometry(QtCore.QRect(480, 30, 31, 111))
        self.g50.setStyleSheet("#g50{\n"
    "color: #fff;"
    "padding-top:65px;"
    "background-color: rgb(0, 0, 0);\n"
    "background-color: qlineargradient(spread:pad, x1:0.028, y1:0.619, x2:1, y2:0.494, stop:0.852273 rgba(0, 0, 0, 250), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "#g50:pressed{\n"
    "background-color: rgb(0, 0, 0);\n"
    "\n"
    "    background-color: qlineargradient(spread:pad, x1:0.857955, y1:0.0170455, x2:1, y2:0, stop:0.125 rgba(0, 0, 0, 255), stop:0.977273 rgba(255, 255, 255, 255));\n"
    "\n"
    "}\n"
    "")
        self.g50.setText("O")
        self.g50.setObjectName("g50")

        self.a50 = QtWidgets.QPushButton(self)
        self.a50.setGeometry(QtCore.QRect(520, 30, 31, 111))
        self.a50.setStyleSheet("#a50{\n"
    "color: #fff;"
    "padding-top:65px;"
    "background-color: rgb(0, 0, 0);\n"
    "background-color: qlineargradient(spread:pad, x1:0.028, y1:0.619, x2:1, y2:0.494, stop:0.852273 rgba(0, 0, 0, 250), stop:1 rgba(255, 255, 255, 255));\n"
    "}\n"
    "#a50:pressed{\n"
    "background-color: rgb(0, 0, 0);\n"
    "\n"
    "    background-color: qlineargradient(spread:pad, x1:0.857955, y1:0.0170455, x2:1, y2:0, stop:0.125 rgba(0, 0, 0, 255), stop:0.977273 rgba(255, 255, 255, 255));\n"
    "\n"
    "}\n"
    "")
        self.a50.setText("P")
        self.a50.setObjectName("a50")
        
        self.connect()
        self.retranslateUi()

    ###########################################################

    def playInstrumentKey(self, music_note, note_num):
        if note_num == 4:
            self.base_freq = 261.63
        elif note_num == 5:
            self.base_freq = 523.25
        elif note_num == 6:
            self.base_freq = 1046.50

        self.setEnteredKey(music_note, self.allkeysInput, self.lastkeyInput)
        data = self.get_song_data(music_note)
        data = data * (16300/np.max(data))
        write('./src/piano.wav', self.samplerate, data.astype(np.int16))
        winsound.PlaySound('./src/piano.wav', winsound.SND_ALIAS)

    def get_song_data(self, music_notes):
        note_freqs = self.get_piano_notes()
        song = self.get_wave(note_freqs[music_notes])
        return song.astype(np.int16)

    def get_piano_notes(self):
        '''
        Returns a dict object for all the piano 
        note's frequencies
        '''
        # White keys are in Uppercase and black keys (sharps) are in lowercase
        octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
        base_freq = self.base_freq #Frequency of Note C4
        
        note_freqs = {octave[i]: base_freq * pow(2,(i/12)) for i in range(len(octave))}        
        note_freqs[''] = 0.0
        
        return note_freqs
        
    def get_wave(self, freq):
        amplitude = 4096
        t = np.linspace(0,  self.duration, int(self.samplerate * self.duration))
        wave = amplitude * np.sin(2 * np.pi * freq * t)
        
        return wave   
        
    ###########################################################
  
    def connect(self):        
        # These are white keys
        self.c4.clicked.connect(partial(self.playInstrumentKey, "C", 4))
        self.d4.clicked.connect(partial(self.playInstrumentKey, "D", 4))
        self.e4.clicked.connect(partial(self.playInstrumentKey, "E", 4))
        self.f4.clicked.connect(partial(self.playInstrumentKey, "F", 4))
        self.g4.clicked.connect(partial(self.playInstrumentKey, "G", 4)) 
        self.a4.clicked.connect(partial(self.playInstrumentKey, "A", 4)) 
        self.b4.clicked.connect(partial(self.playInstrumentKey, "B", 4))

        self.c5.clicked.connect(partial(self.playInstrumentKey, "C", 5)) 
        self.d5.clicked.connect(partial(self.playInstrumentKey, "D", 5)) 
        self.e5.clicked.connect(partial(self.playInstrumentKey, "E", 5)) 
        self.f5.clicked.connect(partial(self.playInstrumentKey, "F", 5))
        self.g5.clicked.connect(partial(self.playInstrumentKey, "G", 5)) 
        self.a5.clicked.connect(partial(self.playInstrumentKey, "A", 5)) 
        self.b5.clicked.connect(partial(self.playInstrumentKey, "B", 5)) 
        self.c6.clicked.connect(partial(self.playInstrumentKey, "C", 6))
        
        # These are the black keys
        self.c40.clicked.connect(partial(self.playInstrumentKey, "c", 4)) 
        self.d40.clicked.connect(partial(self.playInstrumentKey, "d", 4)) 
        self.f40.clicked.connect(partial(self.playInstrumentKey, "f", 4))
        self.g40.clicked.connect(partial(self.playInstrumentKey, "g", 4)) 
        self.a40.clicked.connect(partial(self.playInstrumentKey, "a", 4))

        self.c50.clicked.connect(partial(self.playInstrumentKey, "c", 5)) 
        self.d50.clicked.connect(partial(self.playInstrumentKey, "d", 5)) 
        self.f50.clicked.connect(partial(self.playInstrumentKey, "f", 5))
        self.g50.clicked.connect(partial(self.playInstrumentKey, "g", 5)) 
        self.a50.clicked.connect(partial(self.playInstrumentKey, "a", 5))
        

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.c4.setShortcut(_translate("MainWindow", "A"))
        self.d4.setShortcut(_translate("MainWindow", "S"))
        self.c40.setShortcut(_translate("MainWindow", "Q"))
        self.d40.setShortcut(_translate("MainWindow", "W"))
        self.e4.setShortcut(_translate("MainWindow", "D"))
        self.f4.setShortcut(_translate("MainWindow", "F"))
        self.g4.setShortcut(_translate("MainWindow", "G"))
        self.a4.setShortcut(_translate("MainWindow", "H"))
        self.b4.setShortcut(_translate("MainWindow", "J"))
        self.c5.setShortcut(_translate("MainWindow", "K"))
        self.d5.setShortcut(_translate("MainWindow", "L"))
        self.a5.setShortcut(_translate("MainWindow", "V"))
        self.e5.setShortcut(_translate("MainWindow", "Z"))
        self.g5.setShortcut(_translate("MainWindow", "C"))
        self.f5.setShortcut(_translate("MainWindow", "X"))
        self.b5.setShortcut(_translate("MainWindow", "B"))
        self.c6.setShortcut(_translate("MainWindow", "N"))
        self.f40.setShortcut(_translate("MainWindow", "E"))
        self.g40.setShortcut(_translate("MainWindow", "R"))
        self.a40.setShortcut(_translate("MainWindow", "T"))
        self.c50.setShortcut(_translate("MainWindow", "Y"))
        self.d50.setShortcut(_translate("MainWindow", "U"))
        self.f50.setShortcut(_translate("MainWindow", "I"))
        self.g50.setShortcut(_translate("MainWindow", "O"))
        self.a50.setShortcut(_translate("MainWindow", "P"))