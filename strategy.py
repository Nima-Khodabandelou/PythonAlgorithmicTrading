import csv
from setInitPrms import initSet


def strFloat(lst):
    lst = [float(i) for i in lst]
    return lst


(basePath, asset) = initSet()[0:2]
with open(basePath + asset + "//strategy//" + 'calcdata.csv', 'r',
          newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

[HSR, mxIndx1h, mnIndx1h, mxIndx1d, mnIndx1d, cc1h, ch1h, cl1h, cc1d, ch1d,
 cl1d, MA1h1, MA1h2, MA1h3, t1d, t1h] = data
lst1 = [HSR, mxIndx1h, mnIndx1h, mxIndx1d, mnIndx1d, cc1h, ch1h, cl1h, cc1d,
        ch1d, cl1d, MA1h1, MA1h2, MA1h3, t1d, t1h]
lst2 = [strFloat(i) for i in lst1[:-2]]
[HSR, mxIndx1h, mnIndx1h, mxIndx1d, mnIndx1d, cc1h, ch1h, cl1h, cc1d, ch1d,
 cl1d, MA1h1, MA1h2, MA1h3] = lst2
del lst1, lst2
# Define the day during which the first 1h candle appears
tradeDayIndx = [t1d.index(i) for i in t1d if i > t1h[0]][0] - 1
# As a starting point, We need a few 1d min/max data before tradingDay to
# identify indexes for defining market scenarios including: up/down trend,
# conv/div/neutral side, move/cor
preMXIndxs1d = [int(i) for i in mxIndx1d if i < tradeDayIndx][-1:-5:-1]
preMNIndxs1d = [int(i) for i in mnIndx1d if i < tradeDayIndx][-1:-5:-1]
preMXIndx1h = mxIndx1h[0:4]
preMNIndx1h = mnIndx1h[0:4]
