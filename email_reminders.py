import communications
import time, datetime, math
from calendar import monthrange
import calendar


class Tenant:
    def __init__(self, rent_per_month, lease_start_date, lease_end_date, email_address, phone_number):
        self.lease_start_date = datetime.datetime.strptime(lease_start_date, '%x')
        self.lease_end_date = datetime.datetime.strptime(lease_end_date, '%x')
        self.rent_per_month = rent_per_month
        self.rent_prorated = self.generate_prorated(self.rent_per_month, self.lease_start_date)
        self.first_name = 'Default_First_Name'
        self.last_name = 'Default_Last_Name'
        self.email_adress = email_address
        self.phone_number = phone_number
        self.utility_share_portion = .3
        self.tenant_address = '123 easy street, colorado springs, CO 80923'
        self.tenant_unit = 'A'

    def send_automatic_emails(self, pay_day=1, remind_days_in_advance=3, grace_period=2):
        reminder_dates,payment_dates,warning_dates = self.reminder_dates_generator\
            (self.lease_start_date, self.lease_end_date, pay_day, remind_days_in_advance, grace_period)
        while 1:
            for x in range(0,len(reminder_dates)):
                today = datetime.datetime.today()
                today = today.replace(today.year,today.month,today.day,0,0,0,0)
                if reminder_dates[x] == today:
                    communications.send_reminder_email(self.first_name,self.email_adress, self.rent_per_month, payment_dates[x])
            time.sleep(60*60*24)


    @staticmethod
    def generate_prorated(rent_per_month, lease_start_date):
        _, end_day = monthrange(lease_start_date.year, lease_start_date.month)
        remaining_days_delta = end_day - lease_start_date.day

        prorated = rent_per_month / end_day * int(remaining_days_delta)

        return math.ceil(prorated)

    @staticmethod
    def reminder_dates_generator(lease_start_date, lease_end_date, pay_day=1, remind_days_in_advance=3, grace_period = 3):
        last_reminder_date = lease_end_date.replace(lease_end_date.year, lease_end_date.month, pay_day)
        payment_date = lease_start_date
        payment_dates = [payment_date]
        reminder_dates = []
        warning_dates = []
        while payment_dates[-1] != last_reminder_date:
            if payment_date.month == 12:
                payment_date = payment_date.replace(payment_date.year + 1, 1, pay_day)
            else:
                payment_date = payment_date.replace(payment_date.year, payment_date.month + 1, pay_day)
            payment_dates.append(payment_date)
            x = payment_date.timestamp() # convert payment date to seconds since epoch
            warning_date = x + 60 * 60 * 24 * grace_period  # add 24hrs times grace period
            warning_date = datetime.datetime.fromtimestamp(warning_date) # convert back to standard datetime format
            warning_dates.append(warning_date)
            reminder_date = x - 60 * 60 * 24 * remind_days_in_advance
            reminder_date = datetime.datetime.fromtimestamp(reminder_date)
            reminder_dates.append(reminder_date)
        payment_dates = payment_dates[1:]
        return reminder_dates, payment_dates, warning_dates



Cameron = Tenant(400, '01/15/19','02/25/20','starkcameron@ymail.com', '7604538591')
Cameron.send_automatic_emails(7,0)
