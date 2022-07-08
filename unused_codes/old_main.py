from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.models import (DatetimeTickFormatter,
                          CustomJS, ColumnDataSource)

import csv

import numpy as np

from math import pi

from datetime import datetime as dtm

from kucoin.client import Client
import json

from Config.KucoinConfig import kucoin_api_key, kucoin_api_passphrase, kucoin_api_secret

import matplotlib.pyplot as plt

import random


utc = dtm.utcfromtimestamp


def data_load(data_path, data_length):
    ''' Loads candlestick data from csv file in a specified date range. '''
    with open(data_path, newline='') as f:
        reader = csv.reader(f)
        dt = list(reader)
    # converting dt from list to  numpy array
    dt = np.array(dt, dtype='U20')

    return dt[0:data_length]


def kucoin_api_data():
    ''' Gets exchange live data through web socket or API connection. '''
    client = Client(kucoin_api_key, kucoin_api_secret,
                    kucoin_api_passphrase)
    # get currencies
    currencies = client.get_currencies()
    # get market depth
    depth = client.get_order_book('KCS-BTC')
    # get symbol klines
    klines = client.get_kline_data('KCS-BTC')
    # get list of markets
    markets = client.get_markets()
    # place a market buy order
    # order = client.create_market_order('NEO', Client.SIDE_BUY, size=20)
    with open('depth1.json', 'w', encoding='utf-8') as f:
        json.dump(depth, f, ensure_ascii=False, indent=4)


def data_edit(dt, exchange, rows):
    '''
    Edits the data file in terms of unix time conversion and unused columns
    deletion. '''
    if exchange == 'binance':
        # converting unix time from milisec to sec
        dt[:, 0] = [(int(dt[i, 0]))/1000 for i in range(rows)]
        # t1 = [utc(1617235200), utc(1617235260)]
        # t2 = [utc(float(dt[0,0])), utc(float(dt[1,0]))]
        t = [utc(float(dt[i, 0])) for i in range(0, rows)]
        # Data stream format and useless columns are explained in README file.
        # Deleting useless cols
        dt = np.delete(dt, [6, 7, 9, 10, 11], 1)

    return dt, t


def candle_data(dt, t):
    '''
    Defines candles' high, low, close, and open values as well as volume and
    time data w.r.t. bullish or bearish market. '''
    candle_high = [float(dt[i, 2]) for i in range(0, rows)]
    candle_low = [float(dt[i, 3]) for i in range(0, rows)]
    candle_open = [float(dt[i, 1]) for i in range(0, rows)]
    candle_close = [float(dt[i, 4]) for i in range(0, rows)]
    vol = [float(dt[i, 5]) for i in range(0, rows)]
    # Initializing lists for the color of increasing/decreasing candles( bull./
    # bear. market).
    inc = []
    dec = []
    # Identifying bull./bear. market index
    for i in range(0, rows):
        if candle_open[i] < candle_close[i]:
            inc.append(i)
        else:
            dec.append(i)
    # Identifying parameters in bull./bear. market)
    t_inc = [t[i] for i in inc]
    candle_open_inc = [candle_open[i] for i in inc]
    candle_close_inc = [candle_close[i] for i in inc]
    t_dec = [t[i] for i in dec]
    candle_open_dec = [candle_open[i] for i in dec]
    candle_close_dec = [candle_close[i] for i in dec]
    vol_inc = [vol[i] for i in inc]
    vol_dec = [vol[i] for i in dec]

    return (t_inc, t_dec, candle_close, candle_high, candle_low,
            candle_close_dec, candle_close_inc, candle_open_dec,
            candle_open_inc, vol, inc, dec, vol_dec, vol_inc)


