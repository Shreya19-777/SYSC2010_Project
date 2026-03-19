#IMU and respiration data handling 
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, firwin


def handle_missing_data(signal):

    s = pd.Series(signal, dtype=float)  #convert to series for easier handling of missing data

    missing_count = s.isna().sum()
    if missing_count > 0:
        print(f"[handle_missing_data] Found {missing_count}  missing values. ")

    if s.isna().all():
        raise ValueError("Signal is entirely NaN — cannot interpolate.")

    cleaned = s.interpolate(method='linear').bfill().ffill()
    return cleaned.to_numpy() #convert back to numpy array

# remove drift for IMU
def remove_drift_IMU(signal):
    mean_val = np.mean(signal)
    return signal - mean_val

#normalization IMU
def normalize_IMU(signal):
    min_val = np.min(signal)
    max_val = np.max(signal)
    if max_val - min_val == 0:
        return signal - min_val
    return (signal - min_val) / (max_val - min_val)

#fft for IMU
def fft_IMU(signal):
    return np.fft.fft(signal)  

#filtering for IMU (IIR and FIR low-pass filters)
def filter_IMU(signal, method='iir', cutoff=5, fs=None, order=5):
    
    if fs is None:
        fs = len(signal) / total_time_in_seconds.  # rough estimate: assume 1 second of data

    signal        = np.array(signal, dtype=float)
    nyq           = 0.5 * fs
    normal_cutoff = cutoff / nyq

    if method == 'iir':
        b, a     = butter(order, normal_cutoff, btype='low', analog=False)
        filtered = filtfilt(b, a, signal)

    elif method == 'fir':
        numtaps  = order if order % 2 != 0 else order + 1  # numtaps must be odd
        coeffs   = firwin(numtaps, normal_cutoff)
        filtered = filtfilt(coeffs, 1.0, signal)

    return filtered

#feature extraction for IMU
def extract_motion_features(filtered):
    features = {
        "Mean": np.mean(filtered),
        "Std Dev": np.std(filtered),
        "RMS (Intensity)": np.sqrt(np.mean(filtered**2)), 
        "Peak Acceleration": np.max(np.abs(filtered)),   
        "Peak-to-Peak": np.ptp(filtered)                 
    }
    return features

#resporation data handling 

#removing drift for respiration data using high-pass filter
def remove_drift_respiration(signal, fs, cutoff=0.05):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(1, normal_cutoff, btype='high', analog=False)
    return filtfilt(b, a, signal)   

#normalization respiration data
def normalize_res(signal):
    min_val = np.min(signal)
    max_val = np.max(signal)
    if max_val - min_val == 0:
        return signal - min_val
    return (signal - min_val) / (max_val - min_val)

#fft for respiration data
def fft_respiration(signal):
    return np.fft.fft(signal)  

#filtering for respiration data (IIR and FIR low-pass filters)
def filter_respiration(signal, method='iir', cutoff=0.8, fs=50, order=5):

    signal        = np.array(signal, dtype=float)
    nyq           = 0.5 * fs
    normal_cutoff = cutoff / nyq

    if method == 'iir':
        b, a     = butter(order, normal_cutoff, btype='low', analog=False)
        filtered = filtfilt(b, a, signal)

    elif method == 'fir':
        numtaps  = order if order % 2 != 0 else order + 1  # numtaps must be odd
        coeffs   = firwin(numtaps, normal_cutoff)
        filtered = filtfilt(coeffs, 1.0, signal)

    return filtered

#feature extraction for IMU
def extract_respiration_features(filtered):
    features = {
        "Mean": np.mean(filtered),
        "Std Dev": np.std(filtered),
        "RMS (Intensity)": np.sqrt(np.mean(filtered**2)), 
        "Peak Acceleration": np.max(np.abs(filtered)),   
        "Peak-to-Peak": np.ptp(filtered)                 
    }
    return features
