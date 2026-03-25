import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import find_peaks

#Feature extraction

def extract_ecg_features(filtered) :
    peaks, _ = signal.find_peaks(filtered, height = 1.0, distance = 100)
    #HR estimation calculations
    rr_intervals = np.diff(peaks) / 360
    heart_rate = 60 / np.mean(rr_intervals)

    features = {
        "Mean": np.mean(filtered),
        "Std Dev": np.std(filtered),
        "RMS": np.sqrt(np.mean(filtered**2)), 
        "Peak Acceleration": np.max(np.abs(filtered)),   
        "Peak-to-Peak": np.ptp(filtered),
        "Heart Rate": heart_rate                 
    }
    return features

def extract_temp_features(filtered) :
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

    return {
        "Mean": round(mean_val, 3),
        "Std Dev": round(std_val, 3),
        "RMS": round(rms_val, 3),
        "Range": round(ptp_range, 3),
        "Breathing Rate (BPM)": round(bpm, 1)
    }