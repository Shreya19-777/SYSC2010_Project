import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import find_peaks

#*********************************************FFT**********************************************88
def plot_fft(dtype, signal_data, sampling_rate, unfiltered):

    #
    N = len(signal_data)
    period = 1.0 / sampling_rate
    
    freq_axis = np.fft.rfftfreq(N, d=period)

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

#***************************************Feature extraction****************************************8

def extract_ecg_features(filtered, fs) :
    
    #Calculating the heart rate
    height_threshold = np.percentile(filtered, 95)

    peaks, _ = signal.find_peaks(filtered, height=height_threshold, distance=fs/3)

    if len(peaks) > 1:
        rr_intervals = np.diff(peaks) / 360
        heart_rate = 60 / np.mean(rr_intervals)
    else:
        #In the case of an error set heaartrate to 0 to avoid NaN
        print("Error with heart rate calculation")
        heart_rate = 0

    features = {
        "Mean": np.mean(filtered),
        "Std Dev": np.std(filtered),
        "RMS": np.sqrt(np.mean(filtered**2)), 
        "Peak Acceleration": np.max(np.abs(filtered)),   
        "Peak-to-Peak": np.ptp(filtered),
        "RR intervals": rr_intervals,
        "Heart Rate": heart_rate                 
    }
    return features

def extract_temp_features(filtered, fs) :
    features = {
        "Mean": np.mean(filtered),
        "Std Dev": np.std(filtered),
        "RMS": np.sqrt(np.mean(filtered**2)), 
        "Peak Acceleration": np.max(np.abs(filtered)),   
        "Peak-to-Peak": np.ptp(filtered)             
    }
    return features

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

    # --- Breathing Rate ---
    peaks, _ = find_peaks(lp_filtered_signal, distance=fs*1.2)
    
    # Calculate Breaths Per Minute (BPM)
    num_breaths = len(peaks)
    duration_min = (len(lp_filtered_signal) / fs) / 60
    bpm = num_breaths / duration_min if duration_min > 0 else 0

    features = {
        "Mean": round(mean_val, 3),
        "Std Dev": round(std_val, 3),
        "RMS": round(rms_val, 3),
        "Range": round(ptp_range, 3),
        "Breathing Rate (BPM)": round(bpm, 1)
    }
    
    return features