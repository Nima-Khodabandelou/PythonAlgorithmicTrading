from itertools import chain


global pcp_base, pcp_time

# GENERAL TERMS AND DEFINITIONS

# pcp_base, dt_base: The predefined minimum price change percentage and
# elapsed time(dt) for every two consecutive extrms to be valid
# (Currently these 2 params are optional but may depend on other params
# in future)

# A candle high/low is an extrm if it passes the lrc condition
# (filter_extrms_based_on_lrc function in the following).
# lrc was defined in the main.py file.

# A candle high/low is a valid extrm if it passes lrc, pcp and dt
# conditions (pcp_time funtion in the following)

# An invalid extrm is an extrm that passed only the lrc condition and
# not the pcp/dt

# A valid extrm is named as mx (stands for max) or mn.

# mx_indx/mn_indx are lists holding VALID max/min indexes


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


def extrms_based_on_neighboring_candles_with_filter(cl, ch, lrc, pcp_base,
                                                    dt_base,
                                                    real_time_mode):
    ''' Finds maximums and minimums of price in a time range.'''
    global mn_indx, mx_indx, max_updated, min_updated

    max_updated = 0
    min_updated = 0

    mx_indx = []
    mn_indx = []

    filter_extrms_based_on_lrc(cl, ch, lrc)

    filter_extrms_based_on_time_and_pcp(cl, ch, pcp_base, dt_base,
                                        real_time_mode)

    return mx_indx, mn_indx


def filter_extrms_based_on_lrc(cl, ch, lrc):
    ''' Selects extrms satisfying lrc condition.'''
    global nd, mx_indx_tmp, mn_indx_tmp, s_r_indx
    # initializing the lists for extremums indexes
    mx_indx_tmp = []
    mn_indx_tmp = []
    s_r_indx = []
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
            if cl[i] <= cl[j]:
                tmp1.append(1)
            else:
                tmp1.append(0)

            if ch[i] >= ch[j]:
                tmp2.append(1)
            else:
                tmp2.append(0)

        if all(tmp1) and all(tmp2):
            s_r_indx.append(i)
            cnt = lrc + 1
            cl_score = 0
            ch_score = 0
            while cnt <= i and i+cnt+1 < no_data:
                for k in chain(range(i-cnt, i), range(i+1, i+cnt+1)):
                    if cl[i] <= cl[k]:
                        cl_score += 1
                    elif ch[i] >= ch[k]:
                        ch_score += 1

                if cl_score > ch_score:
                    mn_indx_tmp.append(i)
                    break
                elif cl_score < ch_score:
                    mx_indx_tmp.append(i)
                    break
                elif cl_score == ch_score:
                    cnt += 1
                    continue

            continue

        # If this cond. holds, it means that minimums of all candles around
        # candle No. j are higher than min of candle j
        if all(tmp1):
            mn_indx_tmp.append(i)

        if all(tmp2):
            mx_indx_tmp.append(i)

    nd_mn = len(mn_indx_tmp)
    nd_mx = len(mx_indx_tmp)
    # Total No. of selected extrms based on lrc that have potential to be
    # max or min
    nd = nd_mx + nd_mn

    return mn_indx_tmp, mx_indx_tmp, nd


def switcher_initial_config(switcher):
    ''' Initial config for switcher '''

    # If 1st extrm is max (mx_indx_tmp[0] < mn_indx_tmp[0]) then 1st element
    # of switcher would be 0.
    if mx_indx_tmp[0] < mn_indx_tmp[0]:
        switcher.append(0)
    # This max would also be 1st valid max and is added to mx_indx list.
        mx_indx.append(mx_indx_tmp[0])
    # An otherwise condition holds for 1st valid min
    else:
        switcher.append(1)
        mn_indx.append(mn_indx_tmp[0])


def pcp_time(indx2, c2, indx1, c1, pcp_base, dt_base):
    ''' Performs comparison for each two consecutive extrm pairs
    (a max and the preceeding min or a min and the preceeding max)
    based on the condition of price change percentage (pcp) and elapsed
    time (dt) and decides on the suitability of the extrm pairs
    (cond = 1 if suitable).
    In calculating pcp, always the 1st extrm (no matter max or min)
    is subtracted from the 2nd one and result is divided by the 1st one.'''

    pcp = 100*abs(c2[indx2] - c1[indx1])/c1[indx1]
    dt = abs(indx2 - indx1)

    cond = 0

    if 0.5*pcp_base < pcp < pcp_base and dt >= dt_base:
        cond = 1
    elif pcp >= pcp_base:
        cond = 1

    return cond, indx2


