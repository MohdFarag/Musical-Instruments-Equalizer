# !/usr/bin/python

import sys
import os
from app import *
import qdarkstyle

os.environ['PYQTGRAPH_QT_LIB'] = 'PyQt5'

if __name__ == "__main__":
    # Initialize Our Window App
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    app.setStyle('Fusion')
    win = Window()
    win.show()

    # Run the application
    sys.exit(app.exec_())