from itertools import chain

import numpy as np

from scipy.signal import savgol_filter


def market_scenarios():
    ''' Calculates/Identifies:

     extrms at different market tfs (different sizes)
     pcp and its time duration w.r.t. extrms
     vol breakout/trend
     correlation between vol, price and not
     movements
     corrections
     shadow
     extrm sudden reversals (time and vol matters)
     S/R
     possible trend
     trend strength (vol matters)
     cnsld periods
     (inclined up/down) cnsld
     (weak/strong) uptrend/downtrend
     downtrend/uptrend reversal
     rally market
     S/R ranking
     side (mean reverting market)
     diverging/converging/neutral side
     highly volatile/little volatile side
     side breakout (time and vol matters)
     side finish: price breaks sideway market to up or down and a
                  consolidation or retest occures indicating a continuation
                  of higher size trend or a breakout in higher size pattern

     any possible pattern mostly (inclined up/down)/neutral traiangle '''
    pass


def extrms_based_on_neighboring_candles_with_filter_v2(cl, ch, lrc):
    ''' Finds maximums and minimums of price in a time range.'''

    # initializing the lists for extremums indexes
    mx_indx_tmp = []
    mn_indx_tmp = []
    mx_indx = []
    mn_indx = []

    def filter_extrms_based_on_lrc():
        ''' Selects extrms satisfying lrc condition.'''

        # no_data: No. of total candles
        no_data = len(cl)
        for i in range(lrc, no_data-lrc):
            # tmp1: temp list initialization for candle low
            tmp1 = []
            # tmp2: temp list initialization for candle high
            tmp2 = []
            # Traversing over a candle to both left and right sides w.r.t. lrc
            # and selecting appropriate ones
            for j in chain(range(i-lrc, i), range(i+1, i+lrc+1)):
                if cl[i] < cl[j]:
                    tmp1.append(1)
                else:
                    tmp1.append(0)

                if ch[i] > ch[j]:
                    tmp2.append(1)
                else:
                    tmp2.append(0)

            # if all(tmp1) and all(tmp2):
            #     extrm_s_r_indx.append(i)
            #     extrm_s_r_price.append(cl[i])
            #     extrm_s_r_price.append(ch[i])
            #     continue

            # If this cond. holds, it means that minimums of all candles around
            # candle No. j are higher than min of candle j
            if all(tmp1):
                mn_indx_tmp.append(i)

            if all(tmp2):
                mx_indx_tmp.append(i)

    filter_extrms_based_on_lrc()

    nd_mn = len(mn_indx_tmp)
    nd_mx = len(mx_indx_tmp)
    # Total No. of selected extrms based on lrc that have potential to be
    # max or min
    nd = nd_mx + nd_mn
    # The predefined minimum pcp and dt for every two consecutive extrms
    # to be valid (Currently these 2 params are optional but may depend on
    # other params in future)
    pcp_base = 10
    dt_base = 10

    def filter_extrms_based_on_time_and_pcp():
        ''' Filters previously selected extrms based on elapsed time
        and price change percentage.'''

        # switcher: list to save counter(cnt) values (cnt is 0 or 1) to switch
        # bet. min and max seeking
        switcher = []
        # cnt_for_switcher: counter for switcher. If cnt_for_switcher = 0 the
        # first valid extrm is max (1st element of mx_indx_tmp) and search is
        # performed for finding the next min. If cnt_for_switcher = 1 the first
        # valid extrm is min (1st element of mn_indx_tmp) and search is 
        # performed for finding the next max.
        cnt_for_switcher = 0
        # total_cnt_min_max: counter for total No. of valid min and max
        total_cnt_min_max = 0
        # total_cnt_min: counter for total No. of valid min
        total_cnt_min = 0
        # total_cnt_max: counter for total No. of valid max
        total_cnt_max = 0
        # total_no_extrms: counter for total No. of valid extrms
        total_no_extrms = 0

        def switcher_initial_config():
            ''' Initial config for switcher '''

            # If 1st extrm is max (mx_indx_tmp[0] < mn_indx_tmp[0]) then
            # 1st element of switcher would be 0. 
            if mx_indx_tmp[0] < mn_indx_tmp[0]:
                switcher.append(0)
            # Moreover this max would also be 1st valid max and is added
            # to mx_indx list.
                mx_indx.append(mx_indx_tmp[0])
            # An otherwise cond holds for 1st valid min
            else:
                switcher.append(1)
                mn_indx.append(mn_indx_tmp[0])

        switcher_initial_config()

        def pcp_time(indx2, c2, indx1, c1):
            ''' Performs comparison for each two consecutive extrm pairs
            (a max and the preceeding min or a min and the preceeding max)
            based on the condition of price change percentage (pcp) and elapsed
            time (dt) and decides on the suitability of the extrm pairs.'''

            # In calculating pcp, always the 1st extrm (no matter max or min)
            # is subtracted from the 2nd one and result is divided by 1st one.
            pcp = 100*abs(c2[indx2] - c1[indx1])/c1[indx1]
            dt = abs(indx2 - indx1)

            if pcp < pcp_base and dt < dt_base:
                cond = 0
            elif pcp < pcp_base and dt >= dt_base:
                cond = 1
            elif pcp >= pcp_base and dt < dt_base:
                cond = 1
            elif pcp >= pcp_base and dt >= dt_base:
                cond = 1

            return cond, indx2

        def search_bet_extrms(state, total_cnt_max, total_cnt_min,
                              total_cnt_min_max):
            '''
            Seeks whether there are any further extrms 
            between two consecutive valid min/max or max/min pairs.
            There are two possibilities for inputs. If state is 'min' then
            we're (looking for/or modifying) next min and vice versa. Hence:

            State = max_to_min --> search for extrms bet. the 1st valid extrm
            (MAX) and the 2nd valid one (MIN)

            State = min_to_max --> search for extrms bet. the 1st valid (MIN)
            and the 2nd valid one (MAX)
            '''
            # At first the No. of found min or max is zero
            cnt_min = 0
            cnt_max = 0
            if state == 'max_to_min':
                extrm_indx_1 = mx_indx
                extrm_indx_2 = mn_indx
                extrm_indx_tmp_1 = mx_indx_tmp
                extrm_indx_tmp_2 = mn_indx_tmp
                cl_or_ch = ch
                cnt_min_max_1 = cnt_max
                cnt_min_max_2 = cnt_min
                total_cnt_max_or_min = total_cnt_max
            elif state == 'min_to_max':
                extrm_indx_1 = mn_indx
                extrm_indx_2 = mx_indx
                extrm_indx_tmp_1 = mn_indx_tmp
                extrm_indx_tmp_2 = mx_indx_tmp
                cl_or_ch = cl
                cnt_min_max_1 = cnt_min
                cnt_min_max_2 = cnt_max
                total_cnt_max_or_min = total_cnt_min
            # range bet two valid extrms
            lst = range(extrm_indx_1[-1] + 1, extrm_indx_2[-1])
            for item in lst:
                if (item in extrm_indx_tmp_1) and\
                   (cl_or_ch[item] < cl_or_ch[extrm_indx_1[-1]]):
                    # In this case the newly found extrm doesn't meet condition
                    # and only indicates that there's one extrm in bet. two
                    # valid ones and should be taken into account
                    cnt_min_max_1 += 1
                elif (item in extrm_indx_tmp_1) and\
                     (cl_or_ch[item] > cl_or_ch[extrm_indx_1[-1]]):

                    extrm_indx_1[-1] = extrm_indx_tmp_1[total_cnt_max_or_min +
                                                        len(extrm_indx_1)]
                    cnt_min_max_1 += 1
                elif item in extrm_indx_tmp_2:
                    cnt_min_max_2 += 1

            total_cnt_min += cnt_min
            total_cnt_max += cnt_max
            total_cnt_min_max += cnt_max + cnt_min

        def search_bet_extrms2(state, total_cnt_max, total_cnt_min,
                               total_cnt_min_max):
            '''
            Seeks whether there are any further extrms between two consecutive
            valid min/max or max/min pairs. There are two possibilities for
            inputs. If state is 'min' then we're (looking for/or modifying)
            next min and vice versa. Hence:

            State = max_to_min --> search for extrms bet. the 1st valid extrm
            (MAX) and the 2nd valid one (MIN)

            State = min_to_max --> search for extrms bet. the 1st valid (MIN)
            and the 2nd valid one (MAX)
            '''
            # At first No. of found min/max is zero
            cnt_min = 0
            cnt_max = 0
            if state == 'max_to_min':
                # range bet. two valid extrms where search is performed
                lst = range(mx_indx[-1] + 1, mn_indx[-1])
                for item in lst:
                    if item in mx_indx_tmp and ch[item] < ch[mx_indx[-1]]:
                        # In this case, the newly found max is lower than the
                        # last valid max (mx_indx[-1]); hence, search only
                        # indicates that there's another max in bet. two valid
                        # MAX and MIN and it should be taken into account and
                        # cnt_max is updated.
                        cnt_max += 1
                    elif item in mx_indx_tmp and ch[item] > ch[mx_indx[-1]]:
                        mx_indx[-1] = mx_indx_tmp[total_cnt_max + len(mx_indx)]
                        cnt_max += 1
                    elif item in mn_indx_tmp:
                        cnt_min += 1

            elif state == 'min_to_max':
                lst = range(mn_indx[-1] + 1, mx_indx[-1])
                for item in lst:
                    if item in mn_indx_tmp and cl[item] > cl[mn_indx[-1]]:
                        cnt_min += 1
                    elif item in mn_indx_tmp and cl[item] < cl[mn_indx[-1]]:
                        mn_indx[-1] = mn_indx_tmp[total_cnt_min + len(mn_indx)]
                        cnt_min += 1
                    elif item in mx_indx_tmp:
                        cnt_max += 1

            total_cnt_min += cnt_min
            total_cnt_max += cnt_max
            total_cnt_min_max += cnt_max + cnt_min

            return total_cnt_min_max, total_cnt_min, total_cnt_max

        # 1st while loop checks if counter for total No. of valid extrms
        # (total_no_extrms) is lower than total No. of extrms (nd)
        while total_no_extrms < nd:
            if switcher[cnt_for_switcher] == 0:
                # ######################## find next min (max_to_min)
                if len(mn_indx) == 0:
                    tmp_lst = mn_indx_tmp
                else:
                    tmp_lst = mn_indx_tmp[len(mn_indx) + total_cnt_min:]

                cnt_for_cond = 0
                cond = 0
                # 2nd while loop for max_to_min case
                while cond == 0:
                    cond, true_indx = pcp_time(tmp_lst[cnt_for_cond],
                                               cl, mx_indx[-1],
                                               ch)
                    cnt_for_cond += 1
                    if cond == 1:
                        # Check if the found_min (true_indx) is higher than the
                        # previous valid max. If it's higher then it's not
                        # acceptable and the previous valid max should be
                        # replaced with another valid max with a higher value
                        # which resides somewhere in bet. the current valid max
                        # and the found_min.
                        if cl[true_indx] > ch[mx_indx[-1]]:
                            (total_cnt_min_max,
                             total_cnt_min,
                             total_cnt_max) =\
                                 search_bet_extrms2('max_to_min',
                                                    total_cnt_max,
                                                    total_cnt_min,
                                                    total_cnt_min_max)
                            # Then search for the new min must be reperformed.
                            # So cond is set to 0 and the 2nd while loop
                            # continues.
                            cond = 0
                        elif cl[true_indx] < ch[mx_indx[-1]]:
                            # Here we have a new found_min which is valid and
                            # added to the list of valid mins.
                            mn_indx.append(true_indx)
                            # There could be other min or max before the found
                            # extrms whose number should be taken into account
                            # in counting the the total number of studied
                            # extrms. So the search is performed to calc.
                            # total_cnt_min_max
                            (total_cnt_min_max,
                             total_cnt_min,
                             total_cnt_max) =\
                                search_bet_extrms2('max_to_min',
                                                   total_cnt_max,
                                                   total_cnt_min,
                                                   total_cnt_min_max)
                            break
                # total No. of extrms is updated so that condition for
                # (continuation of/stoping) the first while loop could
                # be checked.
                total_no_extrms = (total_cnt_min_max + len(mx_indx) +
                                   len(mn_indx))

                cnt_for_switcher += 1
                # go for next max
                switcher.append(1)

            else:
                # ######################## find next max (min_to_max)
                if len(mx_indx) == 0:
                    tmp_lst = mx_indx_tmp
                else:
                    tmp_lst = mx_indx_tmp[len(mx_indx) + total_cnt_max:]

                cnt_for_cond = 0
                cond = 0
                # 2nd while loop for min_to_max case
                while cond == 0:
                    cond, true_indx = pcp_time(tmp_lst[cnt_for_cond],
                                               ch, mn_indx[-1],
                                               cl)
                    cnt_for_cond += 1

                    if cond == 1:
                        if ch[true_indx] < cl[mn_indx[-1]]:
                            (total_cnt_min_max,
                             total_cnt_min,
                             total_cnt_max) =\
                                 search_bet_extrms2('min_to_max',
                                                    total_cnt_max,
                                                    total_cnt_min,
                                                    total_cnt_min_max)
                            cond = 0
                        elif ch[true_indx] > cl[mn_indx[-1]]:
                            # Here we have a new true max.
                            mx_indx.append(true_indx)
                            # calc total_cnt_min_max
                            (total_cnt_min_max,
                             total_cnt_min,
                             total_cnt_max) =\
                                search_bet_extrms2('min_to_max',
                                                   total_cnt_max,
                                                   total_cnt_min,
                                                   total_cnt_min_max)
                            break

                total_no_extrms = (total_cnt_min_max + len(mx_indx) +
                                   len(mn_indx))

                cnt_for_switcher += 1
                # go for next min
                switcher.append(0)

        return filter_extrms_based_on_time_and_pcp

    filter_extrms_based_on_time_and_pcp()

    return mx_indx, mn_indx


