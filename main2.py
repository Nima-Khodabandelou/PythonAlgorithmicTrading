from dataManip.histDataPrep import BullBearMrks
from setInitPrms import initSetDef
import plot.bokehV21h1d as plot
from tech import ma, hsr


'''
Trading System:
    # Set a time window for HSR lookback, for instance t_w = 2000.
    # Set lrc1 and lrc2 (lrc1 > lrc2) for HSR filtering. HSRs associated with
      lrc1 could be remained forever or omitted after a certain time.
    # As trading operation advances, t_w should also move forwared leading to
      the deletion of HSRs associated with lrc2 and addition of new HSRs.
    # Find min/max pairs (extrms) prior to the starting candle within a
      time window, for instance t_w2 = 200. Take the average of price change
      percentage (pcp) of the extrms in question as a base for minimum pcp
      to identify further extrms.
'''

# ################ Initial Config #############################################
(path, asset, ts, tf, nd) = initSetDef()
# ################ Candles Params Calc ########################################
(t, tInc, tDec, cc, ch, cl, ccDec, ccInc, coDec,
 coInc) = BullBearMrks(asset, tf, ts, path, nd)[0:10]

# ############################ Horizontal Support/Ressistance #################
lrc1 = 80
lrc2 = 40
lookback = 500
cnd_start = 501
HSRs = {}
HSRs = hsr(cl, ch, cc, lrc1, HSRs, lookback, cnd_start)
HSRs = hsr(cl, ch, cc, lrc2, HSRs, lookback, cnd_start)
# ############################ PLOT ###########################################
candle_width_bokeh = [400000, 2000000]
plot.chrt(t, ch, cl, tInc, tDec, ccInc, ccDec, coInc, coDec,
          candle_width_bokeh[0], HSRs)
