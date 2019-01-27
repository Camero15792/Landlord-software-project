
import time, datetime, math
from calendar import monthrange


class Tenant:
    def __init__(self, rent_per_month, lease_start_date, lease_end_date):
        self.lease_start_date = datetime.datetime.strptime(lease_start_date, '%x')
        self.lease_end_date = datetime.datetime.strptime(lease_end_date, '%x')
        self.rent_per_month = rent_per_month
        self.rent_prorated = self.generate_prorated(self.rent_per_month, self.lease_start_date)
        self.first_name = 'Default_First_Name'
        self.last_name = 'Default_Last_Name'
        self.utility_share_portion = .3
        self.tenant_address = '123 easy street, colorado springs, CO 80923'
        self.tenant_unit = 'A'

    @staticmethod
    def generate_prorated(rent_per_month, lease_start_date):
        _, end_day = monthrange(lease_start_date.year, lease_start_date.month)
        remaining_days_delta = end_day - lease_start_date.day

        prorated = rent_per_month / end_day * int(remaining_days_delta)

        return math.ceil(prorated)

    @staticmethod
    def reminder_dates_generator(lease_start_date, lease_end_date, pay_day=1, remind_days_in_advance=3):
        # Returns two lists: one is all the dates the tenant must pay rent. The other is x amount of days before the tenant must pay rent
        # The idea is to build logic to automatically email and/or text the tenant that rent is due in x days
        last_reminder_date = lease_end_date.replace(lease_end_date.year, lease_end_date.month, pay_day)
        payment_dates = [lease_start_date]
        while payment_dates[-1] != last_reminder_date:
            if lease_start_date.month == 12:
                lease_start_date = lease_start_date.replace(lease_start_date.year + 1, 1, pay_day)
            else:
                lease_start_date = lease_start_date.replace(lease_start_date.year, lease_start_date.month + 1, pay_day)
            payment_dates.append(lease_start_date)
        payment_dates = payment_dates[1:]
        reminder_dates = []
        for reminder_date in payment_dates:
            reminder_date = reminder_date.timestamp()
            reminder_date = reminder_date - 60 * 60 * 24 * remind_days_in_advance
            reminder_date = datetime.datetime.fromtimestamp(reminder_date)
            reminder_dates.append(reminder_date)
        return reminder_dates, payment_dates



# We will need to generate tenant objects that can be used to store information for the tenants during runtime. The tenant information
# can be saved into a config file or other storage medium when program is not in use. From these tenant objects we can do all other work.

# Lets get the basic information into our object. prorated is automatically generated.
example_tenant = Tenant(400, '05/15/19', '05/15/20')

# If we want to reference this tenant we can read its unique ID, later on we can reference using the tenants name once we know it.
print(id(example_tenant))

# The tenant gave us his drivers licesnse so now we can add his legal name to the object
example_tenant.first_name = 'John'
example_tenant.last_name = 'Doe'

# We can great a list with an arbitrary amount of tenants
all_tenants = [example_tenant, Tenant(600, '02/15/19', '02/15/21')]

# ...and keep their unique IDs from each other even though we dont know the name of tenant 2
print(id(all_tenants[0]))
