from itertools import chain


def lrc(cnd, cl, ch, lrc):
    '''This function selects extrms satisfying lrc condition.'''
    mx = []
    mn = []
    while cnd < ma[-1] - 10:
        mntmp = []
        mxtmp = []
        for j in chain(range(cnd-lrc, cnd), range(cnd+1, cnd+lrc+1)):
            if cl[cnd] <= cl[j]:
                mntmp.append(1)
            else:
                mntmp.append(0)

            if ch[cnd] >= ch[j]:
                mxtmp.append(1)
            else:
                mxtmp.append(0)
        if all(mntmp):
            mn.append(cnd)

        if all(mxtmp):
            mx.append(cnd)
        cnd += 1

    return mx, mn


def hsr(cl, ch, cc, lrc, sr, lookback, cnd_start):
    '''This function calculates the most recent horizontal supports and
    resistence levels based on a given time window.'''
    # cnd: candle index
    new_sr_cnd = cnd_start - lrc
    atr_period = 40
    atr_multip = 4

    def chk_rept(sr, new_sr_cnd, cl_or_ch):
        '''This function checks the repetitivness of sr.'''
        status = False
        for cnd in sr:
            new_sr_val = cl_or_ch[new_sr_cnd]
            dist = abs(new_sr_val - sr[cnd])
            min_dist = atr_multip*atr(cl, ch, cc, new_sr_cnd, atr_period)
            if dist < min_dist:
                status = True
                break

        return status

    while new_sr_cnd > cnd_start - lookback:
        srtmp1 = []
        srtmp2 = []
        loop_range = chain(range(new_sr_cnd-lrc, new_sr_cnd),
                           range(new_sr_cnd+1, new_sr_cnd+lrc+1))
        for j in loop_range:
            if cl[new_sr_cnd] <= cl[j]:
                srtmp1.append(1)
            else:
                srtmp1.append(0)

            if ch[new_sr_cnd] >= ch[j]:
                srtmp2.append(1)
            else:
                srtmp2.append(0)

        if all(srtmp1) and sr == {}:
            sr[new_sr_cnd] = cl[new_sr_cnd]
        elif all(srtmp1) and sr != {}:
            if chk_rept(sr, new_sr_cnd, cl) is False:
                sr[new_sr_cnd] = cl[new_sr_cnd]

        if all(srtmp2) and sr == {}:
            sr[new_sr_cnd] = ch[new_sr_cnd]
        elif all(srtmp2) and sr != {}:
            if chk_rept(sr, new_sr_cnd, ch) is False:
                sr[new_sr_cnd] = ch[new_sr_cnd]

        new_sr_cnd -= 1
        if new_sr_cnd == 931000:
            start_debug = True

    return sr


def atr(ch, cl, cc, cnd, period):
    '''This function calculates ATR indicator.'''
    # tr: True Range
    tr = []
    for i in range(cnd, cnd - period, -1):
        tr.append(max(ch[i] - cl[i], abs(ch[i] - cc[i-1]),
                      abs(cl[i] - cc[i-1])))

    atr = sum(tr)/period
    return atr


def extrms(cl, ch):
    lookback = 200
    advancing_status = -1
    cnd = 2200
    lrc = 5
    mn = []
    mx = []
    while cnd - lookback > 0:
        mntmp = []
        mxtmp = []
        loop_range = chain(range(cnd-lrc, cnd),
                           range(cnd+1, cnd+lrc+1))
        for j in loop_range:
            if cl[cnd] <= cl[j]:
                mntmp.append(1)
            else:
                mntmp.append(0)

            if ch[cnd] >= ch[j]:
                mxtmp.append(1)
            else:
                mxtmp.append(0)

        if all(mntmp):
            mn_status = True

        if all(mxtmp):
            mx_status = True

        if mn == [] and mn_status is True:
            mn.append(cnd)

        if mx == [] and mx_status is True:
            mx.append(cnd)

        if mn != [] and mn_status is True:
            if cl[cnd] < cl[mn[-1]]:
                mn[-1] = cnd

        if mx != [] and mx_status is True:
            if ch[cnd] > ch[mx[-1]]:
                mx[-1] = cnd

        cnd = cnd + advancing_status

        if cnd == 931000:
            start_debug = True


def var_coeff():
    '''This function calculates correlation and coefficient of variation for
    multiple assets. Calculations are based on time series comparison and not
    a single varibale.'''
    pass


def sessions():
    '''This function sends alerts for specific market openning times in
    US, uk, Germany, Japan, Hong Kong, and Australia.'''
    pass


def liquid():
    '''This function checks markets' liquidity.'''
    pass


def average(data, Period):
    '''This function calculates average value of a series.'''
    ave = sum([data[i] for i in range(Period)])/Period

    return ave


def ma(useMA, cc1h, periods):
    '''This function calculates moving average vector of given data for
    different periods.'''
    nod = len(cc1h)
    if useMA is True:
        ma_vecs = [[] for i in range(len(periods))]
        for j in range(len(ma_vecs)):
            for i in range(periods[j], nod):
                # mean = average(cc1h[i: i - periods[j]: -1], periods[j])
                mean = average(cc1h[i - periods[j]: i], periods[j])
                ma_vecs[j].append(mean)
    else:
        ma_vecs = [0, 0, 0]

    return ma_vecs
