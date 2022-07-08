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


def JS_Callback():
    code = '''
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
    '''

    return code


def showExtrmShapeObj(fig, trendSizes, trendSize, mxIndx, mnIndx, t, cl, ch,
                      tLowerTF, objSize, objVertPosCoeff, objColor, alpha):
    ''' Shows colored circles above and below each max/min.'''
    cond1 = trendSizes[0] == 'Def' and trendSize == '1h'
    cond2 = trendSizes[0] == 'Def' and trendSize == '1d'
    cond3 = trendSizes[0] == '1h' and trendSize == '1d'
    cond4 = trendSizes[0] == 'Def' and trendSize == 'Def'
    cond5 = trendSizes[0] == '1h' and trendSize == '1h'
    # alpha is for color contrast
    if cond1 or cond2 or cond3:

        cnt1 = len(mxIndx)
        cnt2 = len(mnIndx)

        if t[-1] > tLowerTF[0]:
            indx1 = [t.index(i) for i in t if i >= tLowerTF[0]][0]
            if mxIndx[-1] > indx1:
                indx2 = [mxIndx.index(i) for i in mxIndx if i >= indx1][0]
            else:
                indx2 = cnt1
        else:
            indx2 = cnt1

        if trendSize == '1d':
            indx2 -= 0
        elif trendSize == '1h':
            indx2 -= 0
        # indx2 = 0
        for i in range(indx2, cnt1):
            fig.circle([t[mxIndx[i]]], [ch[mxIndx[i]]*objVertPosCoeff[0]],
                       size=objSize, color=objColor[1], alpha=alpha)
            # if cond2 or cond3:
            fig.text([t[mxIndx[i]]], [ch[mxIndx[i]]*1.0003], [mxIndx[i]],
                     text_color='white', text_font_size='24px')

        if t[-1] > tLowerTF[0]:
            indx1 = [t.index(i) for i in t if i >= tLowerTF[0]][0]
            if mnIndx[-1] > indx1:
                indx3 =  [mnIndx.index(i) for i in mnIndx if i >= indx1][0]
            else:
                indx3 = cnt2
        else:
            indx3 = cnt2

        if trendSize == '1d':
            indx3 -= 0
        elif trendSize == '1h':
            indx3 -= 0
        # indx3 = 0
        for i in range(indx3, cnt2):
            fig.circle([t[mnIndx[i]]], [cl[mnIndx[i]]*objVertPosCoeff[1]],
                       size=objSize, color=objColor[0], alpha=alpha)
            # if cond2 or cond3:
            fig.text([t[mnIndx[i]]], [cl[mnIndx[i]]*0.9997], [mnIndx[i]],
                     text_color='white', text_font_size='24px')

    elif cond4 or cond5:

        cnt1 = len(mxIndx)
        for i in range(0, cnt1):
            fig.square([t[mxIndx[i]]], [ch[mxIndx[i]]*objVertPosCoeff[0]],
                       size=objSize, color=objColor[1], alpha=alpha)
            fig.text([t[mxIndx[i]]], [ch[mxIndx[i]]*1.0003],
                     [mxIndx[i]],
                     text_color='white', text_font_size='24px')
        cnt2 = np.shape(mnIndx)[0]
        for i in range(0, cnt2):
            fig.square([t[mnIndx[i]]], [cl[mnIndx[i]]*objVertPosCoeff[1]],
                       size=objSize, color=objColor[0], alpha=alpha)
            fig.text([t[mnIndx[i]]], [cl[mnIndx[i]]*0.9997],
                     [mnIndx[i]],
                     text_color='white', text_font_size='24px')


