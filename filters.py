import matplotlib.pyplot as plt
from scipy import signal
from tkinter import messagebox

#File imports
import analysis

def apply_filter(choice, signal_data, t, fs, unfiltered) :
    #ECG Signal:
    if choice == "ECG":
        print("Applying ECG Bandpass Filter")
        filtered_signal, extract = ecg_filter(fs, signal_data, t, unfiltered) 
        return filtered_signal, extract
    #Temperature:
    elif choice == "Temperature" :
        print("Applying Temperature Filter")
        filtered_signal, extract = temp_lowpass_filter(signal_data, fs, 5, unfiltered, t)
        return filtered_signal, extract
    #Motion
    elif choice == "Motion":
        print("Applying Motion Median Filter")
        filtered_signal, extract = imu_lowpass_filter(signal_data, fs, 4, unfiltered, t)
        return filtered_signal, extract
    #Respiration
    elif choice == "Respiration" :
        print("Applying Respiration Filter")
        filtered_signal, extract = respiration_lowpass_filter(signal_data, fs, 4, unfiltered, t)
        return filtered_signal, extract

#Applying the different filters for each type of signal
def ecg_filter(fs, signal_data, t, unfiltered) :
    
    #Using FIR to lose less data about the QRS complex in ECG signal
    minimum = 0.5
    high = 40

    sos = signal.butter(10, [minimum, high], btype='band', fs=fs, output='sos')
    bp_filtered_ecg = signal.sosfiltfilt(sos, signal_data)

#plt.figure(figsize=(12,8))
   # plt.title("Band Pass Filtered Signal")
   # plt.xlabel("Time (s)")
   # plt.ylabel("Amplitude")
   # plt.tight_layout()
    #plt.plot(t, bp_filtered_ecg, color='purple')
    #plt.show()
    
    #Comparison between filtered and unfiltered
   # plt.figure(figsize=(12,8))
   # plt.title("Comparison of Filtered and Unfiltered ECG")
   # plt.xlabel("Time (s)")
   # plt.ylabel("Amplitude")
   # plt.tight_layout()
   # plt.plot(t, unfiltered, color='pink')
    #plt.plot(t, bp_filtered_ecg, color='purple')
    #plt.show()
    
    extract = analysis.extract_ecg_features(bp_filtered_ecg, fs)
    
    analysis.plot_fft("ECG", bp_filtered_ecg, fs, unfiltered)
    
    return bp_filtered_ecg,extract
    
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

   # plt.figure(figsize=(12,8))
   # plt.title("Filtered Temperature Signal")
   # plt.xlabel("Time (s)")
   # plt.ylabel("Amplitude")
  #  plt.tight_layout()
   # plt.plot(t, lp_filtered, color='blue')
   # plt.show()
    
    #Comparison between filtered and unfiltered
   # plt.figure(figsize=(12,8))
    #plt.title("Comparison of Filtered and Unfiltered Temperature")
   # plt.xlabel("Time (s)")
    #plt.ylabel("Amplitude")
    #plt.tight_layout()
    #plt.plot(t, unfiltered, color='pink')
    #plt.plot(t, lp_filtered, color='blue')
    #plt.show()
    
    extract = analysis.extract_temp_features(lp_filtered, fs)
    
    analysis.plot_fft("Temperature", lp_filtered, fs, unfiltered)
    
    return lp_filtered,extract

#****************************************************Resoiration**********************************************
def respiration_lowpass_filter(signal_data, fs, order, unfiltered, t):
   #IRR lowpass filter to isolate breathing cycles
    nyquist = 0.5 * fs
    cutoff = 0.7 #standard cutoff for respiration data 
    
    if cutoff >= nyquist:
        cutoff = 0.9 * nyquist
        
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    lp_filtered = signal.filtfilt(b, a, signal_data)
   
    #plt.figure(figsize=(12,8))
    #plt.title("Filtered Respiration Signal")
    #plt.xlabel("Time (s)")
    #plt.ylabel("Amplitude")
    #plt.tight_layout()
    #plt.plot(t, lp_filtered, color='blue')
    #plt.show()
    
    #Comparison between filtered and unfiltered
    #plt.figure(figsize=(12,8))
    #plt.title("Comparison of Filtered and Unfiltered Respiration")
    #plt.xlabel("Time (s)")
    #plt.ylabel("Amplitude")
    #plt.tight_layout()
    #plt.plot(t, unfiltered, color='pink')
    #plt.plot(t, lp_filtered, color='blue')
    #plt.show()
    
    analysis.plot_fft("Respiration", lp_filtered, fs, unfiltered)
    
    extract = analysis.extract_respiration_features(lp_filtered, fs)
    
    return lp_filtered, extract

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

    #plt.figure(figsize=(12,8))
    #plt.title("Filtered IMU Signal")
    #plt.xlabel("Time (s)")
    #plt.ylabel("Amplitude")
    #plt.tight_layout()
    #plt.plot(t, lp_filtered, color='blue')
    #plt.show()
    
    #Comparison between filtered and unfiltered
    #plt.figure(figsize=(12,8))
    #plt.title("Comparison of Filtered and Unfiltered IMU")
    #plt.xlabel("Time (s)")
    #plt.ylabel("Amplitude")
    #plt.tight_layout()
    #plt.plot(t, unfiltered, color='pink')
    #plt.plot(t, lp_filtered, color='blue')
    #plt.show()
    
    analysis.plot_fft("IMU", lp_filtered, fs, unfiltered)
    
    extract = analysis.extract_motion_features(lp_filtered)
    
    return lp_filtered,extract
    
    