def extrms_based_on_neighboring_candles_without_filter(cl, ch, lrc):
    ''' Finds maximums and minimums of price in a time range.'''
    # initializing the lists for extremums indexes
    mx_indx_tmp = []
    mn_indx_tmp = []
    # lrc defines the number of left or right neighboring candles for
    # extremum comparison,i.e. if for instance lrc=5 and a specific
    # candle's high is higher than 5 candles on the leftside and 5 candles on
    # the rightside then that candle would be considered as a maximum extrm.
    nd = len(cl)
    for i in range(lrc, nd-lrc):
        # temp list for candle low
        tmp1 = []
        tmp2 = []

        for j in chain(range(i-lrc, i), range(i+1, i+lrc+1)):
            if cl[i] < cl[j]:
                tmp1.append(1)
            else:
                tmp1.append(0)

            if ch[i] > ch[j]:
                tmp2.append(1)
            else:
                tmp2.append(0)

        if all(tmp1) and all(tmp2):
            continue

        if all(tmp1):
            mn_indx_tmp.append(i)

        if all(tmp2):
            mx_indx_tmp.append(i)

    return mx_indx_tmp, mn_indx_tmp


def ma(cc, nd):
    ''' Calculates exponential/simple moving average'''
    ma_val = [sum([cc[i] for i in range(nd)])/nd]

    return ma_val


