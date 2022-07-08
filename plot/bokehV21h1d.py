from bokeh.io import curdoc
from bokeh.plotting import figure, show, curdoc
from bokeh.models import (DatetimeTickFormatter, Span,
                          CustomJS, ColumnDataSource)
from bokeh.layouts import gridplot

from math import pi


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


def extrmShapeObj(fig, trendSizes, trendSize, mxIndx, mnIndx, t, cl, ch,
                  tLowerTF, objSize, objVertPosCoeff, objColor, alpha):
    ''' Shows colored circles above and below each max/min.'''

    cond3 = trendSizes[0] == '1h' and trendSize == '1d'
    cond5 = trendSizes[0] == '1h' and trendSize == '1h'
    # alpha is for color contrast
    if cond3:

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
            fig.text([t[mxIndx[i]]], [ch[mxIndx[i]]*objVertPosCoeff[0]],
                     [mxIndx[i]], text_color='white', text_font_size='16px')

        if t[-1] > tLowerTF[0]:
            indx1 = [t.index(i) for i in t if i >= tLowerTF[0]][0]
            if mnIndx[-1] > indx1:
                indx3 = [mnIndx.index(i) for i in mnIndx if i >= indx1][0]
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
            fig.text([t[mnIndx[i]]], [cl[mnIndx[i]]*objVertPosCoeff[1]],
                     [mnIndx[i]], text_color='white', text_font_size='16px')

    elif cond5:

        cnt1 = len(mxIndx)
        for i in range(0, cnt1):
            fig.square([t[mxIndx[i]]], [ch[mxIndx[i]]*objVertPosCoeff[0]],
                       size=objSize, color=objColor[1], alpha=alpha)
            fig.text([t[mxIndx[i]]], [ch[mxIndx[i]]*objVertPosCoeff[0]],
                     [mxIndx[i]],
                     text_color='white', text_font_size='16px')
        cnt2 = len(mnIndx)
        for i in range(0, cnt2):
            fig.square([t[mnIndx[i]]], [cl[mnIndx[i]]*objVertPosCoeff[1]],
                       size=objSize, color=objColor[0], alpha=alpha)
            fig.text([t[mnIndx[i]]], [cl[mnIndx[i]]*objVertPosCoeff[1]],
                     [mnIndx[i]],
                     text_color='white', text_font_size='16px')


def chart1h(t1h, ch1h, cl1h, mxIndx1h, mnIndx1h, t1d, ch1d, cl1d, mxIndx1d,
            mnIndx1d, tInc1h, tDec1h, ccInc1h, ccDec1h, coInc1h, coDec1h,
            HSRData, showExtrm, showSR, showMA, MA_Vecs1h,
            showBB):

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
    fig.segment(t1h, ch1h, t1h, cl1h, color="white", line_width=1)
    w = 2000000
    fig.vbar(tInc1h, w, coInc1h, ccInc1h, fill_color="green")
    fig.vbar(tDec1h, w, coDec1h, ccDec1h, fill_color="red")

    if showExtrm == 'showExtrm':
        trendSizes = ['1h', '1d']
        extrmShapeObj(fig, trendSizes, '1h', mxIndx1h, mnIndx1h, t1h,
                      cl1h, ch1h, t1h, 10, [1.0005, 0.9995],
                      ['white', 'yellow'],  0.9)
        extrmShapeObj(fig, trendSizes, '1d',   mxIndx1d, mnIndx1d,  t1d,
                      cl1d,  ch1d, t1h, 30, [1.001, 0.997],
                      ['blue', 'red'], 0.9)

    def sr_show():
        color = 'blue'
        for i in HSRData:
            hline = Span(location=i, dimension='width', line_color=color,
                         line_width=0.8)
            fig.add_layout(hline)

    if showSR == 'showSR':
        sr_show()

    def MA_show():
        numberOfMA_lines = len(MA_Vecs1h)
        vectorSizeOfEachMA_line = [len(MA_Vecs1h[0]),
                                   len(MA_Vecs1h[1]),
                                   len(MA_Vecs1h[2])]
        totalNumberOfCandles = len(t1h)
        colors = ['white', 'green', 'red', 'red']

        timeVectorForMA_lines =\
            [t1h[:totalNumberOfCandles - vectorSizeOfEachMA_line[0] - 1:-1],
             t1h[:totalNumberOfCandles - vectorSizeOfEachMA_line[1] - 1:-1],
             t1h[:totalNumberOfCandles - vectorSizeOfEachMA_line[2] - 1:-1]]

        for i in range(numberOfMA_lines):
            fig.line(timeVectorForMA_lines[i], MA_Vecs1h[i], color=colors[i],
                     alpha=0.9, line_width=4)

    if showMA == 'showMA':
        MA_show()

    def BB_show():
        vecSizeOfBB = len(BB_LB[0])
        totalNoOfCandles = len(t1h)
        timeVecForBB = t1h[:totalNoOfCandles - vecSizeOfBB - 1:-1]

        def drawBB(t, ma, bbLB, bbUB, color, alpha, lineWidth, lineDash):
            fig.line(t, ma, color=color[0], alpha=alpha,
                     line_width=lineWidth[0])
            fig.line(t, bbLB, color=color[1], alpha=alpha,
                     line_width=lineWidth[1], line_dash=lineDash)
            fig.line(t, bbUB, color=color[1], alpha=alpha,
                     line_width=lineWidth[1], line_dash=lineDash)

        drawBB(timeVecForBB, BB_MA[0], BB_LB[0], BB_UB[0],
               ['red', 'yellow'], 0.9, [4, 1], [6])
        drawBB(timeVecForBB, BB_MA[1], BB_LB[1], BB_UB[1],
               ['red', 'blue'], 0.9, [4, 1], [6])
        drawBB(timeVecForBB, BB_MA[2], BB_LB[2], BB_UB[2],
               ['red', 'gray'], 0.9, [4, 1], [6])

    if showBB == 'showBB':
        BB_show()

    scaleFactor = 0.12
    source2 = ColumnDataSource({'date': t1h, 'high': ch1h, 'low': cl1h})

    callback = CustomJS(args={'y_range': fig.y_range, 'source': source2,
                              'scaleFactor': scaleFactor},
                        code=JS_Callback())

    fig.x_range.js_on_change('start', callback)
    layout = gridplot([[fig]])

    return show(layout)


