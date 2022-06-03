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

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
from math import pi, sin, cos, sqrt, pow, log
from adafruit_itertools.adafruit_itertools import islice, count, chain, repeat
import array

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/tschucker/Teaandtechtime_CircuitPython_FFT.git"

#Computes the complex fft of the input array needs to be power of 2 length to work.
def fft(x):
    N = len(x)
    if N <= 1: return x
    even = fft(list(islice(
        chain(x, repeat(0)),
        0, N, 2
    )))
    odd = fft(list(islice(
        chain(x, repeat(0)),
        1, N, 2
    )))
    T = [cos(2*pi*k/N)*odd[k].real+sin(2*pi*k/N)*odd[k].imag + (cos(2*pi*k/N)*odd[k].imag-sin(2*pi*k/N)*odd[k].real)*1j for k in range(N//2)]
    return [even[k].real + T[k].real + (even[k].imag + T[k].imag)*1j for k in range(N//2)] + \
           [even[k].real - T[k].real + (even[k].imag - T[k].imag)*1j for k in range(N//2)]

#Computes the complex inverse fft of the input array needs to be power of 2 length to work
#not the most efficiant but uses the same fft code.
def ifft(x):
    fft_len = float(len(x))
    x_swap = []
    for s in x:
        x_swap.append(s.imag + s.real*1j)
    temp = fft(x_swap)
    temp_swap = []
    for s in temp:
        temp_swap.append((s.imag/fft_len) + (s.real/fft_len)*1j)
    return temp_swap

#Computes the double sided spectrogram of the input array needs to be a power of 2 to work
def spectrogram(x):
    freq = fft(x)
    temp_list = []
    for f in freq:
        abs_val = abs(f)
        if  abs_val != 0.0:
            temp_list.append(int(log(abs_val)))
        else:
            temp_list.append(0)
    return temp_list

