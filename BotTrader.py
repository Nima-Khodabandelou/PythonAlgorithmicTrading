from dataManip.histDataPrep import BullBearMrks, initialDataConfig
from tech import ma, atr


path = "C:\\Java_files\\PythonAlgorithmicTrading\\data\\"
asset = 'SOLUSDT'
ts = ''
# tf: time frame
tf = '1m'
# nod: number Of data (rows) extracted from csv file and used for calculation
nod = 10000
(t, tInc, tDec, cc, ch, cl, ccDec, ccInc, coDec,
 coInc) = BullBearMrks(asset, tf, ts, path, nod)[0:10]
# ma_p: periods used for calculating moving averages
ma_p = [100, 150, 500]
# all_ma: all moving averages calculated for each MA period
all_ma = ma(True, cc, ma_p)

atr_p = 10

ma_for_global_trend = all_ma[2]
ma_for_local_momentum1 = all_ma[0]
ma_for_local_momentum2 = all_ma[1]



