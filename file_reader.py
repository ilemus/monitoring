from datetime import datetime
import os
import pytz
import glob


class Tick:
    Datetime = datetime.utcnow()
    Open = 0.0
    High = 0.0
    Low = 0.0
    Close = 0.0
    Volume = 0
    OpenInt = 0


# Format for stooq hourly data
# Date,Time,Open,High,Low,Close,Volume,OpenInt
# ex. 2015-06-04,20:00:00,24.525,24.525,24.525,24.525,1019,0
# Date,Open,High,Low,Close,Volume,OpenInt
# ex. 1970-01-02,3.1254,3.1254,3.092,3.1254,29448,0
def read_line(line):
    columns = line.split(',')
    data = Tick()
    # If the line does not match the format, then return empty object
    if len(columns) < 7:
        return data

    if len(columns) == 8:
        time = columns[0] + ' ' + columns[1]
        # GMT-2
        date = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        # To EST
        data.Datetime = date.replace(tzinfo=pytz.timezone('Etc/GMT-2')).astimezone(pytz.timezone('US/Michigan'))
        data.Open = float(columns[2])
        data.High = float(columns[3])
        data.Low = float(columns[4])
        data.Close = float(columns[5])
        data.Volume = int(columns[6])
        data.OpenInt = int(columns[7])
    elif len(columns) == 7:
        time = columns[0]
        data.Datetime = datetime.strptime(time, '%Y-%m-%d')
        data.Open = float(columns[1])
        data.High = float(columns[2])
        data.Low = float(columns[3])
        data.Close = float(columns[4])
        data.Volume = int(columns[5])
        data.OpenInt = int(columns[6])

    return data


def get_file_path(index):
    # file format
    return find(index.lower() + '.us.txt', '.')


def find(name, path):
    # Found online: https://stackoverflow.com/questions/1724693/find-a-file-in-python
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return ''


def get_index_data(index):
    ticks = []
    try:
        contents = []
        with open(get_file_path(index)) as file:
            contents = file.readlines()

        if len(contents) == 0:
            return ticks

        # Remove the first line since it is just the header
        contents.pop(0)

        for i in range(len(contents)):
            ticks.append(read_line(contents[i]))

    except FileNotFoundError:
        return ticks
    return ticks


def get_file_list():
    return glob.glob('data/**/*.us.txt', recursive=True)


def get_index_name(file_path):
    temp = file_path.split("\\")
    arr = []
    for part in temp:
        if part.find(".") != -1:
            arr = part.split(".")

    if len(arr) == 0:
        return ""

    return arr[0]


def get_indexes_list():
    arr = []
    for file in get_file_list():
        arr.append(get_index_name(file))

    return  arr
