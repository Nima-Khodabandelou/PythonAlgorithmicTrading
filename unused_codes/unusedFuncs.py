# #####################################################################
def computeLeastSquaresMA(t, x, n):
    ''' Calculates least squares moving average over a time series data.
    x: vector, n: period, t: time '''

    def list_operations(list1, list2, operator):
        ''' Dot operation for two lists'''
        if operator == 'sub':
            result = [i-j for i, j in zip(list1, list2)]
        elif operator == 'add':
            result = [i+j for i, j in zip(list1, list2)]
        elif operator == 'product':
            result = [i*j for i, j in zip(list1, list2)]
        elif operator == 'divide':
            result = [i/j for i, j in zip(list1, list2)]

        return result

    time = range(len(t))
    c1 = n*sum(list_operations(time, x, 'product'))
    b = (c1 - sum(time)*sum(x))/(n*sum(time) - sum(time)*sum(time))
    a = (1/n)*sum(x) - b*(1/n)*sum(time)
    LSMA = [b*item+a for item in time]

    # LSMA mapping:
    # x1 = x2 = t, y1 = [a, b], y2 = [a, c], a = min(cc), b = max(cc),
    # c = max(LSMA) --> func = a + (x - a)*(b - a)/(c - a)
    # func maps LSMA with vertical range of [a, c] to a new LSMA with vertical
    # range of [a, b]; hence, candlesticks and their LSMA would be in the same
    # range
    min_x = min(x)
    max_x = max(x)
    max_LSMA = max(LSMA)
    LSMA1 = [min_x + (item - min_x)*(max_x - min_x)/(max_LSMA - min_x)
             for item in LSMA]

    return LSMA1


# #####################################################################
def computeExponentialMA(cc, nd, smoothing=2):
    ema_val = [sum(cc[:nd]) / nd]
    for price in cc[nd:]:
        ema_val.append((price * (smoothing / (1 + nd))) + ema[-1] *
                       (1 - (smoothing / (1 + nd))))
    return ema_val

# #####################################################################
def calculatePivotLevelsVersion1(cl, ch):
        # p.p. parameters
        pp = [12, '12hr']
        pp = [24, '24hr']
        # no_pp: Number of pivots
        no_pp = 3
        period = pp[0]
        time_h = t[-1].hour
        time_m = t[-1].minute
        if time_h == 0 or time_h == pp[1]:
            # go for pp calc
            lcpci = (len(t) - 1) - (time_h)
            pp_high = max(ch[lcpci:lcpci + period])
            pp_low = min(cl[lcpci:lcpci + period])
            pp_close = cl[lcpci]
            pp_time_range = t[ch[lcpci:lcpci + period]]
        elif time_h != 0 and time_h != pp[1]:
            if 0 < time_h < 12:
                # pass time_h previous candles to pp calc
                cnt1 = time_m/10 + 1
                cnt2 = int((time_h - period + 1)*cnt1)
                lcpci = int((len(t) - 1) - cnt2)
                pp_high = max(ch[lcpci + 1:lcpci + cnt2 + 1])
                pp_low = min(ch[lcpci + 1:lcpci + cnt2 + 1])
                pp_close = cl[lcpci + cnt2]
                pp_time_range = t[lcpci + 1:lcpci + cnt2 + 1]
            elif 12 <= time_h <= 23:
                # We should find index of the candle before time_h
                # representing the last candle
                # for the last period (period:12hr, 24hr, 72hr, ...)
                # lcpci:The index of the last completed period candle
                # counting from end of the t list
                cnt1 = time_m/10 + 1
                cnt2 = int((time_h - period + 1)*cnt1)
                lcpci = int((len(t) - 1) - cnt2)
                pp_high = max(ch[lcpci + 1:lcpci + cnt2 + 1])
                pp_low = min(ch[lcpci + 1:lcpci + cnt2 + 1])
                pp_close = cl[lcpci + cnt2]
                pp_time_range = t[lcpci + 1:lcpci + cnt2 + 1]

        (pivotpoint, r1, r2, r3, r4, s1, s2, s3, s4) = pivots(pp_low, pp_high,
                                                              pp_close)
        return pp_time_range, pivotpoint, r1, r2, r3, r4, s1, s2, s3, s4


def calculatePivotLevelsVersion2(ch, cl, cc):
    ''' This func calculates standard pivots. There could be useful in
    defining s/r in sideway, trending, and rally market conditions.'''

    # There are several formulas to calculate pivot points three of which are
    # mentioned bellow:
    # p = (ch + cl + cc + co)/4
    # p = (ch + cl + 2*cc)/4
    # classic pivot
    p = (ch + cl + cc)/3
    r1 = 2*p - cl
    s1 = 2*p - ch
    r2 = p + (r1 - s1)
    s2 = p - (r1 - s1)
    r3 = ch + 2*(p - cl)
    s3 = cl - 2*(ch - p)
    r4 = ch + 3*(p - cl)
    s4 = cl - 3*(ch - p)

    return p, r1, r2, r3, r4, s1, s2, s3, s4


def initializePivotPoints(usePP, cl, ch):
    if usePP == 1:
        (pp_time_range, pivotpoint,
            r1, r2, r3, r4, s1, s2, s3, s4) = calculatePivotLevels(cl, ch)
    else:
        (pp_time_range, pivotpoint,
            r1, r2, r3, r4, s1, s2, s3, s4) = [0]*10

# #####################################################################
def defineVWAPConfig(cc, vol):
    ''' Define vwap configs and initial parameters'''
    no_vwaps = len(vwap_periods)
    vwap_smoothing = 0
    vwap_window_size = 15
    vwap_poly_order = 2

    vwaps = [[] for i in range(no_vwaps)]
    for i in range(no_vwaps):
        # if i == no_vwaps - 1:
        #   vwap_smoothing = 1

        vwaps[i].append(calculateVWAP(cc, vol, vwap_periods[i],
                                        vwap_smoothing,
                                        vwap_window_size, vwap_poly_order))

    return vwaps, no_vwaps


def calculateVWAP(cc, vol, period, smoothing, window_size, poly_order):
    ''' Calculates volume-weighted average price (vwap) and (if needed) applies
    Savitzky-Golay filter to smooth it. '''
    # No. of total data
    nd = len(cc)
    vwap = []

    for cnt in range(0, nd-period):
        lst = range(nd-period-cnt, nd-cnt)
        num = sum([cc[i]*vol[i] for i in lst[::-1]])
        denum = sum([vol[i] for i in lst[::-1]])
        if denum == 0:
            vwap_val = vwap[-1]
        else:
            vwap_val = num/denum
        vwap.append(vwap_val)

    if smoothing == 1:
        vwap1 = savgol_filter(vwap, window_size, poly_order)
        vwap1 = np.array(vwap1)
        vwap = vwap1.tolist()
        # for i in range(len(vwap1)):
        #     vwap[i] = vwap1[i]

    return vwap


def weighted_vwap(cc, vol, period, smoothing, window_size, poly_order):
    ''' Calculates vwaps with weight factors on volume and price'''
    # No. of total data
    nd = len(cc)
    vwap = []
    w = []
    cnt = 0
    # weighting_window
    ww = 10
    for cnt in range(0, nd-ww):
        lst = vol[0:nd-cnt*ww]
        w[cnt] = max(lst[nd-cnt*ww::-1])

    pass


def initializeVWAP(useVWAP, cc, vol, vwap_periods):
    if useVWAP == 1:
        vwaps, no_vwaps = defineVWAPConfig(cc, vol)
    else:
        vwaps, no_vwaps = [0, 0]

    return vwaps, no_vwaps

