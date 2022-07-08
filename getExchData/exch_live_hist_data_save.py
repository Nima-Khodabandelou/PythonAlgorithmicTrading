import json

import time
from datetime import datetime

import math

from kucoin.client import Client

from Config.KucoinConfig import kucoin_api_key, kucoin_api_passphrase, kucoin_api_secret


def kucoin_api_data(start):
    ''' Gets exchange live data through web socket or API connection. '''
    client = Client(kucoin_api_key, kucoin_api_secret,
                    kucoin_api_passphrase)

    end = start + 60
    klines = client.get_kline_data('ADA-USDT', kline_type='1min',
                                   start=str(start), end=str(end))

    return klines


current_time = math.floor(time.time())
res = current_time % 60
current_1min_time = current_time - res
start = current_1min_time - 10*60

with open('klines.json', 'w', encoding='utf-8') as f:
    while True:
        if start < current_1min_time:
            klines = kucoin_api_data(start)
            json.dump(klines, f, ensure_ascii=False, indent=4)
            print('Recorded: ', datetime.utcfromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S'))
            # print('Current: ' , datetime.utcfromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S'))
            start += 60
        else:
            print('Sleep 5 seconds')
            time.sleep(5)
            try:
                klines = kucoin_api_data(start)
                if klines == []:
                    continue
                else:
                    json.dump(klines, f, ensure_ascii=False, indent=4)
                    print('Recorded: ', datetime.utcfromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S'))

                start += 60
            except:
                continue
