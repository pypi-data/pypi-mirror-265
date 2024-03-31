"""A package designed to kill a function after a specified amount of time."""

import multiprocessing
import time

__version__ = "1.0-rc2"
__author__ = "xyzpw"
__description__ = "A package designed to kill a function after a specified amount of time."

def timeout(seconds: int|float, err_msg: str = ""):
    def funcWrapper(func):
        def wrapper(*args, **kwargs):
            killthread = multiprocessing.Process(target=func, args=args, kwargs=kwargs, daemon=True)
            killthread.start()
            epochAtTermination = time.time() + seconds
            while time.time() < epochAtTermination:
                if not killthread.is_alive():
                    return func(*args, **kwargs)
                time.sleep(0.05)
            if killthread.is_alive():
                killthread.terminate()
                raise TimeoutError(err_msg)
            return func(*args, **kwargs)
        return wrapper
    return funcWrapper


