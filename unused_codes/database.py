import pandas as pd
import pymongo
import numpy as np
# from selected_assets import assets


client = pymongo.MongoClient('localhost', 27017)

path = "C:\\files\\algotrader\\main\\data\\hist_data\\ETHUSDT_10min_p_copy.csv"
base_path = "D:\\Binance_data\\complete_data\\"
base_path = "C:\\files\\algotrader\\main\\data\\hist_data\\\
files_with_headers\\"


def read_csv(base_path, asset):
    # ########## To add col names to csv file
    # df = pd.read_csv("test.csv", names=['unix time', 'open',
    #                                     'high', 'low', 'close',
    #                                     'volume', 'dum1',
    #                                     'dum2', 'dum3', 'dum4',
    #                                     'dum5', 'dum6'])

    # ######## Selecting specific cols if csv file that already has col names
    fields = ['unix time', 'open', 'high', 'low', 'close', 'volume']

    df = pd.read_csv(base_path + asset + "_1min_p.csv", skipinitialspace=True,
                     usecols=fields)

    return df


def create_mongodb_database_and_insert_csv(base_path, asset, client,
                                           db_name, coll_name):
    ''' This function gets database and collection names and create the
    database then inserts csv data to it.'''
    database = client[db_name]
    collection = database[coll_name]
    df = read_csv(base_path, asset)
    collection.insert_many(df.to_dict('records'))

    return collection


def load_existing_mongodb_database(client, db_name, coll_name):
    ''' This function loads an existing mongodb database and collection
    and create the database then inserts csv data to it.'''
    database = client[db_name]
    collection = database[coll_name]
    return collection


assets = ['ADAUSDT',
          'ADABTC',
          'ALGOUSDT']
# If db_mode = 0 --> create db else load db
db_mode = 1
coll_name = 'data'
if db_mode == 0:
    for asset in assets:
        collection = create_mongodb_database_and_insert_csv(base_path, asset,
                                                            client,
                                                            asset,
                                                            coll_name)
else:
    collection = load_existing_mongodb_database(client, assets[0], coll_name)

a = np.array([[], []])
# lst = [[]]
# print(lst[0]['unix time'])
# cnt = 0
# for x in collection.find():
#     lst[cnt].append(x['unix time'])
#     lst[cnt].append(x['open'])
#     lst[cnt].append(x['high'])
#     lst[cnt].append(x['low'])
#     lst[cnt].append(x['close'])
#     lst[cnt].append(x['volume'])
#     lst.append([])
#     cnt += 1


# print(lst[0]['low'])
