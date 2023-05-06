from asyncio.windows_events import NULL
import csv
import numpy as np
from datetime import datetime as dtm


utc = dtm.utcfromtimestamp


def dataLoad(dataPath, dataLength, dataSelect):

    ''' Loads candlestick data from csv file in a specified date range. '''

    with open(dataPath, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    # converting data from list to  numpy array
    data = np.array(data, dtype='U20')

    if dataLength == 'None':
        dataLength = np.shape(data)[0]

    NoOfData = np.shape(data)[0]

    if dataSelect == 0:
        return data[0:dataLength]
    else:
        return data[NoOfData - dataLength:NoOfData]


def dataEdit(data):
    '''
    Edits the data file in terms of unix time conversion and unused columns
    deletion.

    BINANCE DATA STREAM FORMAT

    [
      0  open time,
      1  Open,
      2  High,
      3  Low,
      4  Close,
      5  Volume,
      6  Close time,
      7  Quote asset volume,
      8  Number of trades,
      9  Taker buy base asset volume,
      10 Taker buy quote asset volume,
      11 Can be ignored
    ]

    Useless columns

    [
      6  Close time,
      7  Quote asset volume,
      9  Taker buy base asset volume,
      10 Taker buy quote asset volume,
      11 Can be ignored
    ]

    After deletion, columns would be:

      0  time,
      1  Open,
      2  High,
      3  Low,
      4  Close,
      5  Volume,
      6  Number of trades'''

    NoOfData = len(data)
    unixTime = data[:, 0].copy()

    # converting unix time from milisec to sec
    data[:, 0] = [(int(data[i, 0]))/1000 for i in range(0, NoOfData)]
    # t1 = [utc(1617235200), utc(1617235260)]
    # t2 = [utc(float(data[0,0])), utc(float(data[1,0]))]
    t = [utc(float(data[i, 0])) for i in range(0, NoOfData)]
    # Data stream format and useless columns are explained in README file.
    # Deleting useless cols
    data = np.delete(data, [6, 7, 9, 10, 11], 1)

    return data, t, unixTime


def initialDataConfig(asset, Tf, TS, basePath, NoOfData):
    '''This function defines initial parameters and setup of the algorithmic
    trading system.'''

    assetDataFilePath = basePath + asset\
        + '_' + Tf + TS + ".csv"

    # dataSelect = 0 --> data is selected from the beginning of the file
    # dataSelect = 1 --> data is selected from the end of the file (more
    # time consuming)
    dataSelect = 1
    data = dataLoad(assetDataFilePath, NoOfData, dataSelect)

    data, time, unixTime = dataEdit(data)

    return data, time


def calcUnixTimeForHigherTf_CSV_Exp(data, Tf):
    # Since time data was converted from unix to utc in data_edit function,
    # in order to generate a new standard csv file based on higher time frame
    # the original unix time data at lower time frame is needed. This data was
    # stored in unixTime vector in data_edit function.
    (data, t, unixTime) = dataEdit(data)
    unixTimeForHigherTfCSV_Exp = []
    NoOfData = len(data)
    residual = NoOfData % Tf
    data = np.delete(data, range(0, residual), 0)
    data_shape2 = np.shape(data)[0]
    for i in range(0, data_shape2, Tf):
        unixTimeForHigherTfCSV_Exp.append(unixTime[i])

    return unixTimeForHigherTfCSV_Exp


def calcCandleParams(data, t, Tf, csvExport, exportCSVFileTf):
    '''
    It also can generate
    (if decided in advance) data of the asset under study at a
    higher time frame and export the data in csv format. '''

    # At first, all lists are set to empty

    # lst1 and lst2 store candles' high and low, respectively at a given
    # interval which is higher time frame (for instance, if higher time frame
    # is 10 minute then the given interval would be 10). Then maximum and
    # minimum of lst1 and lst2 would be selected as high and low at higher
    # time frame.

    tmpList1 = []
    tmpList2 = []
    chVec = []
    clVec = []
    coVec = []
    volVec = []
    no_of_trades = []
    time = []
    NoOfData = len(data)
    # Since there could be residual candles after the last higher time frame
    # candle, these residuals must be deleted. In real time, they would be
    # stored so that after recieving sufficient data the final candle at higher
    # time would be formed and exported.
    if csvExport is True:
        Tf = int(exportCSVFileTf/Tf)
    else:
        Tf = 1

    residual = NoOfData % Tf
    data = np.delete(data, range(0, residual), 0)
    dataLength = np.shape(data)[0]
    for i in range(0, dataLength, Tf):
        # here data are appended to previous empty lists, i.e. candle open,
        # volume, No. of trades (if applicable), utc time, and
        # unix time ( which is for csv export)
        coVec.append(float(data[i, 1]))
        volVec.append((float(data[i, 5])+float(data[i+int(Tf/2), 5])))
        no_of_trades.append(float(data[i, 6])+float(data[i+int(Tf/2), 6]))
        time.append(t[i])
        # Regarding high and low at higher time frame, data should be
        # selected at given interval using maximum and minimum functions
        for j in range(i, i+Tf):
            tmpList1.append(float(data[j, 2]))
            tmpList2.append(float(data[j, 3]))
        # Next, max and min of lst1 and lst2 are stored as candle high and low
        # at higher time frame
        chVec.append(max(tmpList1))
        clVec.append(min(tmpList2))
        # lst1 and lst2 are again set to empy list for the next round
        tmpList1 = []
        tmpList2 = []
    # candle close is selected for higher time frame data
    ccVec = [float(data[i, 4]) for i in range(Tf-1, NoOfData, Tf)]

    return (time, ccVec, coVec, chVec, clVec, volVec)


def BullBearMrks(asset, Tf, TS, basePath, NoOfData):
    '''Defines candles' high, low, close, and open values as well as volume and
    time data w.r.t. bullish or bearish market. '''

    (data,
     timeVecBeforePossibleCSVExp) = initialDataConfig(
         asset, Tf, TS, basePath,
         NoOfData)

    csvExport = False
    expCSV_Tf = NULL

    (timeVecAfterPossibleCSVExp,
     ccVec,
     coVec,
     chVec,
     clVec,
     volVec) = calcCandleParams(data, timeVecBeforePossibleCSVExp, Tf,
                                csvExport, expCSV_Tf)

    # Initializing lists for the color of increasing/decreasing candles( bull./
    # bear. market).
    time = timeVecAfterPossibleCSVExp
    inc = []
    dec = []
    NoOfData = np.shape(time)[0]
    # Identifying bull./bear. market index
    for i in range(0, NoOfData):
        if coVec[i] < ccVec[i]:
            inc.append(i)
        else:
            dec.append(i)
    # Identifying parameters in bull./bear. market)
    tInc = []
    coVecInc = []
    ccVecInc = []
    volIncVec = []
    for i in inc:
        tInc.append(time[i])
        coVecInc.append(coVec[i])
        ccVecInc.append(ccVec[i])
        volIncVec.append(volVec[i])

    tDecVec = []
    coVecDec = []
    ccVecDec = []
    volDecVec = []
    for i in dec:
        tDecVec.append(time[i])
        coVecDec.append(coVec[i])
        ccVecDec.append(ccVec[i])
        volDecVec.append(volVec[i])

    return (time, tInc, tDecVec, ccVec, chVec, clVec,
            ccVecDec, ccVecInc, coVecDec,
            coVecInc, volVec, inc, dec, volDecVec, volIncVec)
