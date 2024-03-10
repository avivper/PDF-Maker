import os.path

import PyPDF2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from time import sleep


class Splitter(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # Input
        self.input = QLabel("Select the PDF file: ")
        self.input_text = QLineEdit()  # Textfield of the targeted PDF
        self.input_file = QPushButton("Browse")

        # Output
        self.output = QLabel("Enter the name for your new PDF file:\n(Without .pdf)")
        self.output_text = QLineEdit()  # Textfield of output new file

        # Button that will execute the creation method
        self.create = QPushButton("Split")

        self.Widgets = [
            self.input, self.input_text, self.input_file,
            self.output, self.output_text, self.create
        ]

        self.init()

    def init(self):
        # Creating UI
        for i in range(len(self.Widgets)):
            widget = self.Widgets[i]
            self.layout.addWidget(self.Widgets[i])

            if isinstance(widget, (QLabel, QLineEdit)):
                widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                font = QFont("Arial", 11)
                widget.setFont(font)

        self.setLayout(self.layout)

        self.input_file.clicked.connect(self.choose)
        self.create.clicked.connect(self.execute)

    def choose(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select a PDF file", "", "PDF Files (*.pdf)"
        )

        if file_path:
            self.input_text.setText(file_path)

    def generate_str(self):
        return self.output_text.text() + ".pdf"

    def execute(self):
        if self.input_text.text().strip():
            if self.output_text.text().strip():

                file = self.input_text.text().strip()
                self.check_pdf(file)
            else:
                QMessageBox.warning(self, "Invalid name", "Please enter a name for your new file",
                                    QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Invalid name", "Please select a PDF file",
                                QMessageBox.Ok)

    def check_pdf(self, pdf_file):
        if os.path.exists(pdf_file) and os.path.splitext(pdf_file)[1].lower() == ".pdf":
            text, start_pressed = QInputDialog.getText(
                self, "Enter the page numbers",
                "Please type one integer, list of numbers (Make sure it has spaces between them)\n"
                "or enter the range of pages you want, for example: '1-10'"
            )

            if start_pressed:
                filename = self.generate_str()
                page_list = self.pdf_list(text)

                if text:
                    self.create_pdf(self.input_text.text(), filename, page_list)
                else:
                    self.QMessageBox.warning(
                        self, "Warning", "You must enter at least one number.", QMessageBox.Ok
                    )
            else:
                return False
        else:
            self.QMessageBox.warning(
                self, "Invalid PDF file",
                "Please select a valid PDF file", QMessageBox.Ok
            )

    def pdf_list(self, text):
        page_list = []

        for item in text.split():
            try:
                if "-" in item:
                    start, end = item.split("-")

                    start = int(start)
                    end = int(end)

                    if start > end:
                        QMessageBox.warning(
                            self, "Invalid input",
                            "The start page number should be less than or equal "
                            "to the final page number.", QMessageBox.Ok
                        )

                        return

                    else:
                        for page_number in range(start, end + 1):
                            page_list.append(page_number)
                else:
                    page_list.append(int(item))

                return page_list

            except ValueError:
                QMessageBox.warning(
                    self, "Invalid input",
                    "Please enter valid page numbers.", QMessageBox.Ok
                )

                return

    def create_pdf(self, input_pdf_path, output_name, page_numbers):
        pdf_writer = PyPDF2.PdfWriter()
        folder = "Created PDF"

        if not os.path.exists(folder):  # Creating the folder for the PDF
            os.makedirs(folder)

        output_path = os.path.join(folder, output_name)

        if os.path.exists(output_path):
            choice = QMessageBox.question(
                self, "File already exist", f"Are you want to replace {output_name}?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if choice == QMessageBox.No:
                return

        with open(input_pdf_path, 'rb') as input_pdf:
            pdf_reader = PyPDF2.PdfReader(input_pdf)

            for i in page_numbers:
                if 1 <= i <= len(pdf_reader.pages):
                    pdf_writer.add_page(pdf_reader.pages[i - 1])
                else:
                    QMessageBox.warning(
                        self, "Error",
                        f"Page {i} doesn't exist in the PDF, enter valid numbers",
                        QMessageBox.Ok
                    )
                    return
            with open(output_path, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

            sleep(0.5)
            QMessageBox.information(
                self, "Success", "PDF Created successfully!",
                QMessageBox.Ok
            )

            self.output_text.clear()
