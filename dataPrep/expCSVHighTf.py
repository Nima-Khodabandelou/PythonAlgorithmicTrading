import csv

from dataManip.histDataPrep\
    import (calcUnixTimeForHigherTf_CSV_Exp,
            dataLoad, dataEdit, calcCandleParams)


def expHighTfCSV(
        Tf, TS, basePath, asset, expCSV_Tf):
    '''This function defines initial parameters and setup of the algorithmic
    trading system.'''

    assetDataFilePath = basePath + "//" + asset + "//" + Tf
    + "//" + asset + '_' + Tf + TS + ".csv"

    # data_select = 0 --> data is selected from the beginning of the file
    dataSelect = 0
    NoOfData = 'None'
    data = dataLoad(assetDataFilePath, NoOfData, dataSelect)

    data, t, unixTime = dataEdit(data)

    unixTimeForHigherTfCSV_Exp = \
        calcUnixTimeForHigherTf_CSV_Exp(data, Tf)
    csvExpStatus = True
    (candleCloseVec,
     candleOpenVec,
     candleHighVec,
     candleLowVec, volVec) = calcCandleParams(data, t, Tf, csvExpStatus,
                                              expCSV_Tf)

    csvFile = open(basePath + asset + "//csv_data//" + asset
                   + "//timespan_data//" + '_'
                   + expCSV_Tf + TS
                   + '.csv', 'w', newline='')

    csvFileWriter = csv.writer(csvFile, delimiter=',')

    for i in range(len(unixTimeForHigherTfCSV_Exp)):
        csvFileWriter.writerow([unixTimeForHigherTfCSV_Exp[i],
                                candleOpenVec[i],
                                candleHighVec[i],
                                candleLowVec[i],
                                candleCloseVec[i],
                                volVec[i],
                                0, 0, 0, 0, 0, 0])
    csvFile.close()
