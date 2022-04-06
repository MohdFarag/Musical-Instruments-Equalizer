# importing Qt widgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from app import *
import qdarkstyle
from qtpy import QtWidgets


class popWindow(QMainWindow):
    """Main Window."""
    def __init__(self, message, options):

        """Initializer."""
        super().__init__()
        self.window = Window()

        self.message = message
        self.options = options
        self.result = None

        # setting Icon
        self.setWindowIcon(QIcon('images/icon.ico'))

        # setting title
        self.setWindowTitle(message)

        self.initUI()

    def initUI(self):
        centralMainWindow = QWidget(self)
        self.setCentralWidget(centralMainWindow)

        # Outer Layout
        outerLayout = QVBoxLayout()
        outerLayout.setAlignment(Qt.AlignCenter)

        messageLabel = QLabel(self.message)
        messageLabel.setAlignment(Qt.AlignCenter)
        messageLabel.setStyleSheet("""
            font-size:16px;
            color: #000;
            text-align: center;
            padding: 10px;
            font-weight: bold;
        """)

        buttonsLayout = QHBoxLayout()
        # TODO: Edit it to be for loop
        # for item in self.options:
        newButton1 = QPushButton(self.options[0])
        newButton1.setStyleSheet("font-size: 15px; padding: 3px 7px; background: #fff")
        newButton1.clicked.connect(lambda: self.returnResult(self.options[0]))
        buttonsLayout.addWidget(newButton1)

        newButton2 = QPushButton(self.options[1])
        newButton2.setStyleSheet("font-size: 15px; padding: 3px 7px; background: #323232; color: #fff")
        newButton2.clicked.connect(lambda: self.returnResult(self.options[1]))
        buttonsLayout.addWidget(newButton2)

        newButton3 = QPushButton(self.options[2])
        newButton3.setStyleSheet("font-size: 15px; padding: 3px 7px; background: #19232d; color: #fff")
        newButton3.clicked.connect(lambda: self.returnResult(self.options[2]))
        buttonsLayout.addWidget(newButton3)

        outerLayout.addWidget(messageLabel)
        outerLayout.addLayout(buttonsLayout)

        centralMainWindow.setLayout(outerLayout)


    def toggle_stylesheet(self, path):
        '''
        Toggle the stylesheet to use the desired path in the Qt resource
        system (prefixed by `:/`) or generically (a path to a file on
        system).

        :path:      A full path to a resource or file on system
        '''

        # get the QApplication instance,  or crash if not set
        app = QApplication.instance()
        if app is None:
            raise RuntimeError("No Qt Application found.")

        file = QFile(path)
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())


    def returnResult(self, theme):
        # Choose dark or light style
        if theme == "Light":
            self.toggle_stylesheet("src/classic/style.qss")
        elif theme == "Dark":
            self.window.setStyleSheet(qdarkstyle.load_stylesheet())
            # Or
            # self.window.setStyleSheet("src/dark_blue/style.qss")
        elif theme == "Orange":
            self.toggle_stylesheet("src/dark_orange/style.qss")

        self.window.setTheme(theme)
        self.window.show()
        self.close()
