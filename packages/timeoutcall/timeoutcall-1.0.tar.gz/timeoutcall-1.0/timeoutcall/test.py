from timeoutcall import *
from time import sleep
from random import randint

if __name__ != "__main__":
    raise SystemExit(1)

@timeout(1, "function has slept longer than timeout time-limit")
def sleepTest(sleeptime):
    print("\nSleeping for %s seconds. Timeout time-limit is set to 1 second." % sleeptime)
    sleep(sleeptime)
    print("Function was successfully executed prior to the timeout time-limit.")

@timeout(1.5, "endless loop has been terminated")
def arrayTest():
    print("\n*The following array will be appended to within a while true loop*:\n")
    foo = []
    while True:
        foo.append(randint(0, 1000))
        print("array:", foo)
        sleep(.5)

@timeout(2, "string return took too long")
def returnTest(myvar, sleeptime):
    print("\n*Returning a string of text after %s seconds*:" % sleeptime)
    sleep(sleeptime)
    return myvar

print("""
Timeout tests have timeout time-limits of 1 and 2 seconds respectively.
NOTE: the third test will always return an error with a time-limit of 1.5 seconds.
NOTE: the third test will will start upon the completion/termination of test 2.
""")

try:
    print("**TEST 1/3: SLEEP**\n{}".format('-'*19))
    sleepTest(float(input("sleep for N seconds: ")))
except TimeoutError as ERROR:
    print("exception caught!!!:", ERROR)

print("\n")

try:
    print("**TEST 2/3: RETURNING VALUES**\n{}".format('-'*30))
    testVal = returnTest(":-)", float(input("sleep for N seconds: ")))
    print("return value:", testVal)
except TimeoutError as ERROR:
    print("exception caught!!!:", ERROR)

print("\n")

try:
    print("**TEST 3/3: WHILE LOOP**\n{}".format('-'*24))
    arrayTest()
except TimeoutError as ERROR:
    print("exception caught!!!:", ERROR)