def bokeh_chart():
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
    # segment:    x0,      y0,      x1,      y1
    fig.segment(t, candle_high, t, candle_low, color="white")
    # candle width w
    w = 1000*30
    # rectangle:     x_center, width, bottom, top
    fig.vbar(t_inc, w, candle_open_inc, candle_close_inc, fill_color="green")
    fig.vbar(t_dec, w, candle_open_dec, candle_close_dec, fill_color="red")

    # VOLUME GRAPH
    c_min = min(candle_low)
    c_max = max(candle_high)
    delta_c = c_max-c_min
    cst1 = c_min - delta_c/5
    v_max = max(vol)
    scaled_vol = [cst1 + (c_min - cst1)*i/v_max for i in vol]
    vol_inc_norm = [scaled_vol[i] for i in inc]
    vol_dec_norm = [scaled_vol[i] for i in dec]
    vol_min = min(scaled_vol)
    vol_low = [vol_min]*rows

    fig.xaxis.major_label_orientation = pi/4
    fig.grid.grid_line_alpha = 0.3
    fig.vbar(t_inc, w, [vol_min]*len(vol_inc), vol_inc_norm)
    fig.vbar(t_dec, w, [vol_min]*len(vol_dec), vol_dec_norm)

    source = ColumnDataSource({'date': t, 'high': candle_high, 'low': vol_low})

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
        var pad = (max - min) * .01;

        window._autoscale_timeout = setTimeout(function() {
            y_range.start = min - pad;
            y_range.end = max + pad;
        });
    ''')

    fig.x_range.js_on_change('start', callback)
    # fig.add_layout(Arrow(end=OpenHead(line_color="firebrick", line_width=4),
    # x_start=t[3], y_start=7.38e-5, x_end=t[3], y_end=7.42e-5))

    return fig
    # show(gridplot([[fig],[p2]]))


# def strategy():
#     ''' Studying candlestick chart to define S/R, trends, patterns, etc.'''
#     pass

def extremum():
    ''' Identifies maximum and minimum points in price history for further
    trend and support/resistence calculations. '''
    pass


def horizontal_sr():
    ''' Horizontal supports and resistence levels '''
    pass


def market_regimes():
    ''' Identifies (up/down)trends or sideways in different time frames
    (both initial and confirmed trends). Calculates price change and its
    time duration w.r.t. extermums to define trend strength and
    consolidation periods. '''
    pass


def price_volume_breakout():
    ''' Identifies possible breakouts in p and v. '''
    pass


def price_volume_pattern():
    ''' Identifies possible patterns in p and v. '''
    pass


def liquidity_check():
    ''' Checks market liquidity and volume and number of trades to select
    the proper base time frame.
    '''
    pass


def volatility():
    ''' Calculates volatility in market.'''
    pass


# ############ Items that could probably be useful
def retest_on_sr():
    ''' Identifies possible Retest on supports and resistence levels. '''
    pass


def hammer():
    ''' Identifies possible Hammer candle. '''
    pass


def divergence_p_v_nt():
    '''
    Defines possibile divergence between price, volume, and number of
    trades. '''
    pass


def stop_hunt():
    ''' Detects possible stop hunting areas for possible enterance or setting
    better stop loss. '''
    pass
# ############


def backtest():
    ''' Having Defined the trading strategy and its components, we use this
    function to perform backtest on historical data in a monte carlo sense. '''

def risk_money_management():
    ''' After performing backtest, the overal performance of the strategy is
    defined laying the groundwork for a better money and risk management in
    the sense that the overal historical trend of the asset gains becomes
    rising.'''
    cap = 1000
    risk = [0.03, 0.05, 0.1, 0.3]
    r_p = [0.9, 0.65, 0.5]
    win_loss = [0]*45 + [1]*55
    random.shuffle(win_loss)
    x = range(0, 101)
    # print(win_loss)
    lst = []
    lst.append(cap)
    for i in win_loss:
        if i == 0:
            cap = cap-risk[1]*cap
            lst.append(cap)
        else:
            cap = cap + cap*risk[1]/r_p[1]
            lst.append(cap)

    plt.plot(x, lst)
    plt.show()


data_path = 'D:\\BBT\\AlgoTrader_v2_BOKEH\\main\\data\\data.csv'
dt = data_load(data_path, 2000)
rows = np.shape(dt)[0]
dt, t = data_edit(dt, 'binance', rows)
(t_inc, t_dec, candle_close, candle_high, candle_low, candle_close_dec,
 candle_close_inc, candle_open_dec, candle_open_inc,
 vol, inc, dec, vol_dec, vol_inc) = candle_data(dt, t)
fig = bokeh_chart()
show(fig)
