# timeoutcall
A package designed to kill a function after a specified amount of time.

## Usage
Killing a function after a specified amount of time:
```python
from timeoutcall import timeout
from time import sleep

@timeout(2, "error: took too long")
def foo():
    sleep(3) # will raise TimeoutError

foo()
```
Running a test/preview:
```bash
$ python3 -m timeoutcall.test
```

## Developers
### Build and Source Distributions
To build the wheel and source distributions, cd into the repositories root directory and run the following command:
```bash
python3 -m build
```
