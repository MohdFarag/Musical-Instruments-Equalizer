# !/usr/bin/python

## import Plotter.py Class
# from plotter import Plot

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
