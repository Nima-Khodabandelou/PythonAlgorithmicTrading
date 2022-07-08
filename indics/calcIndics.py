from cmath import sqrt
from scipy.signal import savgol_filter


# #####################################################################
def calcScalarValOfSTDV_OfA_Vec(data, period):
    ''' Calculates standard deviation of a given series (data) over a given
    period. '''

    mean = sum(data)/len(data)
    numerator = 0
    for i in range(0, period):
        numerator += (data[i] - mean)**2

    stdv = sqrt(numerator/(period - 1)).real

    return stdv


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


def computeBB_AtdataPoint(data, BB_Period, BB_STDV_Multiplier):

    BB_MA_AtDataPoint =\
        calcScalarValOfMA_OfA_Vec(
            data, BB_Period)
    BB_STDV = calcScalarValOfSTDV_OfA_Vec(
        data, BB_Period)

    BB_UB_AtDataPoint = BB_MA_AtDataPoint +\
        BB_STDV_Multiplier*BB_STDV

    BB_LB_AtDataPoint = BB_MA_AtDataPoint -\
        BB_STDV_Multiplier*BB_STDV

    return (BB_MA_AtDataPoint, BB_UB_AtDataPoint,
            BB_LB_AtDataPoint)


def CalcBB_VecsforSTDV_Coeffs(useBB, data, BB_Params):

    numberOfData = len(data)
    # numberOfSTDV_Multipliers = len(BB_STDV_Multiplier)
    numberOfBB = len(BB_Params)

    if useBB is True:

        BB_MA_Vec = [[] for i in range(numberOfBB)]
        BB_UB_Vec = [[] for i in range(numberOfBB)]
        BB_LB_Vec = [[] for i in range(numberOfBB)]

        for j in range(numberOfBB):
            for i in range(numberOfData - 1, BB_Params[j][0] - 1, -1):

                (BB_MA_AtdataPoint,
                    BB_UB_AtdataPoint,
                    BB_LB_AtdataPoint) =\
                    computeBB_AtdataPoint(
                    data[i: i - BB_Params[j][0]: -1], BB_Params[j][0],
                    BB_Params[j][1])

                BB_MA_Vec[j].append(
                    BB_MA_AtdataPoint)
                BB_UB_Vec[j].append(
                    BB_UB_AtdataPoint)
                BB_LB_Vec[j].append(
                    BB_LB_AtdataPoint)

    else:

        BB_MA_Vec, BB_UB_Vec, BB_LB_Vec = [0, 0, 0]

    return (BB_MA_Vec, BB_UB_Vec, BB_LB_Vec)


# #####################################################################
def calcATR(ch, cl, cc):
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


# #####################################################################
def calcOscillationBound(ch, cl):
    ''' Evaluates the vertical range in which price is fluctuating. '''
    dt = len(cl)
    init = 10
    bound = []
    bound = [ch[i] - cl[i] for i in range(init, dt)]
    Bound = sum(bound)/abs(dt - init)
    return Bound



