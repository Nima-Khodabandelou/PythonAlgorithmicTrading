import requests
from datetime import datetime
from requests.exceptions import (HTTPError, ConnectionError, Timeout,
                                 RequestException)


url = "https://myip.dnsomatic.com/"
with open('ip_report.txt', 'w') as f:
    while True:

        try:
            r = requests.get(url)
            r.raise_for_status()

        except HTTPError as err01:
            print("HTTP error: ", err01)
            # time.sleep(1)
            continue

        except ConnectionError as err02:
            print("Error connecting: ", err02)
            # time.sleep(1)
            continue

        except Timeout as err03:
            # time.sleep(1)
            print("Timeout error:", err03)
            continue

        except RequestException as err04:
            print("Error: ", err04)
            continue

        else:
            print(r.content)

            f.write("{0},
 {1}".format(datetime.now(),str(r.content)))
            f.write("\n")
            # time.sleep(3)
            continue
            # break
