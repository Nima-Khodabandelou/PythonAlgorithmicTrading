def extrms_based_on_neighboring_candles3(cl, ch, lrc):
    ''' Finds maximums and minimums of price in a time range
    (simpler approach with smaller code).'''
    # initializing the lists for extremums indexes
    mx_indx_tmp = []
    mx_price = []
    mn_indx_tmp = []
    mn_price = []
    mx_indx = []
    mn_indx = []
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

        # if all(tmp1) and all(tmp2):
        #     extrm_s_r_indx.append(i)
        #     extrm_s_r_price.append(cl[i])
        #     extrm_s_r_price.append(ch[i])
        #     continue

        if all(tmp1):
            mn_indx_tmp.append(i)
            mn_price.append(cl[i])

        if all(tmp2):
            mx_indx_tmp.append(i)
            mx_price.append(ch[i])

    def filter_extrms_based_on_time_and_pcp():
        ''' Identifies extremums based on elapsed time and price change
        percentage.'''
        # switcher: list to save cnt values (cnt is 0 or 1)
        switcher = []
        if mx_indx_tmp[0] < mn_indx_tmp[0]:
            # cnt: switcher for searching for max or min. If cnt=0 the first
            # extrm is max and search for min
            switcher.append(0)
            mx_indx.append(mx_indx_tmp[0])
        else:
            switcher.append(1)
            mn_indx.append(mn_indx_tmp[0])

        def pcp_time(indx2, c2, indx1, c1):
            ''' Calculates price change percentage (pcp), time elapsed (dt),
            and the condition based on which we determine the suitability of
            extrm under study for each extrm pairs.'''
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
 
        # The predefined minimum pcp and dt for every two consecutive extrms
        # to be valid
        pcp_base = 10
        dt_base = 10

        nd_mn = len(mn_indx_tmp)
        nd_mx = len(mx_indx_tmp)
        nd = nd_mx + nd_mn
        # i: counter for all data in mn_indx_tmp and mx_indx_tmp
        i = 0
        # j: counter for 
        j = i
        cnt_min = 0
        cnt_max = 0
        cnt3 = 0
        total_cnt_min_max = 0
        total_cnt_min = 0
        total_cnt_max = 0
        total_no_extrms = 0
        while total_no_extrms < nd:
            if switcher[cnt3] == 0:
                # ###################################### next min
                if len(mn_indx) == 0:
                    second1 = mn_indx_tmp
                else:
                    second1 = mn_indx_tmp[mn_indx_tmp.index(mn_indx[-1])+1+cnt_min:]

                second2 = cl
                first1 = mx_indx
                first2 = ch
                cond = 0
                while cond == 0:
                    cond, true_indx = pcp_time(second1[j], second2, first1[-1],
                                               first2)
                    j += 1
                    if cond == 1:
                        # check if the found min is lower than previous true max
                        # if it's higher then not acceptable
                        if cl[true_indx] > ch[mx_indx[-1]]:
                            mx_indx[-1] = mx_indx_tmp[total_no_extrms - (j-1) - total_cnt_min]
                            total_cnt_max += 1
                            cond = 0
                        # and if it's lower then the result is normal
                        elif cl[true_indx] < ch[mx_indx[-1]]:
                            mn_indx.append(true_indx)
                            break
                # now we have a new min
                # There could be other min or max before the found extrm whose
                # number should be taken into account in counting the total
                # number of studied extrms, i.e. i

                cnt_min = 0
                cnt_max = 0
                lst = range(mx_indx[-1] + 1, mn_indx[-1])
                for item in lst:
                    if item in mx_indx_tmp and ch[item] < ch[mx_indx[-1]]:
                        cnt_max += 1
                    elif item in mx_indx_tmp and ch[item] > ch[mx_indx[-1]]:
                        mx_indx[-1] = mx_indx_tmp[total_cnt_max + len(mx_indx)]
                        cnt_max += 1
                    elif item in mn_indx_tmp:
                        cnt_min += 1

                total_cnt_min += cnt_min
                total_cnt_max += cnt_max
                total_cnt_min_max += cnt_max + cnt_min
                total_no_extrms = total_cnt_min_max + len(mx_indx) + len(mn_indx)

                tmp = cnt_min + cnt_max + len(mx_indx) + len(mn_indx)
                # j for next max
                j = tmp - len(mn_indx) - cnt_min - 1
                cnt3 += 1
                switcher.append(1)

            else:
                # #################################### next max
                if len(mx_indx) == 0:
                    second1 = mx_indx_tmp
                else:
                    second1 = mx_indx_tmp[mx_indx_tmp.index(mx_indx[-1])+1+cnt_max:]

                second2 = ch
                first1 = mn_indx
                first2 = cl
                cond = 0
                while cond == 0:
                    cond, true_indx = pcp_time(second1[j], second2, first1[-1],
                                               first2)
                    j += 1

                    if cond == 1:
                        if ch[true_indx] < cl[mn_indx[-1]]:
                            mn_indx[-1] = mn_indx_tmp[total_no_extrms - (j-1) - total_cnt_max]
                            total_cnt_min += 1
                            cond = 0
                        elif ch[true_indx] > cl[mn_indx[-1]]:
                            mx_indx.append(true_indx)
                            break
                    # now we have the max.
                    # we search bet this max and previous min for further min
                    # and max that didn't satidfy cond

                cnt_min = 0
                cnt_max = 0
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
                total_no_extrms = total_cnt_min_max + len(mx_indx) + len(mn_indx)

                tmp = cnt_min + cnt_max + len(mx_indx) + len(mn_indx)
                # j for next min
                j = tmp - len(mx_indx) - cnt_max - 1
                cnt3 += 1
                switcher.append(0)

        return filter_extrms_based_on_time_and_pcp

    filter_extrms_based_on_time_and_pcp()

    return mx_indx, mn_indx


