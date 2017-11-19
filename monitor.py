import os, json, time, google_finance, file_reader, calculations


# https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
def string_b_on_lg(line):
    return '\033[92m' + line + '\033[0m'


def string_b_on_lr(line):
    return '\033[91m' + line + '\033[0m'


class Index:
    purchase_price = 0.0
    stochastic = []
    closes = []
    ema = []
    share = google_finance.Share


class Monitoring:
    mArgs = None
    mList = []
    indexes = []

    def __init__(self, args):
        self.mArgs = args
        self.load_preferences()

    def clear(self):
        os.system('cls')

    # Main looping thread
    def run(self):
        while 1 == 1:
            self.clear()
            list_size = len(self.mList)
            if len(self.mList) == 0:
                text = input("Enter stock to watch: ")
                self.mList.append(text)
                self.save_to_file()
            else:
                for i in range(len(self.mList)):
                    share = self.indexes[i].share
                    current_price = ''
                    l = float(share.get_price())
                    op = float(share.get_open())
                    delta = l - op
                    if delta >= 0:
                        current_price = string_b_on_lg('(+' + "{0:.2f}".format(delta / op * 100) + '%) ' + str(l))
                    else:
                        current_price = string_b_on_lr('(-' + "{0:.2f}".format(abs(delta) / op * 100) + '%) ' + str(l))
                    out_line = self.mList[i] + ': ' + current_price
                    print(out_line)

            time.sleep(5)

    def load_preferences(self):
        if os.path.exists("prefs"):
            if os.path.isfile("prefs/last"):
                file_object = open("prefs/last", "r")
                temp = json.loads(file_object.read())
                for index in temp['indexes']:
                    self.mList.append(index)

        if len(self.mList) > 0 and os.path.exists("prefs/indexes"):
            for index in self.mList:
                if os.path.isfile("prefs/indexes/" + index):
                    file_object = open("prefs/indexes", "r")
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


        ret_obj = Index
        ret_obj.stochastic = stochastic[len(stochastic) - 20: len(stochastic)]
        ret_obj.ema = ema24[len(ema24) - 20: len(ema24)]
        ret_obj.closes = closes[len(closes) - 20: len(closes)]
        ret_obj.share = google_finance.Share(index)
        ret_obj.purchase_price = float(input("Enter purcahse price " + index + ": "))


    def parse_index(self, jObj):
        ret_obj = Index
        if 'purchase_price' in jObj:
            ret_obj.purchase_price = jObj['purchase_price']
        if 'stochastic' in jObj:
            for stoch in jObj['stochastic']:
                ret_obj.stochastic.append(float(stoch))
        if 'closes' in jObj:
            for close in jObj['closes']:
                ret_obj.closes.append(float(close))
        if 'ema' in jObj:
            for ema in jObj['ema']:
                ret_obj.ema.append(float(ema))
        return ret_obj

    def create_index(self, index):
        jObj = {'purchase_price': 0.0, 'stochastic': [], 'closes': [], 'ema': []}
        jObj['purchase_price'] = index.purchase_price
        for stoch in index.stochastic:
            jObj['stochastic'].append(stoch)
        for close in index.closes:
            jObj['closes'].append(close)
        for ema in index.ema:
            jObj['ema'].append(ema)

        return jObj

    def save_to_file(self):
        try:
            if not os.path.exists("prefs"):
                os.makedirs("prefs")

            with open('prefs/last', 'w') as outfile:
                to_file = {'indexes': []}
                for i in range(len(self.mList)):
                    to_file['indexes'].append(self.mList[i])
                json.dump(to_file, outfile)
        except OSError:
            return


# temp = Monitoring('asdf')
# temp.run()