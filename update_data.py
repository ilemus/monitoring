# https://github.com/lukaszbanasiak/yahoo-finance
from google_finance import Share
from datetime import datetime
import pytz
import os


def get_hourly_prices_from_file(from_date, to_date, index):
    date1 = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S')
    date2 = datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S')
    # 2017-10-30 20:01:00
    if date2 < date1:
        return []

    try:
        filename = "data/" + index + ".csv"
        file_obj = open(filename, 'r')
        data = file_obj.readlines()
    except FileNotFoundError as e:
        return []

    # Parse the data and make sure that return is between those dates
    if len(data) < 9:
        return []
    else:
        return data


def update_hourly_prices(index):
    getter = Share(index)
    price = getter.get_price()
    date = datetime.now()
    # 'US/Michigan' to 'Etc/GMT-2'
    date = date.replace(tzinfo=pytz.timezone('US/Michigan')).astimezone(pytz.timezone('Etc/GMT-2'))
    output = date.strftime('%Y-%m-%d,%H:%M:%S') + ',' + str(price)\
             + ',' + str(price) + ',' + str(price) + ','\
             + str(price) + ',' + str(0) + ',' + str(0) + '\n'
    print(output)
    filename = "data/" + index + ".us.txt"

    # Create directory if it does not exist
    if not os.path.exists("data"):
        os.makedirs("data")

    try:
        file_obj = open(filename, 'a')
        file_obj.write(output)
    except FileNotFoundError:
        file_obj = open(filename, 'w')
        file_obj.write(output)