def bokehChartDef(tDef, chDef, clDef, mxIndxDef, mnIndxDef,
                  t1d, ch1d, cl1d, mxIndx1d, mnIndx1d,
                  incDef, decDef,
                  tIncDef, tDecDef,
                  ccIncDef, ccDecDef, coIncDef, coDecDef,
                  volDef, volIncDef, volDecDef,
                  BB_MA_Def, BB_UB_Def, BB_LB_Def,
                  HSRData,
                  t1h, ch1h, cl1h, mxIndx1h, mnIndx1h,
                  BB_MA1h, BB_UB1h, BB_LB1h,
                  MA_Vecs,
                  showExtrm, showMA, showVol, showSR, showBB_Def, showBB1h):

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
    w = 500000
    # rectangle:     x_center, width, bottom, top
    fig.vbar(tIncDef, w, coIncDef, ccIncDef, fill_color="green")
    fig.vbar(tDecDef, w, coDecDef, ccDecDef, fill_color="red")

    v = figure(# sizing_mode='stretch_both',
                tools="xpan,xwheel_zoom,undo,redo,reset,crosshair,save",
                active_drag='xpan',
                active_scroll='xwheel_zoom',
                x_axis_type='datetime',
                x_range=fig.x_range,
                # y_range=fig.y_range,
                plot_width=fig.plot_width,
                plot_height=300)

    if showExtrm == 'showExtrm':
        trendSizes = ['Def', '1h', '1d']
        showExtrmShapeObj(fig, trendSizes, 'Def', mxIndxDef, mnIndxDef, tDef,
                          clDef, chDef, tDef, 15, [1.0020, 0.9980],
                          ['white', 'darkolivegreen'],  0.9)
        showExtrmShapeObj(fig, trendSizes, '1h',   mxIndx1h, mnIndx1h,  t1h,
                          cl1h,  ch1h, tDef, 25, [1.0001, 0.9999],
                          ['blue', 'yellow'], 0.9)
        showExtrmShapeObj(fig, trendSizes, '1d',   mxIndx1d, mnIndx1d,  t1d,
                          cl1d,  ch1d, tDef, 40, [1.0001, 0.9999],
                          ['red', 'gray'], 0.9)

    def volShow():
        ''' Prepare the data and figures for plot of volume bars on Bokeh. '''
        v_max = max(volDef)
        scaled_vol = [i/v_max for i in volDef]
        scaled_vol = volDef
        vol_inc_norm = [scaled_vol[i] for i in incDef]
        vol_dec_norm = [scaled_vol[i] for i in decDef]
        vol_min = min(scaled_vol)
        vol_min = min(volDef)
        vol_min = 0

        global volLow
        rows = len(volDef)
        volLow = [vol_min]*rows

        v.xaxis.major_label_orientation = pi/4
        v.grid.grid_line_alpha = 0.3
        v.vbar(tIncDef, w, [vol_min]*len(volIncDef), vol_inc_norm)
        v.vbar(tDecDef, w, [vol_min]*len(volDecDef), vol_dec_norm)

    if showVol == 'showVol':
        volShow()

    def sr_show():
        color = 'blue'
        for i in HSRData:
            hline = Span(location=i, dimension='width', line_color=color,
                         line_width=3)
            fig.add_layout(hline)

    if showSR == 'showSR':
        sr_show()

    def BB_show(Tf, t, BB_MA, BB_LB, BB_UB):
        numberOfBB_Branches = len(BB_LB)
        vecSizeOfEachBB_Branch = len(BB_LB[0])
        NoOfCandles = len(t)
        boundColors = ['white', 'yellow', 'gray']
        MA_Colors = ['green', 'red', 'red', 'red']

        timeVecForBB_BranchesAndBB_MA =\
            t[:NoOfCandles - vecSizeOfEachBB_Branch - 1:-1]

        if Tf == '1h':
            lineDash = [[7], [7], [7]]
        else:
            lineDash = [[], [], []]

        # lineDash = [[], [7], [7]]
        lineWidth = [2, 1, 1]

        for i in range(numberOfBB_Branches):
            if Tf == 'Def':
                fig.line(timeVecForBB_BranchesAndBB_MA, BB_MA[i],
                         color=MA_Colors[i], alpha=0.9, line_width=3)
            else:
                fig.line(timeVecForBB_BranchesAndBB_MA, BB_MA[i],
                         color=MA_Colors[i+1], alpha=0.9, line_width=6)

            fig.line(timeVecForBB_BranchesAndBB_MA, BB_LB[i],
                     color=boundColors[i], alpha=0.9, line_width=lineWidth[i],
                     line_dash=lineDash[i])
            fig.line(timeVecForBB_BranchesAndBB_MA, BB_UB[i],
                     color=boundColors[i], alpha=0.9, line_width=lineWidth[i],
                     line_dash=lineDash[i])

        return timeVecForBB_BranchesAndBB_MA

    if showBB_Def == 'showBB_Def':
        timeVecForBB_BranchesAndBB_MA = BB_show('Def', tDef, BB_MA_Def,
                                                BB_LB_Def, BB_UB_Def)

        # scaleFactor = 0.07
        # source1 = ColumnDataSource({'date': timeVecForBB_BranchesAndBB_MA,
        #                             'high': BB_UB_Def[-1],
        #                             'low': BB_LB_Def[-1]})
    # if showBB1h == 'showBB1h':
    #     timeVecForBB_BranchesAndBB_MA = BB_show('1h', t1h, BB_MA1h, BB_LB1h,
    #                                             BB_UB1h)

        # scaleFactor = 0.07
        # source2 = ColumnDataSource({'date': timeVecForBB_BranchesAndBB_MA,
        #                             'high': BB_UB1h[-1],
        #                             'low': BB_LB1h[-1]})
    # else:
    #     scaleFactor = 0.07
    #     source3 = ColumnDataSource({'date': tDef, 'high': chDef, 'low': clDef})

    scaleFactor = 0.15
    source4 = ColumnDataSource({'date': tDef, 'high': chDef, 'low': clDef})

    def MA_show():
        numberOfMA_lines = len(MA_Vecs)
        vectorSizeOfEachMA_line = [len(MA_Vecs[0]), len(MA_Vecs[1])]

        totalNumberOfCandles = len(tDef)
        colors = ['white', 'yellow', 'blue', 'red']
        lineWidth = [1, 2, 3, 4, 5]

        timeVectorForMA_lines =\
            [tDef[:totalNumberOfCandles - vectorSizeOfEachMA_line[0] - 1:-1],
             tDef[:totalNumberOfCandles - vectorSizeOfEachMA_line[1] - 1:-1]]

        for i in range(numberOfMA_lines):
            fig.line(timeVectorForMA_lines[i], MA_Vecs[i], color=colors[i],
                     alpha=0.9, line_width=lineWidth[i])

    if showMA == 'showMA':
        MA_show()

    # Javascript function for scaling charts on Bokeh on both x and y range
    callback1 = CustomJS(args={'y_range': fig.y_range, 'source': source4,
                               'scaleFactor': scaleFactor}, code=JS_Callback())

    fig.x_range.js_on_change('start', callback1)

    # source5 = ColumnDataSource({'date': tDef, 'high': volDef, 'low': volLow})

    # callback2 = CustomJS(args={'y_range': v.y_range, 'source': source5,
    #                            'scaleFactor': scaleFactor}, code=JS_Callback())

    # v.x_range.js_on_change('start', callback2)

    # layout = gridplot([[fig], [v]])
    layout = gridplot([[fig]])

    return show(layout)


