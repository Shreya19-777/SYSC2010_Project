import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from scipy import signal

#FFT
def plot_fft(dtype, signal_data, sampling_rate, unfiltered):
    
    freq_axis = np.fft.rfftfreq(len(signal_data), d=1/sampling_rate)
    filtered_fft = np.fft.rfft(signal_data)
    unfiltered_fft = np.fft.rfft(unfiltered)
    
    filtered_magnitude = np.abs(filtered_fft)
    unfiltered_magnitude = np.abs(unfiltered_fft)
    
    plt.figure(figsize=(12, 6))
    plt.plot(freq_axis, unfiltered_magnitude, label='Unfiltered signal', alpha=0.4, color='red')
    plt.plot(freq_axis, filtered_magnitude, label='Filtered signal', color='teal')
    plt.title(f"FFT of Filtered {dtype} Signal")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, 60)
    plt.legend()
    plt.grid(True)
    plt.show()