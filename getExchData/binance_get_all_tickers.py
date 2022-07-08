from binance.client import Client


API_KEY = 'NZsrbx4ZNf98YNAr25H35agc2cys2oThZPdFquxoKSx21nR9Y5nSsZYLWOXkr2wZ'
API_SECRET = '3Eh4p0Bi2hlKw9ZbQlgN535z85uS7QozTvIfLZyq3I0J8lo4A5mKHVRD8QCGm5Rf'

client = Client(API_KEY, API_SECRET)

symbols = client.get_all_tickers()

lst = []

for val in range(1, len(symbols)):
    lst.append(symbols[val]['symbol'])

print(lst)

BNBpairs = []
BTCpairs = []
USDTpairs = []
ETHpairs = []

for el in lst:
    if (len(el) - len('USDT')) == el.find('USDT'):
        USDTpairs.append(el)
        # mylist.pop(mylist.index(el))

    elif (len(el) - len('BNB')) == el.find('BNB'):
        BNBpairs.append(el)

    elif (len(el) - len('BTC')) == el.find('BTC'):
        BTCpairs.append(el)

    elif (len(el) - len('ETH')) == el.find('ETH'):
        ETHpairs.append(el)

print('BNBpairs:', BNBpairs)
print()
print('BTCpairs:', BTCpairs)
print()
print('ETHpairs:', ETHpairs)
print()
print('USDTpairs:', USDTpairs)
