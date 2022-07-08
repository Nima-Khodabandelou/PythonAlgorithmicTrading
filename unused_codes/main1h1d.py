from dataManip.histDataPrep import BullBearMrks
from setInitPrms import initSet
import plot.bokehV21h1d as plot
from getExchData import weekDataIFCM
from getExchData.exch_live_data_api import kucoin_api_data
from unused_codes.tech_old import filtOrOrdExms, PP
from dataPrep.checkHSR_Data import chkAssetHSR
from dataManip.HSR_List import HSRList
from dataPrep.expCSVHighTf import expHighTfCSV
from indics.calcIndics import computeMA_Vecs, CalcBB_VecsforSTDV_Coeffs
from config.KucoinConfig import (kucoin_api_key, kucoin_api_passphrase,
                                 kucoin_api_secret)
import datetime
import csv


# ################ Initial Config ####################
(basePath, asset, TS, Tf1h, Tf1d, ND1h, ND1d, exch, plotMode, LRC1h, LRC1d,
 MND, PCP1h, PCP1d, DeltaT1h, DeltaT1d, ETM, RTM) = initSet()
# ################ Export CSV ###########################
exportCSVFileForHigherTf = False
exportCSVFileTf = 10
if exportCSVFileForHigherTf is True:
    expHighTfCSV(Tf1h, TS, basePath, asset, exportCSVFileTf)
# ################ CANDLE PARAMETERS CALCULATIONS ###########################
(t1h, tInc1h, tDec1h, cc1h, ch1h, cl1h, ccDec1h, ccInc1h, coDec1h, coInc1h,
 vol1h, inc1h, dec1h, volDec1h, volInc1h) = BullBearMrks(asset, Tf1h, TS,
                                                         basePath, ND1h)

(t1d, tInc1d, tDec1d, cc1d, ch1d, cl1d, ccDec1d, ccInc1d, coDec1d, coInc1d,
 vol1d, inc1d, iec1d, volDec1d, volInc1d) = BullBearMrks(asset, Tf1d, TS,
                                                         basePath, ND1d)
# ################ EXTREMUMS (High and Lows) ###############################
(mxIndx1d, mnIndx1d,
 unvalMxIndx1d, unvalMnIndx1d) = filtOrOrdExms(ETM, RTM, cl1d, ch1d, LRC1d,
                                               PCP1d, DeltaT1d)
(mxIndx1h, mnIndx1h,
 unvalMxIndx1h, unvalMnIndx1h) = filtOrOrdExms(ETM, RTM, cl1h, ch1h, LRC1h,
                                               PCP1h, DeltaT1h)
# ################ SUPPORT/RESISTENCE LINES ################################
(HSRStat, HSRName, HSRPath) = chkAssetHSR(asset, basePath, TS, MND)
backstp = 20
HSR = HSRList(HSRStat, cl1d, ch1d, backstp, MND, asset, TS, HSRPath, HSRName)
# ################ MA ##############################################
MA_Vecs1h = computeMA_Vecs(True, cc1h, [50, 100, 200])
MA1h1 = MA_Vecs1h[0]
MA1h2 = MA_Vecs1h[1]
MA1h2 = MA_Vecs1h[2]
# (BB_MA1h, BB_UB1h, BB_LB1h) = CalcBB_VecsforSTDV_Coeffs(True, cc1h,
#                                                         [(800, 0.8),
#                                                          (800, 1.6),
#                                                          (800, 2.5)])
# ########################## P.P. ###############################
# start_unixtime = int(t1h[0].timestamp())
# end_unixtime = int(t1h[-1].timestamp())
# week_data = kucoin_api_data(kucoin_api_key, kucoin_api_secret,
#                             kucoin_api_passphrase, start_unixtime,
#                             end_unixtime)

# ########################### Strategy #########################
Fisrt save calc data for easier loading
csvFile = open(basePath + asset + "//strategy//" + 'calcdata.csv', 'w+',
               newline='')
csvFileWriter = csv.writer(csvFile)
lst = [HSR, mxIndx1h, mnIndx1h, mxIndx1d, mnIndx1d, cc1h, ch1h, cl1h,
       cc1d, ch1d, cl1d, MA1h1, MA1h2, t1d, t1h]
for i in range(len(lst)):
    csvFileWriter.writerow(lst[i])
csvFile.close()
# ############################ PLOT #########################################
if plotMode == 1:
    plot.chart1h(t1h, ch1h, cl1h, mxIndx1h, mnIndx1h, t1d, ch1d, cl1d,
                 mxIndx1d, mnIndx1d, tInc1h, tDec1h, ccInc1h, ccDec1h, coInc1h,
                 coDec1h, HSR, '-showExtrm', 'showSR', 'showMA', MA_Vecs1h,
                 '-showBB')
    plot.chart1d(t1d, tInc1d, tDec1d, ccDec1d, ccInc1d, coDec1d, coInc1d, ch1d,
                 cl1d, mxIndx1d, mnIndx1d)
