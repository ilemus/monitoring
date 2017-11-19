from threading import Thread
import file_reader
import calculations
import time
import datetime
import update_data
from google_finance import Share
# import matplotlib.pyplot
import sys
import monitor


def spawn_worker(arg, current):
    datetime_temp = datetime.datetime.strptime('Nov 10 2017  3:20PM', '%b %d %Y %I:%M%p')
    index = arg
    # print(index)
    # update_data.update_hourly_prices(index)

    array = file_reader.get_index_data(index)
    times = []
    closes = []
    for tick in array:
        closes.append(tick.Close)
        times.append(tick.Datetime)

    stochastic = calculations.get_k(closes, 14)
    ppo = calculations.get_ppo(closes)
    ema24 = calculations.get_ema(closes, 24)

    if len(ema24) == 0 or len(ppo) == 0 or len(stochastic) == 0:
        return
    # mins = []
    # maxs = []
    # mins_n = []
    # maxs_n = []
    # min_i = []
    # max_i = []
    curr_buy = []
    total = 0.0
    days_own = 0
    range_ema = [0] * 100

    # index_over2016 = 0

    # THIS IS THE ORIGINAL CODE
    #  ,  , x, x, x, x, x
    # 0, 1, 2, 3, 4, 5, 6, 7, 8
    # for i in range(24, len(ppo)):
        # if times[i] < datetime_temp:
            # continue
        # elif index_over2016 == 0:
            # index_over2016 = i
        # if len(curr_buy) > 0:
            # days_own += 1
        # if ema24[i - 24] < ema24[i]:
            # if calculations.get_min_index(ppo[i:(i + 5)]) == 3:
            # if stochastic[i] < 20:
                # mins.append(ppo[i + 4])
                # min_i.append(i)
                # if len(curr_buy) == 0:
                    # curr_buy.append(closes[i])
                    # print(datetime.datetime.strftime(times[i], "%Y-%m-%d") + " to ", end="")
                    # print("buy " + index + ", price: " + str(closes[i]))
            # elif calculations.get_max_index(ppo[i:(i + 5)]) == 3:
            # elif stochastic[i] > 80:
                # maxs.append(ppo[i + 4])
                # max_i.append(i)
                # if len(curr_buy) > 0:
                    # temp_price = closes[i] - curr_buy.pop(0)
                    # total += temp_price
                    # print(datetime.datetime.strftime(times[i], "%Y-%m-%d") + ': ' + "{0:.2f}".format(temp_price))
        # else:
        #     if calculations.get_min_index(ppo[i:(i + 5)]) == 3:
                # mins_n.append(ppo[i + 4])
        #         continue
        #     elif calculations.get_max_index(ppo[i:(i + 5)]) == 3:
                # maxs_n.append(ppo[i + 4])
        #         continue
    # THIS IS THE ORIGINAL CODE

    # print("ppo: " + str(len(ppo)) + ", closes: " + str(len(closes)))

    # avg_max = sum(maxs) / len(maxs)
    # avg_min = sum(mins) / len(mins)
    # avg_max_n = sum(maxs_n) / len(maxs_n)
    # avg_min_n = sum(mins_n) / len(mins_n)

    # avg_max_s = sorted(maxs)
    # median_max = 0
    # avg_min_s = sorted(mins)
    # median_min = 0

    # if len(avg_max_s) % 2 == 0:
    #     median_max = (avg_max_s[int(len(avg_max_s) / 2)] + avg_max_s[int((len(avg_max_s)) / 2) + 1]) / 2
    # else:
    #     median_max = avg_max_s[int(len(avg_max_s) / 2) + 1]

    # if len(avg_min_s) % 2 == 0:
    #     median_min = (avg_min_s[int(len(avg_min_s) / 2)] + avg_min_s[int((len(avg_min_s)) / 2) + 1]) / 2
    # else:
    #     median_min = avg_min_s[int(len(avg_min_s) / 2)]

    # avg_dist_min = 0
    # for i in range(1, len(min_i)):
    #     avg_dist_min += min_i[i] - min_i[i - 1]

    # avg_dist_min /= len(min_i)

    # avg_dist_max = 0
    # for i in range(1, len(max_i)):
    #     avg_dist_max += max_i[i] - max_i[i - 1]

    # avg_dist_max /= len(max_i)

    # print('max avg.: ' + str(avg_max))
    # print('max median: ' + str(median_max))
    # print('max dist: ' + str(avg_dist_max))
    # print('min avg.: ' + str(avg_min))
    # print('min median: ' + str(median_min))
    # print('min dist: ' + str(avg_dist_min))
    # print('max n avg.: ' + str(avg_max_n))
    # print('min n avg.: ' + str(avg_min_n))
    # print('Total gain: ' + str(total) + ', %: ' + str(total / closes[index_over2016] * 100))
    # print('start price: ' + str(closes[index_over2016]) + ', end: ' + str(closes[len(closes) - 1]))
    # print('Average gain: ' + str(closes[len(closes) - 1] - closes[index_over2016]) + ", %: "
                    # + str((closes[len(closes) - 1] - closes[index_over2016])/closes[index_over2016] * 100))
    # print('hours owned: (' + str(days_own) + '/' + str(len(closes) - index_over2016) + ')' + '\n')
    # 0.378 (*2)
    #  ,  , 2, 3, 4, 5 len = 4
    # 0, 1, 2, 3, 4, 5 len = 6
    # print('avg total: ' + str(sum(ppo[40:len(ppo)]) / (len(ppo) - 40)))

    # data = []
    # for i in range(0, 50):
    #     data.append(i)

    # matplotlib.pyplot.plot(ppo)
    # matplotlib.pyplot.show()
    last_day = len(ppo) - 1
    avg_1 = (stochastic[last_day - 1] + stochastic[last_day - 2] + stochastic[last_day - 3]) / 3
    avg_0 = (stochastic[last_day] + stochastic[last_day - 1] + stochastic[last_day - 2]) / 3
    value = 0
    if stochastic[last_day] - stochastic[last_day - 1] == 0:
        value = 0
    else:
        value = ((closes[last_day] - closes[last_day - 1]) / closes[last_day - 1] * 100)\
                / (stochastic[last_day] - stochastic[last_day - 1])

    if ema24[last_day - 24] < ema24[last_day]:
        if ema24[last_day - 24] == 0:
            return
        ema_delta = (ema24[last_day] - ema24[last_day - 24]) / ema24[last_day - 24] * 100
        if stochastic[last_day] < 20:
            if stochastic[last_day - 1] < stochastic[last_day]:
                meta = Share(index)
                # sys.stdout.flush()
                print('[' + meta.get_industry() + '] buy ' + index+ ' ' + meta.get_market_cap()
                      + ' ' + "{0:.2f}".format(closes[last_day]) + ' '
                      + "{0:.2f}".format(ema_delta) + ' '
                      + "{0:.2f}".format(stochastic[last_day]) + " " + "{0:.2f}".format(value))
        # elif stochastic[last_day] > 80:
        #     if stochastic[last_day - 1] > stochastic[last_day]:
        #         meta = Share(index)
                # sys.stdout.flush()
        #         print('[' + meta.get_industry() + '] sell ' + index+ ' ' + meta.get_market_cap()
        #               + ' ' + "{0:.2f}".format(closes[last_day]) + ' '
        #               + "{0:.2f}".format(ema_delta) + ' '
        #               + "{0:.2f}".format(stochastic[last_day]) + " " + "{0:.2f}".format(value))
        # elif 20 < stochastic[last_day] < 80:
        #     if avg_1 > avg_0:
        #         meta = Share(index)
                # sys.stdout.flush()
        #         print('[' + meta.get_industry() + '] sell ' + index + ' ' + meta.get_market_cap()
        #               + ' ' + "{0:.2f}".format(closes[last_day]) + ' '
        #               + "{0:.2f}".format(ema_delta) + ' '
        #               + "{0:.2f}".format(stochastic[last_day]) + " " + "{0:.2f}".format(value))

    # time.sleep(1)


