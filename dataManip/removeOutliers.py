import csv


base_path = "M:\\Binance_data\\complete_data\\"

data_path = base_path + "USDT_1min.csv"

with open(data_path, newline='') as f:
    reader = csv.reader(f)
    dt = list(reader)

c = 0

for i in dt:
    # the sixth column is volume
    if i[5] == 0:
        i[5] = 1
        c += 1

print('c:', c)