def extrms_based_on_neighboring_candles4(cl, ch, lrc):
    ''' Finds maximums and minimums of price in a time range
    (better naming convention).'''
    # initializing the lists for extremums indexes
    all_max_indexs_based_on_lrc = []
    all_min_indexs_based_on_lrc = []

    desired_max_indexs_based_on_pcp_dt = []
    desired_min_indexs_based_on_pcp_dt = []
    # lrc defines the number of left or right neighboring candles for
    # extremum comparison,i.e. if for instance lrc=5 and a specific
    # candle's high is higher than 5 candles on the leftside and 5 candles on
    # the rightside then that candle would be considered as a maximum extrm.
    total_no_of_data = len(cl)
    for i in range(lrc, total_no_of_data-lrc):
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

        # if all(tmp1) and all(tmp2):
        #     extrm_s_r_indx.append(i)
        #     extrm_s_r_price.append(cl[i])
        #     extrm_s_r_price.append(ch[i])
        #     continue

        if all(tmp1):
            all_min_indexs_based_on_lrc.append(i)

        if all(tmp2):
            all_max_indexs_based_on_lrc.append(i)

    def filter_extrms_based_on_time_and_pcp():
        ''' Identifies extremums based on elapsed time and price change
        percentage.'''
        # switcher: list to save cnt values (cnt is 0 or 1)
        switcher = []
        if all_max_indexs_based_on_lrc[0] < all_min_indexs_based_on_lrc[0]:
            # cnt: switcher for searching for max or min. If cnt=0 the first
            # extrm is max and search for min
            switcher.append(0)

            desired_max_indexs_based_on_pcp_dt.append(
                all_max_indexs_based_on_lrc[0])
        else:
            switcher.append(1)
            desired_min_indexs_based_on_pcp_dt\
                .append(all_min_indexs_based_on_lrc[0])

        def pcp_time(indx2, c2, indx1, c1):
            ''' Calculates price change percentage (pcp), time elapsed (dt),
            and the condition based on which we determine the suitability of
            extrm under study for each extrm pairs.'''
            pcp = 100*abs(c2[indx2] - c1[indx1])/c1[indx1]
            dt = abs(indx2 - indx1)

            if pcp < min_desired_pcp and dt < min_desired_dt:
                condition = 0
            elif pcp < min_desired_pcp and dt >= min_desired_dt:
                condition = 1
            elif pcp >= min_desired_pcp and dt < min_desired_dt:
                condition = 1
            elif pcp >= min_desired_pcp and dt >= min_desired_dt:
                condition = 1

            return condition, indx2
 
        # The predefined minimum pcp and dt for every two consecutive extrms
        # to be valid
        min_desired_pcp = 10
        min_desired_dt = 10

        nd_mn = len(all_min_indexs_based_on_lrc)
        nd_mx = len(all_max_indexs_based_on_lrc)
        total_no_extrm_based_on_lrc = nd_mx + nd_mn
        
        counter_for_pcp_dt_calc = 0
        improper_min_counter = 0
        improper_max_counter = 0
        switcher_counter = 0
        total_improper_extrm_counter = 0
        total_no_extrms = 0
        
        while total_no_extrms < total_no_extrm_based_on_lrc:
            if switcher[switcher_counter] == 0:
                # next min
                if len(desired_min_indexs_based_on_pcp_dt) == 0:
                    second1 = all_min_indexs_based_on_lrc
                else:
                    second1 = all_min_indexs_based_on_lrc[
                              all_min_indexs_based_on_lrc.index
                              (desired_min_indexs_based_on_pcp_dt[-1]) +
                              1 +
                              improper_min_counter:]

                condition = 0
                while condition == 0:
                    condition, true_indx = pcp_time(
                        second1[counter_for_pcp_dt_calc],
                        cl,
                        desired_max_indexs_based_on_pcp_dt[-1],
                        ch)
    
                    counter_for_pcp_dt_calc += 1
                # check if the found min is lower than previous true max
                # if it's higher then not acceptable
                if cl[true_indx] > ch[desired_max_indexs_based_on_pcp_dt[-1]]:
                    desired_max_indexs_based_on_pcp_dt[-1] =\
                     all_max_indexs_based_on_lrc[counter_for_pcp_dt_calc-2]
                # and if it's lower then the result is normal
                elif (cl[true_indx] <
                      ch[desired_max_indexs_based_on_pcp_dt[-1]]):
                    desired_min_indexs_based_on_pcp_dt.append(true_indx)
                # now we have a new min
                # There could be other min or max before the found extrm whose
                # number should be taken into account in counting the total
                # number of studied extrms, i.e. i

                improper_min_counter = 0
                improper_max_counter = 0

                lst = range(desired_max_indexs_based_on_pcp_dt[-1] + 1,
                            desired_min_indexs_based_on_pcp_dt[-1])

                for item in lst:
                    if item in all_min_indexs_based_on_lrc:
                        improper_min_counter += 1
                    elif item in all_max_indexs_based_on_lrc:
                        improper_max_counter += 1

                total_improper_extrm_counter += (improper_max_counter +
                                                 improper_min_counter)

                total_no_extrms = (total_improper_extrm_counter +
                                   len(desired_max_indexs_based_on_pcp_dt) +
                                   len(desired_min_indexs_based_on_pcp_dt))

                tmp = (improper_min_counter +
                       improper_max_counter +
                       len(desired_max_indexs_based_on_pcp_dt) +
                       len(desired_min_indexs_based_on_pcp_dt))
                # counter_for_pcp_dt_calc for next max
                counter_for_pcp_dt_calc = (
                    tmp - len(desired_min_indexs_based_on_pcp_dt) -
                    improper_min_counter - 1)

                switcher_counter += 1
                switcher.append(1)

            else:
                # next max
                if len(desired_max_indexs_based_on_pcp_dt) == 0:
                    second1 = all_max_indexs_based_on_lrc
                else:
                    second1 = all_max_indexs_based_on_lrc[
                        all_max_indexs_based_on_lrc.index
                        (desired_max_indexs_based_on_pcp_dt[-1]) +
                        1 +
                        improper_max_counter:]

                condition = 0

                while condition == 0:
                    condition, true_indx = pcp_time(
                        second1[counter_for_pcp_dt_calc],
                        ch,
                        desired_min_indexs_based_on_pcp_dt[-1],
                        cl)

                    counter_for_pcp_dt_calc += 1

                if ch[true_indx] < cl[desired_min_indexs_based_on_pcp_dt[-1]]:
                    desired_min_indexs_based_on_pcp_dt[-1] =\
                        all_min_indexs_based_on_lrc[counter_for_pcp_dt_calc-2]
                elif (ch[true_indx] >
                      cl[desired_min_indexs_based_on_pcp_dt[-1]]):
                    desired_max_indexs_based_on_pcp_dt.append(true_indx)
                    # now we have the max.
                    # we search bet this max and previous min for further min
                    # and max that didn't satidfy condition            

                improper_min_counter = 0
                improper_max_counter = 0

                lst = range(desired_min_indexs_based_on_pcp_dt[-1] + 1,
                            desired_max_indexs_based_on_pcp_dt[-1])

                for item in lst:
                    if item in all_min_indexs_based_on_lrc:
                        improper_min_counter += 1
                    elif item in all_max_indexs_based_on_lrc:
                        improper_max_counter += 1

                total_improper_extrm_counter += (improper_max_counter +
                                                 improper_min_counter)

                total_no_extrms = (total_improper_extrm_counter +
                                   len(desired_max_indexs_based_on_pcp_dt) +
                                   len(desired_min_indexs_based_on_pcp_dt))

                tmp = (improper_min_counter + improper_max_counter +
                       len(desired_max_indexs_based_on_pcp_dt) +
                       len(desired_min_indexs_based_on_pcp_dt))
                # counter_for_pcp_dt_calc for next min
                counter_for_pcp_dt_calc = (
                    tmp - len(desired_max_indexs_based_on_pcp_dt) -
                    improper_max_counter - 1)

                switcher_counter += 1
                switcher.append(0)

        return filter_extrms_based_on_time_and_pcp

    filter_extrms_based_on_time_and_pcp()

    return (desired_max_indexs_based_on_pcp_dt,
            desired_min_indexs_based_on_pcp_dt)


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