def bokehChart1h(t1h, ch1h, cl1h, mxIndx1h, mnIndx1h, t1d, ch1d, cl1d,
                 mxIndx1d, mnIndx1d, inc1h, dec1h, tInc1h, tDec1h, ccInc1h,
                 ccDec1h, coInc1h, coDec1h, vol1h, volInc1h, volDec1h,
                 HSRData,
                 BB_MA, BB_LB, BB_UB,
                 # MA_Vectors,
                 showExtrm, showVol, showSR, showBB, showMA):

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

    if showExtrm == 'showExtrm':
        trendSizes = ['1h', '1d']
        showExtrmShapeObj(fig, trendSizes, '1h', mxIndx1h, mnIndx1h, t1h,
                          cl1h, ch1h, t1h, 15, [1.004, 0.993],
                          ['white', 'darkolivegreen'],  0.9)
        showExtrmShapeObj(fig, trendSizes, '1d',   mxIndx1d, mnIndx1d,  t1d,
                          cl1d,  ch1d, t1h, 25, [1.0001, 0.9999],
                          ['green', 'red'], 0.9)

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

    if showVol == 'showVol':
        volume_graph_show()

    def sr_show():
        color = 'blue'
        for i in HSRData:
            hline = Span(location=i, dimension='width', line_color=color,
                         line_width=0.8)
            fig.add_layout(hline)

    if showSR == 'showSR':
        sr_show()

    def BB_show():
        # numberOfBB_Branches = len(BB_LB)
        vecSizeOfBB1 = len(BB_LB[0])
        vecSizeOfBB2and3 = len(BB_UB[1])
        totalNoOfCandles = len(t1h)

        timeVecForBB1 = t1h[:totalNoOfCandles - vecSizeOfBB1 - 1:-1]
        timeVecForBB2and3 = t1h[:totalNoOfCandles - vecSizeOfBB2and3 - 1:-1]

        def drawBB(t, ma, bbLB, bbUB, color, alpha, lineWidth, lineDash):
            fig.line(t, ma, color=color[0], alpha=alpha,
                     line_width=lineWidth[0])
            fig.line(t, bbLB, color=color[1], alpha=alpha,
                     line_width=lineWidth[1], line_dash=lineDash)
            fig.line(t, bbUB, color=color[1], alpha=alpha,
                     line_width=lineWidth[1], line_dash=lineDash)

        drawBB(timeVecForBB1, BB_MA[0], BB_LB[0], BB_UB[0],
               ['yellow', 'blue'], 0.9, [5, 6], [5])
        drawBB(timeVecForBB2and3, BB_MA[1], BB_LB[1], BB_UB[1],
               ['yellow', 'blue'], 0.9, [5, 6], [5])
        drawBB(timeVecForBB2and3, BB_MA[2], BB_LB[2], BB_UB[2],
               ['yellow', 'blue'], 0.9, [5, 6], [5])

        drawBB(timeVecForBB2and3, BB_MA[3], BB_LB[3], BB_UB[3],
               ['yellow', 'white'], 0.9, [5, 6], [5])
        drawBB(timeVecForBB2and3, BB_MA[4], BB_LB[4], BB_UB[4],
               ['yellow', 'white'], 0.9, [5, 6], [5])
        drawBB(timeVecForBB1, BB_MA[5], BB_LB[5], BB_UB[5],
               ['yellow', 'white'], 0.9, [5, 6], [5])

        drawBB(timeVecForBB2and3, BB_MA[6], BB_LB[6], BB_UB[6],
               ['yellow', 'red'], 0.9, [5, 6], [5])
        drawBB(timeVecForBB2and3, BB_MA[7], BB_LB[7], BB_UB[7],
               ['yellow', 'red'], 0.9, [5, 6], [5])
        drawBB(timeVecForBB2and3, BB_MA[8], BB_LB[8], BB_UB[8],
               ['yellow', 'red'], 0.9, [5, 6], [5])

        drawBB(timeVecForBB2and3, BB_MA[9], BB_LB[9], BB_UB[9],
               ['yellow', 'green'], 0.9, [5, 6], [5])

    if showBB == 'showBB':
        BB_show()

    #     timeVectorForBB_BranchesAndBB_MA = BB_show()

    #     scaleFactor = 0.07
    #     source2 = ColumnDataSource({'date': timeVectorForBB_BranchesAndBB_MA,
    #                                 'high': bollingerbandsUpperBound[-1],
    #                                 'low': bollingerbandsLowerBound[-1]})
    # else:
    #     scaleFactor = 0.07
    #     source2 = ColumnDataSource({'date': t1h, 'high': ch1h, 'low': cl1h})

    def MA_show():
        numberOfMA_lines = len(MA_Vectors)
        vectorSizeOfEachMA_line = [len(MA_Vectors[0]), len(MA_Vectors[1]),
                                   len(MA_Vectors[2]), len(MA_Vectors[3])]
        totalNumberOfCandles = len(t1h)
        colors = ['red', 'yellow', 'white', 'gray']

        timeVectorForMA_lines =\
            [t1h[:totalNumberOfCandles - vectorSizeOfEachMA_line[0] - 1:-1],
             t1h[:totalNumberOfCandles - vectorSizeOfEachMA_line[1] - 1:-1],
             t1h[:totalNumberOfCandles - vectorSizeOfEachMA_line[2] - 1:-1],
             t1h[:totalNumberOfCandles - vectorSizeOfEachMA_line[3] - 1:-1]]

        for i in range(numberOfMA_lines):
            fig.line(timeVectorForMA_lines[i], MA_Vectors[i], color=colors[i],
                     alpha=0.9, line_width=5)

        # return timeVectorsFor_MA

    if showMA == 'showMA':
        MA_show()
    #     timeVectorsFor_MA = MA_show()

    #     scaleFactor = 0.07
    #     source2 = ColumnDataSource({'date': timeVectorsFor_MA,
    #                                 'high': ch1h,
    #                                 'low': cl1h})
    # else:
    scaleFactor = 0.12
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

    # source3 = ColumnDataSource({'date': t1h, 'high': vol1h, 'low': vol_low})

    # callback2 = CustomJS(args={'y_range': v.y_range, 'source': source3,
    #                            'scaleFactor': 0.07}, code='''
    #     // clearTimeout(window._autoscale_timeout);

    #     var date = source.data.date,
    #         low = source.data.low,
    #         high = source.data.high,
    #         start = cb_obj.start,
    #         end = cb_obj.end,
    #         min = Infinity,
    #         max = -Infinity;

    #     for (var i=0; i < date.length; ++i) {
    #         if (start <= date[i] && date[i] <= end) {
    #             max = Math.max(high[i], max);
    #             min = Math.min(low[i], min);
    #         }
    #     }
    #     var pad = (max - min) * scaleFactor;

    #     window._autoscale_timeout = setTimeout(function() {
    #         y_range.start = min - pad;
    #         y_range.end = max + pad;
    #     });
    # ''')

    # # fig.add_layout(Arrow(end=OpenHead(line_color="firebrick", line_width=4),
    # # x_start=t[3], y_start=7.38e-5, x_end=t[3], y_end=7.42e-5))

    # v.x_range.js_on_change('start', callback2)

    # layout = gridplot([[fig], [v]])

    layout = gridplot([[fig]])

    return show(layout)


