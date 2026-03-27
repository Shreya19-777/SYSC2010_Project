import matplotlib.pyplot as plt
from scipy import signal

#File imports
import analysis

def apply_filter(choice, signal_data, t, fs, unfiltered) :
    #ECG Signal:
    if choice == "ECG":
        print("Applying ECG Bandpass Filter")
        extract = ecg_filter(fs, signal_data, t, unfiltered) 
        return extract
    #Temperature:
    elif choice == "Temperature" :
        print("Applying Temperature Filter")
        extract = temp_lowpass_filter(signal_data, fs, 5, unfiltered, t)
        return extract
    #Motion
    elif choice == "Motion":
        print("Applying Motion Median Filter")
        extract = imu_lowpass_filter(signal_data, fs, 4, unfiltered, t)
        return extract
    #Respiration
    elif choice == "Respiration" :
        print("Applying Respiration Filter")
        extract = respiration_lowpass_filter(signal_data, fs, 4, unfiltered, t)
        return extract
           
#Applying the different filters for each type of signal
def ecg_filter(fs, signal_data, t, unfiltered) :
    
    #Using FIR to lose less data about the QRS complex in ECG signal
    minimum = 0.5
    high = 40

    sos = signal.butter(10, [minimum, high], btype='band', fs=fs, output='sos')
    bp_filtered_ecg = signal.sosfiltfilt(sos, signal_data)

    plt.figure(figsize=(12,8))
    plt.title("Band Pass Filtered Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.plot(t, bp_filtered_ecg, color='purple')
    plt.show()
    
    #Comparison between filtered and unfiltered
    plt.figure(figsize=(12,8))
    plt.title("Comparison of Filtered and Unfiltered ECG")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.plot(t, unfiltered, color='pink')
    plt.plot(t, bp_filtered_ecg, color='purple')
    plt.show()
    
    extract = analysis.extract_ecg_features(bp_filtered_ecg, fs)
    
    analysis.plot_fft("ECG", bp_filtered_ecg, fs, unfiltered)
    
    return extract
    
#****************************************************Temperature**********************************************
def temp_lowpass_filter(signal_data, fs, order, unfiltered, t):
    
    print(f"THE SAMPLING FREQUENCY IS {fs}")
    
    normal_cutoff = 0.2
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    lp_filtered = signal.filtfilt(b, a, signal_data)

    plt.figure(figsize=(12,8))
    plt.title("Filtered Temperature Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.plot(t, lp_filtered, color='blue')
    plt.show()
    
    #Comparison between filtered and unfiltered
    plt.figure(figsize=(12,8))
    plt.title("Comparison of Filtered and Unfiltered Temperature")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.plot(t, unfiltered, color='pink')
    plt.plot(t, lp_filtered, color='blue')
    plt.show()
    
    extract = analysis.extract_temp_features(lp_filtered)
    
    analysis.plot_fft("Temperature", lp_filtered, fs, unfiltered)
    
    return extract

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
    
    analysis.plot_fft("Respiration", lp_filtered, fs, unfiltered)
    
    extract = analysis.extract_respiration_features(lp_filtered, fs)
    
    return extract

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
    
    analysis.plot_fft("IMU", lp_filtered, fs, unfiltered)
    
    extract = analysis.extract_motion_features(lp_filtered)
    
    return extract
    
    