def extrms_based_on_neighboring_candles_with_filter_v1(cl, ch, lrc):
    ''' Finds maximums and minimums of price in a time range.'''
    # initializing the lists for extremums indexes
    mx_indx_tmp = []
    mn_indx_tmp = []
    mx_indx = []
    mn_indx = []

    def lrc_filter():
        ''' Filters all candles based on lrc'''        
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

            # if all(tmp1) and all(tmp2):
            #     extrm_s_r_indx.append(i)
            #     extrm_s_r_price.append(cl[i])
            #     extrm_s_r_price.append(ch[i])
            #     continue

            if all(tmp1):
                mn_indx_tmp.append(i)

            if all(tmp2):
                mx_indx_tmp.append(i)

    lrc_filter()

    def filter_extrms_based_on_time_and_pcp():
        ''' Identifies extremums based on elapsed time and price change
        percentage.'''
        # switcher: list to save cnt values (cnt is 0 or 1)
        switcher = []
        if mx_indx_tmp[0] < mn_indx_tmp[0]:
            # cnt: switcher for searching for max or min. If cnt=0 the first
            # extrm is max and search for min
            switcher.append(0)
            mx_indx.append(mx_indx_tmp[0])
        else:
            switcher.append(1)
            mn_indx.append(mn_indx_tmp[0])

        def pcp_time(indx2, c2, indx1, c1):
            ''' Calculates price change percentage (pcp), time elapsed (dt),
            and the condition based on which we determine the suitability of
            extrm under study for each extrm pairs.'''
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

        # The predefined minimum pcp and dt for every two consecutive extrms
        # to be valid (generally an extrm is valid if it passes lrc, pcp, and
        # dt filters)
        pcp_base = 10
        dt_base = 10

        nd_mn = len(mn_indx_tmp)
        nd_mx = len(mx_indx_tmp)
        nd = nd_mx + nd_mn
        # i: counter for all data in mn_indx_tmp and mx_indx_tmp
        # i = 0
        # j: counter for
        # j = i
        cnt_min = 0
        cnt_max = 0
        cnt_for_switcher = 0
        total_cnt_min_max = 0
        total_cnt_min = 0
        total_cnt_max = 0
        total_no_extrms = 0
        while total_no_extrms < nd:
            if switcher[cnt_for_switcher] == 0:
                # ######################## find next min
                if len(mn_indx) == 0:
                    second1 = mn_indx_tmp
                else:
                    second1 = mn_indx_tmp[len(mn_indx) + total_cnt_min:]

                second2 = cl
                first1 = mx_indx
                first2 = ch
                cnt_for_cond = 0
                cond = 0
                while cond == 0:
                    cond, true_indx = pcp_time(second1[cnt_for_cond],
                                               second2, first1[-1],
                                               first2)
                    cnt_for_cond += 1
                    if cond == 1:
                        # check if the found min is lower than previous true
                        # max. If it's higher then it's not acceptable
                        if cl[true_indx] > ch[mx_indx[-1]]:
                            mx_indx[-1] = mx_indx_tmp[total_no_extrms -
                                                      (cnt_for_cond-1) -
                                                      total_cnt_min]
                            total_cnt_max += 1
                            cond = 0
                        # and if it's lower then the result is normal
                        elif cl[true_indx] < ch[mx_indx[-1]]:
                            mn_indx.append(true_indx)
                            break
                # now we have a new min
                # There could be other min or max before the found extrm whose
                # number should be taken into account in counting the total
                # number of studied extrms, i.e. i

                cnt_min = 0
                cnt_max = 0
                lst = range(mx_indx[-1] + 1, mn_indx[-1])
                for item in lst:
                    if item in mx_indx_tmp and ch[item] < ch[mx_indx[-1]]:
                        cnt_max += 1
                    elif item in mx_indx_tmp and ch[item] > ch[mx_indx[-1]]:
                        mx_indx[-1] = mx_indx_tmp[total_cnt_max + len(mx_indx)]
                        cnt_max += 1
                    elif item in mn_indx_tmp:
                        cnt_min += 1

                total_cnt_min += cnt_min
                total_cnt_max += cnt_max
                total_cnt_min_max += cnt_max + cnt_min
                total_no_extrms = (total_cnt_min_max + len(mx_indx) +
                                   len(mn_indx))

                cnt_for_switcher += 1
                # go for next max
                switcher.append(1)

            else:
                # ######################## find next max
                if len(mx_indx) == 0:
                    second1 = mx_indx_tmp
                else:
                    second1 = mx_indx_tmp[len(mx_indx) + total_cnt_max:]

                second2 = ch
                first1 = mn_indx
                first2 = cl
                cnt_for_cond = 0
                cond = 0
                while cond == 0:
                    cond, true_indx = pcp_time(second1[cnt_for_cond],
                                               second2, first1[-1],
                                               first2)
                    cnt_for_cond += 1

                    if cond == 1:
                        if ch[true_indx] < cl[mn_indx[-1]]:
                            mn_indx[-1] = mn_indx_tmp[total_no_extrms -
                                                      (cnt_for_cond-1) -
                                                      total_cnt_max]
                            total_cnt_min += 1
                            cond = 0
                        elif ch[true_indx] > cl[mn_indx[-1]]:
                            mx_indx.append(true_indx)
                            break
                    # now we have the max.
                    # we search bet this max and previous min for further min
                    # and max that didn't satidfy cond

                cnt_min = 0
                cnt_max = 0
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
                total_no_extrms = (total_cnt_min_max + len(mx_indx) +
                                   len(mn_indx))

                cnt_for_switcher += 1
                # go for next min
                switcher.append(0)

        return filter_extrms_based_on_time_and_pcp

    filter_extrms_based_on_time_and_pcp()

    return mx_indx, mn_indx


