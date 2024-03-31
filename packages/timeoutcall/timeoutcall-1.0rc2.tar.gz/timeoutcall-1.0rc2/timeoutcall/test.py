from timeoutcall import timeout
from time import sleep
from random import randint

if __name__ != "__main__":
    raise SystemExit(1)

@timeout(1, "error: function took too long - terminated")
def sleepTest(sleeptime):
    print("Sleeping for %s seconds, TimeoutError will be raised if timeout has been reached." % sleeptime)
    sleep(sleeptime)
    print("Function was successfully completed before timeout has occurred.\n")

@timeout(3, "error: function took too long - terminated")
def arrayTest():
    foo = []
    while True:
        foo.append(randint(0, 1000))
        print(foo)
        sleep(.5)

@timeout(2, "error: function took too long - terminated")
def returnTest(myvar):
    sleep(.5)
    return myvar

try:
    a = returnTest(":-)")
    print(a)
    sleepTest(sleeptime=float(input("sleep time: ")))
    arrayTest()
except TimeoutError as ERROR:
    print(ERROR)

