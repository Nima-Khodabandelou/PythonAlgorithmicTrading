import asyncio

import time

import csv

from kucoin.client import Client
from kucoin.asyncio import KucoinSocketManager

from Config.KucoinConfig import kucoin_api_key, kucoin_api_passphrase, kucoin_api_secret


api_key = kucoin_api_key
api_secret = kucoin_api_secret
api_passphrase = kucoin_api_passphrase

pair = 'BTC-USDT'

tick_price = []


async def main():
    global loop

    # callback function that receives messages from the socket
    async def handle_evt(msg):
        if msg['topic'] == '/market/ticker:' + pair:
            print(f'got {pair} tick:{msg["data"]["price"]}')
            tick_price.append(msg["data"]["price"])
            csvfile = open(f'{pair}.csv', 'w', newline='')
            csv.writer(csvfile, delimiter=',').writerow(tick_price)
            csvfile.close()
            time.sleep(5)
        elif msg['topic'] == '/market/snapshot:BTC':
            print(f'got BTC market snapshot:{msg["data"]}')

        elif msg['topic'] == '/market/snapshot:' + pair:
            print(f'got {pair} symbol snapshot:{msg["data"]}')

        elif msg['topic'] == '/market/ticker:all':
            print(f'got all market snapshot:{msg["data"]}')

        elif msg['topic'] == '/account/balance':
            print(f'got account balance:{msg["data"]}')

        elif msg['topic'] == '/market/level2:' + pair:
            print(f'got L2 msg:{msg["data"]}')

        elif msg['topic'] == '/market/match:' + pair:
            print(f'got market match msg:{msg["data"]}')

        elif msg['topic'] == '/market/level3:' + pair:
            if msg['subject'] == 'trade.l3received':
                if msg['data']['type'] == 'activated':
                    # must be logged into see these messages
                    print(f"L3 your order activated: {msg['data']}")
                else:
                    print(f"L3 order received:{msg['data']}")
            elif msg['subject'] == 'trade.l3open':
                print(f"L3 order open: {msg['data']}")
            elif msg['subject'] == 'trade.l3done':
                print(f"L3 order done: {msg['data']}")
            elif msg['subject'] == 'trade.l3match':
                print(f"L3 order matched: {msg['data']}")
            elif msg['subject'] == 'trade.l3change':
                print(f"L3 order changed: {msg['data']}")

    client = Client(api_key, api_secret, api_passphrase)

    ksm = await KucoinSocketManager.create(loop, client, handle_evt)

    # for private topics such as '/account/balance' pass private=True
    # ksm_private = await KucoinSocketManager.create(loop, client, handle_evt, private=True)

    # Note: try these one at a time, if all are on you will see a lot of output

    # await ksm.subscribe('/market/candles:ETH-USDT_1min')  doesn't work

    # ETH-USDT Market Ticker
    await ksm.subscribe('/market/ticker:' + pair)
    # # BTC Symbol Snapshots
    # await ksm.subscribe('/market/snapshot:BTC')
    # # KCS-BTC Market Snapshots
    # await ksm.subscribe('/market/snapshot:KCS-BTC')
    # # All tickers
    # await ksm.subscribe('/market/ticker:all')
    # # Level 2 Market Data
    # await ksm.subscribe('/market/level2:KCS-BTC')
    # # Market Execution Data
    # await ksm.subscribe('/market/match:BTC-USDT')
    # # Level 3 market data
    # await ksm.subscribe('/market/level3:BTC-USDT')
    # # Account balance - must be authenticated
    # await ksm_private.subscribe('/account/balance')

    while True:
        print("sleeping to keep loop open")
        await asyncio.sleep(5, loop=loop)


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
