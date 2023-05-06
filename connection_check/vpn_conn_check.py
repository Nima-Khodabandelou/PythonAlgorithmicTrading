import os
import subprocess
import re
import time

print("start monitor vpn monitor check")
expected_IP = "185.17.113.23" # ENTER YOUR EXPECTED PUBLIC IPv4 ADDRESS HERE
current_IP = subprocess.check_output(["dig", "+short", "myip.opendns.com @resolver1.opendns.com"])

try:

    while True:
        if expected_IP in str(current_IP):
            print("IPs Match - Things are normal")
        else:
            print("Current IP: " + str(current_IP) + "\nIP NOT AS EXPECTED!")
            #Code to complete actions called here
        time.sleep(5) # Change this timer to reduce/increase time between checks (seconds)
except KeyboardInterrupt:
    print("\nHard Exit Initiated. Goodbye!")