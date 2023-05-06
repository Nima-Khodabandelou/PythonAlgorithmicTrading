from dataManip.histDataPrep import BullBearMrks, initialDataConfig
import plot.bokehV21h1d as plot
# MA: Moving Average
from tech import ma as movingAverge
# ATR: Average True Range
from tech import atr as averageTruerange


path = "C:\\Java_files\\PythonAlgorithmicTrading\\data\\"
asset = 'SOLUSDT'
ts = ''
timeFrame = '1m'
numberOfData = 5000
(t, tInc, tDec, cc, ch, cl, ccDec, ccInc, coDec,
 coInc) = BullBearMrks(asset, timeFrame, ts, path, numberOfData)[0:10]

MA_Periods = [20, 30, 250]
movingAverageVector = movingAverge(True, cc, MA_Periods)

# close_pos_criterion = p > 3*ATR
ATR_Period = 10
ATR_Multiplier = 2

movingAverageForGlobalTrend = movingAverageVector[2]
movingAverageForLocalMomentum1 = movingAverageVector[0]
movingAverageForLocalMomentum2 = movingAverageVector[1]



