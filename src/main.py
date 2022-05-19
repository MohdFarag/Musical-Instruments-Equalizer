# !/usr/bin/python

import sys
from app import *
from setColorWindow import *

StyleSheet = '''
#RedProgressBar {
    text-align: center;
}
#RedProgressBar::chunk {
    background-color: #F44336;
}
#GreenProgressBar {
    min-height: 12px;
    max-height: 12px;
    border-radius: 6px;
}
#GreenProgressBar::chunk {
    border-radius: 6px;
    background-color: #009688;
}
#BlueProgressBar {
    border: 2px solid #2196F3;
    border-radius: 5px;
    background-color: #E0E0E0;
}
#BlueProgressBar::chunk {
    background-color: #2196F3;
    width: 10px;
    margin: 0.5px;
}
'''

qss = """
#widget {
    border-image: url(images/start.png) 0 0 0 0 stretch stretch;
}
""" 

if __name__ == "__main__":

    # Initialize Our Window App
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(StyleSheet)
    app.setStyleSheet(qss)

    popWin = popWindow("Dark or Light or Orange ?", ["Light", "Orange", "Dark"])
    popWin.show()
    # Win = Window()
    # Win.show()

    # Run the application
    sys.exit(app.exec_())