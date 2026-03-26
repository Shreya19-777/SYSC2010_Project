import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

#FFT
def plot_fft(dtype, signal_data, sampling_rate, unfiltered):
    
    print(sampling_rate)
    
    N = len(signal_data)
    T = 1.0 / sampling_rate
    
    freq_axis = np.fft.rfftfreq(N, d=T)

    fft_unfiltered = (np.abs(np.fft.rfft(unfiltered)) / N) * 2
    fft_filtered = (np.abs(np.fft.rfft(signal_data)) / N) * 2
    
    plt.figure(figsize=(12, 8))
    plt.plot(freq_axis, fft_unfiltered, label='Unfiltered signal', alpha=0.4, color='red')
    plt.plot(freq_axis, fft_filtered, label='Filtered signal', color='blue')

#adjust y-axis limits to better visualize differences
    max_amp = max(np.max(fft_unfiltered), np.max(fft_filtered))
    plt.ylim(0, max_amp * 1.2)
    
    if dtype == "Respiration":
        plt.xlim(0, 2)
    elif dtype == "ECG":
        plt.xlim(0, 10)
    elif dtype == "Temperature":
        plt.xlim(0, 0.5)
    else:
        plt.xlim(0, 50)
        
    plt.title("Frequency Domain Analysis")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude") 
    plt.legend()
    plt.grid(True)
    plt.show()
