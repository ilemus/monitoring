import os, json, time, google_finance, file_reader, calculations, signal
from datetime import datetime


# https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
def string_b_on_lg(line):
    return '\033[92m' + line + '\033[0m'


def string_b_on_lr(line):
    return '\033[91m' + line + '\033[0m'


class Index:
    stochastic = []
    closes = []
    ema = []
    share = google_finance.Share
    avg_stoch = 0.0

    def __init__(self):
        self.stochastic = []
        self.closes = []
        self.ema = []
        self.share = None
        self.avg_stoch = 0.0


class Monitoring:
    mArgs = None
    mList = []
    indexes = []

    def __init__(self, args):
        self.mArgs = args
        self.load_preferences()
        signal.signal(signal.SIGINT, self.signal_handler)

    def clear(self):
        os.system('cls')

    # Main looping thread
    def run(self):
        while 1 == 1:
            self.clear()
            print("index\t%chg/price\t%K\td%K\tAvg. %K")
            list_size = len(self.mList)
            if len(self.mList) == 0:
                text = input("Enter stock to watch: ")
                self.mList.append(text)
                self.save_to_file()
            else:
                for i in range(len(self.mList)):
                    share = self.indexes[i].share
                    share.refresh()
                    current_price = ''
                    l = float(share.get_price())
                    op = float(share.get_open())
                    delta = l - op
                    if delta >= 0:
                        current_price = string_b_on_lg('(+' + "{0:.2f}".format(delta / op * 100) + '%) ' + str(l))
                    else:
                        current_price = string_b_on_lr('(-' + "{0:.2f}".format(abs(delta) / op * 100) + '%) ' + str(l))
                    temp = self.indexes[i].closes
                    temp.append(l)
                    new_stoch = calculations.get_k(temp, 14)
                    temp.pop(len(temp) - 1)
                    stochastic_print = ''
                    delta = new_stoch[len(new_stoch) - 1] - new_stoch[len(new_stoch) - 2]
                    if delta >= 0:
                        stochastic_print = string_b_on_lg("{0:.2f}".format(new_stoch[len(new_stoch) - 1]))
                    else:
                        stochastic_print = string_b_on_lr("{0:.2f}".format(new_stoch[len(new_stoch) - 1]))


                    stoch_delta = "{0:.2f}".format(delta)
                    avg_stoch = "{0:.2f}".format(self.indexes[i].avg_stoch)
                    # date = datetime.strptime(self.indexes[i].purchase_date, '%YYYY-%mm-%dd')

                    # Format is index\t%chg price\tstochiastic
                    out_line = self.mList[i] + ':\t' + current_price + '\t' + stochastic_print\
                               + '\t' + stoch_delta + '\t' + avg_stoch
                    print(out_line)

            time.sleep(300)

    def load_preferences(self):
        if os.path.exists("prefs"):
            if os.path.isfile("prefs/last"):
                file_object = open("prefs/last", "r")
                temp = json.loads(file_object.read())
                for index in temp['indexes']:
                    self.mList.append(index)
        if not os.path.exists("prefs/indexes"):
            os.makedirs("prefs/indexes")
        if len(self.mList) > 0 and os.path.exists("prefs/indexes"):
            for index in self.mList:
                if os.path.isfile("prefs/indexes/" + index):
                    file_object = open("prefs/indexes/" + index, "r")
                    temp = json.loads(file_object.read())
                    temp = self.parse_index(temp)
                    temp.share = google_finance.Share(index)
                    self.indexes.append(temp)
                else:
                    temp = self.generate_index(index)
                    self.indexes.append(temp)

    def generate_index(self, index):
        array = file_reader.get_index_data(index)
        closes = []
        for tick in array:
            closes.append(tick.Close)

        stochastic = calculations.get_k(closes, 14)
        ema24 = calculations.get_ema(closes, 24)

        ret_obj = Index()
        ret_obj.stochastic = stochastic[len(stochastic) - 20: len(stochastic)]
        ret_obj.ema = ema24[len(ema24) - 20: len(ema24)]
        ret_obj.closes = closes[len(closes) - 20: len(closes)]
        ret_obj.share = google_finance.Share(index)
        if len(stochastic) > 100:
            ret_obj.avg_stoch = sum(stochastic[len(stochastic) - 90: len(stochastic)]) / 90
        else:
            ret_obj.avg_stoch = sum(stochastic[len(stochastic) - 20: len(stochastic)]) / 20

        return ret_obj

    def parse_index(self, jObj):
        ret_obj = Index()
        if 'stochastic' in jObj:
            for stoch in jObj['stochastic']:
                ret_obj.stochastic.append(float(stoch))
        if 'closes' in jObj:
            for close in jObj['closes']:
                ret_obj.closes.append(float(close))
        if 'ema' in jObj:
            for ema in jObj['ema']:
                ret_obj.ema.append(float(ema))
        if 'avg_stoch' in jObj:
            ret_obj.avg_stoch = jObj['avg_stoch']
        return ret_obj

    def create_index(self, idx):
        jObj = {'stochastic': [], 'closes': [], 'ema': [], 'avg_stoch': ''}
        for stoch in idx.stochastic:
            jObj['stochastic'].append(stoch)
        for close in idx.closes:
            jObj['closes'].append(close)
        for ema in idx.ema:
            jObj['ema'].append(ema)
        jObj['avg_stoch'] = idx.avg_stoch

        return jObj

    def save_to_file(self):
        try:
            # Save stock list (which indexes are watched)
            if not os.path.exists("prefs"):
                os.makedirs("prefs")

            with open('prefs/last', 'w') as outfile:
                to_file = {'indexes': []}
                for i in range(len(self.mList)):
                    to_file['indexes'].append(self.mList[i])
                json.dump(to_file, outfile)
        except OSError:
            return

        try:
            # Save stock meta data
            if len(self.mList) > 0 and os.path.exists("prefs/indexes"):
                for i in range(len(self.mList)):
                    with open('prefs/indexes/' + self.mList[i], 'w') as outfile:
                        json.dump(self.create_index(self.indexes[i]), outfile)
        except OSError:
            return

    def signal_handler(self, signal, frame):
        print('Saving...')
        self.save_to_file()
        exit(0)

temp = Monitoring('asdf')
temp.run()