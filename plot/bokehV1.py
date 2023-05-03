from bokeh.io import curdoc

from bokeh.plotting import figure, show, curdoc

from bokeh.models import (DatetimeTickFormatter, Span,
                          CustomJS, ColumnDataSource)
from bokeh.layouts import gridplot

from math import pi

import numpy as np


def VWAP_Show(fig, NoOfData, VWAP_Vecs, VWAP_Periods, NoOfVWAPs):
    ''' Shows vwap graphs'''

    colors = ['white', 'white', 'white', 'white', 'white',
                'blue', 'blue', 'blue', 'blue', 'blue',
                'red', 'red', 'red', 'red', 'red',
                'yellow']
    colors = ['white', 'yellow', 'blue', 'red', 'gray']
    colors = ['yellow', 'blue']
    timeVecs = [[] for i in range(NoOfVWAPs)]
    for i in range(len(VWAP_Vecs)):
        timeVecs[i] = t[:-(NoOfData+1-VWAP_Periods[i]):-1]
        fig.line(timeVecs[i], VWAP_Vecs[i][0], color=colors[i], alpha=0.9)


def showExtrmShapeObj(fig, trendSizes, trendSize, mxIndx, mnIndx, t, cl, ch, tLowerTF, objSize, objVertPosCoeff,
                        objColor, alpha):
    ''' Shows colored circles above and below each max/min.'''
    # alpha is for color contrast
    if (trendSizes[0] == 'Def' and trendSize == '1h') or (trendSizes[0] == '1h' and trendSize == '1d'):

        cnt1 = len(mxIndx)
        cnt2 = len(mnIndx)

        if t[-1] > tLowerTF[0]:
            indx1 = [t.index(i) for i in t if i >= tLowerTF[0]][0]
            if mxIndx[-1] > indx1:
                indx2 =\
                    [mxIndx.index(i) for i in mxIndx if i >= indx1][0]
            else:
                indx2 = cnt1
        else:
            indx2 = cnt1


        for i in range(indx2, cnt1):
            fig.circle([t[mxIndx[i]]],
                        [ch[mxIndx[i]]*objVertPosCoeff[0]],
                        size=objSize, color=objColor[1],
                        alpha=alpha)
            fig.text([t[mxIndx[i]]], [ch[mxIndx[i]]*1.0003],
                        [mxIndx[i]],
                        text_color='white', text_font_size='24px')

        
        if t[-1] > tLowerTF[0]:
            indx1 = [t.index(i) for i in t if i >= tLowerTF[0]][0]
            if mnIndx[-1] > indx1:
                indx3 =\
                    [mnIndx.index(i) for i in mnIndx if i >= indx1][0]
            else:
                indx3 = cnt2
        else:
            indx3 = cnt2

        for i in range(indx3, cnt2):
            fig.circle([t[mnIndx[i]]],
                        [cl[mnIndx[i]]*objVertPosCoeff[1]],
                        size=objSize, color=objColor[0],
                        alpha=alpha)
            fig.text([t[mnIndx[i]]], [cl[mnIndx[i]]*0.9997],
                        [mnIndx[i]],
                        text_color='white', text_font_size='24px')

    elif trendSize == 'Def':

        cnt1 = len(mxIndx)
        for i in range(0, cnt1):
            fig.square([t[mxIndx[i]]],
                        [ch[mxIndx[i]]*objVertPosCoeff[0]],
                        size=objSize, color=objColor[1],
                        alpha=alpha)
            # fig.text([tDef[mxIndxDef[i]]], [chDef[mxIndxDef[i]]*1.0003],
            #          [mxIndxDef[i]],
            #          text_color='white', text_font_size='24px')
        cnt2 = np.shape(mnIndx)[0]
        for i in range(0, cnt2):
            fig.square([t[mnIndx[i]]],
                        [cl[mnIndx[i]]*objVertPosCoeff[1]],
                        size=objSize, color=objColor[0],
                        alpha=alpha)
            # fig.text([tDef[mnIndxDef[i]]], [clDef[mnIndxDef[i]]*0.9997],
            #          [mnIndxDef[i]],
            #          text_color='white', text_font_size='24px')


