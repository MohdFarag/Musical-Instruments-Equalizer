# !/usr/bin/python

# import Plotter.py Class
from ast import Num
from importlib.resources import path
from musicPlayer import Player
from spectrogram import MplCanvas
from piano import Piano
from sound import music
from drum import Drum
from Guitar import Guitar


import datetime
# Sound package
from scipy.io import wavfile
import scipy.io
import io

from mutagen.wave import WAVE
import sounddevice as sd
from pydub import AudioSegment
import simpleaudio as sa

# Definition of Main Color Palette
from Defs import COLOR1,COLOR2,COLOR3,COLOR4, COLOR5

# importing Qt widgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import QFileInfo

# importing numpy and pandas
import numpy as np
import pandas as pd

# importing pyqtgraph as pg
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.dockarea import *

# importing sys package
import sys
import os

import logging
logging.basicConfig(filename="logfile.log",
                    filemode="a",
                    format="(%(asctime)s)  | %(name)s | %(levelname)s |  %(message)s ",
                    datefmt="%d  %B  %Y , %H:%M:%S")
logger= logging.getLogger("Logging")

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
        
class Window(QMainWindow):
    """Main Window."""
    def __init__(self):
        
        """Initializer."""
        super().__init__()

        # Initialize Variable
        self.gain_List = [1, 1, 1]
        self.timer = QtCore.QTimer()
        # Time Domain
        self.dataPlot = list()
        self.data = list()
        self.time = list()
        # Length of time
        self.length = 0
        self.samplerate = 0

        # Frequency Domain
        self.fftData = list()
        self.freqFftData = list()

        self.speaker = music()

        # setting Icon
        self.setWindowIcon(QIcon('images/icon.ico'))
          
        # setting  the fixed width of window
        width = 1400
        height = 800
        self.setMinimumSize(width,height)
        
        # setting title
        self.setWindowTitle("Musical Instruments Equalizer")

        # UI contents
        self.createMenuBar()

        #self.createtoolBar()
        self.initUI()
        
        # Status Bar
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet(f"""font-size:13px;
                                 padding: 3px; 
                                 color: {COLOR1}; 
                                 font-weight:900;""")
        self.statusBar.showMessage("Welcome to our application...")
        self.setStatusBar(self.statusBar)

        self.connect()

    # Menu
    def createMenuBar(self):
        # MenuBar
        menuBar = self.menuBar()
        
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        
        openFile = QAction("Open...",self)
        openFile.setShortcut("Ctrl+o")
        openFile.setStatusTip('Open a new signal')
        openFile.triggered.connect(self.browseSignal)

        fileMenu.addAction(openFile)

        quit = QAction("Exit",self)
        quit.setShortcut("Ctrl+q")
        quit.setStatusTip('Exit application')
        quit.triggered.connect(self.exit)
        
        fileMenu.addAction(quit)

        # Add file tab to the menu
        menuBar.addMenu(fileMenu)

        logger.info("menubar has created.")

    # GUI
    def initUI(self):
        centralMainWindow = QWidget(self)
        self.setCentralWidget(centralMainWindow)

        # Outer Layout
        outerLayout = QVBoxLayout()

        ######### INIT GUI #########
        # Initialize tab screen
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""color:{COLOR1}; 
                            font-size:15px;""")

        # TODO: Add tabs and its functions
        self.mainTab = QWidget()
        self.mainTab.setStyleSheet(f"""background: {COLOR4}""")
        self.mainLayout()
        tabs.addTab(self.mainTab, "Music")
        
        self.devicesTab = QWidget()
        self.devicesTab.setStyleSheet(f"""background: {COLOR4}""")
        self.devicesTabLayout(self.devicesTab)
        tabs.addTab(self.devicesTab, "Instruments")

        outerLayout.addWidget(tabs)
        ######### INIT GUI #########
        centralMainWindow.setLayout(outerLayout)

    # Browse signal
    def browseSignal(self):
        path, fileExtension = QFileDialog.getOpenFileName(None, "Load Sound File" ,filter="wav(*.wav)")        
        
        if path == "":
                self.speaker.crash()
                return

        if fileExtension == "wav(*.wav)":
            audio = WAVE(path)
            # contains all the metadata about the wavepack file
            audio_info = audio.info
            self.length = int(audio_info.length)
            self.samplerate, self.data = wavfile.read(path)
            self.data = np.int16(np.mean(self.data, axis=1))

        self.time = np.linspace(0, self.length, len(self.data))
        self.playButton.setIcon(QIcon("images/pause.ico"))
        self.playerPlot.playerPause = False

        # update progress slider
        self.startLabel.setText("00:00")
        self.progressSlider.setMinimum(0)
        self.progressSlider.setMaximum(self.length)
        self.endLabel.setText(str(datetime.timedelta(seconds=self.length))[-5:7])
        
        # Play Sound
        self.speaker.loadFile(path)
        
        # Compute the one-dimensional discrete Fourier Transform for real input.
        
        self.fourierTransform(self.data, self.samplerate)
        
        self.updateEverything()

    # Main layout contains plot and spectrogram
    def mainLayout(self):
        mainLayout = QVBoxLayout()

        # Top layout
        topLayout = QHBoxLayout()

        # Player layout
        playerLayout = QVBoxLayout()
        # Player plot
        self.playerPlot = Player("Music")

        # Control Panel of player
        controlPanel = QHBoxLayout()
        # Progress Panel of player
        progressPanel = QHBoxLayout()

        self.startLabel = QLabel("--:--")
        self.progressSlider = QSlider(Qt.Horizontal)
        self.progressSlider.setEnabled(0)
        self.endLabel = QLabel("--:--")

        progressPanel.addWidget(self.startLabel)
        progressPanel.addWidget(self.progressSlider)
        progressPanel.addWidget(self.endLabel)

        self.playButton = QPushButton()
        self.playButton.setIcon(QIcon("images/play.ico"))
        self.playButton.setStyleSheet(f"""font-size:14px; 
                            border-radius: 6px;
                            border: 1px solid {COLOR1};
                            padding: 5px 15px; 
                            background: {COLOR4}; 
                            color: {COLOR4};""")

        self.restartButton = QPushButton()
        self.restartButton.setIcon(QIcon("images/rewind.ico"))
        self.restartButton.setStyleSheet(f"""font-size:14px; 
                            border-radius: 6px;
                            border: 1px solid {COLOR1};
                            padding: 5px 15px; 
                            background: {COLOR4}; 
                            color: {COLOR4};""")

        self.soundIcon = QLabel()
        self.soundIcon.setPixmap(QPixmap('images/downVol.svg'))
        self.soundSlider = QSlider(Qt.Horizontal)
        self.soundSlider.setValue(50)
        self.soundlabel = QLabel("50%")

        controlPanel.addWidget(self.playButton ,1)
        controlPanel.addWidget(QVLine())
        controlPanel.addWidget(self.restartButton,1)
        controlPanel.addSpacerItem(QSpacerItem(500, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        controlPanel.addWidget(self.soundIcon)
        controlPanel.addWidget(self.soundSlider,3)
        controlPanel.addWidget(self.soundlabel)

        playerLayout.addWidget(self.playerPlot)
        playerLayout.addLayout(progressPanel)
        playerLayout.addLayout(controlPanel)
        playerLayout.setSpacing(10)

        # Spectrogram layout
        spectrogramLayout = QVBoxLayout()
        # plot
        self.spectrogramPlot = MplCanvas()
        self.spectrogramPlot.clearSignal()
        self.spectrogramPlot.autoFillBackground()
        self.spectrogramPlot.addColorBar()

        spectrogramLayout.addWidget(self.spectrogramPlot)
        spectrogramLayout.addSpacerItem(QSpacerItem(10, 70, QSizePolicy.Expanding))

        topLayout.addLayout(playerLayout,6)
        topLayout.setSpacing(20)
        topLayout.addLayout(spectrogramLayout,4)

        # Bottom part layout
        bottomLayout = QHBoxLayout()
        
        # Clarinet instrument slider
        guitarSlider = QSlider()
        # Drum instrument slider
        drumSlider = QSlider()
        # Piano instrument slider
        pianoSlider = QSlider()
        
        bottomLayout.addLayout(self.sliderInstrumentLayout(guitarSlider,"images/guitarIcon.ico", (155, 630),0))
        bottomLayout.addLayout(self.sliderInstrumentLayout(drumSlider,"images/drumIcon.png", (50,150),1))
        bottomLayout.addLayout(self.sliderInstrumentLayout(pianoSlider,"images/pianoIcon.png", (1000,2000),2))

        mainLayout.addLayout(topLayout,1)
        mainLayout.addWidget(QHLine())
        mainLayout.addLayout(bottomLayout,1)

        self.mainTab.setLayout(mainLayout)

    # Devices tab layout
    def devicesTabLayout(self, deviceTab):
        mainLayout = QVBoxLayout()

        TopLayout = QHBoxLayout()

        # TODO: Add layout of Drum
        drumLayout = QHBoxLayout()
        self.Drum = Drum()
        drumLayout.addWidget(self.Drum)
        TopLayout.addLayout(drumLayout)

        # TODO: Add layout of guitar
        # Add image of guitar
        guitarLayout = QHBoxLayout()
        self.Guitar = Guitar()
        guitarLayout.addWidget(self.Guitar)
        TopLayout.addLayout(guitarLayout)

        # TODO: Add layout of Piano
        pianoLayout = QHBoxLayout()
        # Add piano
        self.piano = Piano()
        spaceLabel = QLabel()

        self.settingsInstruments = QComboBox()
        piano_modes_names = ["Octave","Major sixth","Minor sixth","Perfect fifth","Perfect fourth","Major third","Minor third"]
        for item in piano_modes_names:
            self.settingsInstruments.addItem(item)
        
        self.settingsInstruments.currentIndexChanged.connect(self.setPianoMode)

        pianoLayout.addWidget(spaceLabel, 3)
        pianoLayout.addWidget(self.piano, 10)


        mainLayout.addSpacerItem(QSpacerItem(10, 100, QSizePolicy.Expanding))
        mainLayout.addLayout(TopLayout,20)
        mainLayout.addLayout(pianoLayout,15)
        mainLayout.addWidget(QLabel("Settings"), 1)
        mainLayout.addWidget(self.settingsInstruments,1)

        deviceTab.setLayout(mainLayout)

    def setPianoMode(self):
        self.piano.setMode(self.settingsInstruments.currentIndex())

    # slider Layout
    def sliderInstrumentLayout(self, instrumentSlider, iconPath, hzRange, num):
        instrumentLayout = QVBoxLayout()
        instrumentLayout.setAlignment(Qt.AlignCenter)

        maxLabel = QLabel("10 db")
        maxLabel.setAlignment(Qt.AlignCenter)

        instrumentSlider.setFocusPolicy(Qt.StrongFocus)
        instrumentSlider.setTickPosition(QSlider.TicksBothSides)
        instrumentSlider.setMinimum(-10)
        instrumentSlider.setMaximum(10)
        instrumentSlider.setTickInterval(5)
        instrumentSlider.setSingleStep(1)
        instrumentSlider.setValue(1)
        
        instrumentSlider.valueChanged[int].connect(lambda: self.equalizeSound(instrumentSlider.value(), hzRange, num))

        minLabel = QLabel("-10 db")
        minLabel.setAlignment(Qt.AlignCenter)

        photo = QLabel()
        img = QPixmap(iconPath).scaled(40,40)
        photo.setPixmap(img)

        instrumentLayout.addWidget(maxLabel)
        instrumentLayout.addWidget(instrumentSlider)
        instrumentLayout.addWidget(minLabel)
        instrumentLayout.addWidget(photo)

        return instrumentLayout
    
    # Fourier transform
    def fourierTransform(self, data, samplerate):
        self.fftData = np.copy(np.fft.rfft(data))
        self.freqFftData = np.fft.rfftfreq(n=len(self.data), d=1./samplerate)

    # Equalize sound
    def equalizeSound(self, gain, freqRange, num):
        self.fourierTransform(self.data, self.samplerate)

        Min_Freq = freqRange[0]
        Max_Freq = freqRange[1]
        rangeFreq = (self.freqFftData >= Min_Freq) & (self.freqFftData <= Max_Freq)
        print("Before",gain)
        if gain < 0: 
            gain = 1/np.abs(gain)
        print("After",gain)
        self.fftData[rangeFreq] /= self.gain_List[num]
        self.gain_List[num] = gain 
        self.fftData[rangeFreq] *= gain
        
        self.data = self.getIfft()
        self.speaker.writeArray("src/temp.wav", self.data)
        self.speaker.loadFile("src/temp.wav", False)

        self.updateEverything()

    # Inverse fourier transform
    def getIfft(self):
        equalizedData = np.fft.irfft(self.fftData)
        equalizedData = np.asanyarray(equalizedData, dtype=np.int16)

        return equalizedData

    def playPause(self):
        if self.playerPlot.playerPause == True :
            self.timer.stop()
            self.speaker.pause()
            self.playerPlot.playerPause = False
            self.playButton.setIcon(QIcon("images/play.ico"))
            self.statusBar.showMessage("Music is paused.")
        else:
            self.timer.start()
            self.speaker.unpause()
            self.playerPlot.playerPause = True
            self.playButton.setIcon(QIcon("images/pause.ico"))
            self.statusBar.showMessage("Music is running.")
        
    def soundChange(self, value):
        if value >= 75 :
            self.soundIcon.setPixmap(QPixmap('images/upVol.svg'))
        elif value > 25 :
            self.soundIcon.setPixmap(QPixmap('images/downVol.svg'))
        else :
            self.soundIcon.setPixmap(QPixmap('images/zeroVol.svg'))
        
        self.soundlabel.setText(str(value)+"%")
        self.speaker.setVolume(value)

    def updateData(self):
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateInstantly)
        self.timer.start()
            
    def updateInstantly(self):
        self.playerPlot.changeRegion(self.speaker.getPosition()/1000)
        self.startLabel.setText(str(datetime.timedelta(seconds=int(self.speaker.getPosition()/1000)))[-5:7])
        self.progressSlider.setValue(int(self.speaker.getPosition()/1000))       

    # After each edit on array
    def updateEverything(self):
        if self.playerPlot.playerPause == True :
            self.speaker.pause()
        else:
            self.speaker.unpause()           

        self.dataPlot = self.data
        self.playerPlot.plotSignal(self.length, self.dataPlot)
        
        # Spectrogram plot
        self.spectrogramPlot.clearSignal()
        self.spectrogramPlot.set_data_channel(self.dataPlot)
        self.spectrogramPlot.plotSignal()

        # Start signal
        self.updateData() 

    # Rewind music
    def restartMusic(self):
        self.speaker.rewind()

    # Connect actions
    def connect(self):
        # TODO: put any necessary connect actions
        self.soundSlider.valueChanged[int].connect(self.soundChange)
        self.playButton.clicked.connect(self.playPause)
        self.restartButton.clicked.connect(self.restartMusic)
    
    # Exit the application
    def exit(self):
        exitDlg = QMessageBox.critical(self,
        "Exit the application",
        "Are you sure you want to exit the application?",
        buttons=QMessageBox.Yes | QMessageBox.No,
        defaultButton=QMessageBox.No)

        if exitDlg == QMessageBox.Yes:
            sys.exit()