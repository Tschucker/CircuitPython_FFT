# The MIT License (MIT)
#
# Copyright (c) 2019 Tom Schucker for Tea and Tech Time
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`teaandtechtime_fft`
================================================================================

CircuitPython FFT Library


* Author(s): Tom Schucker

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s). Use unordered list & hyperlink rST
   inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports
from math import pi, sin, cos, sqrt, pow, log
from adafruit_itertools import islice, count

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/tschucker/Teaandtechtime_CircuitPython_FFT.git"


def cpy_fft(x):
    N = len(x)
    if N <= 1: return x
    even = cpy_fft(list(islice(x,0,N,2)))
    odd =  cpy_fft(list(islice(x,1,N,2)))
    T = [(cos(2*pi*k/N)*odd[k][0]+sin(2*pi*k/N)*odd[k][1], cos(2*pi*k/N)*odd[k][1]-sin(2*pi*k/N)*odd[k][0]) for k in range(N//2)]
    return [(even[k][0] + T[k][0], even[k][1] + T[k][1]) for k in range(N//2)] + \
           [(even[k][0] - T[k][0] , even[k][1] - T[k][1]) for k in range(N//2)]

def cpy_abs(x):
    return sqrt(pow(x[0],2) + pow(x[1],2))

def spectro(x):
    freq = cpy_fft(x)
    temp_list = []
    for f in freq:
        abs_val = cpy_abs(f)
        if  abs_val != 0.0:
            temp_list.append(int(log(abs_val)))
        else:
            temp_list.append(0)

    return temp_list
