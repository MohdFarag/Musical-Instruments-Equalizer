# !/usr/bin/python

import sys
import os
from app import *
from setColorWindow import *

if __name__ == "__main__":

    # Initialize Our Window App
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    popWin = popWindow("Dark or Light or Orange ?", ["Light", "Orange", "Dark"])
    popWin.show()

    # Run the application
    sys.exit(app.exec_())