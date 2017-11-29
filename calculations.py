

# get the EMA of a period starting at the index of the period - 1
# 0, 0, 0, 0, 5
def get_ema(values, period):
    if period > len(values):
        return []

    ret_arr = [0] * len(values)
    multiplier = (2.0 / (period + 1))
    ret_arr[period - 1] = sum(values[0:period]) / period
    # print(sum(values[0:period]))
    # print(values[0])
    for i in range(0, period - 1):
        ret_arr[i] = 0
    for i in range(period, len(values)):
        ret_arr[i] = (values[i] - ret_arr[i - 1]) * multiplier + ret_arr[i - 1]

    # print('ema' + str(period) + ': ' + str(ret_arr[period - 1: period + 5]))

    return ret_arr


# 9day  - 26day / 26day ema
def get_ppo(values):
    if len(values) < 26:
        return []
    day12 = get_ema(values, 12)
    day26 = get_ema(values, 26)
    ret_arr = [0] * len(values)
    for i in range(26, len(values)):
        ret_arr[i] = (day12[i] - day26[i]) / day26[i]

    return ret_arr


def get_max_index(values):
    max = values[0]
    index = 0
    for i in range(1, len(values)):
        if values[i] > max:
            max = values[i]
            index = i

    return index


def get_min_index(values):
    min = values[0]
    index = 0
    for i in range(1, len(values)):
        if values[i] < min:
            min = values[i]
            index = i

    return index


def get_high(values):
    temp = 0
    for value in values:
        if value > temp:
            temp = value

    return temp


def get_low(values):
    temp = values[0]
    for i in range(1, len(values)):
        if values[i] < temp:
            temp = values[i]

    return temp


def get_k(values, period):
    if len(values) < period:
        return []

    ret_arr = [0] * len(values)

    for i in range(period - 1, len(values)):
        if (get_high(values[i - (period - 1): i + 1]) - get_low(values[i - (period - 1):i + 1])) == 0:
            ret_arr[i] = 100
        else:
            ret_arr[i] = (values[i] - get_low(values[i - (period - 1):i + 1])) /\
                     (get_high(values[i - (period - 1): i + 1]) - get_low(values[i - (period - 1):i + 1])) * 100

    return ret_arr