def lsma(t, x, n):
    ''' Calculates least squares moving average over a time series data.
    x: vector, n: period, t: time '''

    def list_operations(list1, list2, operator):
        ''' Dor product of two lists'''
        if operator == 'sub':
            result = [i-j for i, j in zip(list1, list2)]
        elif operator == 'add':
            result = [i+j for i, j in zip(list1, list2)]
        elif operator == 'product':
            result = [i*j for i, j in zip(list1, list2)]
        elif operator == 'divide':
            result = [i/j for i, j in zip(list1, list2)]

        return result

    c1 = n*sum(list_operations(t, x, 'product'))
    b = (c1 - sum(t)*sum(x))/(n*sum(t) - sum(t)*sum(t))
    a = (1/n)*sum(x) - b*(1/n)*sum(t)
    LSMA = [b*item+a for item in t]

    return LSMA


def ema(cc, nd, smoothing=2):
    ema_val = [sum(cc[:nd]) / nd]
    for price in cc[nd:]:
        ema_val.append((price * (smoothing / (1 + nd))) + ema[-1] *
                       (1 - (smoothing / (1 + nd))))
    return ema_val


def vwap(cc, vol, period, smoothing, window_size, poly_order):
    ''' Calculates volume-weighted average price (vwap) and (if needed) applies
    Savitzky-Golay filter to smooth it. '''
    # No. of total data
    nd = len(cc)
    vwap = []

    for cnt in range(0, nd-period):
        lst = range(nd-period-cnt, nd-cnt)
        num = sum([cc[i]*vol[i] for i in lst[::-1]])
        denum = sum([vol[i] for i in lst[::-1]])
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


