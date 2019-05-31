import communications
import time, datetime, math
from calendar import monthrange
import calendar
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import re, os
import warnings
warnings.simplefilter("ignore", Warning)
import PyPDF2
import imaplib
import email


class PDFReader:
    """
    Scans through the utility bill and finds key information
    """
    def __init__(self):
        file_obj = open("C:\\Users\\Cameron Stark\\Documents\\BillView.pdf", 'rb')
        self.pdf_obj = PyPDF2.PdfFileReader(file_obj)

    def find_total(self):
        extracted_text = self.pdf_obj.getPage(0).extractText()
        total = float(extracted_text[extracted_text.find('Total Current Bill$')+19:extracted_text.find('New Account Balance')])
        return total

    def find_util_month(self):
        extracted_text = self.pdf_obj.getPage(0).extractText()
        date = extracted_text[extracted_text.find('Billing Date:') + 13:extracted_text.find('Billing Date:') + 21]
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
    Searches email inbox for and downloads utility bill. If I had a Colorado Springs Utilities Account this function
    would grab the bill from the CSU website.
    """
    mail = imaplib.IMAP4_SSL('imap.gmail.com',993)
    mail.login('starksupply0@gmail.com', 'business1579')
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
                if os.path.exists('C:/Users/Cameron Stark/Documents/ViewBill.pdf'):
                    os.remove('C:/Users/Cameron Stark/Documents/ViewBill.pdf')
                if os.path.exists('C:/Users/Cameron Stark/Documents/BillView.pdf'):
                    os.remove('C:/Users/Cameron Stark/Documents/BillView.pdf')
                filePath = os.path.join('C:/Users/Cameron Stark/Documents/', fileName)
                if not os.path.isfile(filePath):
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                print('Downloaded "{file}" from email titled "{subject}"'.format(file=fileName,subject=subject))


def import_tenant_data():
    def int_list(list):
        new_list = []
        for x in list:
            new_list.append(int(x))
        return new_list

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        '', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open('Tenant_Data').sheet1

    firstnames = wks.col_values(1)[1:]
    lastnames = wks.col_values(2)[1:]
    rents = int_list(wks.col_values(3)[1:])
    utilities = int_list(wks.col_values(4)[1:])
    pay_dates = int_list(wks.col_values(5)[1:])
    emails = wks.col_values(6)[1:]
    phone_numbers = wks.col_values(7)[1:]
    start_days = int_list(wks.col_values(8)[1:])
    start_months = int_list(wks.col_values(9)[1:])
    start_years = int_list(wks.col_values(10)[1:])
    end_months = int_list(wks.col_values(11)[1:])
    end_years = int_list(wks.col_values(12)[1:])
    return firstnames,lastnames,rents,utilities,pay_dates,emails,phone_numbers,start_days,start_months,start_years,end_months,end_years

gather_pdf()

pdf = PDFReader()
try:
    utility_month, utility_date = pdf.find_util_month()
    utility_bill = pdf.find_total()
except:
    utility_month = input('Enter Utility Month')
    utility_date = datetime.datetime.strptime(input('Enter Utility Date Format: month/day/yr'),'%x')
    utility_bill = float(input('Enter Utility Bill Format: float'))


Firstnames, Lastnames, Rents, Utilities, Pay_dates, Emails, Phone_Numbers, Start_days, Start_months, Start_years, End_months, End_years = import_tenant_data()

while 1:
    for y in range(0,len(Firstnames)):
        reminder_dates = reminder_dates_generator(Start_days[y],Start_months[y],Start_years[y],End_months[y],End_years[y],Pay_dates[y])[0]
        payment_dates = reminder_dates_generator(Start_days[y],Start_months[y],Start_years[y],End_months[y],End_years[y],Pay_dates[y])[1]
        if payment_dates[0] > utility_date:
            Utilities[y] = 0
        today = datetime.datetime.today()
        today = today.replace(today.year,today.month,today.day,0,0,0,0)
        for x in range(0,len(reminder_dates)):
            if today == reminder_dates[x]:
                if reminder_dates[x] == reminder_dates[-1]:
                    Last_Month = True
                else:
                    Last_Month = False
                communications.send_reminder_email(Firstnames[y],Emails[y],Rents[y],payment_dates[x],utility_bill,len(Firstnames),utility_month,Utilities[y],Last_Month)
                print('hello '+Firstnames[y]+' at '+ Emails[y])
    time.sleep(60*60*24)
