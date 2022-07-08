from itertools import chain

import copy

global PCPBase, dtBase


def ValidExms(cl, ch, LRC, PCPBase, dtBase, RT):
    ''' Finds maximums and minimums of price in a time range.'''
    global mnIndx, mxIndx, mxUpdated, mnUpdated

    mxUpdated = 0
    mnUpdated = 0

    mxIndx = []
    mnIndx = []

    LRCExms(cl, ch, LRC)
    (unStudMX_Indx, unStudMN_Indx) = PCPDtExms(cl, ch, PCPBase, dtBase, RT)

    return (mxIndx, mnIndx, unStudMX_Indx, unStudMN_Indx)


def LRCExms(cl, ch, LRC):
    '''This function selects Exms satisfying lrc condition.'''
    global ND, mxIndxTmp, mnIndxTmp, SR_Indx
    # initializing the lists for Exms indexes
    mxIndxTmp = []
    mnIndxTmp = []
    SR_Indx = []
    # no_data: No. of total candles
    ND = len(cl)
    for i in range(LRC, ND-LRC):
        # tmp1: temp list initialization for candle low
        tmp1 = []
        # tmp2: temp list initialization for candle high
        tmp2 = []
        # Traversing over a candle to both left and right sides w.r.t. lrc
        # and selecting appropriate ones
        for j in chain(range(i-LRC, i), range(i+1, i+LRC+1)):
            if cl[i] <= cl[j]:
                tmp1.append(1)
            else:
                tmp1.append(0)

            if ch[i] >= ch[j]:
                tmp2.append(1)
            else:
                tmp2.append(0)

        if all(tmp1) and all(tmp2):
            SR_Indx.append(i)
            cnt = LRC + 1
            cl_score = 0
            ch_score = 0
            while cnt <= i and i+cnt+1 < ND:
                for k in chain(range(i-cnt, i), range(i+1, i+cnt+1)):
                    if cl[i] <= cl[k]:
                        cl_score += 1
                    elif ch[i] >= ch[k]:
                        ch_score += 1

                if cl_score > ch_score:
                    mnIndxTmp.append(i)
                    break
                elif cl_score < ch_score:
                    mxIndxTmp.append(i)
                    break
                elif cl_score == ch_score:
                    cnt += 1
                    continue

            continue

        # If this cond. holds, it means that minimums of all candles around
        # candle No. j are higher than min of candle j
        if all(tmp1):
            mnIndxTmp.append(i)

        if all(tmp2):
            mxIndxTmp.append(i)

    mnND = len(mnIndxTmp)
    mxND = len(mxIndxTmp)
    # nd: Total No. of selected Exms based on lrc that have potential to be
    # max or min
    ND = mxND + mnND

    return mxIndxTmp, mnIndxTmp


def chkPCPDt(indx2, c2, indx1, c1, PCPBase, DT_Base):
    ''' Performs comparison for each two consecutive Exm pairs
    (a max and the preceeding min or a min and the preceeding max)
    based on the condition of price change percentage (pcp) and elapsed
    time (dt) and decides on the suitability of the Exm pairs
    (cond = 1 if suitable).
    In calculating pcp, always the 1st Exm (no matter max or min)
    is subtracted from the 2nd one and result is divided by the 1st one.'''

    pcp = 100*abs(c2[indx2] - c1[indx1])/c1[indx1]
    dt = abs(indx2 - indx1)

    cond = 0

    if 0.5*PCPBase < pcp < PCPBase and dt >= DT_Base:
        cond = 1
    elif pcp >= PCPBase:
        cond = 1

    return cond, indx2


