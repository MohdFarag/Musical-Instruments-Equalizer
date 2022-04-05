# !/usr/bin/python

import sys
from app import *
import qdarkstyle

if __name__ == "__main__":
    # Initialize Our Window App
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    app.setStyle('Fusion')
    win = Window()
    win.show()

    # Run the application
    sys.exit(app.exec_())