def bokehChart1d(t1d, tInc1d, tDec1d, ccDec1d, ccInc1d, coDec1d,
                 coInc1d, ch1d, cl1d, mx_indx1d, mn_indx1d,
                 # MA_Vecs,
                 BB_MA, BB_LB, BB_UB,
                 showMA, showBB):
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

    def MA_show():

        totalNumberOfCandles = len(t1d)
        colors = ['white', 'yellow', 'blue', 'red', 'green', 'gray']

        timeVectorForMA_line1 =\
            t1d[:totalNumberOfCandles - len(MA_Vecs[0]) - 1:-1]
        timeVectorForMA_line2 =\
            t1d[:totalNumberOfCandles - len(MA_Vecs[1]) - 1:-1]
        timeVectorForMA_line3 =\
            t1d[:totalNumberOfCandles - len(MA_Vecs[2]) - 1:-1]
        timeVectorForMA_line4 =\
            t1d[:totalNumberOfCandles - len(MA_Vecs[3]) - 1:-1]
        timeVectorForMA_line5 =\
            t1d[:totalNumberOfCandles - len(MA_Vecs[4]) - 1:-1]
        timeVectorForMA_line6 =\
            t1d[:totalNumberOfCandles - len(MA_Vecs[5]) - 1:-1]

        fig.line(timeVectorForMA_line1, MA_Vecs[0], color=colors[0],
                 alpha=0.9, line_width=3)
        fig.line(timeVectorForMA_line2, MA_Vecs[1], color=colors[1],
                 alpha=0.9, line_width=3)
        fig.line(timeVectorForMA_line3, MA_Vecs[2], color=colors[2],
                 alpha=0.9, line_width=3)
        fig.line(timeVectorForMA_line4, MA_Vecs[3], color=colors[3],
                 alpha=0.9, line_width=3)
        fig.line(timeVectorForMA_line5, MA_Vecs[4], color=colors[4],
                 alpha=0.9, line_width=3)
        fig.line(timeVectorForMA_line6, MA_Vecs[5], color=colors[5],
                 alpha=0.9, line_width=3)

    if showMA == 'showMA':
        MA_show()

    def BB_show():
        # numberOfBB_Branches = len(BB_LB)
        vecSizeOfBB1 = len(BB_LB[0])
        vecSizeOfBB2and3 = len(BB_UB[1])
        totalNoOfCandles = len(t1d)

        timeVecForBB1 = t1d[:totalNoOfCandles - vecSizeOfBB1 - 1:-1]
        timeVecForBB2and3 = t1d[:totalNoOfCandles - vecSizeOfBB2and3 - 1:-1]

        def drawBB(t, ma, bbLB, bbUB, color, alpha, lineWidth, lineDash):
            fig.line(t, ma, color=color[0], alpha=alpha,
                     line_width=lineWidth[0])
            fig.line(t, bbLB, color=color[1], alpha=alpha,
                     line_width=lineWidth[1], line_dash=lineDash)
            fig.line(t, bbUB, color=color[1], alpha=alpha,
                     line_width=lineWidth[1], line_dash=lineDash)

        drawBB(timeVecForBB1, BB_MA[0], BB_LB[0], BB_UB[0],
               ['yellow', 'blue'], 0.9, [5, 6], [5])
        drawBB(timeVecForBB2and3, BB_MA[1], BB_LB[1], BB_UB[1],
               ['yellow', 'blue'], 0.9, [5, 6], [5])
        drawBB(timeVecForBB2and3, BB_MA[2], BB_LB[2], BB_UB[2],
               ['yellow', 'blue'], 0.9, [5, 6], [5])

        drawBB(timeVecForBB2and3, BB_MA[3], BB_LB[3], BB_UB[3],
               ['yellow', 'white'], 0.9, [5, 6], [5])
        drawBB(timeVecForBB2and3, BB_MA[4], BB_LB[4], BB_UB[4],
               ['yellow', 'white'], 0.9, [5, 6], [5])
        drawBB(timeVecForBB1, BB_MA[5], BB_LB[5], BB_UB[5],
               ['yellow', 'white'], 0.9, [5, 6], [5])

        drawBB(timeVecForBB2and3, BB_MA[6], BB_LB[6], BB_UB[6],
               ['yellow', 'red'], 0.9, [5, 6], [5])
        drawBB(timeVecForBB2and3, BB_MA[7], BB_LB[7], BB_UB[7],
               ['yellow', 'red'], 0.9, [5, 6], [5])
        drawBB(timeVecForBB2and3, BB_MA[8], BB_LB[8], BB_UB[8],
               ['yellow', 'red'], 0.9, [5, 6], [5])

        drawBB(timeVecForBB2and3, BB_MA[9], BB_LB[9], BB_UB[9],
               ['yellow', 'green'], 0.9, [5, 6], [5])
        drawBB(timeVecForBB2and3, BB_MA[10], BB_LB[10], BB_UB[10],
               ['yellow', 'green'], 0.9, [5, 6], [5])
        drawBB(timeVecForBB2and3, BB_MA[11], BB_LB[11], BB_UB[11],
               ['yellow', 'green'], 0.9, [5, 6], [5])

    if showBB == 'showBB':
        BB_show()

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
