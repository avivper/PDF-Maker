import sys
import splitter
import unifier

from PyQt5.QtWidgets import *


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        # Title
        self.title = "PDF Creator"

        self.layout = QVBoxLayout()

        self.setLayout(self.layout)
        self.setWindowTitle(self.title)
        self.setFixedWidth(700)
        self.setFixedHeight(700)

        self.tabs = Table(self)
        self.setCentralWidget(self.tabs)

        self.show()


class Table(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.splitter = splitter.Splitter()
        self.unifier = unifier.Unifier()

        self.tabs.resize(600, 600)

        self.tabs.addTab(self.splitter, "Splitter")
        self.tabs.addTab(self.unifier, "Unifier")

        self.init()

    def init(self):
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class Confirmation(QMessageBox):
    def __init__(self, parent=None):
        super(QMessageBox, self).__init__(parent)
        self.setIcon(QMessageBox.Question)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    def confirm(self, text):
        self.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())
