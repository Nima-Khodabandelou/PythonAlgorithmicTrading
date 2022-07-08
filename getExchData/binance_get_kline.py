import csv

from binance.client import Client

import sys
sys.path.append('../..')

# from selected_assets import assets


base_path = "C:\\files\\algotrader\\main\\"
data_path = base_path + "data\\hist_data\\"

API_KEY = 'NZsrbx4ZNf98YNAr25H35agc2cys2oThZPdFquxoKSx21nR9Y5nSsZYLWOXkr2wZ'
API_SECRET = '3Eh4p0Bi2hlKw9ZbQlgN535z85uS7QozTvIfLZyq3I0J8lo4A5mKHVRD8QCGm5Rf'

client = Client(API_KEY, API_SECRET)
asset = ['ADABTC']
suffix = '_1day_up_to_2022'
# suffix = '_60min_last_6_month_of_2021.csv'
# suffix = '_60min_up_to_2022.csv'
# suffix = '_5min_last_3_month_of_2021.csv'
for item in asset:
    csvfile = open(data_path + item + suffix,
                   'w', newline='')

    candlestick_writer = csv.writer(csvfile, delimiter=',')
    try:
        # candlesticks = client.get_historical_klines(item,
        #                                             Client.KLINE_INTERVAL_5MINUTE,
        #                                             "1 Oct, 2020",
        #                                             "31 Dec, 2020")
        candlesticks = client.get_historical_klines(item,
                                                    Client.KLINE_INTERVAL_1DAY,
                                                    )
    except:
        print(item)

    for candlestick in candlesticks:
        # candlestick[0] = candlestick[0] / 1000
        candlestick_writer.writerow(candlestick)

    csvfile.close()
