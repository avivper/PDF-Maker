import PyPDF2
import sys
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
        self.output = QLabel("Enter the name for your new PDF file: ")
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
        text, start_pressed = QInputDialog.getText(
            self, "Enter the pages number",
            "Type an integer, list of numbers (Make sure it has spaces between them)\n"
            "Or Type a page number until the page number do you want, for instance: '1-10'"
        )

        if start_pressed:
            if text:
                page_list = []

                for item in text.split():
                    if "-" in item:
                        start, end = item.split("-")
                        page_list.extend(
                            range(int(start),
                                  int(end) + 1)
                        )
                    else:
                        page_list.append(int(item))

                self.pages = page_list
                print(f"User input pages: {self.pages}")
                self.start()
            else:
                print("You must enter at least one number.")
        else:
            print("Canceled")

    def start(self):
        elements = [self.output_text.text(),
                    self.input_text.text(), self.pages]

        for i in elements:
            if i is None:
                return False

        name = elements[0] + ".pdf"
        pdf_file = elements[1]
        selected_pages = elements[2]

        create(pdf_file, name, selected_pages)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDF()
    sys.exit(app.exec_())
