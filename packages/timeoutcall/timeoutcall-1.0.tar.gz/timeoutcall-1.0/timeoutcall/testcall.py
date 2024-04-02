
if __name__ != "__main__":
    raise SystemExit(1)

import timeoutcall
import time

def lol(xD: int|float):
    time.sleep(xD)
    print("Function was successfully executed prior to the timeout time-limit.\n")

def endlessCount():
    print("*while true*")
    while True:
        print("endless loop")
        time.sleep(.5)

print("""
Test functions have a timeout time-limit of 3 and 2 seconds respectively.
The latter function will always raise an exception.
""")

try:
    timeoutcall.call(lol, 3, "function slept too long", int(input("sleep time: ")))
except TimeoutError as ERROR:
    print("exception caught!!!:", ERROR)
try:
    timeoutcall.call(endlessCount, 2, "timeout time-limit reached")
except TimeoutError as ERROR:
    print("exception caught!!!:", ERROR)