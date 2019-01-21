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
        start_day, end_day = monthrange(lease_start_date.year, lease_start_date.month)
        remaining_days_delta = end_day - lease_start_date.day

        prorated = rent_per_month / end_day * int(remaining_days_delta)

        return math.ceil(prorated)


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
print(id(all_tenants[1]))



# To be continued

# def payment_dates_generator(start_date, lease_length, pay_day='default'):
#     """
#     Output all payment dates in a lease in proper format to be converted to epoch number
#     :param start_date: <type string> <format day.month.year> <example '01.04.2019'>
#     :param lease_length: <type integer> <example 3>
#     :param pay_day: (optional, default start date) <type string> <format day> <example '05'>
#     :return: <example ['05.04.2019 12:00:00', '05.05.2019 12:00:00', '05.06.2019 12:00:00']
#     """
#     if pay_day != 'default':
#         pass
#     else:
#         pay_day = start_date[0:2]
#     start_date = start_date + ' 12:00:00'
#     i = int(start_date[3:5])
#     payment_dates = []
#     for x in range(0, lease_length):
#         si = str(i)
#         if len(si) == 1:
#             si = '0' + si
#         payment_dates.append(pay_day + '.' + si + start_date[5:])
#         i += 1
#         if i == 13:
#             i = 1
#     return payment_dates
#
#
# for x in payment_dates_generator('01.04.2019', 3, '05'):
#     pattern = '%d.%m.%Y %H:%M:%S'
#     epoch = int(time.mktime(time.strptime(x, pattern)))
#     print(epoch)
#     reminder_date = epoch - 60 * 60 * 24 * 3
#     print(time.ctime(reminder_date))
