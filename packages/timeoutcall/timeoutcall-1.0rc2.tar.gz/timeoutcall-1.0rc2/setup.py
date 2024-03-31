import setuptools
import timeoutcall

def readme():
    with open("README.md", "r") as f:
        return f.read()


setuptools.setup(
    name="timeoutcall",
    version=timeoutcall.__version__,
    author=timeoutcall.__author__,
    maintainer=timeoutcall.__author__,
    description=timeoutcall.__description__,
    url="https://github.com/xyzpw/timeoutcall/",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.8",
    license="MIT",
)