def bokeh_chart(t_inc, t_dec, candle_high, candle_low, candle_close_dec,
                
                
                candle_close_inc, candle_open_dec, candle_open_inc, vol,
                inc, dec, vol_dec, vol_inc, rows, t, tf):
    ''' Utilizes bokeh library to plot candlestick chart. '''
    curdoc().theme = 'dark_minimal'
    # TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    fig = figure(sizing_mode='stretch_both',
                 tools="xpan,xwheel_zoom,undo,redo,reset,crosshair,save",
                 active_drag='xpan',
                 active_scroll='xwheel_zoom',
                 x_axis_type='datetime',
                 plot_width=2700,
                 plot_height=300)

    fig.xaxis.formatter = DatetimeTickFormatter(days="%m/%d", hours="%H",
                                                minutes="%H:%M")
    fig.xaxis.major_label_orientation = pi/4

    fig.grid.grid_line_alpha = 0.3
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None

    # segment:    x0,      y0,      x1,      y1
    fig.segment(t, candle_high, t, candle_low, color="white")
    # candle width
    w = 1000*30*tf
    # rectangle:     x_center, width, bottom, top
    fig.vbar(t_inc, w, candle_open_inc, candle_close_inc, fill_color="green")
    fig.vbar(t_dec, w, candle_open_dec, candle_close_dec, fill_color="red")

    # alpha is for color contrast, 
    cnst = 9
    fig.circle([t[cnst]], [candle_high[cnst]*1.005], size=50, color="white",
               alpha=0.5)

    def volume_graph():
        ''' Prepare the data and figures for plot of volume bars on Bokeh. '''
        c_min = min(candle_low)
        c_max = max(candle_high)
        delta_c = c_max-c_min
        cst1 = c_min - delta_c/5
        v_max = max(vol)
        scaled_vol = [cst1 + (c_min - cst1)*i/v_max for i in vol]
        vol_inc_norm = [scaled_vol[i] for i in inc]
        vol_dec_norm = [scaled_vol[i] for i in dec]
        vol_min = min(scaled_vol)

        global vol_low

        vol_low = [vol_min]*rows

        fig.xaxis.major_label_orientation = pi/4
        fig.grid.grid_line_alpha = 0.3
        fig.vbar(t_inc, w, [vol_min]*len(vol_inc), vol_inc_norm)
        fig.vbar(t_dec, w, [vol_min]*len(vol_dec), vol_dec_norm)

    volume_graph()

    source = ColumnDataSource({'date': t, 'high': candle_high,
                               'low': vol_low})
    # Javascript function for scaling charts on Bokeh on both x and y range
    callback = CustomJS(args={'y_range': fig.y_range, 'source': source},
                        code='''
        clearTimeout(window._autoscale_timeout);

        var date = source.data.date,
            low = source.data.low,
            high = source.data.high,
            start = cb_obj.start,
            end = cb_obj.end,
            min = Infinity,
            max = -Infinity;

        for (var i=0; i < date.length; ++i) {
            if (start <= date[i] && date[i] <= end) {
                max = Math.max(high[i], max);
                min = Math.min(low[i], min);
            }
        }
        var pad = (max - min) * .1;

        window._autoscale_timeout = setTimeout(function() {
            y_range.start = min - pad;
            y_range.end = max + pad;
        });
    ''')

    fig.x_range.js_on_change('start', callback)
    # fig.add_layout(Arrow(end=OpenHead(line_color="firebrick", line_width=4),
    # x_start=t[3], y_start=7.38e-5, x_end=t[3], y_end=7.42e-5))

    return show(fig)
    # show(gridplot([[fig],[p2]]))


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



