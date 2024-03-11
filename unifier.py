import os.path
from time import sleep

import PyPDF2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont


class Unifier(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # Create 2 LineEdit(), in Parallel to input 2 path and will unify them

        # 2 Input in parallel
        self.input = QLabel("Select two PDF files to unify ")
        self.input_1 = QLineEdit()
        self.input_2 = QLineEdit()
        self.browse = QPushButton("Browse")

        # Output
        self.output = QLabel("Enter the name for your new PDF file:\n(Without .pdf)")
        self.output_text = QLineEdit()  # Textfield of output new file

        self.create = QPushButton("Unify")

        self.Widgets = [
            self.input, self.input_1, self.input_2, self.browse,
            self.output, self.output_text, self.create
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
        self.setLayout(self.layout)

    def choose(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select a PDF file", "", "PDF Files (*.pdf)"
        )

        if file_path:
            self.input_path(file_path)

    def input_path(self, file_path):
        option_dialog = RadioInput()
        selected_option = option_dialog.get_option()
        parse_option = option_dialog.parse_input()

        if selected_option:
            print(f"{selected_option}, \n" + file_path)
            self.input_1.setText(file_path)

        if parse_option:
            print(f"{parse_option}")


class RadioInput(QDialog):
    def __init__(self, parent=None):
        super(RadioInput, self).__init__(parent)

        self.setWindowTitle("Input")

        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

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

        self.select_button.clicked.connect(self.get_option)
        self.cancel_button.clicked.connect(self.reject)

    def get_option(self):
        if self.input_1.isChecked():
            return True
        elif self.input_2.isChecked():
            return False
        else:
            self.reject()

    def parse_input(self):
        result = self.exec_()
        if result == QDialog.Accepted:
            return self.result()

        return None
