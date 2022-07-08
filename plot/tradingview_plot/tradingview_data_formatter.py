import csv
import copy
import numpy as np
import json, codecs
import os


if os.path.isfile("bundle.js"):
    os.remove("bundle.js")

file = 'BTCUSDT_5min_last_6_month_of_2021'
with open('C:/files/algoTrader/main/data/hist_data/'+file+'.csv',
            newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

# dt stands for data
dt = copy.copy(data[0:7*24*60])
# We need the Volume in usdt in a seperate file. We can go through list methods
# but working with numpy arrays is much easier.
dt = np.array(dt)
# No. of rows in dt equals to:
rows = np.shape(dt)[0]
# converting unix time from milisec to sec
dt[:,0] = [(float(dt[i,0]))/1000 for i in range(rows)]
# assigning volume values to a separate array
vol = dt[:,8]

######### FOR BINANCE EXCHANGE DATA

# Now deleting useless cols that we don't need in LigthWeightCharts.(if needed)
dt = np.delete(dt, [6,7,8,9,10,11], 1)

# init vector for the color of bull-bear vol values
color_col = np.zeros((rows), dtype='U20')
counter = 0
for el in dt:
    # if open price < close price
    if el[1] < el[4]:
        color_col[counter] = "#009688cc"
    else:
        color_col[counter] = "#ff5252cc"
    counter +=1

# tmp2 is initialized to contain keys(i.e. time, open, ...) in  JSON file
# passing to browser
# U10 is the max length of each str in tmp2 
tmp2 = np.zeros((rows,7), dtype='U10')
tmp2[:,0] = 'time'
tmp2[:,1] = 'open'
tmp2[:,2] = 'high'
tmp2[:,3] = 'low'
tmp2[:,4] = 'close'
# value and color are for vol array
tmp2[:,5] = 'value'
tmp2[:,6] = 'color'

# el is defined to access tmp2 and dt indexes
el = [0,1,2,3,4]
# tmp2 keys are inserted into dt
dt = np.insert(dt, el, tmp2[:,el], axis=1)


# volume dict initializes
volume = np.empty((rows,0), dtype=dt.dtype)
# first 2 cols are 'time' and unix time value
volume = np.insert(volume, 0, tmp2[:,0], axis=1)
volume = np.insert(volume, 1, dt[:,1], axis=1)
# second 2 cols are 'value' and volume value
volume = np.insert(volume, 2, tmp2[:,5], axis=1)
volume = np.insert(volume, 3, vol, axis=1)
volume = np.insert(volume, 4, tmp2[:,6], axis=1)
volume = np.insert(volume, 5, color_col, axis=1)


# dt to json
lst = dt.tolist()
items = {}
candles = []
odd = [1,3,5,7,9]
even = [0,2,4,6,8]
for el in lst:
    for i in range(5):
        key, value = el[even[i]], float(el[odd[i]])
        #print(key, value)
        items[key] = value        
    candles.append(items) 
    items = {}

# your path variable
candle_path = "C:/files/algoTrader/main/plot/tradingview/javascript_chart_files/candle.json" 
# this saves the array in .json format with elements as string
json.dump(candles, codecs.open(candle_path, 'w', encoding='utf-8'),
            separators=(',', ':'), sort_keys=True, indent=4) 


volumes = []
odd = [1,3,5]
even = [0,2,4]
for el in volume:
    for i in range(3):
        if i in range(2):
            key, value = el[even[i]], float(el[odd[i]])
        else:
            key, value = el[even[i]], el[odd[i]]
        #print(key, value)
        items[key] = value        
    volumes.append(items) 
    items = {}

vol_path = "C:/files/algoTrader/main/plot/tradingview/javascript_chart_files/vol.json" 
json.dump(volumes, codecs.open(vol_path, 'w', encoding='utf-8'),
            separators=(',', ':'), sort_keys=True, indent=4) 

var = os.system(
      "cd C:/files/algoTrader/main/plot/tradingview/javascript_chart_files & browserify index.js -o bundle.js")




############ If we want to write to txt file instead of creating Json:
# keys = ['time:', 'open:', 'high:', 'low:', 'close:']

# with open('NEOUSDT_1min_Candle_for_LightWeightCharts.txt', 'w') as file1:
#     for line in dt:
#         writer1 = file1.write('{ ')
#         for el in line:                        
#             if el in keys:            
#                 writer2 = file1.write(el)
#                 writer2 = file1.write(" ")
#             else:                                    
#                 writer2 = file1.write(el + ",")
#                 writer2 = file1.write(" ")
#         writer3 = file1.write('}')
#         writer3 = file1.write('\n')

# keys = ['time:', 'value:']
# with open('NEOUSDT_1min_Volume_for_LightWeightCharts.txt', 'w') as file2:    
#     for line in volume:
#         writer1 = file2.write('{ ')
#         for el in line:                        
#             if el in keys:            
#                 writer2 = file2.write(el)
#                 writer2 = file2.write(" ")
#             else:                                    
#                 writer2 = file2.write(el + ",")
#                 writer2 = file2.write(" ")
#         writer3 = file2.write('}')
#         writer3 = file2.write('\n')