def s_r_identification(cl, ch):
    '''This function calculates horizontal supports and resistence levels based
    on daily candlesticks. To do so, lrc is decremented from a large number
    such as 100 to lower values. After each decrimentation, the normalized
    distance between previous s/r and the new one is measured. If this value
    is greater than a predetermined offset (such as 0.01) then the s/r in
    qustion is acceptable.'''

    all_time_max = max(ch)
    all_time_min = min(cl)
    min_nondim_dist = 0.02

    lrc_init = 30
    lrc = range(lrc_init, 1, -1)
    sr = []

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
        sr_mx, sr_mn, _ = filter_extrms_based_on_lrc(cl, ch, item)
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
                # There are 4 possibilities for occur in 1st and last elements
                # of sr list:
                # occur of sr[0] is 0
                # occur of sr[0] is 1
                # occur of sr[-1] is 0
                # occur of sr[-1] is 1

                # If 1st occur is 0, then the 1st instance of occur=1 would be
                # the base for assessing this 1st 0 occur and possible
                # further 0 ones.
                # For instance (here only occur is showed in sr list and the
                # other tuple is omited for brevity):
                #               occur: [0,0,0,1,....] or [0,1,...]
                #                             /\
                #                             ||
                #                     1st instance of occur=1

                # If 1st occur is 1 and the next one(s) is(are) also 0, then
                # this 1st occur=1 would be the base for further comparison.
                # For instance: occur: [1,0,0,..] or [1,0,1,...]
                #                       /\            /\
                #                       ||            ||

                # If 1st occur is 1 and the remaining ones are also 1, then
                # the last occur=1 would be the base for comparison.
                # Ex. occur: [1,1,0,...] or [1,1,1,1,0,..]
                #               /\                 /\
                #               ||                 ||

                # Similarly, if last occur is 0 --> the 1st instance of occur=1
                # before this last element would be the base.
                # --> [.....,1,0] or [......,1,0,1,0,0,0]
                #            /\                  /\
                #            ||                  ||

                # And if Last is 1 and previous ones are zero -->
                #  [....,1,0,0,1,1,0,0,1]
                #                      /\
                #                      ||

                # also if Last occur is 1 and previous ones are also 1 -->
                # the nearest to last 0 is indeed the base -->
                #     [.....,0,1,0,0,1,1,1,1]
                #                    /\
                #                    ||

                # If sr under study is between two occur=1, then it should pass
                # the distance criterion for both instances of occur=1 to be
                # a valid sr.

                # cnt1: counter for traversing the sr list
                cnt1 = 0
                left_occur_1 = -1000
                last_occur_1 = False
                # 1st loop for traversing along sr list elements.
                while cnt1 < len(sr):
                    # cnt1=0 --> 1st element of sr list
                    # occur ~ sr[cnt1][1] == 0 --> The cnt1 element of sr list
                    # has an occur equal to 0. Herein, if cnt1=0, search
                    # continues to find a sr with occur=1. If cnt!=0,
                    # comparison process is performed.

                    # left_occur_1: Starting from sr[0], index of the last sr element
                    # that has occur=1 on condition that sr[0] has occur=1
                    # Ex.:   [1,1,1,1,0,....] or [1,0,.....]
                    #               /\            /\
                    #               ||            ||
                    # If sr[0] has occur=0 then there's no need for left-side
                    # comparison. Hence, by default left_occur_1=None.
                    if cnt1 == 0 and sr[cnt1][2] == 1:
                        left_occur_1 = 0
                        cnt1 += 1
                        continue
                    elif cnt1 == len(sr) - 1 and sr[cnt1][2] == 0:
                        last_occur_1 = True
                        sr[cnt1][2] = 1
                        # cnt1 = len(sr) - 1
                        continue
                    elif cnt1 >= 0 and sr[cnt1][2] == 0:
                        cnt1 += 1
                        continue
                    elif cnt1 > 0 and sr[cnt1][2] == 1:
                        if (
                            sr[cnt1-1][2] == 1 and cnt1 + 1 < len(sr)
                             ) or (
                            sr[0][2] == 0 and left_occur_1 < -100
                           ):

                            left_occur_1 = copy.copy(cnt1)
                            cnt1 += 1
                            continue

                        cnt2 = copy.copy(cnt1)
                        cnt3 = 1
                        cnt4 = 1
                        while (
                            cnt2 > left_occur_1 and
                            (cnt2 - cnt3) > left_occur_1 and
                            (cnt2 - cnt3) >= 0
                              ) or (
                            last_occur_1 is True and
                            sr[-2][2] == 1 and
                            left_occur_1 + 1 < len(sr)
                              ):

                            if last_occur_1 is True and cnt2 == len(sr) - 1:
                                sr[len(sr) - 1][2] = 0
                                cnt3 = 0

                                if left_occur_1 >= 0:
                                    tmp2 = nondim_price(
                                        sr[left_occur_1+cnt4][1],
                                        all_time_max,
                                        all_time_min)
                                    tmp3 = nondim_price(
                                        sr[left_occur_1][1],
                                        all_time_max,
                                        all_time_min)
                                    dist2 = abs(tmp2 - tmp3)

                                if dist2 >= min_nondim_dist:
                                    sr[left_occur_1+cnt4][2] = 1
                                    if (left_occur_1+cnt4+1) >= len(sr):
                                        cnt3 += 1

                                    left_occur_1 += cnt4
                                    cnt4 = 1
                                else:
                                    if (left_occur_1+cnt4+1) >= len(sr):
                                        cnt3 += 1

                                    cnt4 += 1
                            else:
                                tmp1 = nondim_price(sr[cnt2][1], all_time_max,
                                                    all_time_min)
                                tmp2 = nondim_price(sr[cnt2-cnt3][1],
                                                    all_time_max,
                                                    all_time_min)
                                dist1 = abs(tmp1 - tmp2)
                                dist2 = min_nondim_dist + 1
                                if left_occur_1 >= 0:
                                    tmp3 = nondim_price(sr[left_occur_1][1],
                                                        all_time_max,
                                                        all_time_min)
                                    dist2 = abs(tmp2 - tmp3)

                                if dist1 >= min_nondim_dist and\
                                        dist2 >= min_nondim_dist:

                                    sr[cnt2-cnt3][2] = 1
                                    cnt2 -= cnt3
                                    cnt3 = 1
                                else:
                                    cnt3 += 1
                        else:
                            if left_occur_1 >= 0:
                                left_occur_1 = cnt1

                        cnt1 += 1
 
                        # 2nd loop starts which is the comparison process, i.e.
                        # assessing the nondimensional distance of cnt2 element
                        # of sr list w.r.t. its possible previous counterparts
                        # having occur=0. It's a matter of possiblity because
                        # there could be no sr element before cnt2 that has
                        # occur=0. In this case, this 2nd loop is terminated
                        # and cnt1 is updated.
 

                        # To begin, if occur(s) of the first element(s) in sr is(are)
                        # zero then one-side comparison (comparing the distance of 
                        # the 1st instance of occur=1 with these zero occures) is sufficient and
                        # a default value greater than min dist is set for
                        # dist2; So, the condition dist2 >= min_nondim_dist would hold automatically.
                        # Otherwise, two-side comparison must be
                        # applied which assesses the nondim dist from both
                        # previous (dist2) and next (dist1) elements. Here, dist2
                        # wouldn't necessarily have a value greater than min_nondim_dist and it should be calculated (dist2=abs(tmp1-tmp3))

    return sr



