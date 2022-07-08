import pandas as pd

from dask import dataframe as dd
import dask.multiprocessing
from multiprocessing import Pool

import os

import time


##################################### large file import
path = "C://files//algotrader//main//data//hist_data//test.csv"
path2 = "D://Binance_data//complete_data//"
path3 = "D://Binance_data//dummy//"

col_names = ['unix time', 'open', 'high', 'low', 'close', 'vol', 'd7', 'd8',
             'd9', 'd10', 'd11', 'd12']
# ########################################################################


def pandas_read_csv_consecutive_parts():
    chunksize = 5
    initial_index = 15
    final_index = 30
    first_chunk = int(initial_index/chunksize) # 6
    delta = (final_index - initial_index)/chunksize # 3
    chunks = [item for item in range(first_chunk, first_chunk + int(delta))]
    df = pd.read_csv(path, chunksize=chunksize, names=col_names)
    i = 0
    frames = []
    for chunk in df:
        if i <= chunks[-1]:
            for j in chunks:
                if i == j:
                    data = pd.DataFrame(chunk)
                    for item in data:
                        frames.append(item)
                break
            if frames != []:            
                combined_df = pd.concat(frames, ignore_index=False)
            i += 1
        else:
            break

    return combined_df

# ########################################################################
def pandas_read_csv_single_part(file):
    initial_index = 11
    final_index = 14
    chunksize = final_index - initial_index
    chunk_index = int(initial_index/chunksize)
    df = pd.read_csv(path3 + file + '.csv', chunksize=chunksize, names=col_names)
    i = 0
    for chunk in df:
        if i == chunk_index:
            data = pd.DataFrame(chunk)
            break
        i += 1

    return data
# pandas_read_csv_consecutive_parts()
pairs = ['OSTBTC_1min', 'OSTETH_1min', 'ZRXBTC_1min']
data = [[],[], []]
i = 0
for pair in pairs:
    data[i] = pandas_read_csv_single_part(pair)
    data[i] = data[i].values.tolist()
    i += 1
print(data[0])
# ########################################################################
start = time.time()
df1 = pd.read_csv(path, chunksize=1000000, names=col_names)
end = time.time()
print("Pandas read csv: ", (end-start), "sec")
# ########################################################################
start = time.time()
df2 = dd.read_csv(path)
df2 = dd.read_csv(path2+'*.csv', blocksize=1000000000)
end = time.time()
print("Dask read csv: ", (end-start), "sec")
# ########################################################################
df = pd.read_csv('sample.csv', delimiter=',')
list_of_csv = [list(row) for row in df.values]
list_of_csv.insert(0, df.columns.tolist())
# ########################################################################
# python code to demonstrate working of reduce()
 # importing functools for reduce()
import functools
# initializing list
lis = [1, 3, 5, 6, 2, ] 
# using reduce to compute sum of list
print("The sum of the list elements is : ", end="")
print(functools.reduce(lambda a, b: a+b, lis)) 
# using reduce to compute maximum element from list
print("The maximum element of the list is : ", end="")
print(functools.reduce(lambda a, b: a if a > b else b, lis))
# ########################################################################
import pandas
from functools import reduce

def get_counts(chunk):
    voters_street = chunk[
        "Residential Address Street Name "]
    return voters_street.value_counts()

def add(previous_result, new_result):
    return previous_result.add(new_result, fill_value=0)

# MapReduce structure:
chunks = pandas.read_csv("voters.csv", chunksize=1000)
processed_chunks = map(get_counts, chunks)
result = reduce(add, processed_chunks)

result.sort_values(ascending=False, inplace=True)
print(result)
