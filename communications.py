import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import calendar
import datetime
import time

Gmail_Account = 'starksupply0@gmail.com'
Password = 'business1579'
# We may need to discontinue using Gmail as our server because they tend to block logins from hosting services
# This file will grow to be a conveiniant way to send emails with attachments, texts and if need be recieve and download email attachements

def send_reminder_email(name, email_address, rent, due_date):
    name,rent = str(name), '${:,.2f}'.format(rent)
    due_month = due_date.strftime('%B')
    due_day = due_date.strftime('%A')

    email_content = """
                      <head>
                        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                      </head>
                      <body>
                        Hello {name},<br>&nbsp;&nbsp;&nbsp;&nbsp; This is a courtesy reminder that rent for {month} is due on {day},
                         please pay the following amount to email address: {Gmail}<br><br>
                         Rent: {Rent}<br><br>
                          <u><a href="https://pay.google.com/payments/u/0/home#sendRequestMoney"> Click to Pay with Google </a></u>
                      </body>
                      """.format(name=name, month=due_month, day=due_day, Rent=rent, Gmail = Gmail_Account)
    TO = email_address
    FROM = Gmail_Account
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
    password = Password
    server.starttls()
    server.login(FROM, password)
    server.sendmail(FROM, [TO], MESSAGE.as_string())
    server.quit()
