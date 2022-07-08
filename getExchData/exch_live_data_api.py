import json

from kucoin.client import Client


def kucoin_api_data(kucoin_api_key, kucoin_api_secret, kucoin_api_passphrase,
                    start_unixtime, end_unixtime):
    ''' Gets exchange live data through web socket or API connection. '''
    client = Client(kucoin_api_key, kucoin_api_secret,
                    kucoin_api_passphrase)

    # get currencies
    # currencies = client.get_currencies()

    # get market depth
    # depth = client.get_order_book('KCS-BTC')

    # get symbol klines
    # klines = client.get_kline_data('KCS-BTC', '1week', 1507479171, 1510278278)
    klines = client.get_kline_data('BTC-USDT', '1week', start_unixtime, end_unixtime)
    # klines output:
    # time
    # open
    # close
    # high
    # low
    # base asset vol
    # qoute asset vol (usdt)

    # get list of markets
    # markets = client.get_markets()

    # place a market buy order
    # order = client.create_market_order('NEO', Client.SIDE_BUY, size=20)

    # with open('klines.json', 'w', encoding='utf-8') as f:
    #     json.dump(klines, f, ensure_ascii=False, indent=4)

    return klines
