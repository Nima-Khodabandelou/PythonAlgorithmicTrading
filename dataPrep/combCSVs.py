import os
import csv

import sys
sys.path.append('..')
from all_binance_pairs import binance_pairs
from unused_codes.selected_assets import assets
# col names on the resulting csv files for binance. Note these are not included
# as headers
csvfile_col_names = ['Ot',
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

years = ["2017", "2018", "2019", "2020", "2021"]
month = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
         "12"]
# years = ["2021"]
# month = ["07", "08", "09", "10", "11", "12"]
pairs = ['ADABTC']
# lst = assets

base_path = "C:\\files\\algotrader\\main\\data\\hist_data\\"
pairs = os.listdir(base_path)

i = 0
j = 0
k = 0

suffix = '_up_to_2022'
tf = ['5m', '1h', '1d']

while i < len(pairs):
    path = base_path + pairs[i] + '\\csv_data\\'
    for tfm in tf:
        with open(path + "{0}_{1}{2}.csv".format(pairs[i], tfm, suffix),
                  'w', newline='',
                  encoding='utf-8') as f1:
            for file in os.listdir(path):
                if (pairs[i] and tfm) in file:
                    while k < len(years):
                        if years[k] in file:
                            while j < len(month):
                                if month[j] in file[-6:-4]:
                                    with open(path + file,
                                              'r', newline='') as f2:
                                        reader = csv.reader(f2)
                                        reader = list(reader)

                                        for line in reader:
                                            csv.writer(f1, delimiter=','
                                                       ).writerow(line)

                                    break
                                j += 1
                            break
                        k += 1
                j = 0
                k = 0
            f1.close()
    i += 1
