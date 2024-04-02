"""A package designed to kill a function after a specified amount of time."""

import multiprocessing
import time

__version__ = "1.0"
__author__ = "xyzpw"
__description__ = "A package designed to kill a function after a specified amount of time."

__all__ = [
    "timeout",
    "call",
]

class NewTimeoutFunction:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.queue = multiprocessing.Queue(1)
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.success = False
    def runFunction(self):
        result = self.func(*self.args, **self.kwargs)
        self.queue.put(result)
        self.success = True

def timeout(timeoutSeconds: int|float, err_msg: str = ""):
    def funcWrapper(func):
        def wrapper(*args, **kwargs):
            newFunc = NewTimeoutFunction(func, *args, **kwargs)
            epochAtTermination = time.time() + timeoutSeconds
            proc = multiprocessing.Process(target=newFunc.runFunction, daemon=True)
            proc.start()
            while epochAtTermination > time.time():
                if not proc.is_alive():
                    break
                time.sleep(1/50)
            if proc.is_alive():
                proc.terminate()
                if not newFunc.success:
                    raise TimeoutError(err_msg)
            return newFunc.queue.get()
        return wrapper
    return funcWrapper

def call(target, timeoutSeconds: int|float, err_msg: str = "", *args, **kwargs):
    """Calls a function and times out after a specified number of seconds."""
    newFunc = NewTimeoutFunction(target, *args, **kwargs)
    epochAtTermination = time.time() + timeoutSeconds
    proc = multiprocessing.Process(target=newFunc.runFunction, daemon=True)
    proc.start()
    while epochAtTermination > time.time():
        if not proc.is_alive():
            break
        time.sleep(1/50)
    if proc.is_alive():
        proc.terminate()
        if not newFunc.success:
            raise TimeoutError(err_msg)
    return newFunc.queue.get()
