import time


# Am rewriting script to make easier to build upon and follow
# Not Complete


def payment_dates_generator(start_date,lease_length,pay_day='default'):
    """
    Output all payment dates in a lease in proper format to be converted to epoch number
    :param start_date: <type string> <format day.month.year> <example '01.04.2019'>
    :param lease_length: <type integer> <example 3>
    :param pay_day: (optional, default start date) <type string> <format day> <example '05'>
    :return: <example ['05.04.2019 12:00:00', '05.05.2019 12:00:00', '05.06.2019 12:00:00']
    """
    if pay_day != 'default':
        pass
    else:
        pay_day = start_date[0:2]
    start_date = start_date+' 12:00:00'
    i = int(start_date[3:5])
    payment_dates = []
    for x in range(0, lease_length):
        si = str(i)
        if len(si) == 1:
            si = '0'+si
        payment_dates.append(pay_day+'.'+si+start_date[5:])
        i += 1
        if i == 13:
            i = 1
    return payment_dates

for x in payment_dates_generator('01.04.2019',3,'05'):
    pattern = '%d.%m.%Y %H:%M:%S'
    epoch = int(time.mktime(time.strptime(x, pattern)))
    print(epoch)
    reminder_date = epoch - 60*60*24*3
    print(time.ctime(reminder_date))

