# timeoutcall
![python requires](https://img.shields.io/badge/python_requires-≥3.8-blue)
![Pepy Total Downlods](https://img.shields.io/pepy/dt/timeoutcall)
![GitHub repo size](https://img.shields.io/github/repo-size/xyzpw/timeoutcall)
![PyPI - Version](https://img.shields.io/pypi/v/timeoutcall?label=latest%20version)


A package designed to kill a function after a specified amount of time.

## Usage
> [!WARNING]
> Timeout functions are their own processes, assigning values will not do so globally.
> Using `while True: n+=1` will not increment `n` globally.

### Calling Functions
```python
from timeoutcall import call
from time import sleep

def foo(n):
    time.sleep(n) # raises TimeoutError

# given that `n` is greater than `timeoutSeconds`, an exception will occur
call(target=foo, timeoutSeconds=1, err_msg="error: took too long", n=5)
```
### Decorators
```python
from timeoutcall import timeout
from time import sleep

@timeout(2, "error: took too long")
def foo():
    sleep(3) # will raise TimeoutError

foo()
```
### Package Testing
```bash
$ python3 -m timeoutcall.test
$ python3 -m timeoutcall.testcall
```

## Developers

### Build and Source Distributions
To build the wheel and source distributions:
- cd into the repositories root directory
- run `python3 -m build`