def pivots(ch, cl, cc, co):
    ''' Calculates standard pivots (preferebly weekly ones) for rally market
    when there isn't enough extrms to define further s/r.'''
    p = (ch + cl + cc)/3
    p = (ch + cl + cc + co)/4
    p = (ch + cl + 2*cc)/4
    r1 = 2*p - cl
    s1 = 2*p - ch
    r2 = p + ch - cl
    s2 = p - ch + cl
    r3 = r1 + ch - cl
    s3 = s1 - ch + cl

    return p, r1, r2, r3, s1, s2, s3


def pcp():
    ''' Defines price change percentage w.r.t each min/max'''


def s_r():
    ''' Calculates horizontal supports and resistence levels '''
    pass


def price_breakout():
    ''' Identifies possible breakouts in p. '''
    pass


def vol_breakout():
    ''' Identifies possible breakouts in v. '''
    pass


def s_r_ranking():
    ''' Ranks S/R based on their effectiveness (the importance of the
        extrms used)'''
    pass


def retest_on_s_r():
    ''' Identifies possible Retest on supports and resistence levels. '''
    pass


def hammer():
    ''' Identifies possible Hammer candle. '''
    pass


def stop_hunt():
    ''' Detects possible stop hunting areas for possible enterance or setting
    better stop loss. '''
    pass


def volatility(ch, cl, cc):
    ''' Calculates volatility in market based on ATR indicator.'''
    dt = len(cc)
    # TR: True Range
    TR = []
    for i in range(dt, 0, -1):
        TR[i] = max(ch[i] - cl[i],
                    abs(ch[i] - cc[i-1]),
                    abs(cl[i] - cc[i-1]))

    ATR = sum(TR)/dt
    return ATR


def oscillation_bound(ch, cl):
    ''' Evaluates the vertical range in which price is fluctuating. '''
    dt = len(cl)
    init = 10
    bound = []
    bound = [ch[i] - cl[i] for i in range(init, dt)]
    Bound = sum(bound)/abs(dt - init)
    return Bound


def correlation():
    ''' Defines correlation between various cryptos'''
    pass


def liquidity():
    ''' Checks market liquidity and volume and number of trades to select
    the proper base time frame.
    '''
    pass