def search_bet_extrms(state, total_cnt_invalid_max, total_cnt_invalid_min,
                      cl, ch, true_indx):
    '''
    Seeks whether there are any further extrms between two consecutive
    valid min/max or max/min pairs. There are two possibilities for
    inputs:

    State = max_to_min --> search for extrms bet. the 1st valid extrm
    (MAX) and the 2nd valid one (MIN)

    State = min_to_max --> search for extrms bet. the 1st valid extrm (MIN)
    and the 2nd valid one (MAX)
    '''
    global max_updated, min_updated

    if state == 'max_to_min':
        # If the following condition holds, there are at least one candle
        # between the two consecutive valid max and min which could represent
        # an extrm.
        if mn_indx != [] and (mx_indx[-1] + 1) <= mn_indx[-1]:
            range_upper_bound = mn_indx[-1]
        elif mn_indx == [] or (mx_indx[-1] + 1) > mn_indx[-1]:
            # Otherwise, {mx_indx[-1] + 1} could be equal to mn_indx[-1]
            # (and not less than it since it's nonsense); hence,
            # there would be no extrm at all between the two consecutive
            # valid max and min.
            range_upper_bound = true_indx

        # range between two valid extrms where search is performed
        lst = range(mx_indx[-1] + 1, range_upper_bound)
        for item in lst:
            if item in mx_indx_tmp and ch[item] <= ch[mx_indx[-1]]:
                # In this case, the newly found max is lower than the
                # last valid max (mx_indx[-1]); hence, search only
                # indicates that there's another max in bet. two valid
                # MAX and MIN and it should be taken into account and
                # cnt_max is updated.
                total_cnt_invalid_max += 1
            elif item in mx_indx_tmp and ch[item] > ch[mx_indx[-1]]:
                # mx_indx[-1] = mx_indx_tmp[total_cnt_invalid_max
                #                           + len(mx_indx)]
                mx_indx[-1] = item
                last_extrms_for_debug()
                total_cnt_invalid_max += 1
                max_updated = 1
                break
            # elif item in mn_indx_tmp and cl[item] < cl[true_indx]:
            #     min_should_be_updated = 1
            #     break
            elif item in mn_indx_tmp:
                total_cnt_invalid_min += 1

    elif state == 'min_to_max':
        if mx_indx != [] and (mn_indx[-1] + 1) <= mx_indx[-1]:
            range_upper_bound = mx_indx[-1]
        elif mx_indx == [] or (mn_indx[-1] + 1) > mx_indx[-1]:
            range_upper_bound = true_indx

        lst = range(mn_indx[-1] + 1, range_upper_bound)
        for item in lst:
            if item in mn_indx_tmp and cl[item] >= cl[mn_indx[-1]]:
                total_cnt_invalid_min += 1
            elif item in mn_indx_tmp and cl[item] < cl[mn_indx[-1]]:
                # mn_indx[-1] = mn_indx_tmp[total_cnt_invalid_min
                #                           + len(mn_indx)]
                mn_indx[-1] = item
                last_extrms_for_debug()
                total_cnt_invalid_min += 1
                min_updated = 1
                break
            # elif item in mx_indx_tmp and ch[item] > ch[true_indx]:
            #     max_should_be_updated = 1
            #     break
            elif item in mx_indx_tmp:
                total_cnt_invalid_max += 1

    return total_cnt_invalid_min, total_cnt_invalid_max


def last_extrms_for_debug():
    ''' This func stores the last updated min and max for easier debugging.
    It doesn't affect the calculation process in any sense.'''
    global amn_last, amx_last
    # mn_last and mx_last store the last two items of mn_indx and
    # mx_indx. They're only for better visual track of valid extrms on
    # the left side debugger window.
    if len(mn_indx) != 0:
        amn_last = mn_indx[-1]
    else:
        amn_last = 0

    if len(mx_indx) != 0:
        amx_last = mx_indx[-1]
    else:
        amx_last = 0

    return amn_last, amx_last