def s_r_identification_optimized(cl, ch, mnd):
    '''This function calculates horizontal supports and resistence levels based
    on daily candlesticks using numpy package instead of default python lists.
    To do so, lrc is decremented from a large number
    such as 100 to lower values. After each decrimentation, the normalized
    distance between previous s/r and the new one is measured. If this value
    is greater than a predetermined offset (such as 0.01) then the s/r in
    qustion is acceptable.'''
    nd = len(cl)
    cl = np.array(cl)
    ch = np.array(ch)
    atmx = max(ch)
    atmn = min(cl)

    lrc_init = 30
    lrc = range(lrc_init, 1, -1)
    sr = np.zeros(1000)

    def dist(el1, el2):
        d1 = nondim_price(el1, atmx, atmn)
        d2 = nondim_price(el2, atmx, atmn)
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
        sr_mx, sr_mn = filter_extrms_based_on_lrc(cl, ch, item)[0:2]
        sr_mx = np.array(sr_mx)
        sr_mn = np.array(sr_mn)
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
                if i == j:
                    # The duplicate sr is removed
                    np.delete(sr_mx, np.where(sr_mx == i))

        for i in sr_mn_copy:
            for j in sr:
                if i == j:
                    np.delete(sr_mn, np.where(sr_mn == i))

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
                sr_mx = [sr_mx(i, ch[i], occur) for i in sr_mx]
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
                srr = copy.copy(sr)
                sr.sort(key=lambda x: -x[1])
                srr.sort(key=lambda x: -x[0])
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

    return sr






















