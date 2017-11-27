import json
import requests
import os


class Share:
    open = 0.0
    close = 0.0
    current = 0.0
    hi = 0.0
    lo = 0.0
    market_cap = 'N/A'
    industry = 'N/A'
    pe_ratio = 0.0
    daily_volume = 'N/A'
    average_volume = 'N/A'
    jResp = None
    mSymbol = None
    shares = ''

    def __init__(self, symbol):
        self.mSymbol = symbol
        if os.path.exists("json"):
            if os.path.isfile("json/" + symbol):
                file_object = open("json/" + symbol, "r")
                self.load_json(json.loads(file_object.read()))
                return
        rsp = requests.get('https://finance.google.com/finance?q=' + symbol + '&output=json')
        if rsp.status_code in (200,):
            try:
                jobj = json.loads(rsp.content[6:-2].decode('unicode_escape'))
                self.jResp = jobj
                self.load_json(jobj)
                self.save_to_file()
            except json.decoder.JSONDecodeError:
                return
        else:
            print('Error Code: ' + str(rsp.status_code))
        return

    def load_json(self, jobj):
        # print(json.dumps(jobj, indent=2))
        try:
            if 'l' in jobj:
                self.current = jobj['l']
            if 'op' in jobj:
                self.open = jobj['op']
            if 'mc' in jobj:
                self.market_cap = jobj['mc']
            if 'sname' in jobj:
                self.industry = jobj['sname']
            if 'pe' in jobj:
                try:
                    self.pe_ratio = float(jobj['pe'].replace(',', ''))
                except ValueError:
                    print(jobj['pe'])
            if 'vo' in jobj:
                self.daily_volume = jobj['vo']
            if 'avvo' in jobj:
                self.average_volume = jobj['avvo']
            if 'shares' in jobj:
                self.shares = jobj['shares']
        except KeyError:
            return

    def refresh(self):
        rsp = requests.get('https://finance.google.com/finance?q=' + self.mSymbol + '&output=json')
        if rsp.status_code in (200,):
            jobj = json.loads(rsp.content[6:-2].decode('unicode_escape'))
            self.jResp = jobj
            self.load_json(jobj)
            self.save_to_file()
        else:
            print('Error Code: ' + str(rsp.status_code))
        return

    def get_price(self):
        return self.current

    def get_open(self):
        return self.open

    def get_market_cap(self):
        return self.market_cap

    def get_industry(self):
        return self.industry

    def get_price_earnings_ratio(self):
        return self.pe_ratio

    def get_daily_volume(self):
        return self.daily_volume

    def get_average_volume(self):
        return self.average_volume

    def get_shares(self):
        return self.shares

    def parse_formatted(self, value):
        appen = value[-1:]

        try:
            ret_val = float(value[0:len(value) - 2])
        except ValueError:
            ret_val = 0

        if appen == 'M':
            ret_val *= 1000000
        elif appen == 'B':
            ret_val *= 1000000000
        elif appen == 'T':
            ret_val *= 1000000000000

        return ret_val


    def save_to_file(self):
        try:
            if not os.path.exists("json"):
                os.makedirs("json")

            with open('json/' + self.mSymbol, 'w') as outfile:
                json.dump(self.jResp, outfile)
        except OSError:
            return
