# !/usr/bin/python

# import Plotter.py Class
import imp
from musicPlayer import Player
from spectrogram import MplCanvas

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
from pyqtgraph.dockarea import *

# importing sys package
import sys
import os
import logging


class Window(QMainWindow):
    """Main Window."""
    def __init__(self):
        
        """Initializer."""
        super().__init__()

        # Initialize Variables
        

        # setting Icon
        self.setWindowIcon(QIcon('images/icon.ico'))
        
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
        path, fileExtension = QFileDialog.getOpenFileName(None, "Load Sound File", os.getenv('HOME') ,"mp3(*.mp3)")
        if path == "":
                return
                
        if fileExtension == "mp3(*.mp3)":
            #TODO: read sound file
            pass
        # TODO: clear signal from plot
        # TODO: update data in plot

    def mainLayout(self):
        mainLayout = QVBoxLayout()

        topLayout = QHBoxLayout()

        # Player layout
        playerLayout = QVBoxLayout()
        # Player plot
        playerPlot = Player("Music")
        # Control Panel of player
        controlPanel = QHBoxLayout()
        # Progress Panel of player
        progressPanel = QHBoxLayout()

        startLabel = QLabel("--:--")
        progressSlider = QSlider(Qt.Horizontal)
        endLabel = QLabel("--:--")

        progressPanel.addWidget(startLabel)
        progressPanel.addWidget(progressSlider)
        progressPanel.addWidget(endLabel)


        playButton = QPushButton()
        playButton.setIcon(QIcon("images/play.ico"))
        playButton.setStyleSheet(f"""font-size:14px; 
                            border-radius: 6px;
                            border: 1px solid {COLOR1};
                            padding: 5px 15px; 
                            background: {COLOR4}; 
                            color: {COLOR4};""")

        soundIcon = QLabel()
        soundIcon.setPixmap(QPixmap('images/downVol.svg'))
        soundSlider = QSlider(Qt.Horizontal)
        soundSlider.setValue(50)
        soundlabel = QLabel("50")

        controlPanel.addWidget(playButton,1)
        controlPanel.addSpacerItem(QSpacerItem(450, 10, QSizePolicy.Expanding))
        controlPanel.addWidget(soundIcon)
        controlPanel.addWidget(soundSlider,3)
        controlPanel.addWidget(soundlabel)

        playerLayout.addWidget(playerPlot)
        playerLayout.addLayout(progressPanel)
        playerLayout.addLayout(controlPanel)

        # Player layout
        spectrogramLayout = QVBoxLayout()
        # Spectrogram plot
        spectrogramPlot = MplCanvas()

        spectrogramLayout.addWidget(spectrogramPlot)
        spectrogramLayout.addSpacerItem(QSpacerItem(10, 31, QSizePolicy.Expanding))

        topLayout.addLayout(playerLayout,5)
        topLayout.addLayout(spectrogramLayout,3)

        bottomLayout = QHBoxLayout()

        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)

        self.mainTab.setLayout(mainLayout)

    def devicesTabLayout(self, deviceTab):
        mainLayout = QVBoxLayout()
        # TODO: Add layout of Piano
        # TODO: Add layout of Clarinet
        # TODO: Add layout of Drum

        deviceTab.setLayout(mainLayout)

    # Connect actions
    def connect(self):
        # TODO: put any necessary connect actions
        pass
    
    # Exit the application
    def exit(self):
        exitDlg = QMessageBox.critical(self,
        "Exit the application",
        "Are you sure you want to exit the application?",
        buttons=QMessageBox.Yes | QMessageBox.No,
        defaultButton=QMessageBox.No)

        if exitDlg == QMessageBox.Yes:
            sys.exit()