def ExmsBetValids(state, allInvalMX, allInvalMN, cl, ch, trueIndx):
    '''
    Seeks whether there are any further Exms between two consecutive
    valid min/max or max/min pairs. There are two possibilities for
    inputs:

    State = max_to_min --> search for Exms bet. the 1st valid Exm
    (MAX) and the 2nd valid one (MIN)

    State = min_to_max --> search for Exms bet. the 1st valid Exm (MIN)
    and the 2nd valid one (MAX)
    '''
    global mxUpdated, mnUpdated

    if state == 'max_to_min':
        # If the following condition holds, there are at least one candle
        # between the two consecutive valid max and min which could represent
        # an Exm.
        if mnIndx != [] and (mxIndx[-1] + 1) <= mnIndx[-1]:
            UB_Range = mnIndx[-1]
        elif mnIndx == [] or (mxIndx[-1] + 1) > mnIndx[-1]:
            # Otherwise, {mx_indx[-1] + 1} could be equal to mn_indx[-1]
            # (and not less than it since it's nonsense); hence,
            # there would be no Exm at all between the two consecutive
            # valid max and min.
            UB_Range = trueIndx

        # range between two valid Exms where search is performed
        lst = range(mxIndx[-1] + 1, UB_Range)
        for item in lst:
            if item in mxIndxTmp and ch[item] <= ch[mxIndx[-1]]:
                # In this case, the newly found max is lower than the
                # last valid max (mx_indx[-1]); hence, search only
                # indicates that there's another max in bet. two valid
                # MAX and MIN and it should be taken into account and
                # cnt_max is updated.
                allInvalMX += 1
            elif item in mxIndxTmp and ch[item] > ch[mxIndx[-1]]:
                # mx_indx[-1] = mx_indx_tmp[total_cnt_invalid_max
                #                           + len(mx_indx)]
                mxIndx[-1] = item
                lastExmsForDebug()
                allInvalMX += 1
                mxUpdated = 1
                break
            # elif item in mn_indx_tmp and cl[item] < cl[true_indx]:
            #     min_should_be_updated = 1
            #     break
            elif item in mnIndxTmp:
                allInvalMN += 1

    elif state == 'min_to_max':
        if mxIndx != [] and (mnIndx[-1] + 1) <= mxIndx[-1]:
            UB_Range = mxIndx[-1]
        elif mxIndx == [] or (mnIndx[-1] + 1) > mxIndx[-1]:
            UB_Range = trueIndx

        lst = range(mnIndx[-1] + 1, UB_Range)
        for item in lst:
            if item in mnIndxTmp and cl[item] >= cl[mnIndx[-1]]:
                allInvalMN += 1
            elif item in mnIndxTmp and cl[item] < cl[mnIndx[-1]]:
                # mn_indx[-1] = mn_indx_tmp[total_cnt_invalid_min
                #                           + len(mn_indx)]
                mnIndx[-1] = item
                lastExmsForDebug()
                allInvalMN += 1
                mnUpdated = 1
                break
            # elif item in mx_indx_tmp and ch[item] > ch[true_indx]:
            #     max_should_be_updated = 1
            #     break
            elif item in mxIndxTmp:
                allInvalMX += 1

    return allInvalMN, allInvalMX


def lastExmsForDebug():
    ''' This func stores the last updated min and max for easier debugging.
    It doesn't affect the calculation process in any sense.'''
    global lastMN, lastMX
    # mn_last and mx_last store the last two items of mn_indx and
    # mx_indx. They're only for better visual track of valid Exms on
    # the left side debugger window.
    if len(mnIndx) != 0:
        lastMN = mnIndx[-1]
    else:
        lastMN = 0

    if len(mxIndx) != 0:
        lastMX = mxIndx[-1]
    else:
        lastMX = 0

    return lastMN, lastMX


