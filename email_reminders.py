import communications
import time, datetime, math
from calendar import monthrange
import calendar
import xlrd
from pathlib import Path
import re, os
import warnings
warnings.simplefilter("ignore", Warning)
import PyPDF2
import imaplib
import email




BillFolder = "C:/Users/Cameron Stark/Documents/"
GmailAccount = ""
Password = ""
ExcelPath = "C:/Users/Cameron Stark/Documents/Tenant_data.xlsx"




class PDFReader:
    """
    Scans through the utility bill and finds key information
    """
    def __init__(self):
        file_obj = open(BillFolder+'ViewBill.pdf', 'rb')
        self.pdf_obj = PyPDF2.PdfFileReader(file_obj)

    def find_total(self):
        extracted_text = self.pdf_obj.getPage(0).extractText()
        total = float(extracted_text[extracted_text.find('Total Current Bill$')+19:extracted_text.find('New Account Balance')])
        return total

    def find_util_month(self):
        extracted_text = self.pdf_obj.getPage(0).extractText()
        date = extracted_text[extracted_text.find('Billing Date:') + 13:extracted_text.find('No Payment Due')]
        date = datetime.datetime.strptime(date, '%x')
        if date.month == 1:
            date = date.replace(date.year-1,12)
        else:
            date = date.replace(date.year,date.month-1)
        util_month = date.strftime('%B')
        return util_month, date


def reminder_dates_generator(lsd,lsm,lsy,lem,ley, pay_day, remind_days_in_advance=3, grace_period=3):
    """
    Generates all reminder dates, payment dates and warning dates given the lease start and end day, month, year
    :param lsd: lease start date
    :param lsm: lease start month
    :param lsy: lease start year
    :param lem: lease end month
    :param ley: lease end year
    :param pay_day: The day of the month the tenant has agreed to pay rent
    :param remind_days_in_advance: How many days in advance to remind the tenant
    :param grace_period:
    :return: Three lists: reminder dates, payment dates and warning dates of the entire lease
    """
    last_reminder_date = datetime.datetime(ley,lem,pay_day)
    payment_date = datetime.datetime(lsy,lsm,lsd)
    payment_dates = [payment_date]
    reminder_dates = []
    warning_dates = []
    while payment_dates[-1] != last_reminder_date:
        if payment_date.month == 12:
            payment_date = payment_date.replace(payment_date.year + 1, 1, pay_day)
        else:
            payment_date = payment_date.replace(payment_date.year, payment_date.month + 1, pay_day)
        payment_dates.append(payment_date)
        x = payment_date.timestamp()  # convert payment date to seconds since epoch
        warning_date = x + 60 * 60 * 24 * grace_period  # add 24hrs times grace period
        warning_date = datetime.datetime.fromtimestamp(warning_date)  # convert back to standard datetime format
        warning_dates.append(warning_date)
        reminder_date = x - 60 * 60 * 24 * remind_days_in_advance
        reminder_date = datetime.datetime.fromtimestamp(reminder_date)
        reminder_dates.append(reminder_date)
    payment_dates = payment_dates[1:]
    return reminder_dates, payment_dates, warning_dates


def gather_pdf():
    """
    Searches email inbox for and downloads utility bill. If I had access to a Colorado Springs Utilities Account this function
    would instead grab the bill from the CSU website.
    """
    mail = imaplib.IMAP4_SSL('imap.gmail.com',993)
    mail.login(GmailAccount, Password)
    mail.select('Inbox')
    type, data = mail.search(None,'(UNSEEN)', '(HEADER Subject "UTILITY_BILL")')
    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()
            if bool(fileName):
                if os.path.exists(BillFolder+'ViewBill.pdf'):
                    os.remove(BillFolder+'ViewBill.pdf')
                filePath = os.path.join(BillFolder, fileName)
                if not os.path.isfile(filePath):
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                print('Downloaded "{file}" from email titled "{subject}"'.format(file=fileName,subject=subject))


def import_tenant_data():
    """
    Gets all tenant data from an excel spreadsheet saved in my computer
    :return:
    """
    wkbk = xlrd.open_workbook(ExcelPath)
    sheet = wkbk.sheet_by_index(0)
    Firstnames = []
    Lastnames = []
    Rents = []
    Utilities = []
    Pay_dates = []
    Emails = []
    Start_days = []
    Start_months = []
    Start_years = []
    End_months = []
    End_years = []
    x = 1
    while 1:
        try:
            Firstnames.append(sheet.cell(x, 0).value)
            Lastnames.append(sheet.cell(x, 1).value)
            Rents.append(sheet.cell(x, 2).value)
            Utilities.append(sheet.cell(x, 3).value)
            Pay_dates.append(int(sheet.cell(x, 4).value))
            Emails.append(sheet.cell(x, 5).value)
            Start_days.append(int(sheet.cell(x, 6).value))
            Start_months.append(int(sheet.cell(x, 7).value))
            Start_years.append(int(sheet.cell(x, 8).value))
            End_months.append(int(sheet.cell(x, 9).value))
            End_years.append(int(sheet.cell(x, 10).value))
            x += 1
        except IndexError:
            break
    return Firstnames, Lastnames, Rents, Utilities, Pay_dates, Emails, Start_days, Start_months, Start_years, End_months, End_years


gather_pdf()

pdf = PDFReader()
utility_bill = pdf.find_total()
utility_month, utility_date = pdf.find_util_month()

Firstnames, Lastnames, Rents, Utilities, Pay_dates, Emails, Start_days, Start_months, Start_years, End_months, End_years = import_tenant_data()

for y in range(0,len(Firstnames)):
    reminder_dates = reminder_dates_generator(Start_days[y],Start_months[y],Start_years[y],End_months[y],End_years[y],Pay_dates[y])[0]
    payment_dates = reminder_dates_generator(Start_days[y],Start_months[y],Start_years[y],End_months[y],End_years[y],Pay_dates[y])[1]
    if payment_dates[0] > utility_date:
        Utilities[y] = 0
    today = datetime.datetime.today()
    today = today.replace(today.year,today.month,today.day,0,0,0,0)
    for x in range(0,len(reminder_dates)):
        if today == reminder_dates[x]:
            communications.send_reminder_email(Firstnames[y],Emails[y],Rents[y],payment_dates[x],utility_bill,len(Firstnames),utility_month,Utilities[y])
            print('hello '+Firstnames[y]+' at '+ Emails[y])
