import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import ttk
from scipy import signal

#GUI for the user to input csv filename, columns to plot and the data type
class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("SYSC 2010 Final Project")
        self.window.geometry("520x380")

        #Getting CSV file name
        tk.Label(self.window, text="CSV File Name", font=('Arial', 11)).pack()
        self.entry_file = tk.Entry(self.window, width=40, font=('Arial', 11))
        self.entry_file.pack(pady=4)

        #Getting the x axis column name
        tk.Label(self.window, text="X-axis Column Name", font=('Arial', 11)).pack()
        self.entry_x = tk.Entry(self.window, width=40, font=('Arial', 11))
        self.entry_x.pack(pady=4)

        #Getting y axis column name
        tk.Label(self.window, text="Y-axis Column Name", font=('Arial', 11)).pack()
        self.entry_y = tk.Entry(self.window, width=40, font=('Arial', 11))
        self.entry_y.pack(pady=4)

        #Data type options
        data_options = ["ECG", "Temperature", "Respiration", "Motion"]

        #Dropdown list
        tk.Label(self.window, text="Select Data Type:").pack(pady=(10, 0))
        self.selected_type = tk.StringVar()
        self.dropdown = ttk.Combobox(self.window, textvariable=self.selected_type, values=data_options,state="readonly")
        self.dropdown.pack(pady=5)
        
        # Set a default value so it isn't initially empty
        self.dropdown.current(0) 

        #Button to plot the initial data
        tk.Button(self.window, text="Load & Filter", font=('Arial', 11),command=self.handle_selection,width=15).pack()
        self.window.mainloop()
    
    #Getting the data type
    def handle_selection (self) :
        choice = self.selected_type.get()
        print(f"User chose {choice}")

        #Data used to plot unfiltered
        filename = self.entry_file.get().strip()
        x = self.entry_x.get().strip()
        y = self.entry_y.get().strip()

        try:
            df = pd.read_csv(filename)
            df = df.interpolate(method='linear')
            
            time = np.array(df[x])
            signal_data = np.array(df[y])

            plt.figure(figsize=(14,6))
            plt.plot(df[x], df[y], color='pink')
            plt.title(f"Unfiltered plot of {y} vs {x}")
            plt.xlabel(x)
            plt.ylabel(y)
            plt.grid(True)
            plt.tight_layout()
            plt.show()    
            
            #Applying correct filter for the given data type
            apply_filter(choice, signal_data, time)     
            
        except Exception as e:
            print("Error", str(e))
        
#**************************************CHOOSING CORRECT FILTER FOR SPECIFIED DATA TYPE****************************************
def apply_filter(choice, signal_data, t) :
    #ECG Signal:
    if choice == "ECG":
        print("Applying ECG Bandpass Filter")
        ecg_bandpass_filter(500, signal_data, t) 
    #Temperature:
    elif choice == "Temperature" :
        print("Applying Temperature Filter")
        filtered_temp = temp_lowpass_filter(0.1, signal_data, order=5)
    #Motion
    elif choice == "Motion":
        print("Applying Motion Median Filter")
        motion_comp_filter(100, signal_data)
    #Respiration
    elif choice == "Respiration" :
        print("Applying Respiration Filter")
        resp_bandpass_filter(25, signal_data, t)
    else :
        print("ERROR, no choice")
        
#Applying the different filters for each type of signal
def temp_lowpass_filter(data, cutoff, fs, order):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    np.convolve()
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return signal.filtfilt(b, a, data)

def ecg_bandpass_filter(fs, signal_data, t) :
    minimum = 0.5
    high = 40
    sos = signal.butter(10, [minimum, high], btype='band', fs=fs, output='sos')
    bp_filtered_ecg = signal.sosfiltfilt(sos, signal_data)
    plt.figure(figsize=(12,8))
    plt.title("Band Pass Filtered Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.plot(t, bp_filtered_ecg, color='purple')
    plt.show()
    
def resp_bandpass_filter(fs, signal_data, t) :
    minimum = 0.1
    high = 0.8

    sos = signal.butter(10, [minimum, high], btype='band', fs=fs, output='sos')
    bp_filtered_resp = signal.sosfiltfilt(sos, signal_data)
    plt.figure(figsize=(10,6))
    plt.title("Respirarion Filtered Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.plot(t, bp_filtered_resp, color='orange')
    plt.show()
    
    return bp_filtered_resp
    
def motion_comp_filter(fs, signal_data) :
    median_filtered = signal.medfilt(signal_data, kernel_size=5)
    
    cutoff = 5.0 
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    
    b, a = signal.butter(4, normal_cutoff, btype='low', analog=False)
    filtered_motion = signal.filtfilt(b, a, median_filtered)
    
    plt.figure(figsize=(10,6))
    plt.title("Respirarion Filtered Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.plot(t, bp_filtered_resp, color='orange')
    plt.show()
    
    return filtered_motion

#FFT of the signals
def get_fft(data, fs):
    fft_vals = np.abs(np.fft.rfft(data))
    freqs = np.fft.rfftfreq(len(data), 1/fs)
    return freqs, fft_vals

def extract_features(signal_data):
    features = {
        "mean": np.mean(signal_data),
        "rms": np.sqrt(np.mean(signal_data**2)),
        "peak_to_peak": np.ptp(signal_data),
        "std_dev": np.std(signal_data)
    }
    return features

if __name__ == "__main__":
    app = GUI()