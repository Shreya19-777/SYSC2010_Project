import matplotlib.pyplot as plt
from scipy import signal
from tkinter import messagebox

#File imports
import analysis

def apply_filter(choice, signal_data, t, fs, unfiltered) :
    #ECG Signal:
    if choice == "ECG":
        print("Applying ECG Bandpass Filter")
        pack = ecg_filter(fs, signal_data, t, unfiltered) 
        return pack
    #Temperature:
    elif choice == "Temperature" :
        print("Applying Temperature Filter")
        package = temp_lowpass_filter(signal_data, fs, 5, unfiltered, t)
        return package
    #Motion
    elif choice == "Motion":
        print("Applying Motion Median Filter")
        package = imu_lowpass_filter(signal_data, fs, 4, unfiltered, t)
        return package
    #Respiration
    elif choice == "Respiration" :
        print("Applying Respiration Filter")
        package = respiration_lowpass_filter(signal_data, fs, 4, unfiltered, t)
        return package

#Applying the different filters for each type of signal
def ecg_filter(fs, signal_data, t, unfiltered) :
    
    minimum = 0.5
    high = 40

    sos = signal.butter(10, [minimum, high], btype='band', fs=fs, output='sos')
    bp_filtered_ecg = signal.sosfiltfilt(sos, signal_data)
    
    stats = analysis.extract_ecg_features(bp_filtered_ecg, fs)
    
    fft_freq, fft_mag = analysis.plot_fft("ECG", bp_filtered_ecg, fs, unfiltered)
    raw_fft_freq, raw_fft_mag = analysis.plot_fft_unfiltered("ECG", bp_filtered_ecg, fs, unfiltered)

    package = {
        "raw_signal": unfiltered,
        "clean_signal": bp_filtered_ecg,
        "time": t,
        "stats": stats,
        "fft_freqs": fft_freq,
        "fft_mag": fft_mag,
        "raw_fft_mag": raw_fft_mag # To compare FFTs on ax2
    }
    return package

#****************************************************Temperature**********************************************
def temp_lowpass_filter(signal_data, fs, order, unfiltered, t):
    #Lowpass filter to remove baseline drift while maintaining the mean
    mean = signal_data.mean()
    cutoff = 0.001
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq

    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    
    filtered_signal = signal.filtfilt(b, a, signal_data)
    
    filtered_signal += mean
    
    normal_cutoff = 0.2
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    lp_filtered = signal.filtfilt(b, a, filtered_signal)
    
    stats = analysis.extract_temp_features(lp_filtered, fs)
    
    fft_freq, fft_mag = analysis.plot_fft("Temperature", lp_filtered, fs, unfiltered)
    raw_fft_freq, raw_fft_mag = analysis.plot_fft_unfiltered("Temperature", lp_filtered, fs, unfiltered)
    
    package= {
        "raw_signal": unfiltered,
        "clean_signal": lp_filtered,
        "time": t,
        "stats": stats,
        "fft_freqs": fft_freq,
        "fft_mag": fft_mag,
        "raw_fft_mag": raw_fft_mag
        }
    return package

#****************************************************Respiration**********************************************
def respiration_lowpass_filter(signal_data, fs, order, unfiltered, t):
   #IRR lowpass filter to isolate breathing cycles
    nyquist = 0.5 * fs
    cutoff = 0.7 #standard cutoff for respiration data 
    
    if cutoff >= nyquist:
        cutoff = 0.9 * nyquist
        
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    lp_filtered = signal.filtfilt(b, a, signal_data)

    
    fft_freq, fft_mag = analysis.plot_fft("Respiration", lp_filtered, fs, unfiltered)
    raw_fft_freq, raw_fft_mag = analysis.plot_fft_unfiltered("Respiration", lp_filtered, fs, unfiltered)
    
    stats = analysis.extract_respiration_features(lp_filtered, fs)
    
    package = {
        "raw_signal": unfiltered,
        "clean_signal": lp_filtered,
        "time": t,
        "stats": stats,
        "fft_freqs": fft_freq,
        "fft_mag": fft_mag,
        "raw_fft_mag": raw_fft_mag
    }
    
    return package

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
    lp_filtered = signal.filtfilt(b, a, signal_data)
    
    fft_freq, fft_mag = analysis.plot_fft("IMU", lp_filtered, fs, unfiltered)
    raw_fft_freq, raw_fft_mag = analysis.plot_fft_unfiltered("IMU", lp_filtered, fs, unfiltered)
    
    stats = analysis.extract_motion_features(lp_filtered)
    
    package = {
        "raw_signal": unfiltered,
        "clean_signal": lp_filtered,
        "time": t,
        "stats": stats,
        "fft_freqs": fft_freq,
        "fft_mag": fft_mag,
        "raw_fft_mag": raw_fft_mag
    }
    
    return package
    