def chrt(t1h, ch1h, cl1h, tInc1h, tDec1h, ccInc1h, ccDec1h, coInc1h,
         coDec1h, MAs, cand_width):

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
    fig.segment(t1h, ch1h, t1h, cl1h, color="white", line_width=1)
    w = cand_width
    fig.vbar(tInc1h, w, coInc1h, ccInc1h, fill_color="green")
    fig.vbar(tDec1h, w, coDec1h, ccDec1h, fill_color="red")
    # ##############################################################
    No_ma = len(MAs)
    ma_vecs_sizes = []
    No_data = len(t1h)

    # colors = ['white', 'green', 'red', 'blue', 'gray', 'yellow']
    # lineWidth = [1, 1, 5, 5, 8, 8]
    # lineDash = [0, 0, 3, 3, 7, 7]

    colors = ['white', 'white', 'blue', 'blue', 'yellow', 'yellow',
              'red', 'red', 'gray', 'gray']
    colors = ['white', 'yellow', 'gray', 'red']
    lineWidth = [1]*No_ma
    lineDash = [0]*No_ma

    for i in range(No_ma):
        ma_vecs_sizes.append(len(MAs[i]))

    t_vecs = []

    for i in range(No_ma):
        t_vecs.append(t1h[No_data - ma_vecs_sizes[i]:No_data])

    for i in range(No_ma):
        fig.line(t_vecs[i], MAs[i], color=colors[i], alpha=0.9,
                 line_width=lineWidth[i], line_dash=[lineDash[i]])

    # ##########################################################
    # color = 'gray'
    # for i in sr:
    #     hline = Span(location=sr[i], dimension='width', line_color=color,
    #                  line_width=0.8)
    #     fig.add_layout(hline)
    # ##########################################################
    scaleFactor = 0.12
    source2 = ColumnDataSource({'date': t1h, 'high': ch1h, 'low': cl1h})

    callback = CustomJS(args={'y_range': fig.y_range, 'source': source2,
                              'scaleFactor': scaleFactor},
                        code=JS_Callback())

    fig.x_range.js_on_change('start', callback)
    layout = gridplot([[fig]])

    return show(layout)


def chrt2(t1h, ch1h, cl1h, tInc1h, tDec1h, ccInc1h, ccDec1h, coInc1h,
          coDec1h, cand_width, sr):

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
    fig.segment(t1h, ch1h, t1h, cl1h, color="white", line_width=1)
    w = cand_width
    fig.vbar(tInc1h, w, coInc1h, ccInc1h, fill_color="green")
    fig.vbar(tDec1h, w, coDec1h, ccDec1h, fill_color="red")
    # ##########################################################
    color = 'gray'
    for i in sr:
        hline = Span(location=sr[i], dimension='width', line_color=color,
                     line_width=0.8)
        fig.add_layout(hline)
    # ##########################################################
    scaleFactor = 0.12
    source2 = ColumnDataSource({'date': t1h, 'high': ch1h, 'low': cl1h})

    callback = CustomJS(args={'y_range': fig.y_range, 'source': source2,
                              'scaleFactor': scaleFactor},
                        code=JS_Callback())

    fig.x_range.js_on_change('start', callback)
    layout = gridplot([[fig]])

    return show(layout)


def chart1d(t1d, tInc1d, tDec1d, ccDec1d, ccInc1d, coDec1d,
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
    fig.segment(t1d, ch1d, t1d, cl1d, color="white")
    w = 60000000
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
    layout = gridplot([[fig]])

    return show(layout)
