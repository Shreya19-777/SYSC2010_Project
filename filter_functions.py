import fft
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import find_peaks

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
        imu_lowpass_filter(signal_data, fs, 4, unfiltered, t)

    #Respiration
    elif choice == "Respiration" :
        print("Applying Respiration Filter")
        respiration_lowpass_filter(signal_data, fs, 4, unfiltered, t)
           
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
def temp_lowpass_filter(signal_data, fs, order, unfiltered, t):
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

#****************************************************Resoiration**********************************************
def respiration_lowpass_filter(signal_data, fs, order, unfiltered, t):
   #IRR lowpass filter to isolate breathing cycles
    nyquist = 0.5 * fs
    cutoff = 0.7 #standard cutoff for respiration data 
    
    if cutoff >= nyquist:
        cutoff = 0.9 * nyquist
        
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    lp_filtered = signal.filtfilt(b, a, data)
   
    plt.figure(figsize=(12,8))
    plt.title("Filtered Respiration Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.plot(t, lp_filtered, color='blue')
    plt.show()
    
    #Comparison between filtered and unfiltered
    plt.figure(figsize=(12,8))
    plt.title("Comparison of Filtered and Unfiltered Respiration")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.plot(t, unfiltered, color='pink')
    plt.plot(t, lp_filtered, color='blue')
    plt.show()
    
    fft.plot_fft("Respiration", lp_filtered, 1/fs, unfiltered)
    return lp_filtered

#****************************************************IMU**********************************************
def imu_lowpass_filter(signal_data, fs, order, unfiltered, t):
    
   # Applies an IIR Low-Pass Filter to smooth motion data.
    #Keeps movement trends while removing high-frequency jitter.
    
    nyquist = 0.5 * fs
    # Higher cutoff to capture rapid physical movements
    cutoff = 20.0 
    
    if cutoff >= nyquist:
        cutoff = 0.9 * nyquist
        
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    lp_filtered = signal.filtfilt(b, a, data)

    plt.figure(figsize=(12,8))
    plt.title("Filtered IMU Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.plot(t, lp_filtered, color='blue')
    plt.show()
    
    #Comparison between filtered and unfiltered
    plt.figure(figsize=(12,8))
    plt.title("Comparison of Filtered and Unfiltered IMU")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.plot(t, unfiltered, color='pink')
    plt.plot(t, lp_filtered, color='blue')
    plt.show()
    
    fft.plot_fft("IMU", lp_filtered, 1/fs, unfiltered)
    return lp_filtered


#Feature extraction


def extract_motion_features(lp_filtered):
    features = {
        "Mean": np.mean(lp_filtered),
        "Std Dev": np.std(lp_filtered),
        "RMS (Intensity)": np.sqrt(np.mean(lp_filtered**2)), 
        "Peak Acceleration": np.max(np.abs(lp_filtered)),   
        "Peak-to-Peak": np.ptp(lp_filtered)                 
    }
    return features

def extract_respiration_features(lp_filtered_signal, fs):
    # Required: mean, std, RMS, peak-to-peak
    mean_val = np.mean(lp_filtered_signal)
    std_val = np.std(lp_filtered_signal) 
    rms_val = np.sqrt(np.mean(lp_filtered_signal**2)) 
    ptp_range = np.ptp(lp_filtered_signal)

    # --- Signal-Specific Feature: Breathing Rate ---
    # Identify peaks in the filtered respiration signal 
    # distance=fs*1.2 ensures peaks are at least 1.2s apart (prevents double counting)
    peaks, _ = find_peaks(lp_filtered_signal, distance=fs*1.2)
    
    # Calculate Breaths Per Minute (BPM)
    num_breaths = len(peaks)
    duration_min = (len(lp_filtered_signal) / fs) / 60
    bpm = num_breaths / duration_min if duration_min > 0 else 0

    return {
        "Mean": round(mean_val, 3),
        "Std Dev": round(std_val, 3),
        "RMS": round(rms_val, 3),
        "Range": round(ptp_range, 3),
        "Breathing Rate (BPM)": round(bpm, 1)
    }