import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import calendar
import datetime
import time
from email import encoders

Gmail_Account = ''
Password = ''
BillPath = 'C:/Users/Cameron Stark/Documents/ViewBill.pdf'



def send_reminder_email(name, email_address, rent, due_date, utility_bill, number_tenants, util_month, util_portion):
    if util_portion == 0:
        utilities = 0
    else:
        utilities = utility_bill/number_tenants
    total = rent + utilities
    name,rent,utilities,total = str(name), '${:,.2f}'.format(rent),'${:,.2f}'.format(utilities),'${:,.2f}'.format(total)
    due_month = due_date.strftime('%B')
    due_day = due_date.strftime('%A')

    email_content = """
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      </head>
      <body>
        Hello {name},<br><br>&nbsp;&nbsp;&nbsp;&nbsp; This is a courtesy reminder that rent for {due_month} and Utilities
         for {util_month} are due on {due_day},
         please pay the following amounts to email address: coholdingsllc@gmail.com<br><br>
         Rent: {rent} + Utilities: {utilities} = Total: {total}<br><br>
          <u><a href="https://pay.google.com/payments/u/0/home#sendRequestMoney"> Click to Pay with Google </a></u>
      </body>
      """.format(name=name, due_month=due_month, due_day=due_day, rent=rent, util_month=util_month, utilities=utilities, total=total)
    TO = email_address
    FROM = Gmail_Account
    py_mail("Courtesy Reminder", email_content, TO, FROM, BillPath)


def py_mail(SUBJECT, BODY, TO, FROM, ATTACHMENT='null'):
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
    # Add attachment
    if ATTACHMENT != 'null':
        part = MIMEBase('application', "octet-stream")
        with open(ATTACHMENT, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % 'ViewBill.pdf')
        MESSAGE.attach(part)
    server = smtplib.SMTP('smtp.gmail.com:587')
    # Credentials (if needed) for sending the mail
    server.starttls()
    server.login(FROM, Password)
    server.sendmail(FROM, [TO], MESSAGE.as_string())
    server.quit()

