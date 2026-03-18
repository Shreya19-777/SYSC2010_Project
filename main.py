import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Using customtkinter instead for easier design
import customtkinter as ctk

from scipy import signal

#GUI for the user to input csv filename, columns to plot and the data type
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SYSC 2010 Final Project")
        self.geometry("500x550")
        
        #Getting CSV file name
        self.label_title = ctk.CTkLabel(self, text="CSV File Name", font=ctk.CTkFont(size=20, weight="bold")).pack()
        self.entry_file = ctk.CTkEntry(self, width=300, font=('Arial', 11))
        self.entry_file.pack(pady=5)

        #Getting the x axis column name
        ctk.CTkLabel(self, text="X-axis Column (Time): ", font=('Arial', 11)).pack()
        self.entry_x = ctk.CTkEntry(self, width=300)
        self.entry_x.pack(pady=5)

        #Getting y axis column name
        ctk.CTkLabel(self, text="Y-axis Column (Signal): ").pack()
        self.entry_y = ctk.CTkEntry(self, width=300)
        self.entry_y.pack(pady=5)

        #Dropdown list
        self.label_type = ctk.CTkLabel(self, text="Select Data Type:")
        self.label_type.pack(pady=(15, 0))
        self.dropdown = ctk.CTkComboBox(self, values=["ECG", "Temperature", "Respiration", "Motion"], width=200)
        self.dropdown.set("ECG") # Default value
        self.dropdown.pack(pady=10)

        #Button to plot the initial data
        self.btn_load = ctk.CTkButton(self, text="Load & Filter Data", 
            command=self.handle_selection,
            fg_color="transparent", 
            border_width=2,
            text_color=("gray10", "#DCE4EE"))
        self.btn_load.pack(pady=30)
    
    def handle_selection (self) :
        #Saving the user inputted data type
        choice = self.dropdown.get()
        print(f"User chose {choice}")

        #Data used to plot unfiltered data
        filename = self.entry_file.get().strip()
        x = self.entry_x.get().strip()
        y = self.entry_y.get().strip()

        #Reading csv and plotting the data
        try:
            df = pd.read_csv(filename)
            df = df.interpolate(method='linear')
            
            time = np.array(df[x])
            signal_data = np.array(df[y])
            
            #Getting the sampling frequency for the data
            # Ensure the time column is in datetime format
            df[x] = pd.to_datetime(df[x])

            #Time difference between consecutive rows
            time_diff = df[x].diff().mean()
            
            fs = 1 / time_diff.total_seconds()
            
            plt.figure(figsize=(10,8))
            plt.plot(df[x], df[y], color='pink')
            plt.title(f"Unfiltered plot of {y} vs {x}")
            plt.xlabel(x)
            plt.ylabel(y)
            plt.grid(True)
            plt.show()    
            
            #Calling function for displaying the key features of the unfiltered data
            features = key_features(signal_data)
            print(features)
            
            #Applying correct filter for the given data type
            apply_filter(choice, signal_data, time, fs) 
                
        #Error message for incorrect inputted values from user
        except Exception as e:
            print("Error", str(e))
        
#**************************************CHOOSING CORRECT FILTER FOR SPECIFIED DATA TYPE****************************************
def apply_filter(choice, signal_data, t, fs) :
    #ECG Signal:
    if choice == "ECG":
        print("Applying ECG Bandpass Filter")
        ecg_bandpass_filter(fs, signal_data, t) 
    #Temperature:
    elif choice == "Temperature" :
        print("Applying Temperature Filter")
        filtered_temp = temp_lowpass_filter(fs, signal_data, order=5)
    #Motion
    elif choice == "Motion":
        print("Applying Motion Median Filter")
        motion_comp_filter(fs, signal_data)
    #Respiration
    elif choice == "Respiration" :
        print("Applying Respiration Filter")
        resp_bandpass_filter(fs, signal_data, t)
    #No choice
    else :
        print("ERROR, no choice")
        
#Applying the different filters for each type of signal

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
    
    return bp_filtered_ecg
    
def temp_lowpass_filter(data, cutoff, fs, order):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return signal.filtfilt(b, a, data)
    
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
    
def motion_comp_filter(fs, signal_data, t) :
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
    plt.plot(t, filtered_motion, color='orange')
    plt.show()
    
    return filtered_motion

#FFT of the signals
def get_fft(data, fs):
    fft_vals = np.abs(np.fft.rfft(data))
    freqs = np.fft.rfftfreq(len(data), 1/fs)
    return freqs, fft_vals

#The key features from the unfiltered data
def key_features(signal_data):
    features = {
        "mean": np.mean(signal_data),
        "rms": np.sqrt(np.mean(signal_data**2)),
        "peak_to_peak": np.ptp(signal_data),
        "std_dev": np.std(signal_data)
    }
    return features

if __name__ == "__main__":
    app = GUI()
    app.mainloop()