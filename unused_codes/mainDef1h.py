from dataManip.histDataPrep\
    import BullBearMrks

from unused_codes.setInitPrmsDef1h1d import initialSetUp

# import plot.bokeh_plot as plot
import plot.bokehV2 as plot

from unused_codes.tech_old import filtOrOrdExtrms

from dataPrep.checkHSR_Data\
    import checkIfAssetHSRDataFileExists

from dataManip.HSR_List import storeHSRDataInList

from indics.calcIndics import\
    CalcBB_VecsforSTDV_Coeffs, computeMA_Vecs

from dataPrep.expCSVHighTf\
    import expHigherTf_CSV


(basePath, asset, indicUse, useVWAP, TS, TfDef, Tf1h, Tf1d, NoOfDataDef,
 NoOfData1h, NoOfData1d, exch, plotMode, LRC_Def, LRC1h, LRC1d, MND, PCP_Def,
 PCP1h, PCP1d, DeltaT_Def, DeltaT1h, DeltaT1d, extrmFilterMode, realTimeMode,
 useBB, BB_ParamsDef, BB_Params1h, BB_Params1d, useMA,
 MA_Periods1h, MA_Periods1d) = initialSetUp()

(HSRFileStatus, HSRFileName, HSRFilePath) = checkIfAssetHSRDataFileExists(
    asset, basePath, TS, MND)

exportCSVFileForHigherTf = False
exportCSVFileTf = 10

if exportCSVFileForHigherTf is True:
    expHigherTf_CSV(Tf1h, TS, basePath, asset, exportCSVFileTf)
# ################ CANDLE PARAMETERS CALCULATIONS ###########################
(tDef, tIncDef, tDecDef, ccDef, chDef, clDef, ccDecDef, ccIncDef, coDecDef,
 coIncDef, volDef, incDef, decDef, volDecDef,
 volIncDef) = BullBearMrks(asset, TfDef, TS, basePath,
                                                   NoOfDataDef)

(t1h, tInc1h, tDec1h, cc1h, ch1h, cl1h, ccDec1h, ccInc1h, coDec1h,
 coInc1h, vol1h, inc1h, dec1h, volDec1h,
 volInc1h) = BullBearMrks(asset, Tf1h, TS, basePath,
                                                  NoOfData1h)

(t1d, tInc1d, tDec1d, cc1d, ch1d, cl1d, ccDec1d, ccInc1d, coDec1d,
 coInc1d, vol1d, inc1d, iec1d, volDec1d,
 volInc1d) = BullBearMrks(asset, Tf1d, TS, basePath,
                                                  NoOfData1d)
# ################ EXTREMUMS (High and Lows) ###############################
(mxIndxDef, mnIndxDef, unvalidMxIndxDef, unvalidMnIndxDef) =\
    filtOrOrdExtrms(extrmFilterMode, realTimeMode, clDef, chDef,
                                   LRC_Def, PCP_Def, DeltaT_Def)

(mxIndx1d, mnIndx1d, unvalidMxIndx1d, unvalidMnIndx1d) =\
    filtOrOrdExtrms(extrmFilterMode, realTimeMode, cl1d, ch1d,
                                   LRC1d, PCP1d, DeltaT1d)

(mxIndx1h, mnIndx1h, unvalidMxIndx1h, unvalidMnIndx1h) =\
    filtOrOrdExtrms(extrmFilterMode, realTimeMode, cl1h, ch1h,
                                   LRC1h, PCP1h, DeltaT1h)


# ############### VWAP/MA/Bollinger Bands SETUP (OPTIONAL)
if indicUse:
    # (BB_MA_Def, BB_UB_Def, BB_LB_Def) = CalcBB_VecsforSTDV_Coeffs(useBB, ccDef,
    #                                                               BB_ParamsDef)

    (BB_MA1h, BB_UB1h, BB_LB1h) = CalcBB_VecsforSTDV_Coeffs(useBB, cc1h,
                                                            BB_Params1h)
    (BB_MA1d, BB_UB1d, BB_LB1d) = CalcBB_VecsforSTDV_Coeffs(useBB, cc1d,
                                                            BB_Params1d)
else:
    (BB_MA1h, BB_UB1h, BB_LB1h) = [0, 0, 0]
    (BB_MA1d, BB_UB1d, BB_LB1d) = [0, 0, 0]
    showBB = '-showBB'
    # MA_Vecs1h = computeMA_Vecs(useMA, cc1h, MA_Periods1h)
    # MA_Vecs1d = computeMA_Vecs(useMA, cc1d, MA_Periods1d)
# ################ SUPPORT/RESISTENCE LINES ################################
backstep = 8

HSRData = storeHSRDataInList(HSRFileStatus, cl1d, ch1d, backstep, MND, asset,
                             TS, HSRFilePath, HSRFileName)
# ############################ PLOT #########################################
if plotMode == 1:
    plot.bokehChartDef(tDef, chDef, clDef, mxIndxDef, mnIndxDef,
                       t1d, ch1d, cl1d, mxIndx1d, mnIndx1d,
                       incDef, decDef,
                       tIncDef, tDecDef,
                       ccIncDef, ccDecDef, coIncDef, coDecDef,
                       volDef, volIncDef, volDecDef,
                       BB_MA_Def, BB_UB_Def, BB_LB_Def,
                       HSRData,
                       t1h, ch1h, cl1h, mxIndx1h, mnIndx1h,
                       BB_MA1h, BB_UB1h, BB_LB1h,
                       MA_Vecs,
                       'showExtrm',
                       'showMA',
                       'showVol',
                       'showSR',
                       '-showBB_Def', '-showBB1h')
    plot.bokehChart1h(t1h, ch1h, cl1h, mxIndx1h, mnIndx1h, t1d, ch1d, cl1d,
                      mxIndx1d, mnIndx1d, inc1h, dec1h, tInc1h, tDec1h,
                      ccInc1h, ccDec1h, coInc1h, coDec1h, vol1h, volInc1h,
                      volDec1h,
                      HSRData,
                      BB_MA1h, BB_UB1h, BB_LB1h,
                      # MA_Vecs1h,
                      'showExtrm', '-showVol', 'showSR', showBB,
                      '-showMA')
    plot.bokehChart1d(t1d, tInc1d, tDec1d, ccDec1d, ccInc1d, coDec1d,
                      coInc1d, ch1d, cl1d, mxIndx1d, mnIndx1d,
                      # MA_Vecs1d,
                      BB_MA1d, BB_LB1d, BB_UB1d,
                      '-showMA', showBB)

