import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import ttk
from scipy import signal

#User interface GUI

dropdown_options = ['ECG', 'Temperature', 'Respiration', 'IMU/Motion']

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("SYSC 2010 Final Project")
        self.window.geometry("520x380")

        tk.Label(self.window, text="CSV File Name", font=('Arial', 11)).pack()
        self.entry_file = tk.Entry(self.window, width=40, font=('Arial', 11))
        self.entry_file.pack(pady=4)

        tk.Label(self.window, text="X-axis Column Name", font=('Arial', 11)).pack()
        self.entry_x = tk.Entry(self.window, width=40, font=('Arial', 11))
        self.entry_x.pack(pady=4)

        tk.Label(self.window, text="Y-axis Column Name", font=('Arial', 11)).pack()
        self.entry_y = tk.Entry(self.window, width=40, font=('Arial', 11))
        self.entry_y.pack(pady=4)

        tk.Button(self.window, text="Enter", font=('Arial', 11),command=self.load_and_plot,width=15).pack()

        self.window.mainloop()
        
#CSV File Handling
def load_and_plot(self):
        filename = self.entry_file.get().strip()
        x = self.entry_x.get().strip()
        y = self.entry_y.get().strip()

        try:
            df = pd.read_csv(filename)
            df = df.interpolate(method='linear')
            
            time = np.array(df[x])
            signal_data = np.array(df[y])

            plt.plot(df[x], df[y], color='teal')
            plt.title(f"Unfiltered plot of {y} vs {x}")
            plt.xlabel(x)
            plt.ylabel(y)
            plt.grid(True)
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print("Error", str(e))
            
        #ECG Signal:
        ecg_bandpass_filter(250, signal_data)
        
        #Temperature:
        temp_lowpass_filter(signal_data)
        
        #Respiration
        resp_bandpass_filter(signal_data)
            
def temp_lowpass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    np.convolve()
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return signal.filtfilt(b, a, data)

def ecg_bandpass_filter(fs, signal_data) :
    minimum = 0.5
    high = 40

    sos = signal.butter(10, [minimum, high], btype='band', fs=fs, output='sos')
    bp_filtered_ecg = signal.sosfiltfilt(sos, signal_data)
    plt.figure()
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
    plt.figure()
    plt.title("Respirarion Filtered Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.plot(t, bp_filtered_resp, color='purple')
    plt.show()

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