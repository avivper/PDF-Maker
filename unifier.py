import os.path
from time import sleep

import PyPDF2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont


class Unifier(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # todo: Create 2 LineEdit(), in Parallel to input 2 path and will unify them

        # 2 Input in parallel
        self.input = QLabel("Select two PDF files to unify ")
        self.input_1 = QLineEdit()
        self.input_2 = QLineEdit()
        self.browse = QPushButton("Browse")

        # Output
        self.output = QLabel("Enter the name for your new PDF file:\n(Without .pdf)")
        self.output_text = QLineEdit()  # Textfield of output new file

        self.unify = QPushButton("Unify")

        self.Widgets = [
            self.input, self.input_1, self.input_2, self.browse,
            self.output, self.output_text, self.unify
        ]

        self.init()

    def init(self):
        for i in range(len(self.Widgets)):
            widget = self.Widgets[i]
            self.layout.addWidget(widget)

            if isinstance(widget, (QLabel, QLineEdit)):
                widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                font = QFont("Arial", 11)
                widget.setFont(font)

        self.browse.clicked.connect(self.choose)
        self.unify.clicked.connect(self.execute_unify)
        self.setLayout(self.layout)

    def choose(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select a PDF file", "", "PDF Files (*.pdf)"
        )

        if file_path:
            self.embed_path(file_path)

    def embed_path(self, file_path):
        embed = RadioInput()
        option = embed.parse_input()

        if option:
            self.input_1.setText(file_path)
        elif option is False:
            self.input_2.setText(file_path)
        else:
            return

    def execute_unify(self):
        if self.input_1.text() == self.input_2.text():
            return  # todo: create option dialog to unify the same file


# todo: create method to check the input name for the new file

class RadioInput(QDialog):
    def __init__(self, parent=None):
        super(RadioInput, self).__init__(parent)

        self.setWindowTitle("Input")

        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout(self)

        self.file = None

        self.input_1 = QRadioButton("File 1")
        self.input_2 = QRadioButton("File 2")

        self.form_layout.addRow("Select an option: ", self.input_1)
        self.form_layout.addRow("", self.input_2)

        self.buttons_layout = QHBoxLayout()
        self.select_button = QPushButton("Select")
        self.cancel_button = QPushButton("Cancel")

        self.buttons_layout.addWidget(self.select_button)
        self.buttons_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.form_layout)
        self.layout.addLayout(self.buttons_layout)

        self.select_button.clicked.connect(self.return_option)
        self.cancel_button.clicked.connect(self.reject)

    def return_option(self):
        if self.input_1.isChecked():
            self.file = True
        elif self.input_2.isChecked():
            self.file = False
        else:
            return None

        self.accept()

    def parse_input(self):
        result = self.exec_()
        if result == QDialog.Accepted:
            return self.file

        return None
