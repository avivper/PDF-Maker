import os
import PyPDF2
import sys
from time import sleep
from PyQt5.QtWidgets import *


class PDF(QWidget):
    def __init__(self):
        super().__init__()

        # Input
        self.input = QLabel("Select the PDF file: ")
        self.input_text = QLineEdit()  # Textfield of the targeted PDF
        self.input_file = QPushButton("Browse")

        # Output
        self.output = QLabel("Enter the name for your new PDF file:\n(Without .pdf)")
        self.output_text = QLineEdit()  # Textfield of output new file

        # Button that will execute the file creation method
        self.create = QPushButton("Start")

        self.Widgets = [self.input, self.input_text,
                        self.input_file, self.output,
                        self.output_text, self.create]  # List to create the widgets in for loop

        self.initui()

    def initui(self):
        layout = QVBoxLayout()

        for i in range(len(self.Widgets)):
            layout.addWidget(self.Widgets[i])

        for i in range(len(self.Widgets)):
            h_layout = QHBoxLayout()
            widget = self.Widgets[i]

            if isinstance(widget, (QLabel, QLineEdit)):
                widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

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
                        if text:  # Checking if the text field is not empty

                            page_list = []  # a local list ot contain that will contain the input from the user

                            for item in text.split():  # For each number in the input
                                if "-" in item:  # If the user chose range of numbers
                                    try:

                                        start, end = item.split("-")

                                        # Convert start and end into int
                                        start = int(start)
                                        end = int(end)

                                        if start > end:  # Check if the user typed a rational numbers
                                            QMessageBox.warning(self, "Invalid input",
                                                                "The start page number should be less than or equal "
                                                                "to the end page number.",
                                                                QMessageBox.Ok)
                                            return

                                        else:  # Assign the input numbers that was assigned by the user to the list
                                            for page_number in range(start, end + 1):
                                                page_list.append(page_number)

                                    except ValueError:
                                        QMessageBox.warning(self, "Invalid input",
                                                            "Please enter valid page numbers "
                                                            "(only numbers and spaces).", QMessageBox.Ok)
                                        return

                                else:  # If the user chose various numbers
                                    try:  # Assign the input numbers that was assigned by the user to the list
                                        page_list.append(int(item))

                                    except ValueError:
                                        QMessageBox.warning(self, "Invalid input",
                                                            "Please enter valid page numbers "
                                                            "(only numbers and spaces).", QMessageBox.Ok)
                                        return

                            # assigned the file type according to the user's input
                            pdf = self.output_text.text() + ".pdf"
                            self.create_pdf(self.input_text.text(), pdf, page_list)

                        else:  # Handle the error if the user just clicked ok without assign any number
                            QMessageBox.warning(self, "Warning",
                                                "You must enter at least one number.", QMessageBox.Ok)
                    else:  # Will return false the user chose Cancel button
                        return False
                else:  # If the user type invalid file or unavailable pdf file
                    QMessageBox.warning(self, "Invalid PDF file",
                                        "Please select a valid PDF file", QMessageBox.Ok)
            else:  # Will pop up if the user didn't type any name
                QMessageBox.warning(self, "Invalid name",
                                    "Please enter a name for your new file", QMessageBox.Ok)
        else:  # Will pop up if the pdf browse textfield is empty
            QMessageBox.warning(self, "Invalid name",
                                "Please select a PDF file", QMessageBox.Ok)

    def create_pdf(self, input_pdf_path, output_name, page_numbers):
        pdf_writer = PyPDF2.PdfWriter()
        folder = "Created PDF"

        if not os.path.exists(folder):  # Creating the folder "Created PDF" if it doesn't exist
            os.makedirs(folder)

        output_path = os.path.join(folder, output_name)  # Get the path including the new output name

        if os.path.exists(output_path):  # Checks if the name already exists, if not, let's go
            choice = QMessageBox.question(
                self, "File already exist", f"Are you sure do you want to replace {output_name}?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if choice == QMessageBox.No:  # If the user choose no, it will end the process
                return

        # If the user chose yes, it will continue the process of creation the file
        with open(input_pdf_path, 'rb') as input_pdf:  # Reads the existing pdf file that was assigned by the user
            pdf_reader = PyPDF2.PdfReader(input_pdf)

            for i in page_numbers:  # Reads the numbers that was assigned by the user
                if 1 <= i <= len(pdf_reader.pages):  # Also sorting the numbers from the low to the high
                    pdf_writer.add_page(pdf_reader.pages[i - 1])
                else:  # If the user was naughty and chose to enter invalid page number that is not exists in the file
                    QMessageBox.warning(self, "Error",
                                        f"Page {i} does not exist in the PDF, enter valid numbers",
                                        QMessageBox.Ok)  # Will appear if the file was created
                    return

            with open(output_path, 'wb') as output_pdf:  # Finally, create the file
                pdf_writer.write(output_pdf)

            sleep(0.5)  # Waiting half second
            QMessageBox.information(self, "Success", "PDF Created successfully!",
                                    QMessageBox.Ok)  # Will appear if the file was created
            self.output_text.clear()  # Clears the textfield of the output file


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDF()
    sys.exit(app.exec_())