def PCPDtExms(cl, ch, PCPBase, DT_Base, RTM):
    ''' Filters previously selected Exms based on elapsed time
    and price change percentage. The resulting Exms would be vaild ones.'''

    global mxUpdated, mnUpdated

    # TERMS AND DEFINITIONS

    # switcher: list to save counter(cnt) values (cnt is 0 or 1) to switch
    # between min and max seeking
    switcher = []
    # cnt_for_switcher --> counter for switcher. If cnt_for_switcher = 0 the
    # first Exm is max (1st element of mx_indx_tmp) and search is
    # performed for finding the next min. If cnt_for_switcher = 1 the first
    # Exm is min (1st element of mn_indx_tmp) and search is
    # performed for finding the next max.
    switchCnt = 0
    # total_cnt_invalid_min: counter for total No. of invalid min
    allInvalMN = 0
    # total_cnt_invalid_max: counter for total No. of invalid max
    allInvalMX = 0
    # total_no_Exms: counter for total No. of valid and invalid Exms
    allExms = 0

    def switcherInitConf(switcher):
        ''' Initial config for switcher '''

        # If 1st Exm is max (mx_indx_tmp[0] < mn_indx_tmp[0]) then 1st
        # element of switcher would be 0.
        if mxIndxTmp[0] < mnIndxTmp[0]:
            switcher.append(0)
        # This max would also be 1st valid max and is added to mx_indx list.
            mxIndx.append(mxIndxTmp[0])
        # An otherwise condition holds for 1st valid min
        else:
            switcher.append(1)
            mnIndx.append(mnIndxTmp[0])

    switcherInitConf(switcher)

    lastExmsForDebug()

    unfoundLastMX = 0
    unfoundLastMN = 0

    # 1st while loop checks if counter for total No. of valid Exms
    # (total_no_Exms) is lower than total No. of Exms (nd)

    # 1st while loop: checks if total no. of found Exms is lower than total
    # no. of existing Exms (valid and invalid)
    while allExms < ND:
        if switcher[switchCnt] == 0:
            # ######################## find next min (max_to_min)

            # At the beginning of the seeking process, if 1st Exm is a
            # max (which has been assigned in switcher_initial_config func)
            # then there would be no min point in mn_indx list. As a result,
            # len(mn_indx) == 0 and the temporary list (tmp_lst) that stores
            # an updated list of Exms to be studied would be equal to
            # mn_indx_tmp.
            if len(mnIndx) == 0:
                tmpLst = mnIndxTmp
            else:
                # An otherwise condition occures when mn_indx is not empty.
                # Hence, certain no. of data in mn_indx_tmp should be selected.
                tmpLst = mnIndxTmp[len(mnIndx) + allInvalMN:]
                if tmpLst == []:
                    # There's no more Exms to be assessed.
                    break

            condCnt = 0
            cond = 0
            # 2nd while loop for max_to_min case: this loop selects proper
            # candidates passing pcp/dt conditions. It also searches for other
            # possible Exms between selected ones and updates the valid ones
            # if needed.
            while cond == 0:
                # 2nd Loop continues until pcp/dt condition is satisfied
                # (cond=1)
                if tmpLst == []:
                    break

                (cond, trueIndx) =\
                    chkPCPDt(
                        tmpLst[condCnt],
                        cl, mxIndx[-1],
                        ch, PCPBase, DT_Base)
                condCnt += 1
                if cond == 1:
                    # pcp/dt is satisfied.
                    # Next, Checks if the found_min (true_indx) is higher than
                    # the previous valid max.
                    # If it's higher then it's not acceptable and the previous
                    # valid max should be replaced with another valid max with
                    # a higher value which resides somewhere in between the
                    # current valid max and the found_min.
                    if cl[trueIndx] >= ch[mxIndx[-1]]:
                        # The last valid max is stored in a temporary variable
                        # so that if this max was replaced with a higher one in
                        # search_bet_Exms func, the search for the next min
                        # be reperformed considering this new max as
                        # the last valid max. In this sense, the last valid min
                        # is not valid anymore and therefore should be deleted.
                        # This deletion is applied in the conditional statement
                        # which comes after search_bet_Exms func in the
                        # following.
                        (allInvalMN, allInvalMX) =\
                            ExmsBetValids('max_to_min', allInvalMX,
                                            allInvalMN, cl, ch, trueIndx)
                        # conditional statement to check if the last valid max
                        # has been replaced or not.
                        if mxUpdated == 0:
                            del mxIndx[-1]
                            lastExmsForDebug()
                            # After deletion, the search for max_to_min must
                            # be reperformed; so, 2nd loop for max_to_min case
                            # stops.
                            break
                        else:
                            # search for next min restarts from first element
                            # of tmp_lst; so, cnt_for_cond should be zero
                            cond = 0
                            condCnt = 0
                            mxUpdated = 0
                            tmpLst = mnIndxTmp[len(mnIndx) + allInvalMN:]

                    elif cl[trueIndx] < ch[mxIndx[-1]]:

                        # Here we have a new found_min which is valid and
                        # added to the list of valid mins.
                        mnIndx.append(trueIndx)
                        lastExmsForDebug()
                        # There could be other min or max before the found
                        # Exms whose number should be taken into account
                        # in counting the the total number of studied
                        # Exms. So, the search is performed to calculate
                        # total_cnt_invalid_min_max
                        (allInvalMN, allInvalMX) =\
                            ExmsBetValids('max_to_min', allInvalMX,
                                            allInvalMN, cl, ch, trueIndx)
                        if mxUpdated == 0:
                            break
                        else:
                            del mnIndx[-1]
                            lastExmsForDebug()
                            cond = 0
                            condCnt = 0
                            mxUpdated = 0
                            tmpLst = mnIndxTmp[len(mnIndx) + allInvalMN:]
                else:
                    if len(tmpLst) < 2 or condCnt >= len(tmpLst):
                        unfoundLastMN = 1
                        # There isn't enough minimum in tmp list for futher
                        # search; hence, in real time, program should wait
                        # for the next min to be identified and continues
                        # the loop. In the backtest phase, Exm identification
                        # is terminated.
                        if RTM == 0:
                            break

            # Total no. of Exms is updated so that condition for
            # (continuation of/stoping) the first while loop could
            # be checked.
            allExms = (allInvalMN + allInvalMX + len(mxIndx) + len(mnIndx))

            if unfoundLastMN == 1 and RTM == 0:
                break

            switchCnt += 1

            lastExmsForDebug()

            # go for next max
            switcher.append(1)

        else:
            # ######################## find next max (min_to_max)
            if len(mxIndx) == 0:
                tmpLst = mxIndxTmp
            else:
                tmpLst = mxIndxTmp[len(mxIndx) + allInvalMX:]
                if tmpLst == []:
                    break

            condCnt = 0
            cond = 0
            # 2nd while loop for min_to_max case
            while cond == 0:
                if tmpLst == []:
                    break

                (cond, trueIndx) = chkPCPDt(tmpLst[condCnt], ch, mnIndx[-1],
                                             cl, PCPBase, DT_Base)
                condCnt += 1

                if cond == 1:
                    if ch[trueIndx] <= cl[mnIndx[-1]]:

                        (allInvalMN, allInvalMX) =\
                            ExmsBetValids('min_to_max', allInvalMX,
                                            allInvalMN, cl, ch, trueIndx)

                        if mnUpdated == 0:
                            del mnIndx[-1]
                            lastExmsForDebug()
                            break
                        else:
                            cond = 0
                            condCnt = 0
                            mnUpdated = 0
                            tmpLst = mxIndxTmp[len(mxIndx) + allInvalMX:]

                    elif ch[trueIndx] > cl[mnIndx[-1]]:
                        # Here we have a new true max.
                        mxIndx.append(trueIndx)
                        lastExmsForDebug()
                        # calculating total_cnt_invalid_min_max
                        (allInvalMN, allInvalMX) =\
                            ExmsBetValids('min_to_max', allInvalMX,
                                            allInvalMN, cl, ch, trueIndx)

                        if mnUpdated == 0:
                            break
                        else:
                            del mxIndx[-1]
                            lastExmsForDebug()
                            cond = 0
                            condCnt = 0
                            mnUpdated = 0
                            tmpLst = mxIndxTmp[len(mxIndx) + allInvalMX:]

                else:
                    if len(tmpLst) < 2 or condCnt >= len(tmpLst):
                        unfoundLastMX = 1
                        if RTM == 0:
                            break

            allExms = (allInvalMN + allInvalMX + len(mxIndx) + len(mnIndx))

            if unfoundLastMX == 1 and RTM == 0:
                break

            switchCnt += 1

            lastExmsForDebug()

            # go for next min
            switcher.append(0)

    # The following condition checks if there exists any remaining Exms
    # in mx_indx_tmp and mn_indx_tmp lists that are not yet identified as
    # valid/invalid Exms. These Exms would be simply based on LRC
    # search and used to define the latest market condition in terms of
    # trend and pcp of Exms relative to each other.
    if mxIndx[-1] < mxIndxTmp[-1] or mnIndx[-1] < mnIndxTmp[-1]:
        tmp1 = mxIndx[-1]
        tmp2 = mxIndxTmp.index(tmp1)
        tmp3 = mnIndx[-1]
        tmp4 = mnIndxTmp.index(tmp3)
        unStudMX_Indx = mxIndxTmp[tmp2 + 1:]
        unStudMN_Indx = mnIndxTmp[tmp4 + 1:]

        return (unStudMX_Indx, unStudMN_Indx)
    else:
        return 0, 0


