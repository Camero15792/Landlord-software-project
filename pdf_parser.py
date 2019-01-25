from pathlib import Path
import os, re

import PyPDF2

ADDRESS_REGEX = '()Details .* at:1704 ACACIA DR'


class PDF:
    def __init__(self, pdf_path):
        file_obj = open(pdf_path, 'rb')
        self.pdf_obj = PyPDF2.PdfFileReader(file_obj)


    def find_address(self):
        extracted_text = self.pdf_obj.getPage(1).extractText()


        print(extracted_text)


script_location = os.path.dirname(os.path.realpath(__file__))

pdf_obj = PDF(str(Path(script_location, 'TestBill.pdf')))
print(pdf_obj.find_address())
