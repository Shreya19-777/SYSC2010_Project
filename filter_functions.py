import fft
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from scipy import signal

def apply_filter(choice, signal_data, t, fs, unfiltered) :
    #ECG Signal:
    if choice == "ECG":
        print("Applying ECG Bandpass Filter")
        ecg_filter(fs, signal_data, t, unfiltered) 
    #Temperature:
    elif choice == "Temperature" :
        print("Applying Temperature Filter")
        filtered_temp = temp_lowpass_filter(signal_data, fs, 5, unfiltered, t)
    #Motion
    elif choice == "Motion":
        print("Applying Motion Median Filter")
    #Respiration
    elif choice == "Respiration" :
        print("Applying Respiration Filter")
           
#Applying the different filters for each type of signal
def ecg_filter(fs, signal_data, t, unfiltered) :
    
    #Using FIR to lose less data about the QRS complex in ECG signal
    #Low and highcut
    minimum = 0.5
    high = 40
    numtaps = 101
    b = signal.firwin(numtaps, [minimum, high], fs=fs, pass_zero=False, window='hamming')
    a = [1.0]
    
    filtered_ecg = signal.lfilter(b, a, signal_data)
    plt.figure(figsize=(24,8))
    plt.title("Filtered ECG Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.plot(t, filtered_ecg, color='purple')
    plt.tight_layout()
    plt.show()
    
    #Comparison between filtered and unfiltered
    plt.figure(figsize=(12,8))
    plt.title("Comparison of Filtered and Unfiltered ECG")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.plot(t, unfiltered, color='pink')
    plt.plot(t, filtered_ecg, color='purple')
    plt.show()
    
    fft.plot_fft("ECG", filtered_ecg, 1/fs, unfiltered)
    
    return filtered_ecg
    
#****************************************************Temperature**********************************************
def temp_lowpass_filter(data, fs, order, unfiltered, t):
    nyquist = 0.5 * fs
    cutoff = 0.9 * nyquist
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    lp_filtered = signal.filtfilt(b, a, data)

    plt.figure(figsize=(12,8))
    plt.title("Filtered ECG Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.plot(t, lp_filtered, color='blue')
    plt.show()
    
    #Comparison between filtered and unfiltered
    plt.figure(figsize=(12,8))
    plt.title("Comparison of Filtered and Unfiltered ECG")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.plot(t, unfiltered, color='pink')
    plt.plot(t, lp_filtered, color='blue')
    plt.show()
    
    fft.plot_fft("Temperature", lp_filtered, 1/fs, unfiltered)
    return signal.filtfilt(b, a, data)
