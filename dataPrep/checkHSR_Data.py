import os


def chkAssetHSR(asset, base_path, TS, MND):
    
    HSRFilePath = base_path + asset + '\\cumulative_data\\'
    files = os.listdir(HSRFilePath)
    HSRFileName = asset + '_sr'+TS+'_mnd_'+'0'\
        + str(int(MND*100))+'.txt'
    if HSRFileName in files:
        D1HSRFileStatus = 'HSRFileForD1Exist'
    else:
        D1HSRFileStatus = 'HSRFileForD1NotExist'

    return D1HSRFileStatus, HSRFileName, HSRFilePath
