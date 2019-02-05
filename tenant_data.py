import datetime, math, json
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



if __name__ == "__main__":
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