from dataPrep import createAssetFolders


def initialSetUp():
    basePath = "C:\\files\\algotrader\\main\\historical_data\\"

    asset = 'FTMUSDT'
    newAsset = False
    if newAsset:
        createAssetFolders(asset, basePath)

    indicUse = False

    useVWAP = False

    useBB = True
    BB_ParamsDef = [(25, 4)]
    BB_Params1h = [(600, 0.9), (600, 1), (600, 1.1),
                   (600, 1.9), (600, 2), (600, 2.1),
                   (600, 2.9), (600, 3), (600, 3.1),
                   (600, 5.5)]

    BB_Params1d = [(600, 0.9), (600, 1), (600, 1.1),
                   (600, 1.9), (600, 2), (600, 2.1),
                   (600, 2.9), (600, 3), (600, 3.1),
                   (600, 6), (600, 6.5), (600, 7)]

    useMA = False
    MA_Periods1h = [40, 200, 400, 600]
    MA_Periods1d = [50, 100, 200, 300, 400, 500]

    TS = '_up_to_2022'
    TfDef = '10m'
    Tf1h = '1h'
    Tf1d = '1d'

    NoOfDataDef = 3000
    NoOfData1h = int(2.5*NoOfDataDef*int(TfDef[0:2])/60)
    NoOfData1d = int(2.5*NoOfData1h/24)
    # NoOfData1d = 2000

    exch = 'binance'

    plotMode = 1

    LRC_Def = 2
    LRC1d = LRC1h = LRC_Def

    MND = 0.03

    PCP_Def = 1
    PCP1h = 5
    PCP1d = 2

    DeltaT_Def = 35
    DeltaT1h = 10
    DeltaT1d = 10
    extrmFilterMode = 1
    realTimeMode = 0

    return (basePath, asset, indicUse, useVWAP, TS, TfDef, Tf1h, Tf1d,
            NoOfDataDef, NoOfData1h, NoOfData1d, exch, plotMode, LRC_Def,
            LRC1h, LRC1d, MND, PCP_Def, PCP1h, PCP1d, DeltaT_Def, DeltaT1h,
            DeltaT1d, extrmFilterMode,
            realTimeMode, useBB, BB_ParamsDef, BB_Params1h, BB_Params1d, useMA,
            MA_Periods1h, MA_Periods1d)