import pandas as pd

from dask import dataframe as dd
import dask.multiprocessing
from multiprocessing import Pool

import os

import time


##################################### large file import
path = "C://files//algotrader//main//data//hist_data//OSTBTC_1min.csv"
path2 = "D://Binance_data//complete_data//"
path3 = "D://Binance_data//dummy//"

col_names = ['unix time', 'open', 'high', 'low', 'close', 'vol', 'd7', 'd8',
             'd9', 'd10', 'd11', 'd12']


def pandas_read_csv_partly():
    df = pd.read_csv(path, chunksize=10, names=col_names)
    i = 0
    for chunk in df:
        if i == 100:
            data = pd.DataFrame(chunk)
            break
        i += 1
    print(data)


def pandas_read_csv(file): 
    f = pd.read_csv(path3+file)
    
    return f


def main():
    files = os.listdir(path3)
    file_list = [filename for filename in files]
    start = time.time()
    # set up your pool
    with Pool(processes=2) as pool: # or whatever your hardware can support

        # have your pool map the file names to dataframes
        df_list = pool.map(pandas_read_csv, file_list)
        combined_df = pd.concat(df_list, ignore_index=True)
    end = time.time()
    print("Pandas multiprocess read csv: ", (end-start), "sec")


if __name__ == '__main__':
    main()