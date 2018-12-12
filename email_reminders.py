from datetime import date
import time
import calendar
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def choose_date():
    x = date.today()
    x = str(x)
    day = x[8:]
    day = int(day)
    year = x[0:4]
    year = int(year)
    month = x[5:7]
    month = int(month)
    NA, days_in_month = calendar.monthrange(year, month)
    month = month + 1
    if month == 13:
        month = 1
        year = year + 1
    day_of_first, NA = calendar.monthrange(year, month)
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for X in range(0,6):
        if day_of_first == X:
            day_of_first = weekdays[X]
    reminder_date = days_in_month - 7
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    for X in range(0,11):
        if month == X + 1:
            month = months[X]
            if X == 0:
                util_month = 'November'
            elif X == 1:
                util_month = 'December'
            else:
                util_month = months[X - 2]
    return day, reminder_date, day_of_first, month, util_month


def py_mail(SUBJECT, BODY, TO, FROM):
    """With this function we send out our html email"""
    # Create message container - the correct MIME type is multipart/alternative here!
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = SUBJECT
    MESSAGE['To'] = TO
    MESSAGE['From'] = FROM
    MESSAGE.preamble = """
       Your mail reader does not support the report format.
       Please visit us <a href="http://www.mysite.com">online</a>!"""
    # Record the MIME type text/html.
    HTML_BODY = MIMEText(BODY, 'html')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    MESSAGE.attach(HTML_BODY)
    # The actual sending of the e-mail
    server = smtplib.SMTP('smtp.gmail.com:587')
    # Credentials (if needed) for sending the mail
    password = "YOUR PASSWORD"
    server.starttls()
    server.login(FROM, password)
    server.sendmail(FROM, [TO], MESSAGE.as_string())
    server.quit()


tenants = ['Mrs. Jones', 'Jay', 'Justin', 'Ian']
rent = [550,500,450,550]
utilities = [1,1,1,0]
emails = ['', '', '', '']
utility_bill = flaot(input('enter utility bill amount:'))
while 1:
    time.sleep(24*60*60)
    day, reminder_date, day_of_first, month, util_month = choose_date()
    if day == reminder_date:
        for x in range(0,4):
            name = str(tenants[x])
            if utilities[x] == 1:
                Utilities = utility_bill/5
            else:
                Utilities = 0
            total = Utilities + rent[x]
            Utilities = str(Utilities)
            Rent = str(rent[x])
            total = str(total)
            email_content = """
                   <head>
                     <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                   </head>
                   <body>
                     Hello {name},<br>&nbsp;&nbsp;&nbsp;&nbsp; This is a courtesy reminder that rent for {month} and Utilities
                      for {util_month} is due next {day_of_first}, 
                      please pay the following amounts to email address: stark.cameron1579@gmail.com,
                      Rent: {Rent} + Utilities: {Utilities} = total: {total}
                       <u><a href="https://pay.google.com/payments/u/0/home#sendRequestMoney"> Click to Pay </a></u>
                   </body>
                   """.format(name=name, month=month, day_of_first=day_of_first, util_month=util_month, Rent=Rent, Utilities=Utilities, total=total)
            TO = emails[x]
            FROM = 'YOUR EMAIL'
            py_mail("Courtesy Reminder", email_content, TO, FROM)
        utility_bill = float(input('enter utility bill amount:'))
