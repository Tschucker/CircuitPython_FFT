import array
import numpy as np
from math import sin, pi

import cp_samples
import cp_fft
import cp_ifft

#assign the fft size we want to use
fft_size = 256

#create basic data structure to hold samples
samples = array.array('f', [0] * fft_size)

#assign a sinusoid to the samples
frequency = 63  # Set this to the Hz of the tone you want to generate.
for i in range(fft_size):
    samples[i] = sin(pi * 2 * i / (fft_size/frequency))

#create complex samples
test_complex_samples = []
for n in range(fft_size):
    test_complex_samples.append(((float(samples[n]))-1 + 0.0j))

#print("samples")
#print(test_complex_samples)

np_fft = np.fft.fft(test_complex_samples)
#print("numpy fft")
#print(np_fft)

np_ifft = np.fft.ifft(np_fft)
#print("numpy ifft")
#print(np_ifft)

error = np_ifft - test_complex_samples
sum_error = np.sum(abs(error))
print("sum error numpy results")
print(sum_error)

sum_error_cp = 0
for i in range(fft_size):
    sum_error_cp = sum_error_cp + abs(cp_ifft.cp_ifft[i] - cp_samples.cp_samples[i])
print("sum error circuitpy results")
print(sum_error_cp)

sum_error_samples = 0
for i in range(fft_size):
    sum_error_samples = sum_error_samples + abs(test_complex_samples[i] - cp_samples.cp_samples[i]) 
print("sum error numpy vs circuitpy samples")
print(sum_error_samples)

error_fft = np_fft - cp_fft.cp_fft
sum_error_fft = np.sum(abs(error_fft))
print("sum error numpy vs circuitpy fft")
print(sum_error_fft)

error_ifft = np_ifft - cp_ifft.cp_ifft
sum_error_ifft = np.sum(abs(error_ifft))
print("sum error numpy vs circuitpy ifft")
print(sum_error_ifft)

#error when using cp_samples as the np.fft input
np_fft_cps = np.fft.fft(cp_samples.cp_samples)
np_ifft_cps = np.fft.ifft(np_fft_cps)

error_fft_cps = np_fft_cps - cp_fft.cp_fft
sum_error_fft_cps = np.sum(abs(error_fft_cps))
print("sum error numpy vs circuitpy fft with cp_samples")
print(sum_error_fft_cps)

error_ifft_cps = np_ifft_cps - cp_ifft.cp_ifft
sum_error_ifft_cps = np.sum(abs(error_ifft_cps))
print("sum error numpy vs circuitpy ifft with cp_samples")
print(sum_error_ifft_cps)
