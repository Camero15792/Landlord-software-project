from datetime import date
import time
import calendar
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def todays_date():
    x = date.today()
    x = str(x)
    today = x[8:]
    today = int(today)
    this_year = x[0:4]
    this_year = int(this_year)
    month = x[5:7]
    month = int(month)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    this_month = [months[month-1],month]
    if month == 1:
        last_month = ['December',12]
    else:
        last_month = [months[month-2],month-1]
    if month == 1:
        two_months_ago = ['November',11]
    elif month == 2:
        two_months_ago = ['December',12]
    else:
        two_months_ago = [months[month-3],month-2]
    if month == 12:
        next_month = ['January',1]
    else:
        next_month = [months[month],month+1]
    NA, days_in_month = calendar.monthrange(this_year,month)

    return two_months_ago, last_month, this_month, next_month, today, this_year, days_in_month

def weekday(day, month, year):
    day_of_first, days_in_month = calendar.monthrange(year,month)
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = day_of_first + day-1
    while 1:
        if day>6:
            day = day-7
        else:
            break
    Day = weekdays[day]
    return Day, days_in_month

def send_email(name, email_address, due_month, util_month, due_day, rent, utilities, utility_bill):
    if utilities == 1:
        utilities = utility_bill/5
    else:
        utilities = 0
    total = rent + utilities
    name,rent,utilities,total = str(name), '${:,.2f}'.format(rent), '${:,.2f}'.format(utilities),'${:,.2f}'.format(total)
    email_content = """
                      <head>
                        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                      </head>
                      <body>
                        Hello {name},<br>&nbsp;&nbsp;&nbsp;&nbsp; This is a courtesy reminder that rent for {month} and Utilities
                         for {util_month} are due on {due_day},
                         please pay the following amounts to email address: YOUR_EMAIL
                         Rent: {Rent} + Utilities: {Utilities} = total: {total}
                          <u><a href="https://pay.google.com/payments/u/0/home#sendRequestMoney"> Click to Pay with Google </a></u>
                      </body>
                      """.format(name=name, month=due_month, due_day=due_day, util_month=util_month, Rent=rent,
                                 Utilities=utilities, total=total)
    TO = email_address
    FROM = 'YOUR_EMAIL'
    py_mail("Courtesy Reminder", email_content, TO, FROM)


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
    password = "Your_Password"
    server.starttls()
    server.login(FROM, password)
    server.sendmail(FROM, [TO], MESSAGE.as_string())
    server.quit()

tenants = ['John', 'Jim', 'Joe', 'Bob']
payment_date = [1,3,1,8]
reminder_date=[]
for x in payment_date: reminder_date.append(x-3)
rent = [550,500,450,550]
utilities = [1,1,1,0]
emails = ['tenant@example.com', 'tenant@example.com', 'tenant@example.com', 'tenant@example.com']
utility_bill = float(input('Enter Utility Bill:'))

while 1:
    twoMonthsAgo, lastMonth, thisMonth, nextMonth, today, thisYear, days_in_month = todays_date()
    for x in range(0,len(tenants)):
        if reminder_date[x] < 1:
            reminder_date[x] = days_in_month + reminder_date[x]
            if reminder_date[x] == today:
                if thisMonth[0] == 'December':
                    send_email(tenants[x],emails[x],nextMonth[0],lastMonth[0],weekday(payment_date[x], nextMonth[1], thisYear+1)[0],rent[x],utilities[x],utility_bill)
                else:
                    send_email(tenants[x], emails[x], nextMonth[0], lastMonth[0],
                               weekday(payment_date[x], nextMonth[1], thisYear)[0], rent[x], utilities[x], utility_bill)
            continue
        if reminder_date[x] > 0:
            if reminder_date[x] == today:
                send_email(tenants[x], emails[x], thisMonth[0], twoMonthsAgo[0], weekday(payment_date[x], thisMonth[1], thisYear)[0],
                           rent[x], utilities[x], utility_bill)
    time.sleep(60*60*24)

