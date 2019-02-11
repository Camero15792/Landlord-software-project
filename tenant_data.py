import datetime, math, time
from calendar import monthrange


class Tenant:
        lease_start_date = datetime.datetime
        lease_end_date = datetime.datetime
        rent_per_month = 0
        rent_prorated = 0
        first_name = ''
        last_name = ''
        utility_share_portion = 0
        tenant_address = ''
        tenant_unit = ''
        tenant_id = 0



def generate_prorated(rent_per_month, lease_start_date):
    start_day, end_day = monthrange(lease_start_date.year, lease_start_date.month)
    remaining_days_delta = end_day - lease_start_date.day

    prorated = rent_per_month / end_day * int(remaining_days_delta)

    return math.ceil(prorated)



def generate_id():
    return int(round(time.time() * 1000))