import requests
import zipfile
import io
import os

from requests.exceptions import (HTTPError, ConnectionError, Timeout,
                                 RequestException)

import time


year1 = ["2017", "2018", "2019", "2020", "2021", "2022"]
year2 = ['2021']
month1 = ["01", "02", "03", "04", "05", "06", "07",
          "08", "09", "10", "11", "12"]
month2 = ['09']
days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
        '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22',
        '23', '24', '25', '26', '27', '28', '29', '30', '31']

base_path = "C:\\files\\algotrade\\PythonAlgorithmicTrading\\data\\"

pairs = ['SOLUSDT']
tfs = ['1m']


for s in pairs:
    if s not in os.listdir(base_path):
        os.mkdir(base_path + '\\' + s)
    for y in year2:
        for m in month2:
            for tf in tfs:
                file = "{0}-{1}-{2}-{3}.csv".format(s, tf, y, m)
                if file not in os.listdir(base_path+'//'+s+'//'):
                    url = "https://data.binance.vision/data/spot/monthly/klines/" +\
                        s + "/"+tf+"/"+s+'-'+tf+'-'+y+"-"+m+".zip"
                    while True:
                        try:
                            r = requests.get(url, timeout=5)
                            r.raise_for_status()

                        except HTTPError as err01:
                            print("HTTP error: ", err01)
                            print("{0}-{1}-{2}-{3}.zip does not exist".format(s, tf, y, m))
                            break

                        except ConnectionError as err02:
                            print("Error connecting: ", err02)
                            time.sleep(5)
                            continue

                        except Timeout as err03:
                            time.sleep(5)
                            print("Timeout error:", err03)
                            continue

                        except RequestException as err04:
                            print("Error: ", err04)
                            continue

                        else:
                            print("{0}-{1}-{2}-{3}.zip downloaded successfully".format(
                                s, tf, y, m))
                            res_time = r.elapsed.total_seconds()
                            print("response time is:", res_time)
                            z = zipfile.ZipFile(io.BytesIO(r.content))
                            z.extractall(base_path+s+"\\")
                            break