if __name__ == "__main__":
    args = sys.argv
    if len(sys.argv > 1):
        temp = monitor.Monitoring
        temp.run()
        exit()

    threads = []
    # this is your portfolio
    indexes = file_reader.get_indexes_list()
    # date = datetime.datetime.strptime('Nov 10 2017  3:20PM', '%b %d %Y %I:%M%p')
    # date2 = datetime.datetime.strptime('Nov 10 2017  4:00PM', '%b %d %Y %I:%M%p')
    # print(str((date2 - date).total_seconds()))
    # if date.time() >= datetime.time(10, 00) and date.time() < datetime.time(16, 00):
        # print('true')
    # else:
        # print('false')
    # exit()
    print("industry buy/sell Cap price ema_delta %K dPdK")

    while 1 == 1:
        old_time = time.time()
        for i in range(len(indexes)):
            threads.append(Thread(target=spawn_worker, args=(indexes[i], i, )))
            threads[len(threads) - 1].start()
            if i % 4 == 0:
                # sys.stdout.flush()
                # sys.stdout.write("\r" + "{0:.2f}".format((i / len(indexes)) * 100) + "%")
                for i in range(len(threads)):
                    threads.pop(0).join()

        for i in range(len(threads)):
            threads.pop(0).join()

        del threads[:]
        # Sleep until next calculation
        if old_time - time.time() < 3600000:
            # time.sleep(10 - (time.time() - old_time))
            break
        else:
            break

    time.sleep(1)
    print("thread finished...exiting")
