from unused_codes.tech_old import HSR

def HSRList(HSR_Status1d, cl1d, ch1d, backstep, MND, asset, TS, HSR_Path,
                  HSR_file):

    if HSR_Status1d != 'D1HSRFileExist':
        HSR_Data = HSR(cl1d, ch1d, MND, backstep, asset, TS,
                                  HSR_Path, HSR_file)

        HSR_Data = [i[1] for i in HSR_Data]
    else:
        with open(HSR_Path + HSR_file) as f:
            HSR_Data = f.read().splitlines()
        HSR_Data = [float(i) for i in HSR_Data]

    return HSR_Data
