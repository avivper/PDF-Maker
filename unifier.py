from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont


class Unifier(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # Input
        self.input = QLabel("Select the PDF file: ")
        self.input_text = QLineEdit()  # Textfield of the targeted PDF
        self.input_file = QPushButton("Browse")

        self.create = QPushButton("Unify")

        self.Widgets = [
            self.input, self.input_text, self.input_file,
            self.create
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

            self.setLayout(self.layout)
