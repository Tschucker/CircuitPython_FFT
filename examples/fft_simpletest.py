import array
from teaandtechtime_fft import fft, ifft
from math import sin, pi

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

#compute fft of complex samples
test_fft = fft(test_complex_samples)

#compute ifft of the fft values
test_ifft = ifft(test_fft)

#print computed values for testing and verification
#print complex samples
print("samples")
for i in test_complex_samples:
    print(i)
    time.sleep(.01)

#print fft values
print("fft")
for i in test_fft:
    print(i)
    time.sleep(.01)

#print ifft values
print("ifft")
for i in test_ifft:
    print(i)
    time.sleep(.01)

#compute absolut value of the error per sample
print("error")
for i in range(fft_size):
    print(abs(test_ifft[i] - test_complex_samples[i]))
    time.sleep(.01)
