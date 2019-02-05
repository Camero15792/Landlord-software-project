from pathlib import Path
import re, os
import PyPDF2

ADDRESS_REGEX = 'Details of your utility service at:(.*)Account'
AMOUNT_DUE_REGEX = 'Amount Due: (.*)Page 2'
BILL_DATE_REGEX = '\$15\$25\$5\$50\$75\$184.73\s[*CR]$(\d|\.|\,)\$81'



class PDF:
    def __init__(self, pdf_path):
        file_obj = open(pdf_path, 'rb')
        self.pdf_obj = PyPDF2.PdfFileReader(file_obj)


    def find_address(self):
        return self.find(ADDRESS_REGEX, 1)


    def find_amount_due(self):
        return self.find(AMOUNT_DUE_REGEX, 1)


    def find_bill_date(self):
        return self.find(BILL_DATE_REGEX, 1)


    def find(self, regex, page):
        extracted_text = self.pdf_obj.getPage(page).extractText()
        re_obj = re.search(regex, extracted_text)

        return re_obj[1].strip().lower()


if __name__ == "__main__":
    script_location = os.path.dirname(os.path.realpath(__file__))

    pdf_obj = PDF(str(Path(script_location, 'TestBill.pdf')))

    print(pdf_obj.find_address())
    print(pdf_obj.find_bill_date())
    print(pdf_obj.find_amount_due())
