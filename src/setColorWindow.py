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

        #  setting Geaometry
        self.setGeometry(100,50,540,540)

        # setting title
        self.setWindowTitle(message)

        self.initUI()

    def initUI(self):
        centralMainWindow = QWidget(self)
        self.setCentralWidget(centralMainWindow)
        centralMainWindow.setObjectName("widget")
        centralMainWindow.setContentsMargins(0, 0, 0, 0)

        # Outer Layout
        outerLayout = QVBoxLayout()
        outerLayout.setAlignment(Qt.AlignCenter)

        buttonsLayout = QHBoxLayout()
        # TODO: Edit it to be for loop
        # for item in self.options:
        newButton1 = QPushButton(self.options[0])

        newButton1.clicked.connect(lambda: self.returnResult(self.options[0]))
        newButton1.setObjectName("button")
        newButton1.setStyleSheet("font-size: 19px; padding: 7px 14px; background: #fff; border-radius:3px; border:#000 solid 1px;")
        buttonsLayout.addWidget(newButton1)

        newButton2 = QPushButton(self.options[1])
        newButton2.setStyleSheet("font-size: 19px; padding: 7px 14px; background: #323232; color: #fff; border: 1px #000 solid; border-radius:3px; border:#000 solid 1px;")
        newButton2.clicked.connect(lambda: self.returnResult(self.options[1]))
        buttonsLayout.addWidget(newButton2)

        newButton3 = QPushButton(self.options[2])
        newButton3.setStyleSheet("font-size: 19px; padding: 7px 14px; background: #19232d; color: #fff; border: 1px #000 solid; border-radius:3px; border:#000 solid 1px;")
        newButton3.clicked.connect(lambda: self.returnResult(self.options[2]))
        buttonsLayout.addWidget(newButton3)

        self.progessBar = QProgressBar(self, minimum=0, maximum=100, objectName="RedProgressBar")
        self.progessBar.hide()

        outerLayout.addLayout(buttonsLayout)
        outerLayout.addWidget(self.progessBar)

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

    # return result
    def returnResult(self, theme):
        app = QApplication.instance()
        # Choose dark or light style
        if theme == "Light":
            self.toggle_stylesheet("src/classic/style.qss")
        elif theme == "Dark":
            app.setStyleSheet(qdarkstyle.load_stylesheet())
            # Or
            # self.window.setStyleSheet("src/dark_blue/style.qss")
        elif theme == "Orange":
            self.toggle_stylesheet("src/dark_orange/style.qss")

        # self.progessBar.show()
        # # Step 2: Create a QThread object
        # self.thread = QThread()
        # # Step 3: Create a worker object
        # self.worker = Worker()
        # # Step 4: Move worker to the thread
        # self.worker.moveToThread(self.thread)
        # # Step 5: Connect signals and slots
        # self.thread.started.connect(self.worker.run)
        # self.worker.finished.connect(self.thread.quit)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        # self.worker._signal.connect(self.loadProgress)
        # # Step 6: Start the thread
        # self.thread.start()

        # Final resets
        # self.setEnabled(False)
        # self.worker.finished.connect(lambda: )
        self.resultCommand(theme)

    def loadProgress(self, n):
        self.progessBar.setValue(n)

    def resultCommand(self, theme):
        self.window.setTheme(theme)
        self.window.show()
        self.close()

