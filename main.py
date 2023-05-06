from dataManip.histDataPrep import BullBearMrks, initialDataConfig

import plot.bokehV21h1d as plot

from tech import ma, atr


path = "C:\\Java_files\\PythonAlgorithmicTrading\\data\\"
asset = 'SOLUSDT'
ts = ''
tf = '1m'
nod = 5000
(t, tInc, tDec, cc, ch, cl, ccDec, ccInc, coDec,
 coInc) = BullBearMrks(asset, tf, ts, path, nod)[0:10]

p = [2, 25]
mas = ma(True, cc, p)

# close_pos_criterion = p > 3*ATR

atr_period = 10
mult = 2

w = 40000
# plot.chrt(t, ch, cl, tInc, tDec, ccInc, ccDec, coInc, coDec, mas, w)


m1 = mas[0]
m2 = mas[1]

indx = p[1]
m1indx = indx - p[0]
m2indx = indx - p[1]

lev = 2
cap_for_each_side_quote = 500

# typically qoute asset is $

base_init_ave_price = (cc[indx] + cl[indx] + ch[indx])/3
base_cap = cap_for_each_side_quote/base_init_ave_price
quote_cap = cap_for_each_side_quote
no_active_trades_on_each_side = 10
# typically min_quote_cap_for_one_trade shouln't be less than 10-15 $
min_quote_cap_for_one_trade = 15
min_base_cap_for_one_trade = min_quote_cap_for_one_trade/base_init_ave_price

max_open_trades = 2*no_active_trades_on_each_side
buy_cap = [min_quote_cap_for_one_trade]*no_active_trades_on_each_side
sell_cap = [min_base_cap_for_one_trade]*no_active_trades_on_each_side

base_balance = [sum(sell_cap)]
quote_balance = [sum(buy_cap)]

free_buy_margin = quote_cap - quote_balance[0]
free_sell_margin = base_cap - base_balance[0]
buy_loss = [0]*no_active_trades_on_each_side
sell_loss = [0]*no_active_trades_on_each_side
total_trades = 0

# opentrade cnd, time, 

trade = {}

if m2[m2indx] > m1[m1indx]:
    mode = 'buy'
else:
    mode = 'sell'

trade_number = 0
sell_trade_number = 0
buy_trade_number = 0
total_sells = 0
total_buys = 0
total_open_trades = 0

indx += 1
m1indx = indx - p[0]
m2indx = indx - p[1]

while indx < nod and (sell_trade_number and buy_trade_number) < 10:
    if mode == 'sell' and m1[m1indx] < m2[m2indx]:
        ave_base_price = (cc[indx] + cl[indx] + ch[indx])/3
        sold_asset_quote_amount = sell_cap[sell_trade_number] * ave_base_price
        trade[trade_number] = [indx, str(t[indx]), mode,
                               'ave_p',
                               str(round(ave_base_price, 3)),
                               'bal_q',
                               str(round(sold_asset_quote_amount*0.999, 3)),
                               'w/l_b', 0, 0, 0, 0]
        sell_trade_number += 1
        trade_number += 1
        total_sells += 1
        total_open_trades += 1
        mode = 'buy'
    elif mode == 'buy' and m1[m1indx] > m2[m2indx]:
        ave_base_price = (cc[indx] + cl[indx] + ch[indx])/3
        bought_asset_base_amount = buy_cap[buy_trade_number] / ave_base_price
        trade[trade_number] = [indx, str(t[indx]), mode,
                               'ave_p',
                               str(round(ave_base_price, 3)),
                               'bal_b',
                               str(round(bought_asset_base_amount*0.999, 3)),
                               'w/l_q', 0, 0, 0, 0]
        buy_trade_number += 1
        trade_number += 1
        total_buys += 1
        total_open_trades += 1
        mode = 'sell'

    indx += 1
    m1indx = indx - p[0]
    m2indx = indx - p[1]

    if trade != {}:
        for i in trade:
            if trade[i][2] == 'sell' and trade[i][9] != 'closed':
                ave_p = (cc[indx] + cl[indx] + ch[indx])/3
                buy_sold_asset_b = 0.999*float(trade[i][6])/ave_p
                sold_asset_b = float(trade[i][6])/float(trade[i][4])
                win_loss = buy_sold_asset_b - sold_asset_b
                trade[i][8] = str(round(win_loss, 3))

                if (ave_base_price > float(trade[i][4]) +
                   mult*atr(ch, cl, cc, trade[i][0], atr_period)) or (
                     m1[m1indx] > m2[m2indx]
                   ):

                    trade[i][9] = 'closed'
                    trade[i][10] = str(round(ave_p, 3))
                    trade[i][11] = indx
                    total_open_trades -= 1

            if trade[i][2] == 'buy' and trade[i][9] != 'closed':
                ave_p = (cc[indx] + cl[indx] + ch[indx])/3
                sell_bought_asset_q = 0.999*float(trade[i][6])*ave_p
                bought_asset_q = float(trade[i][6])*float(trade[i][4])
                win_loss = sell_bought_asset_q - bought_asset_q
                trade[i][8] = str(round(win_loss, 3))

                if (ave_p < float(trade[i][4]) -
                   mult*atr(ch, cl, cc, trade[i][0], atr_period)) or (
                     m1[m1indx] < m2[m2indx]
                   ):

                    trade[i][9] = 'closed'
                    trade[i][10] = str(round(ave_p, 3))
                    trade[i][11] = indx
                    total_open_trades -= 1

    total_trades = total_buys + total_sells
    if total_open_trades >= max_open_trades:
        break

sell_sum = sum([float(trade[i][8]) for i in trade if trade[i][2] == 'sell'])
buy_sum = sum([float(trade[i][8]) for i in trade if trade[i][2] == 'buy'])
base_balance.append(sum(sell_cap) + sell_sum)
quote_balance.append(sum(buy_cap) + buy_sum)

print('base balance: ', base_balance)

print('quote balance: ', quote_balance)


