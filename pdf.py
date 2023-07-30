import os.path

import PyPDF2
import sys
from time import sleep
from PyQt5.QtWidgets import *


def create(input_pdf_path, output_name, page_numbers):
    pdf_writer = PyPDF2.PdfWriter()

    with open(input_pdf_path, 'rb') as input_pdf:
        pdf_reader = PyPDF2.PdfReader(input_pdf)

        for i in page_numbers:
            if 0 < i <= len(pdf_reader.pages):
                pdf_writer.add_page(pdf_reader.pages[i - 1])
            else:
                print(f"Page {i} does not exist in the PDF.")

    with open(output_name, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)


class PDF(QWidget):
    def __init__(self):
        super().__init__()

        # Input
        self.input = QLabel("Select the PDF file: ")
        self.input_text = QLineEdit()
        self.input_file = QPushButton("Browse")

        # Output
        self.output = QLabel("Enter the name for your new PDF file:\n(Without .pdf)")
        self.output_text = QLineEdit()

        # Create button
        self.create = QPushButton("Start")

        self.Widgets = [self.input, self.input_text,
                        self.input_file, self.output,
                        self.output_text, self.create]

        self.pages = []

        self.initui()

    def initui(self):
        layout = QVBoxLayout()

        for i in range(len(self.Widgets)):
            layout.addWidget(self.Widgets[i])

        self.input_file.clicked.connect(self.choose)
        self.create.clicked.connect(self.input_pages)

        self.setLayout(layout)
        self.setWindowTitle("PDF Creator")
        self.setFixedWidth(600)
        self.setFixedHeight(600)
        self.show()

    def choose(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select a PDF file", "", "PDF Files (*.pdf)"
        )

        if file_path:
            self.input_text.setText(file_path)

    def input_pages(self):
        if self.input_text.text().strip():  # Check if the text input is not null
            if self.output_text.text().strip():  # Also checking the output name text if it's not null

                pdf_file = self.input_text.text().strip()  # This variable contains the string path data

                # Checking if the file exists and if it's a pdf file
                if os.path.exists(pdf_file) and os.path.splitext(pdf_file)[1].lower() == ".pdf":

                    # The input window that is awaiting the user's input
                    text, start_pressed = QInputDialog.getText(
                        self, "Enter the page numbers", "Please type one integer, "
                        "list of numbers (Make sure it has spaces between them)\n"
                        "or enter the range of pages do you want, for instance: '1-10'"
                    )

                    if start_pressed:  # If start_pressed is true, or if the user clicked on OK
                        if text:   # Checking if the text field is not empty

                            page_list = []  # a local list ot contain that will contain the input from the user

                            for item in text.split():  # For each number in the input
                                if "-" in item:  # If the user chose range of numbers
                                    start, end = item.split("-")
                                    page_list.extend(  # convert start number from string to int, also end
                                        range(int(start), int(end) + 1)
                                    )
                                else: # If the user chose various numbers
                                    page_list.append(int(item))

                            self.pages = page_list  # assign the numbers to the public class list
                            self.start()  # execute the method

                        else:
                            QMessageBox.warning(self, "Warning",
                                                "You must enter at least one number.")
                    else:
                        return False
                else:
                    QMessageBox.warning(self, "Invalid PDF file",
                                        "Please select a valid PDF file")
            else:
                QMessageBox.warning(self, "Invalid name",
                                    "Please enter a name for your new file")
        else:
            QMessageBox.warning(self, "Invalid name",
                                "Please select a PDF file")

    def start(self):
        elements = [self.output_text.text(),
                    self.input_text.text(), self.pages]

        for i in elements:  # Checks again if the data is not null
            if i is None:
                QMessageBox.error(self, "Invalid Data", "Please try again")

        name = elements[0] + ".pdf"  # assigned the file type according to the user's input
        pdf_file = elements[1]  # User file path
        selected_pages = elements[2]

        create(pdf_file, name, selected_pages)
        sleep(1)
        QMessageBox.information(self, "Success", "PDF Created successfully!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDF()
    sys.exit(app.exec_())
