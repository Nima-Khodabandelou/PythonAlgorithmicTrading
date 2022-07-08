def initSet():
    basePath = "C:\\files\\algotrader\\main\\histData\\"
    asset = 'EOSUSDT'
    TS = '_up_to_2022'
    Tf1h = '1h'
    Tf1d = '1d'
    NoOfData1h = 3000
    NoOfData1d = int(3*NoOfData1h/24)
    exch = 'binance'
    plotMode = 1
    LRC1d = LRC1h = 2
    MND = 0.01
    PCP1h = 2
    PCP1d = 10
    DeltaT1h = 10
    DeltaT1d = 10
    extrmFilterMode = 1
    realTimeMode = 0

    return (basePath, asset, TS, Tf1h, Tf1d, NoOfData1h, NoOfData1d, exch,
            plotMode, LRC1h, LRC1d, MND, PCP1h, PCP1d, DeltaT1h, DeltaT1d,
            extrmFilterMode, realTimeMode)


def initSet1h():
    basePath = "C:\\files\\algotrader\\main\\histData\\"
    asset = 'EOSUSDT'
    TS = '_up_to_2022'
    Tf1h = '1h'
    NoOfData1h = 6000
    NoOfData1d = int(3*NoOfData1h/24)

    return (basePath, asset, TS, Tf1h, NoOfData1h, NoOfData1d)


def initSetDef():
    path = "C:\\files\\algotrader\\main\\histData\\"
    asset = 'LINKBTC'
    ts = '_up_to_2022'
    tf = '10m'
    nod = 6000

    return (path, asset, ts, tf, nod)
