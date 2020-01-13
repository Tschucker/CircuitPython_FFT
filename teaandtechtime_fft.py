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
import array

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/tschucker/Teaandtechtime_CircuitPython_FFT.git"

def fft(x):
    N = len(x)
    if N <= 1: return x
    even = fft(list(islice(x,0,N,2)))
    odd =  fft(list(islice(x,1,N,2)))
    T = [cos(2*pi*k/N)*odd[k].real+sin(2*pi*k/N)*odd[k].imag + (cos(2*pi*k/N)*odd[k].imag-sin(2*pi*k/N)*odd[k].real)*1j for k in range(N//2)]
    return [even[k].real + T[k].real + (even[k].imag + T[k].imag)*1j for k in range(N//2)] + \
           [even[k].real - T[k].real + (even[k].imag - T[k].imag)*1j for k in range(N//2)]

def cmplx_abs(x):
    return sqrt(pow(x.real,2) + pow(x.imag,2))

def spectrogram(x):
    freq = fft(x)
    temp_list = []
    for f in freq:
        abs_val = cmplx_abs(f)
        if  abs_val != 0.0:
            temp_list.append(int(log(abs_val)))
        else:
            temp_list.append(0)
    return temp_list

def ifft(x):
    for s in x:
        s = (s.imag + s.real*1j)
    temp = fft(x)
    for s in temp:
        s = (s.imag + s.real*1j)/float(len(x))
    return temp