def filtOrOrdExms(ETM, RTM,
                                   cl, ch, LRC, PCP, DTBase):
    '''This function returns Exm indexes for arbitrary
    size trends (typically daily and hourly time frames).'''

    if ETM == 0:
        (mxIndx, mnIndx) = LRCExms(cl, ch, LRC)
    elif ETM == 1:
        (mxIndx, mnIndx, unStudMX_Indx,
         unStudMN_Indx) = ValidExms(cl, ch, LRC, PCP, DTBase, RTM)

    return (mxIndx, mnIndx, unStudMX_Indx, unStudMN_Indx)


def nondimPriceCalc(price, all_time_max, all_time_min):
    '''This function normalizes any price value to a range from zero
    to one. x is an arbitrary number typically representing a candle high
    or low. ch and cl are vectors of all candles' high and
    low, respectively.'''

    nondim_price = (price - all_time_min)/(all_time_max - all_time_min)

    return nondim_price


def HSR(cl, ch, mnd, backstep, asset, timeframe, dataPath, SR_File):
    '''This function calculates horizontal supports and resistence levels based
    on daily candlesticks. To do so, lrc is decremented from a large number
    such as 100 to lower values. After each decrimentation, the normalized
    distance between previous s/r and the new one is measured. If this value
    is greater than a predetermined offset (such as 0.01) then the s/r in
    qustion is valid.'''
    ch = ch[:-backstep]
    cl = cl[:-backstep]

    atmx = max(ch)
    atmn = min(cl)

    lrc_init = 80
    lrc_final = 30
    lrc = range(lrc_init, lrc_final, -1)
    sr = []

    def dist(el1, el2):
        d1 = nondimPriceCalc(el1, atmx, atmn)
        d2 = nondimPriceCalc(el2, atmx, atmn)
        # d: distance between d1 and d2
        d = abs(d1 - d2)

        return d

    # Definition:
    #  occur: The occurrence of s/r based on lrc values (for each lrc value
    #  we could have new or repeated sr).

    # At first, lrc has an initial value (lrc_init) and there is an initial sr
    # for this lrc_init. Since initial sr is based on a large lrc value
    # (for instance, lrc_init=30 or 100), it is indeed a valid sr (actually it
    # has to be a valid one since it's the first occurance of an sr) and occur
    # is set to one before lrc loop starts (occur=1).
    # As lrc decreases, we'd have new s/r occurrence(s) which could be valid
    # or invalid (by default all new sr are invalid unless otherwise proven by
    # nondimensional distance criterion which will be explained further).
    # Example of a valid sr with occur=1 is a tuple like (m, 1) which states
    # that candle number m is a true support/resistence.
    # As regards unidentified sr, we'd have sth like (n, 0) for n>m and the
    # validity of this sr has yet to be determined.

    occur = 1
    # lrc loop
    for item in lrc:
        # sr_mx, sr_mn: The lists of found sr
        # Some sr are related to maximum points and some to minimum.
        sr_mx, sr_mn = LRCExms(cl, ch, item)[0:2]
        # Obviously, if sr lists are empy loop continues to the next lrc.
        if sr_mx == [] and sr_mn == []:
            continue

        # A deep copy of sr_mx and sr_mn is needed so that the found sr
        # are not affected in the removal process which is explained next.
        sr_mx_copy = copy.copy(sr_mx)
        sr_mn_copy = copy.copy(sr_mn)

        # Duplicate sr removal process: If the new found sr has been
        # previously studied and its (in)validity is known already then it
        # should be removed from the new lists of found sr.
        for i in sr_mx_copy:
            for j in sr:
                if i == j[0]:
                    # The duplicate sr is removed
                    sr_mx.remove(i)

        for i in sr_mn_copy:
            for j in sr:
                if i == j[0]:
                    sr_mn.remove(i)

        # The deep copies are of no use anymore.
        del sr_mx_copy, sr_mn_copy

        # if any of sr lists is not empty after removal process calculation
        # proceeds.
        if sr_mx != [] or sr_mn != []:
            # The case of occur=1 only holds at the beginning of sr finding
            # process for lrc_init when no sr is identified yet. Later on,
            # we'd have to assume occur=0 unless otherwise proven. Hence, we
            # should if are at the beginning of the lrc loop or not. The
            # following condition is only met when item=lrc[0]
            if occur == 1:
                # The tuples ((i, ch[i]), occur) (i is the candle number) are
                # derived from values in sr_mx and sr_mn and added to sr.
                sr_mx = [[i, ch[i], occur] for i in sr_mx]
                sr_mn = [[i, cl[i], occur] for i in sr_mn]
                sr = sr_mx + sr_mn

                sr_mx = []
                sr_mn = []
                # sr is sorted based on the 2nd value in the 1st tuple
                # (which is cl[i] or ch[i]) in a descending order
                sr.sort(key=lambda x: -x[1])
                # occur is set to 0 so that loop continues to find sr for
                # further lrc values smaller than lrc_init

                m = len(sr)
                # i, j: counters
                i = 0
                j = 1
                del_indx = []
                while m > 1 and j < m:
                    d = dist(sr[i][1], sr[j][1])
                    if d < mnd:
                        del_indx.append(j)
                        j += 1
                    else:
                        i = j
                        j += 1

                i = 0
                cnt = 0
                while i < len(del_indx):
                    del sr[del_indx[i] - cnt]
                    i += 1
                    cnt += 1

                occur = 0
            # If sr =! 1, it means that sr has been assigned with some values
            # and is not empty anymore. So, as stated before, occur is zero
            # and the process continues until new sr is identified and possibly
            # validated.
            else:
                # The tuples are created.
                sr_mx = [[i, ch[i], occur] for i in sr_mx]
                sr_mn = [[i, cl[i], occur] for i in sr_mn]
                sr += sr_mx + sr_mn

                sr_mx = []
                sr_mn = []
                # sr is sorted
                sr.sort(key=lambda x: -x[1])
                # Now, we have a sorted list of both valid (occur=1) and
                # invalid (occur=0) sr. The suitability of unidentified
                # ones is decided based on a distance comparison process which
                # is as follows:

                # The nondimensional distance between every pair of valid and
                # invalid sr should be greater than a predetermined number
                # (Roughly 0.01~0.05) so as to change the invalid one to valid.
                n = len(sr)
                # i0: list of indexes for occur=0 in sr list
                # i1: list of indexes for occur=1 in sr list
                i0 = []
                i1 = []
                for item in range(n):
                    if sr[item][2] == 0:
                        i0.append(item)
                    else:
                        i1.append(item)

                i = 0
                j = 0
                # sr_s_lst: list for starting part of sr list if available
                # sr_e_lst: list for ending part of sr list if available
                sr_s_lst = []
                sr_e_lst = []
                if i1[0] > 0 and i1[-1] < n-1:
                    sr_s_lst = sr[0:i1[0]+1]
                    sr_e_lst = sr[i1[-1]:n+1]
                    sr = sr[i1[0]:i1[-1]+1]
                elif i1[0] > 0:
                    sr_s_lst = sr[0:i1[0]+1]
                    sr = sr[i1[0]:]
                elif i1[-1] < n-1:
                    sr_e_lst = sr[i1[-1]:n+1]
                    sr = sr[0:i1[-1]+1]

                def compare(array):
                    '''This function checks the validity of sr elements.
                    Input array could be sr, sr_s_lst, and sr_e_lst.'''
                    l = len(array)
                    if array != []:
                        if array == sr_s_lst:
                            i = l - 1
                            j = i - 1
                            while j >= 0:
                                d = dist(array[i][1], array[j][1])
                                if d >= mnd:
                                    array[j][2] = 1
                                    i = j
                                    j -= 1
                                else:
                                    j -= 1
                                    continue
                        elif array == sr_e_lst:
                            i = 0
                            j = i + 1
                            while j < l:
                                d = dist(array[i][1], array[j][1])
                                if d >= mnd:
                                    array[j][2] = 1
                                    i = j
                                    j = i + 1
                                else:
                                    j += 1
                                    continue
                        elif array == sr and len(array) > 1:
                            p = 0
                            i = i1[p] - i1[0]
                            j = i1[p+1] - i1[0]
                            k = i + 1
                            while j < len(array):
                                while k < j:
                                    d1 = dist(array[i][1], array[k][1])
                                    d2 = dist(array[j][1], array[k][1])
                                    if d1 >= mnd and d2 >= mnd:
                                        array[k][2] = 1
                                        i = k
                                        k = i + 1
                                    else:
                                        # i = k
                                        k += 1
                                p += 1
                                i = i1[p] - i1[0]
                                if p + 1 < len(i1):
                                    j = i1[p+1] - i1[0]
                                else:
                                    break
                                k = i + 1

                    return array

                srs = compare(sr_s_lst)
                sr = compare(sr)
                sre = compare(sr_e_lst)
                sr = srs[0:-1] + sr + sre[1:]

    sr = [i for i in sr if i[2] != 0]

    with open(dataPath + SR_File, 'w') as f:
        for item in sr:
            f.write("%s\n" % item[1])

    return sr


def identifyNewHorizontalSupportAndResistencelevelsInRealTime():
    '''This function utilizes the output of the 'sr_identification' function
    as a base for identifying the possibly new sr in real time.'''
    pass


def PP(ch, cl, cc):
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


def calcVarCoeff():
    '''This function determines the possible correlation between multiple
    assets. Calculations are based on time series comparison and not a single
    varibale.'''
    pass


def alertMarketSessions():
    '''This function sends alerts for specific market openning times in
    New York, London, Berlin, Tokyo, and Hong Kong. It also notifies the
    previous market close price of the pertinent asset in aforementioned
    locations.'''
    pass


def identPriceBreak():
    ''' Identifies possible breakouts in p. '''
    pass


def identVolumeBreakout():
    ''' Identifies possible breakouts in v. '''
    pass


def identRetest():
    ''' Identifies possible Retest on supports and resistence levels. '''
    pass


def identPinBar():
    ''' Identifies possible pin bar candle. '''
    pass


def identStopHunt():
    ''' Detects possible stop hunting areas for possible enterance or setting
    better stop loss. '''
    pass


def chkLiquidity():
    ''' Checks markets' liquidity, volume, and number of trades to select
    the proper base time frame.
    '''
    pass
