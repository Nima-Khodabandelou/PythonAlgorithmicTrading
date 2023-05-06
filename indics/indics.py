def calcScalarValOfMA_OfA_Vec(data, Period):
    ''' Calculates exponential/simple moving average'''
    MA_Scalar = sum([data[i] for i in range(Period)])/Period

    return MA_Scalar


def computeMA_Vecs(useMA, cc1h, MA_Periods):

    numberOfData = len(cc1h)

    if useMA is True:

        MA_Vecs = [[] for i in range(len(MA_Periods))]

        for j in range(len(MA_Vecs)):

            for i in range(numberOfData - 1, MA_Periods[j] - 1, -1):

                MA_AtEverydataPoint =\
                    calcScalarValOfMA_OfA_Vec(
                                    cc1h[i: i - MA_Periods[j]: -1],
                                    MA_Periods[j])
                MA_Vecs[j].append(MA_AtEverydataPoint)

    else:

        MA_Vecs = [0, 0, 0]

    return MA_Vecs


def ATR(ch, cl, cc):
    ''' Calculates market volatility based on ATR indicator.'''
    dt = len(cc)
    # TR: True Range
    TR = []
    for i in range(dt, 0, -1):
        TR[i] = max(ch[i] - cl[i],
                    abs(ch[i] - cc[i-1]),
                    abs(cl[i] - cc[i-1]))

    ATR = sum(TR)/dt
    return ATR
