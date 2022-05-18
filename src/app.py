# !/usr/bin/python

# AdditionsQt
from additionsQt import *
# Threads
from Threads import *
# import Classes
from additionsQt import *
from musicPlayer import Player
from spectrogram import MplCanvas
from piano import Piano
from drum import Drum
from Guitar import Guitar
from sound import music

import datetime
# Sound package
from scipy.io import wavfile
from mutagen.wave import WAVE

# Definition of Main Color Palette
from Defs import COLOR1,COLOR2,COLOR3,COLOR4, COLOR5

# importing Qt widgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qtwidgets import AnimatedToggle

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

# Logging configuration
import logging
logging.basicConfig(filename="errlog.log",
                    filemode="a",
                    format="(%(asctime)s)  | %(name)s | %(levelname)s:%(message)s",
                    datefmt="%d  %B  %Y , %H:%M:%S",
                    level=logging.INFO)


class Window(QMainWindow):
    """Main Window."""
    def __init__(self):

        """Initializer."""
        super().__init__()
        logging.debug("Application started")

        # Initialize Variable
        self.gain_List = [1, 1, 1]
        self.timer = QtCore.QTimer()
        # Time Domain
        self.data = np.array([0])
        self.time = np.array([0])
        # Length of time
        self.length = 0
        self.samplerate = 0
        # Frequency Domain
        self.fftData = np.array([0])
        self.freqFftData = np.array([0])
        # Music
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

        self.initUI()

        # Status Bar
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet(f"""font-size:13px;
                                 padding: 3px;
                                 color: {COLOR1};
                                 font-weight:900;""")
        self.statusBar.showMessage("Welcome to our application...")
        self.setStatusBar(self.statusBar)

        # Connect action
        self.connect()

    def setFftData(self, data):
        self.fftData = data

    def setFreqFftData(self, data):
        self.freqFftData = data

    def setData(self, data):
        self.data = data

    def setTheme(self, theme):
        self.spectrogramPlot.setMode(theme)

    # Menu
    def createMenuBar(self):
        # MenuBar
        menuBar = self.menuBar()

        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)

        # Open file in menu
        self.openFile = QAction("Open...",self)
        self.openFile.setShortcut("Ctrl+o")
        self.openFile.setStatusTip('Open a new signal')

        fileMenu.addAction(self.openFile)

        # Exit file in menu
        self.quit = QAction("Exit",self)
        self.quit.setShortcut("Ctrl+q")
        self.quit.setStatusTip('Exit application')

        fileMenu.addAction(self.quit)

        # Add file tab to the menu
        menuBar.addMenu(fileMenu)

        logging.info("Menubar has created.")

    # GUI
    def initUI(self):
        centralMainWindow = QWidget(self)
        self.setCentralWidget(centralMainWindow)

        # Outer Layout
        outerLayout = QVBoxLayout()

        ######### INIT GUI #########
        # Initialize tab screen
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""font-size:15px;""")

        # TODO: Add tabs and its functions
        self.mainTab = QWidget()
        self.mainLayout()
        tabs.addTab(self.mainTab, "Music")

        self.devicesTab = QWidget()
        # self.devicesTab.setStyleSheet(f"""background: {COLOR4}""")
        self.devicesTabLayout(self.devicesTab)
        tabs.addTab(self.devicesTab, "Instruments")

        outerLayout.addWidget(tabs)
        ######### INIT GUI #########
        centralMainWindow.setLayout(outerLayout)

    # Browse signal
    def browseSignal(self):
        # Open sound file
        path, fileExtension = QFileDialog.getOpenFileName(None, "Load Sound File" ,filter="wav(*.wav)")

        if path == "":
                self.speaker.crash()
                logging.warning("File not specified!")
                return

        if fileExtension == "wav(*.wav)":
            audio = WAVE(path)
            # contains all the metadata about the wavepack file
            audio_info = audio.info
            self.length = int(audio_info.length)
            self.samplerate, self.data = wavfile.read(path)

            try:
                if np.ndim(self.data) > 1:
                    self.data = np.int16(np.mean(self.data, axis=1))
            except:
                logging.error(f"Array with {np.ndim(self.data)} dimension doesn't loaded successfully.")

        self.time = np.linspace(0, self.length, len(self.data))
        self.playButton.setIcon(QIcon("images/pause.ico"))
        self.playerPlot.playerPlay = True

        # update progress slider
        self.startLabel.setText("00:00")
        self.progressSlider.setMinimum(0)
        self.progressSlider.setMaximum(self.length)
        self.endLabel.setText(str(datetime.timedelta(seconds=self.length))[-5:7])

        # Play sound
        self.speaker.loadFile(path)
        # Compute the one-dimensional discrete Fourier Transform for real input.
        # self.fourierTransform(self.data, self.samplerate)

        # Update all data
        self.updateEverything()

    # Main layout contains time plot and spectrogram
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
        self.restartButton.setIcon(QIcon("images/rewind.svg"))
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
        controlPanel.addWidget(self.restartButton, 1)
        controlPanel.addWidget(QVLine())

        #controlPanel.addSpacerItem(QSpacerItem(500, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        controlPanel.addWidget(QLabel(),10)

        controlPanel.addWidget(QVLine())
        controlPanel.addWidget(self.soundIcon)
        controlPanel.addWidget(self.soundSlider,4)
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

        spectrogramLayout.addWidget(self.spectrogramPlot)

        topLayout.addLayout(playerLayout,5)
        topLayout.setSpacing(10)
        topLayout.addLayout(spectrogramLayout,4)

        # Bottom part layout
        bottomLayout = QHBoxLayout()

        # Clarinet instrument slider
        self.guitarSlider = QSlider()
        # Drum instrument slider
        self.drumSlider = QSlider()
        # Piano instrument slider
        self.pianoSlider = QSlider()

        bottomLayout.addLayout(self.sliderInstrumentLayoutEQ(self.guitarSlider,"images/guitarIcon.ico", (155, 630),0))
        bottomLayout.addLayout(self.sliderInstrumentLayoutEQ(self.drumSlider,"images/drumIcon.png", (50,120),1))
        bottomLayout.addLayout(self.sliderInstrumentLayoutEQ(self.pianoSlider,"images/pianoIcon.png", (1000,2000),2))

        mainLayout.addLayout(topLayout,1)
        mainLayout.addWidget(QHLine())
        mainLayout.addLayout(bottomLayout,1)

        self.mainTab.setLayout(mainLayout)

    # Devices tab layout
    def devicesTabLayout(self, deviceTab):
        mainLayout = QVBoxLayout()
        Title = QLabel("Play the musical instruments")
        Title.setAlignment(Qt.AlignCenter)
        Title.setStyleSheet("""
            font-family:Baskerville,Times,'Times New Roman',serif;
            font-size:45px;
            color:#0f8;
            font-variant:small-caps;
            text-align:center;
            font-weight:bold;
        """)

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
        pianoLayout = QVBoxLayout()
        pianoPad = QHBoxLayout()
        # Add piano
        self.piano = Piano()
        spaceLabel = QLabel()

        pianoPad.addWidget(spaceLabel, 5)
        pianoPad.addWidget(self.piano, 15)
        pianoLayout.addLayout(pianoPad)

        settingsLayout = QHBoxLayout()
        settingsLayout.addWidget(self.pianoGroupBox())
        settingsLayout.addWidget(self.guitarGroupBox())
        settingsLayout.addWidget(self.drumGroupBox())

        mainLayout.addWidget(Title, 1)
        mainLayout.addSpacerItem(QSpacerItem(10, 30, QSizePolicy.Expanding))
        mainLayout.addLayout(TopLayout,25)
        mainLayout.addLayout(pianoLayout,20)
        mainLayout.addLayout(settingsLayout)

        deviceTab.setLayout(mainLayout)

    def pianoGroupBox(self):
        pianoGroupBox = QGroupBox('Piano settings')

        VBox = QVBoxLayout()

        self.pianoSettings = QComboBox()
        piano_modes_names = ["Octave", "Major sixth", "Minor Sixth", "Perfect fifth", "Perfect Fourth", "Major Third", "Minor Third"]
        for item in piano_modes_names:
            self.pianoSettings.addItem(item)

        lastKeyInput = QLineEdit()
        allKeysInput = QLineEdit()

        lastKeyInput.setEnabled(0)
        lastKeyInput.setStyleSheet("""
            border: 0;
            border-radius: 6px;
            background: #000105;
            color: #fff;
            padding: 5px;
            text-align: center;
        """)

        allKeysInput.setEnabled(0)
        allKeysInput.setStyleSheet("""
            border: 0;
            border-radius: 6px;
            background: #000105;
            color: #fff;
            padding: 5px;
            text-align: center;
        """)

        inputs = QHBoxLayout()
        inputs.addWidget(lastKeyInput, 1)
        inputs.addWidget(allKeysInput, 5)
        self.piano.setInputs(allKeysInput, lastKeyInput)

        setting1 = QHBoxLayout()
        setting1.addWidget(QLabel("Piano settings:"),1)
        setting1.addWidget(self.pianoSettings, 5)

        VBox.addLayout(inputs)
        VBox.addLayout(setting1)

        pianoGroupBox.setLayout(VBox)

        return pianoGroupBox

    def drumGroupBox(self):
        drumGroupBox = QGroupBox('Drum settings')

        vbox = QVBoxLayout()

        sliderH = QHBoxLayout()

        self.drumSlider = QSlider(Qt.Horizontal)
        self.drumSlider.setFocusPolicy(Qt.StrongFocus)
        self.drumSlider.setMinimum(10)
        self.drumSlider.setMaximum(80)
        self.drumSlider.setTickInterval(50)
        self.drumSlider.setSingleStep(1)
        self.drumSlider.setValue(40)

        sliderH.addWidget(self.drumSlider, 10)
        sliderValue = QLabel("40")
        sliderH.addWidget(sliderValue,1)

        self.drumSlider.valueChanged[int].connect(lambda: self.Drum.editFreq(self.drumSlider.value(), sliderValue))

        vbox.addWidget(QLabel("Amplitude:"))
        vbox.addLayout(sliderH)

        drumGroupBox.setLayout(vbox)

        return drumGroupBox

    def guitarGroupBox(self):
        x = QLineEdit()

        guitarGroupBox = QGroupBox('Guitar settings')

        vBox = QVBoxLayout()

        hBox = QHBoxLayout()
        durationToggle = AnimatedToggle(checked_color="#FFB000", pulse_checked_color="#44FFB000")
        durationToggle.toggled.connect(self.Guitar.changeDuration)

        hBox.addWidget(QLabel("Short"))
        hBox.addWidget(durationToggle)
        hBox.addWidget(QLabel("Long"))

        vBox.addLayout(hBox)
        guitarGroupBox.setLayout(vBox)

        return guitarGroupBox

    def setPianoMode(self):
        self.piano.setMode(self.pianoSettings.currentIndex())

    # slider Layout
    def sliderInstrumentLayoutEQ(self, instrumentSlider, iconPath, hzRange, num):
        # Instrument equalizer slider
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
        instrumentSlider.setValue(0)

        instrumentSlider.sliderReleased.connect(lambda: self.equalizeSound(instrumentSlider.value(), hzRange, num))

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

    # Equalize sound
    def equalizeSound(self, gain, freqRange, num):
        # Disable sliders
        self.guitarSlider.setEnabled(False)
        self.drumSlider.setEnabled(False)
        self.pianoSlider.setEnabled(False)

        # Fourier transform for the sound
        self.fourierTransform(self.data, self.samplerate)

        # Initialize min and max frequencies
        minFreq = freqRange[0]
        maxFreq = freqRange[1]

        rangeFreq = (self.freqFftData >= minFreq) & (self.freqFftData <= maxFreq)
        self.fftData[rangeFreq] /= 10**(self.gain_List[num]/20)
        self.fftData[rangeFreq] *= 10**(gain/20)
        self.gain_List[num] = gain

        logging.info(f"Gain of instrument {num} with frequency ranges between {minFreq} and {maxFreq} has changed to {gain}")

        # Inverse fourier transform for the sound
        self.data = self.inverseFourierTransform(self.fftData)

        self.speaker.writeFile("src/temp.wav", self.data)
        self.speaker.loadFile("src/temp.wav", False)

        self.guitarSlider.setEnabled(True)
        self.drumSlider.setEnabled(True)
        self.pianoSlider.setEnabled(True)

        self.updateEverything()

    # Fourier transform
    def fourierTransform(self, data, samplerate):
        try:
            self.fftData = np.copy(np.fft.rfft(data))
            self.freqFftData = np.fft.rfftfreq(n=len(self.data), d=1./samplerate)
        except:
            logging.error(f"Failed to make DFT on array with {np.ndim(self.data)} dimension and shape = {np.shape(self.data)}.")

    # Inverse fourier transform
    def inverseFourierTransform(self, fftData):
        try:
            equalizedData = np.fft.irfft(fftData)
            if np.ndim(equalizedData) == 1:
                equalizedData = np.asanyarray(equalizedData, dtype=np.int16)
            return equalizedData
        except:
            logging.error(f"Failed to make Inverse DFT on array with {np.ndim(fftData)} dimension and shape = {np.shape(fftData)}.")

    # Play and Pause Function
    def playPause(self):
        if self.playerPlot.playerPlay == True :
            # if player is unpaused, pause it.
            self.timer.stop()
            self.speaker.pause()
            self.playerPlot.playerPlay = False
            self.playButton.setIcon(QIcon("images/play.ico"))
            self.statusBar.showMessage("Music is paused.")
            logging.info(f"Music player paused.")
        else:
            # if player is paused, unpause it.
            self.timer.start()
            self.speaker.unpause()
            self.playerPlot.playerPlay = True
            self.playButton.setIcon(QIcon("images/pause.ico"))
            self.statusBar.showMessage("Music is running.")
            logging.info(f"Music player unpaused.")

    # Change volume of the sound
    def soundChange(self, value):
        if value >= 75 :
            self.soundIcon.setPixmap(QPixmap('images/upVol.svg'))
        elif value >= 25 :
            self.soundIcon.setPixmap(QPixmap('images/downVol.svg'))
        else :
            self.soundIcon.setPixmap(QPixmap('images/zeroVol.svg'))

        self.soundlabel.setText(str(value)+"%")
        self.speaker.setVolume(value)
        logging.info(f"sound of music changed to {value}%.")

    def updateData(self):
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.updateInstantly)
        self.timer.start()

    def updateInstantly(self):
        # Update data while music is running
        self.playerPlot.changeRegion(self.speaker.getPosition()/1000)
        self.startLabel.setText(str(datetime.timedelta(seconds=int(self.speaker.getPosition()/1000)))[-5:7]) # Change text of start min
        self.progressSlider.setValue(int(self.speaker.getPosition()/1000)) # Change progress of player

    # After each process on Array
    def updateEverything(self):
        if self.playerPlot.playerPlay == False :
            self.speaker.pause()
        else:
            self.speaker.unpause()

        self.playerPlot.updateData(self.length, self.data)

        # Spectrogram plot
        self.spectrogramPlot.clearSignal()
        self.spectrogramPlot.set_data_channel(self.data)
        self.spectrogramPlot.plotSignal(self.samplerate)

        # Start signal
        self.updateData()

    # Rewind music
    def restartMusic(self):
        self.speaker.rewind()
        self.timer.start()
        self.speaker.unpause()
        self.playerPlot.playerPlay = True
        self.playButton.setIcon(QIcon("images/pause.ico"))
        self.statusBar.showMessage("Music is running.")
        logging.info(f"Music player unpaused.")

    # Connect actions
    def connect(self):
        # Menu connect actions
        self.openFile.triggered.connect(self.browseSignal)
        self.quit.triggered.connect(self.exit)

        # Other
        self.soundSlider.valueChanged[int].connect(self.soundChange)
        self.playButton.clicked.connect(self.playPause)
        self.restartButton.clicked.connect(self.restartMusic)
        self.pianoSettings.currentIndexChanged.connect(self.setPianoMode)

    # Exit the application
    def exit(self):
        exitDlg = QMessageBox.critical(self,
        "Exit the application",
        "Are you sure you want to exit the application?",
        buttons=QMessageBox.Yes | QMessageBox.No,
        defaultButton=QMessageBox.No)

        if exitDlg == QMessageBox.Yes:
            # Exit the application
            sys.exit()