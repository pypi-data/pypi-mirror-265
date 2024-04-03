# Pipe stdout/stderr to TXT/HTML (Windows only)

## Tested against Windows 10 / Python 3.11 / Anaconda

### pip install outerr2html

### pip install ansi2html (if you want HTML output too)


```PY
from outerr2html import stdout_redirector, libc, config

config.enco = "utf-8"
import sys
import os
import time

with stdout_redirector(
    outfolder="c:\\htmltestoutput",
    print_stdout=True,
    print_stderr=True,
    line_limit_out=1000, # creates a new file when limit has been reached
    line_limit_err=1000,
    sleep_at_end=2,
    convert2html=False,
    sleep_between_checks=0.1,
):
    for h in range(10):
        sys.stderr.write("stderr test\n")
        sys.stderr.flush()  # necessary
        os.system("echo console test")  # won't be captured with ipython
        libc.puts(b"C test")  # won't be captured with ipython
        libc.fflush(None)  # necessary
        print("python test ")
        print(1234)
        time.sleep(1)
print("oi")  # not captured

import pandas as pd
from PrettyColorPrinter import add_printer

add_printer(1)
df = pd.read_csv(
    r"https://github.com/datasciencedojo/datasets/raw/master/titanic.csv",
    engine="python",
    on_bad_lines="skip",
    encoding="utf-8",
    encoding_errors="ignore",
)
with stdout_redirector(
    outfolder="c:\\htmltestoutput",
    print_stdout=True,
    print_stderr=True,
    line_limit_out=1000,
    line_limit_err=1000,
    sleep_at_end=2,
    convert2html=False,
    sleep_between_checks=0.1,
):
    for h in range(10):
        sys.stderr.write("stderr test\n")
        sys.stderr.flush()  # necessary
        print(df)
        os.system("echo console test")  # won't be captured with ipython
        libc.puts(b"C test")  # won't be captured with ipython
        libc.fflush(None)  # necessary
        print("python test ")
        print(1234)
        time.sleep(1)
print("oi")  # not captured
```