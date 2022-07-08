from datetime import datetime as dtm
import MetaTrader5 as mt5


def weekDataIFCM(asset):
    '''This function gets data from IFCM terminal.'''
    startTime = dtm(2020, 1, 28, 13)
    # connect to MetaTrader 5
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    # request connection status and parameters
    print(mt5.terminal_info())
    # get data on MetaTrader 5 version
    print(mt5.version())

    # get bars from different symbols in a number of ways
    weekdata = mt5.copy_rates_from(asset, mt5.TIMEFRAME_W1, startTime, 1000)

    return weekdata
