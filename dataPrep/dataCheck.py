# this module checks the consistency of data in different timeframes
from asyncore import read

import csv

import os

import pandas as pd

import numpy as np

from pandas import *

from pprint import pprint

tf = ['_10m', '_1h', '_1d']
suffix = '_up_to_2022'

col_names = ['Ot',
             'O',
             'H',
             'L',
             'C',
             'Vol',
             'Ct',
             'Quote asset vol',
             'Num. of trades',
             'Taker buy base asset vol',
             'Taker buy quote asset vol',
             'ignore']


def data_continuity(asset, data_path):
    '''this function checks if data files are continuous in time.'''

    def file_check(tf, suffix):
        with open(data_path + asset + tf + suffix + '.csv') as f:
            reader = pd.read_csv(f, chunksize=1000, names=col_names)
            dt = []
            for item in reader:
                dt.append(pd.DataFrame(item))

        unix_time_lst = dt[0]['Ot'].tolist()
        outlier = []
        missing_tf_multipler = []
        default_delta_t = unix_time_lst[1] - unix_time_lst[0]
        i = 1
        while i < len(unix_time_lst):
            deltat = unix_time_lst[i] - unix_time_lst[i-1]
            if deltat != default_delta_t:
                outlier.append(i)
                missing_tf_multipler.append(int(deltat/default_delta_t))
            i += 1

        return outlier, missing_tf_multipler

    state = []
    for item in tf:
        outlier, missing_tf_pultiplier = file_check(item, suffix)
        if outlier == []:
            state.append([item, True])
        else:
            state.append([item, False, outlier, missing_tf_pultiplier])

    return state


base_path = "C:\\files\\algotrader\\main\\data\\hist_data\\"
pairs = os.listdir(base_path)
# pairs = ['ADAUSDT']
for pair in pairs:
    state = data_continuity(pair, base_path + pair + '\\csv_data\\')
    print('{0} state: {1}', pair, state)