def filter_extrms_based_on_time_and_pcp(cl, ch, pcp_base, dt_base,
                                        real_time_mode):
    ''' Filters previously selected extrms based on elapsed time
    and price change percentage. The resulting extrms would be vaild ones.'''

    global max_updated, min_updated

    # TERMS AND DEFINITIONS

    # switcher: list to save counter(cnt) values (cnt is 0 or 1) to switch
    # between min and max seeking
    switcher = []
    # cnt_for_switcher --> counter for switcher. If cnt_for_switcher = 0 the
    # first extrm is max (1st element of mx_indx_tmp) and search is
    # performed for finding the next min. If cnt_for_switcher = 1 the first
    # extrm is min (1st element of mn_indx_tmp) and search is
    # performed for finding the next max.
    cnt_for_switcher = 0
    # total_cnt_invalid_min: counter for total No. of invalid min
    total_cnt_invalid_min = 0
    # total_cnt_invalid_max: counter for total No. of invalid max
    total_cnt_invalid_max = 0
    # total_no_extrms: counter for total No. of valid and invalid extrms
    total_no_extrms = 0

    switcher_initial_config(switcher)

    last_extrms_for_debug()

    last_max_not_found = 0
    last_min_not_found = 0

    # 1st while loop checks if counter for total No. of valid extrms
    # (total_no_extrms) is lower than total No. of extremums (nd)

    # 1st while loop: checks if total no. of found extrms is lower than total
    # no. of existing extrms (valid and invalid)
    while total_no_extrms < nd:
        if switcher[cnt_for_switcher] == 0:
            # ######################## find next min (max_to_min)

            # At the beginning of the seeking process, if 1st extrm is a
            # max (which has been assigned in switcher_initial_config func)
            # then there would be no min point in mn_indx list. As a result,
            # len(mn_indx) == 0 and the temporary list (tmp_lst) that stores
            # an updated list of extrms to be studied would be equal to
            # mn_indx_tmp.
            if len(mn_indx) == 0:
                tmp_lst = mn_indx_tmp
            else:
                # An otherwise condition occures when mn_indx is not empty.
                # Hence, certain no. of data in mn_indx_tmp should be selected.
                tmp_lst = mn_indx_tmp[len(mn_indx) + total_cnt_invalid_min:]
                if tmp_lst == []:
                    # There's no more extrms to be assessed.
                    break

            cnt_for_cond = 0
            cond = 0
            # 2nd while loop for max_to_min case: this loop selects proper
            # candidates passing pcp/dt conditions. It also searches for other
            # possible extrms between selected ones and updates the valid ones
            # if needed.
            while cond == 0:
                # 2nd Loop continues until pcp/dt condition is satisfied
                # (cond=1)
                cond, true_indx = pcp_time(tmp_lst[cnt_for_cond],
                                           cl, mx_indx[-1],
                                           ch, pcp_base, dt_base)
                cnt_for_cond += 1
                if cond == 1:
                    # pcp/dt is satisfied.
                    # Next, Checks if the found_min (true_indx) is higher than
                    # the previous valid max.
                    # If it's higher then it's not acceptable and the previous
                    # valid max should be replaced with another valid max with
                    # a higher value which resides somewhere in between the
                    # current valid max and the found_min.
                    if cl[true_indx] >= ch[mx_indx[-1]]:
                        # The last valid max is stored in a temporary variable
                        # so that if this max was replaced with a higher one in
                        # search_bet_extrms func, the search for the next min
                        # be reperformed considering this new max as
                        # the last valid max. In this sense, the last valid min
                        # is not valid anymore and therefore should be deleted.
                        # This deletion is applied in the conditional statement
                        # which comes after search_bet_extrms func in the
                        # following.
                        (total_cnt_invalid_min,
                         total_cnt_invalid_max) =\
                            search_bet_extrms('max_to_min',
                                              total_cnt_invalid_max,
                                              total_cnt_invalid_min, cl, ch,
                                              true_indx)
                        # conditional statement to check if the last valid max
                        # has been replaced or not.
                        if max_updated == 0:
                            del mx_indx[-1]
                            last_extrms_for_debug()
                            # After deletion, the search for max_to_min must
                            # be reperformed; so, 2nd loop for max_to_min case
                            # stops.
                            break
                        else:
                            # search for next min restarts from first element
                            # of tmp_lst; so, cnt_for_cond should be zero
                            cond = 0
                            cnt_for_cond = 0
                            max_updated = 0
                            tmp_lst = mn_indx_tmp[len(mn_indx) +
                                                  total_cnt_invalid_min:]

                    elif cl[true_indx] < ch[mx_indx[-1]]:

                        # Here we have a new found_min which is valid and
                        # added to the list of valid mins.
                        mn_indx.append(true_indx)
                        last_extrms_for_debug()
                        # There could be other min or max before the found
                        # extrms whose number should be taken into account
                        # in counting the the total number of studied
                        # extrms. So, the search is performed to calculate
                        # total_cnt_invalid_min_max
                        (total_cnt_invalid_min,
                         total_cnt_invalid_max) =\
                            search_bet_extrms('max_to_min',
                                              total_cnt_invalid_max,
                                              total_cnt_invalid_min, cl, ch,
                                              true_indx)
                        if max_updated == 0:
                            break
                        else:
                            del mn_indx[-1]
                            last_extrms_for_debug()
                            cond = 0
                            cnt_for_cond = 0
                            max_updated = 0
                            tmp_lst = mn_indx_tmp[len(mn_indx) +
                                                  total_cnt_invalid_min:]
                else:
                    if len(tmp_lst) < 2 or cnt_for_cond >= len(tmp_lst):
                        last_min_not_found = 1
                        # There isn't enough minimum in tmp list for futher
                        # search; hence, in real time, program should wait
                        # for the next min to be identified and continues
                        # the loop. In the backtest phase, extrm identification
                        # is terminated.
                        if real_time_mode == 0:
                            break

            # Total no. of extrms is updated so that condition for
            # (continuation of/stoping) the first while loop could
            # be checked.
            total_no_extrms = (total_cnt_invalid_min + total_cnt_invalid_max +
                               len(mx_indx) + len(mn_indx))

            if last_min_not_found == 1 and real_time_mode == 0:
                break

            cnt_for_switcher += 1

            last_extrms_for_debug()

            # go for next max
            switcher.append(1)

        else:
            # ######################## find next max (min_to_max)
            if len(mx_indx) == 0:
                tmp_lst = mx_indx_tmp
            else:
                tmp_lst = mx_indx_tmp[len(mx_indx) + total_cnt_invalid_max:]
                if tmp_lst == []:
                    break

            cnt_for_cond = 0
            cond = 0
            # 2nd while loop for min_to_max case
            while cond == 0:
                cond, true_indx = pcp_time(tmp_lst[cnt_for_cond],
                                           ch, mn_indx[-1],
                                           cl, pcp_base, dt_base)
                cnt_for_cond += 1

                if cond == 1:
                    if ch[true_indx] <= cl[mn_indx[-1]]:
                        (total_cnt_invalid_min,
                         total_cnt_invalid_max) =\
                            search_bet_extrms('min_to_max',
                                              total_cnt_invalid_max,
                                              total_cnt_invalid_min, cl, ch,
                                              true_indx)
                        if min_updated == 0:
                            del mn_indx[-1]
                            last_extrms_for_debug()
                            break
                        else:
                            cond = 0
                            cnt_for_cond = 0
                            min_updated = 0
                            tmp_lst = mx_indx_tmp[len(mx_indx) +
                                                  total_cnt_invalid_max:]

                    elif ch[true_indx] > cl[mn_indx[-1]]:
                        # Here we have a new true max.
                        mx_indx.append(true_indx)
                        last_extrms_for_debug()
                        # calculating total_cnt_invalid_min_max
                        (total_cnt_invalid_min,
                         total_cnt_invalid_max) =\
                            search_bet_extrms('min_to_max',
                                              total_cnt_invalid_max,
                                              total_cnt_invalid_min, cl, ch,
                                              true_indx)
                        if min_updated == 0:
                            break
                        else:
                            del mx_indx[-1]
                            last_extrms_for_debug()
                            cond = 0
                            cnt_for_cond = 0
                            min_updated = 0
                            tmp_lst = mx_indx_tmp[len(mx_indx) +
                                                  total_cnt_invalid_max:]

                else:
                    if len(tmp_lst) < 2 or cnt_for_cond >= len(tmp_lst):
                        last_max_not_found = 1
                        if real_time_mode == 0:
                            break

            total_no_extrms = (total_cnt_invalid_min + total_cnt_invalid_max +
                               len(mx_indx) + len(mn_indx))

            if last_max_not_found == 1 and real_time_mode == 0:
                break

            cnt_for_switcher += 1

            last_extrms_for_debug()

            # go for next min
            switcher.append(0)

    return filter_extrms_based_on_time_and_pcp

