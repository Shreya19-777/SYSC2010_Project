import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

#FFT
def plot_fft(dtype, signal_data, sampling_rate, unfiltered):
    
    freq_axis = np.fft.rfftfreq(len(signal_data), d=1/sampling_rate)

    fft_unfiltered = np.abs(np.fft.rfft(unfiltered))
    fft_filtered = np.abs(np.fft.rfft(signal_data))

    plt.figure(figsize=(24, 12))
    plt.plot(freq_axis, fft_unfiltered, label='Unfiltered signal', alpha=0.4, color='red')
    plt.plot(freq_axis, fft_filtered, label='Filtered signal', color='blue')
    plt.title("FFT of Filtered and Unfiltered Signal")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, 50)
    plt.legend()
    plt.grid(True)
    plt.show()
    