def bokehChartDef(tDef, chDef, clDef, mxIndxDef, mnIndxDef,
                       incDef, decDef,
                       tIncDef, tDecDef,
                       ccIncDef, ccDecDef, coIncDef, coDecDef,
                       volDef, volIncDef, volDecDef,
                       BB_MA_Def, BB_UB_Def, BB_LB_Def,
                       HSRData,
                       t1h, ch1h, cl1h, mxIndx1h, mnIndx1h,
                       BB_MA1h, BB_UB1h, BB_LB1h,
                       MA_Vecs,
                       showExtrm, showVol, showSR, showBB,
                       showMA):

    '''This function utilizes bokeh library to plot candlestick chart. '''
    # No. of data
    NoOfData = len(chDef)
    
    curdoc().theme = 'dark_minimal'
    # TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    fig = figure(sizing_mode='stretch_both',
                 tools="xpan,xwheel_zoom,undo,redo,reset,crosshair,save",
                 active_drag='xpan',
                 active_scroll='xwheel_zoom',
                 x_axis_type='datetime',
                 plot_width=3000,
                 plot_height=300)

    fig.xaxis.formatter = DatetimeTickFormatter(days="%m/%d", hours="%H",
                                                minutes="%H:%M")
    fig.xaxis.major_label_orientation = pi/4
    fig.grid.grid_line_alpha = 0.3
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    fig.xaxis.major_label_text_font_size = "20pt"
    fig.yaxis.major_label_text_font_size = "20pt"
    # segment:    x0,      y0,      x1,      y1
    fig.segment(tDef, chDef, tDef, clDef, color="white")
    # candle width
    w = 3000000
    # rectangle:     x_center, width, bottom, top
    fig.vbar(tIncDef, w, coIncDef, ccIncDef, fill_color="green")
    fig.vbar(tDecDef, w, coDecDef, ccDecDef, fill_color="red")

    def showExtrmShapeObj(trendSizes, objSize, objVertPosCoeff,
                            objColor, alpha):
        ''' Shows colored circles above and below each max/min.'''
        # alpha is for color contrast
        
        def selectRangeOfExtrmShapeObjToShowBasedOnTf(trendSize, tLowerTf, tHigherTf, mxIndxLowerTf, mnIndxLowerTf, mxIndxHigherTf, mnIndxHigherTf):
            
            
        

        # alpha is for color contrast
        if trendSize == '1h':

            cnt1 = len(mxIndx1h)
            cnt2 = len(mnIndx1h)

            if t1h[-1] > tDef[0]:
                indx1 = [t1h.index(i) for i in t1h if i >= tDef[0]][0]
                if mxIndx1h[-1] > indx1:
                    indx2 =\
                     [mxIndx1h.index(i) for i in mxIndx1h if i >= indx1][0]
                else:
                    indx2 = cnt1
            else:
                indx2 = cnt1


            for i in range(indx2, cnt1):
                fig.circle([t1h[mxIndx1h[i]]],
                           [ch1h[mxIndx1h[i]]*objVertPosCoeff[0]],
                           size=objSize, color=objColor[1],
                           alpha=alpha)
                fig.text([t1h[mxIndx1h[i]]], [ch1h[mxIndx1h[i]]*1.0003],
                         [mxIndx1h[i]],
                         text_color='white', text_font_size='24px')

            
            if t1h[-1] > tDef[0]:
                indx1 = [t1h.index(i) for i in t1h if i >= tDef[0]][0]
                if mnIndx1h[-1] > indx1:
                    indx3 =\
                     [mnIndx1h.index(i) for i in mnIndx1h if i >= indx1][0]
                else:
                    indx3 = cnt2
            else:
                indx3 = cnt2

            for i in range(indx3, cnt2):
                fig.circle([t1h[mnIndx1h[i]]],
                           [cl1h[mnIndx1h[i]]*objVertPosCoeff[1]],
                           size=objSize, color=objColor[0],
                           alpha=alpha)
                fig.text([t1h[mnIndx1h[i]]], [cl1h[mnIndx1h[i]]*0.9997],
                         [mnIndx1h[i]],
                         text_color='white', text_font_size='24px')

        elif trendSize == 'Def':

            cnt1 = len(mxIndxDef)
            for i in range(0, cnt1):
                fig.square([tDef[mxIndxDef[i]]],
                           [chDef[mxIndxDef[i]]*objVertPosCoeff[0]],
                           size=objSize, color=objColor[1],
                           alpha=alpha)
                # fig.text([tDef[mxIndxDef[i]]], [chDef[mxIndxDef[i]]*1.0003],
                #          [mxIndxDef[i]],
                #          text_color='white', text_font_size='24px')
            cnt2 = np.shape(mnIndxDef)[0]
            for i in range(0, cnt2):
                fig.square([tDef[mnIndxDef[i]]],
                           [clDef[mnIndxDef[i]]*objVertPosCoeff[1]],
                           size=objSize, color=objColor[0],
                           alpha=alpha)
                # fig.text([tDef[mnIndxDef[i]]], [clDef[mnIndxDef[i]]*0.9997],
                #          [mnIndxDef[i]],
                #          text_color='white', text_font_size='24px')

    if showExtrm == 'showExtrm':
        showExtrmShapeObj('1h', 15, [1.004, 0.993],
                            ['white', 'darkolivegreen'], 0.9)
        showExtrmShapeObj('1d', 25, [1.0001, 0.9999], ['green', 'red'], 0.9)


    def volume_graph_show():
        ''' Prepare the data and figures for plot of volume bars on Bokeh. '''
        v = figure(# sizing_mode='stretch_both',
               tools="xpan,xwheel_zoom,undo,redo,reset,crosshair,save",
               active_drag='xpan',
               active_scroll='xwheel_zoom',
               x_axis_type='datetime',
               x_range=fig.x_range,
               # y_range=fig.y_range,
               plot_width=fig.plot_width,
               plot_height=300)

        v_max = max(vol)
        scaled_vol = [i/v_max for i in vol]
        vol_inc_norm = [scaled_vol[i] for i in inc]
        vol_dec_norm = [scaled_vol[i] for i in dec]
        vol_min = min(scaled_vol)

        global vol_low
        rows = len(vol)
        vol_low = [vol_min]*rows

        v.xaxis.major_label_orientation = pi/4
        v.grid.grid_line_alpha = 0.3
        v.vbar(t_inc, w, [vol_min]*len(vol_inc), vol_inc_norm)
        v.vbar(t_dec, w, [vol_min]*len(vol_dec), vol_dec_norm)

    if show_vol == 'show_vol':
        volume_graph_show()

    # def pp_graph_show():
    #     '''This function plots pivot point and its supports and resistance.'''
    #     color = 'cyan'
    #     pps = [r1, r2, r3, r4, s1, s2, s3, s4]
    #     for i in pps:
    #         fig.segment(pp_time_range[0], i, pp_time_range[-1], i, color=color)

    #     fig.segment(pp_time_range[0], pivotpoint, pp_time_range[-1], pivotpoint, color='blue')

    # if show_pp == 'show_pp':
    #     pp_graph_show()

    # def ma_show():
    #     ''' Shows moving average line on candlestick chart.'''
    #     lst = t[:-(nd+1-ma_period):-1]
    #     fig.line(lst, LSMA[0:170], color='white', alpha=0.9)

    # if show_ma == 'show_ma':
    #     ma_show()

    def sr_show():
        color = 'white'
        for i in sr:
            hline = Span(location=i, dimension='width', line_color=color, line_width=1)
            fig.add_layout(hline)

    if show_sr == 'show_sr':
        sr_show()

    source2 = ColumnDataSource({'date': t, 'high': ch, 'low': cl})
    # Javascript function for scaling charts on Bokeh on both x and y range
    callback = CustomJS(args={'y_range': fig.y_range, 'source': source2},
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
        var pad = (max - min) * .15;

        window._autoscale_timeout = setTimeout(function() {
            y_range.start = min - pad;
            y_range.end = max + pad;
        });
    ''')

    fig.x_range.js_on_change('start', callback)

    # fig.add_layout(Arrow(end=OpenHead(line_color="firebrick", line_width=4),
    # x_start=t[3], y_start=7.38e-5, x_end=t[3], y_end=7.42e-5))

    # layout = gridplot([[fig], [v]])
    layout = gridplot([[fig]])

    return show(layout)


def bokehChart1h(t1h, ch1h, cl1h, mx_indx1h, mn_indx1h, t1d, ch1d, cl1d,
                   mx_indx1d, mn_indx1d, inc1h, dec1h, tInc1h, tDec1h, ccInc1h,
                   ccDec1h, coInc1h, coDec1h, vol1h, volInc1h, volDec1h,
                   HSRData,
                   bollingerBandsMovingAverage, bollingerbandsLowerBound,
                   bollingerbandsUpperBound, MA_Vectors,
                   show_circles, show_vol, show_sr, show_BB, show_MA):

    '''This function utilizes bokeh library to plot candlestick chart. '''
    curdoc().theme = 'dark_minimal'
    # TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    fig = figure(sizing_mode='stretch_both',
                 tools="xpan,xwheel_zoom,undo,redo,reset,crosshair,save",
                 active_drag='xpan',
                 active_scroll='xwheel_zoom',
                 x_axis_type='datetime',
                 plot_width=3000,
                 plot_height=700)

    fig.xaxis.formatter = DatetimeTickFormatter(days="%m/%d", hours="%H",
                                                minutes="%H:%M")
    fig.xaxis.major_label_orientation = pi/4
    fig.grid.grid_line_alpha = 0.3
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    fig.xaxis.major_label_text_font_size = "20pt"
    fig.yaxis.major_label_text_font_size = "20pt"
    # segment:    x0,      y0,      x1,      y1
    fig.segment(t1h, ch1h, t1h, cl1h, color="white", line_width=1)
    # candle width
    w = 2000000
    # rectangle:     x_center, width, bottom, top
    fig.vbar(tInc1h, w, coInc1h, ccInc1h, fill_color="green")
    fig.vbar(tDec1h, w, coDec1h, ccDec1h, fill_color="red")

    v = figure(# sizing_mode='stretch_both',
                tools="xpan,xwheel_zoom,undo,redo,reset,crosshair,save",
                active_drag='xpan',
                active_scroll='xwheel_zoom',
                x_axis_type='datetime',
                x_range=fig.x_range,
                # y_range=fig.y_range,
                plot_width=fig.plot_width,
                plot_height=300)

    def extrms_circles_show(trend_size, object_size,
                            object_vert_pos_multiplier,
                            object_color, alpha):
        ''' Shows colored circles above and below each max/min.'''

        # alpha is for color contrast
        if trend_size == '1d':
            max_index = mx_indx1d
            min_index = mn_indx1d

            cnt1 = len(max_index)
            if t1d[-1] > t1h[0]:
                indx1 = [t1d.index(i) for i in t1d if i >= t1h[0]][0]
                if max_index[-1] > indx1:
                    indx2 =\
                     [max_index.index(i) for i in max_index if i >= indx1][0]
                else:
                    indx2 = cnt1
            else:
                indx2 = cnt1

            time = t1d
            low = cl1d
            high = ch1d

            for i in range(indx2, cnt1):
                fig.circle([time[max_index[i]]],
                           [high[max_index[i]]*object_vert_pos_multiplier[0]],
                           size=object_size, color=object_color[1],
                           alpha=alpha)
                fig.text([time[max_index[i]]], [high[max_index[i]]*1.0003],
                         [max_index[i]],
                         text_color='white', text_font_size='24px')

            cnt2 = len(min_index)
            if t1d[-1] > t1h[0]:
                indx1 = [t1d.index(i) for i in t1d if i >= t1h[0]][0]
                if min_index[-1] > indx1:
                    indx3 =\
                     [min_index.index(i) for i in min_index if i >= indx1][0]
                else:
                    indx3 = cnt2
            else:
                indx3 = cnt2

            for i in range(indx3, cnt2):
                fig.circle([time[min_index[i]]],
                           [low[min_index[i]]*object_vert_pos_multiplier[1]],
                           size=object_size, color=object_color[0],
                           alpha=alpha)
                fig.text([time[min_index[i]]], [low[min_index[i]]*0.9997],
                         [min_index[i]],
                         text_color='white', text_font_size='24px')

        elif trend_size == '1h':
            max_index = mx_indx1h
            min_index = mn_indx1h
            time = t1h
            low = cl1h
            high = ch1h
            cnt1 = len(max_index)
            for i in range(0, cnt1):
                fig.square([time[max_index[i]]],
                           [high[max_index[i]]*object_vert_pos_multiplier[0]],
                           size=object_size, color=object_color[1],
                           alpha=alpha)
                # fig.text([time[max_index[i]]], [ch[max_index[i]]*1.0003],
                #          [max_index[i]],
                #          text_color='white', text_font_size='24px')
            cnt2 = np.shape(min_index)[0]
            for i in range(0, cnt2):
                fig.square([time[min_index[i]]],
                           [low[min_index[i]]*object_vert_pos_multiplier[1]],
                           size=object_size, color=object_color[0],
                           alpha=alpha)
                # fig.text([time[min_index[i]]], [cl[min_index[i]]*0.9997],
                #          [min_index[i]],
                #          text_color='white', text_font_size='24px')

    if show_circles == 'show_circles':
        extrms_circles_show('1h', 15, [1.004, 0.993],
                            ['white', 'darkolivegreen'], 0.9)
        extrms_circles_show('1d', 25, [1.0001, 0.9999], ['green', 'red'], 0.9)

    def volume_graph_show():
        ''' Prepare the data and figures for plot of volume bars on Bokeh. '''
        v_max = max(vol1h)
        scaled_vol = [i/v_max for i in vol1h]
        scaled_vol = vol1h
        vol_inc_norm = [scaled_vol[i] for i in inc1h]
        vol_dec_norm = [scaled_vol[i] for i in dec1h]
        vol_min = min(scaled_vol)
        vol_min = min(vol1h)
        vol_min = 0

        global vol_low
        rows = len(vol1h)
        vol_low = [vol_min]*rows

        v.xaxis.major_label_orientation = pi/4
        v.grid.grid_line_alpha = 0.3
        v.vbar(tInc1h, w, [vol_min]*len(volInc1h), vol_inc_norm)
        v.vbar(tDec1h, w, [vol_min]*len(volDec1h), vol_dec_norm)

    if show_vol == 'show_vol':
        volume_graph_show()

    def sr_show():
        color = 'blue'
        for i in HSRData:
            hline = Span(location=i, dimension='width', line_color=color,
                         line_width=3)
            fig.add_layout(hline)

    if show_sr == 'show_sr':
        sr_show()

    def BB_show():
        numberOfBB_Branches = len(bollingerbandsLowerBound)
        vectorSizeOfEachBB_Branch = len(bollingerbandsLowerBound[1])
        totalNumberOfCandles = len(t1h)
        boundColors = ['white', 'yellow']
        MA_Colors = ['green', 'red']

        timeVectorForBB_BranchesAndBB_MA =\
            t1h[:totalNumberOfCandles - vectorSizeOfEachBB_Branch - 1:-1]

        # fig.line(timeVectorForBB_BranchesAndBB_MA,
        #          bollingerBandsMovingAverage[0], color=colors[3],
        #          alpha=0.9, line_width=10)

        for i in range(numberOfBB_Branches):
            fig.line(timeVectorForBB_BranchesAndBB_MA,
                     bollingerBandsMovingAverage[i], color=MA_Colors[i],
                     alpha=0.9, line_width=10)

            fig.line(timeVectorForBB_BranchesAndBB_MA,
                     bollingerbandsLowerBound[i], color=boundColors[i],
                     alpha=0.9, line_width=3)
            fig.line(timeVectorForBB_BranchesAndBB_MA,
                     bollingerbandsUpperBound[i], color=boundColors[i],
                     alpha=0.9, line_width=3)

        return timeVectorForBB_BranchesAndBB_MA

    if show_BB == 'show_BB':
        timeVectorForBB_BranchesAndBB_MA = BB_show()

        scaleFactor = 0.07
        source2 = ColumnDataSource({'date': timeVectorForBB_BranchesAndBB_MA,
                                    'high': bollingerbandsUpperBound[-1],
                                    'low': bollingerbandsLowerBound[-1]})
    else:
        scaleFactor = 0.07
        source2 = ColumnDataSource({'date': t1h, 'high': ch1h, 'low': cl1h})

    def MA_show():
        numberOfMA_lines = len(MA_Vectors)
        vectorSizeOfEachMA_line = [len(MA_Vectors[0]), len(MA_Vectors[1]),
                                   len(MA_Vectors[2])]
        totalNumberOfCandles = len(t1h)
        colors = ['white', 'yellow', 'blue', 'red']

        timeVectorForMA_lines =\
            [t1h[:totalNumberOfCandles - vectorSizeOfEachMA_line[0] - 1:-1],
             t1h[:totalNumberOfCandles - vectorSizeOfEachMA_line[1] - 1:-1],
             t1h[:totalNumberOfCandles - vectorSizeOfEachMA_line[2] - 1:-1]]

        for i in range(numberOfMA_lines):
            fig.line(timeVectorForMA_lines[i], MA_Vectors[i], color=colors[i],
                     alpha=0.9, line_width=3)

        return timeVectorsFor_MA

    if show_MA == 'show_MA':
        timeVectorsFor_MA = MA_show()

        scaleFactor = 0.07
        source2 = ColumnDataSource({'date': timeVectorsFor_MA,
                                    'high': ch1h,
                                    'low': cl1h})
    else:
        scaleFactor = 0.07
        source2 = ColumnDataSource({'date': t1h, 'high': ch1h, 'low': cl1h})

    # Javascript function for scaling charts on Bokeh on both x and y range
    callback = CustomJS(args={'y_range': fig.y_range, 'source': source2,
                              'scaleFactor': scaleFactor},
                        code='''
        // clearTimeout(window._autoscale_timeout);

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
        var pad = (max - min) * scaleFactor;

        window._autoscale_timeout = setTimeout(function() {
            y_range.start = min - pad;
            y_range.end = max + pad;
        });
    ''')

    fig.x_range.js_on_change('start', callback)

    source3 = ColumnDataSource({'date': t1h, 'high': vol1h, 'low': vol_low})

    callback2 = CustomJS(args={'y_range': v.y_range, 'source': source3,
                               'scaleFactor': 0.07}, code='''
        // clearTimeout(window._autoscale_timeout);

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
        var pad = (max - min) * scaleFactor;

        window._autoscale_timeout = setTimeout(function() {
            y_range.start = min - pad;
            y_range.end = max + pad;
        });
    ''')

    # fig.add_layout(Arrow(end=OpenHead(line_color="firebrick", line_width=4),
    # x_start=t[3], y_start=7.38e-5, x_end=t[3], y_end=7.42e-5))
    v.x_range.js_on_change('start', callback2)

    layout = gridplot([[fig], [v]])
    # layout = gridplot([[fig]])

    return show(layout)


def bokehChart1d(t1d, tInc1d, tDec1d, ccDec1d, ccInc1d, coDec1d,
                   coInc1d, ch1d, cl1d, mx_indx1d, mn_indx1d):
    '''This function utilizes bokeh library to plot candlestick chart. '''
    # No. of data
    curdoc().theme = 'dark_minimal'
    # TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    fig = figure(sizing_mode='stretch_both',
                 tools="xpan,xwheel_zoom,undo,redo,reset,crosshair,save",
                 active_drag='xpan',
                 active_scroll='xwheel_zoom',
                 x_axis_type='datetime',
                 plot_width=3000,
                 plot_height=300)

    fig.xaxis.formatter = DatetimeTickFormatter(days="%m/%d", hours="%H",
                                                minutes="%H:%M")
    fig.xaxis.major_label_orientation = pi/4
    fig.grid.grid_line_alpha = 0.3
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    fig.xaxis.major_label_text_font_size = "20pt"
    fig.yaxis.major_label_text_font_size = "20pt"
    # segment:    x0,      y0,      x1,      y1
    fig.segment(t1d, ch1d, t1d, cl1d, color="white")
    # candle width
    w = 60000000
    # rectangle:     x_center, width, bottom, top
    fig.vbar(tInc1d, w, coInc1d, ccInc1d, fill_color="green")
    fig.vbar(tDec1d, w, coDec1d, ccDec1d, fill_color="red")

    cnst1 = len(mx_indx1d)
    # cnst1 = 20
    for i in range(-1, -cnst1-1, -1):
        fig.circle([t1d[mx_indx1d[i]]], [ch1d[mx_indx1d[i]]*1.0001],
                   size=40, color='blue', alpha=0.5)
        fig.text([t1d[mx_indx1d[i]]], [ch1d[mx_indx1d[i]]*1.0003],
                 [mx_indx1d[i]], text_color='white', text_font_size='24px')

    cnst2 = len(mn_indx1d)
    # cnst2 = 20
    for i in range(-1, -cnst2-1, -1):
        fig.circle([t1d[mn_indx1d[i]]], [cl1d[mn_indx1d[i]]*0.9999],
                   size=40, color='white', alpha=0.5)
        fig.text([t1d[mn_indx1d[i]]], [cl1d[mn_indx1d[i]]*0.9997],
                 [mn_indx1d[i]], text_color='white', text_font_size='24px')

    source2 = ColumnDataSource({'date': t1d, 'high': ch1d, 'low': cl1d})
    # Javascript function for scaling charts on Bokeh on both x and y range
    callback = CustomJS(args={'y_range': fig.y_range, 'source': source2},
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
        var pad = (max - min) * .15;

        window._autoscale_timeout = setTimeout(function() {
            y_range.start = min - pad;
            y_range.end = max + pad;
        });
    ''')

    fig.x_range.js_on_change('start', callback)

    # fig.add_layout(Arrow(end=OpenHead(line_color="firebrick", line_width=4),
    # x_start=t[3], y_start=7.38e-5, x_end=t[3], y_end=7.42e-5))

    # layout = gridplot([[fig], [v]])
    layout = gridplot([[fig]])

    return show(layout)
