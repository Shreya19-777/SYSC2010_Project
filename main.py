import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import customtkinter as ctk
from scipy import signal

#*************************************************GUI**********************************************
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SYSC 2010 Final Project")
        self.geometry("800x550")
        
        #Getting CSV file name
        self.label_title = ctk.CTkLabel(self, text="CSV File Name", font=ctk.CTkFont(weight="bold")).pack()
        self.entry_file = ctk.CTkEntry(self, width=300)
        self.entry_file.pack(pady=5)

        #Getting the x axis column name (time)
        ctk.CTkLabel(self, text="X-axis Column (Time): ").pack()
        self.entry_x = ctk.CTkEntry(self, width=300)
        self.entry_x.pack(pady=5)

        #Getting y axis column name (signal)
        ctk.CTkLabel(self, text="Y-axis Column (Signal): ").pack()
        self.entry_y = ctk.CTkEntry(self, width=300)
        self.entry_y.pack(pady=5)

        #Dropdown list (choosing data type)
        self.label_type = ctk.CTkLabel(self, text="Select Data Type:")
        self.label_type.pack(pady=(15, 0))
        self.dropdown = ctk.CTkComboBox(self, values=["ECG", "Temperature", "Respiration", "Motion"], width=200)
        self.dropdown.set("ECG") # Default
        self.dropdown.pack(pady=5)

        #Button
        self.btn_load = ctk.CTkButton(self, text="Load & Filter Data", 
            command=self.handle_selection,
            fg_color="transparent", 
            border_width=2,
            text_color=("gray10", "#DCE4EE"))
        self.btn_load.pack(pady=30)
        
        #-------------------------------------KEY FEATURES---------------------------------------------
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(pady=10, padx=20, fill="x") # Added .pack()
        
        self.stats_title = ctk.CTkLabel(self.stats_frame, text="Key Features", font=ctk.CTkFont(weight="bold"))
        self.stats_title.pack(pady=5)
        
        # Changed name to self.stat_labels to match your handle_selection logic
        self.stat_labels = {} 
        for stat in ["mean", "rms", "peak_to_peak", "std_dev"]:
            label = ctk.CTkLabel(self.stats_frame, text=f"{stat.replace('_', ' ').title()}: -")
            label.pack()
            self.stat_labels[stat] = label
    
    #---------------------------------------HANDLING USER INPUTS------------------------------------------
    def handle_selection (self) :
        #data type
        choice = self.dropdown.get()

        #Reading csv filename and columns
        filename = self.entry_file.get().strip()
        x = self.entry_x.get().strip()
        y = self.entry_y.get().strip()
        
        try:
            df = pd.read_csv(filename)
            print(df[x])
            time = np.array(df[x])
            signal_data = np.array(df[y])
            
            #----------------------------------KEY FEATURES---------------------------------
            stats = {
                    "mean": np.mean(signal_data),
                    "rms": np.sqrt(np.mean(signal_data**2)),
                    "peak_to_peak": np.ptp(signal_data),
                    "std_dev": np.std(signal_data)
                }
        
            #Looping through elements and displaying the resulting value to 4 decimal places
            for key,value in stats.items() :
                self.stat_labels[key].configure(text=f"{key.replace('_', ' ').title()}: {value:.4f}")
            #-------------------------------------PLOTTING RAW DATA---------------------------
            plt.figure(figsize=(20,15))
            plt.plot(df[x], df[y], color='pink')
            plt.title(f"Unfiltered plot of {y} vs {x}", fontsize=24)
            plt.xlabel(x, fontsize=16)
            plt.ylabel(y, fontsize=16)
            plt.tight_layout()
            plt.grid(True)
            plt.show()

            #------------------------------------PREPROCESSING--------------------------------
            print(df.isna().sum())
            print(df.describe())
            df = df.interpolate(method='linear')
            
            #Getting the sampling frequency
            #Calculating the time between each sample, 1/sampling period formula
            time_diff = np.diff(time)
            sampling_period = np.median(time_diff)
            fs = (1/sampling_period)
            
            #Step 1: High pass filter to remove baseline drift
            if (choice == "ECG") :
                cutoff = 0.5
            elif (choice == "Temperature") :
                cutoff = 0.001
            elif (choice == "Respiration") :
                cutoff = 0.25
            else :
                cutoff = 5
                
            print(f"Cutoff frequency is {cutoff}")
                
            nyquist_f = 0.5 * fs
            normal_cutoff = cutoff/nyquist_f
            b, a = signal.butter(4, normal_cutoff, btype='high', analog=False)
            filtered_signal_data = signal.filtfilt(b, a, signal_data)
            
            filter_median = np.median(signal_data)
            hp_filtered = filtered_signal_data + filter_median
            
            #Normalization
            s_min = np.min(hp_filtered)
            s_max = np.max(hp_filtered)
            normalized = (hp_filtered-s_min) / (s_max-s_min)
            
            plt.figure(figsize=(16,10))
            plt.plot(time, normalized, color='pink')
            plt.title(f"Preprocessed plot of {y} vs {x}")
            plt.xlabel(x, fontsize=16)
            plt.ylabel(y, fontsize=16)
            plt.tight_layout()
            plt.grid(True)
            plt.show()
            
            print(f"Fs is {fs}")    
            #Applying correct filter for the given data type
            apply_filter(choice, normalized, time, fs, signal_data)
                
        #Error message for incorrect inputted values from user
        except Exception as e:
            print("Error", str(e))
        
#**************************************CHOOSING CORRECT FILTER FOR SPECIFIED DATA TYPE****************************************
def apply_filter(choice, signal_data, t, fs, unfiltered) :
    #ECG Signal:
    if choice == "ECG":
        print("Applying ECG Bandpass Filter")
        ecg_bandpass_filter(fs, signal_data, t, unfiltered) 
    #Temperature:
    elif choice == "Temperature" :
        print("Applying Temperature Filter")
        filtered_temp = temp_lowpass_filter(signal_data, fs, 5, unfiltered, t)
    #Motion
    elif choice == "Motion":
        print("Applying Motion Median Filter")
    #Respiration
    elif choice == "Respiration" :
        print("Applying Respiration Filter")
           
#Applying the different filters for each type of signal
def ecg_bandpass_filter(fs, signal_data, t, unfiltered) :
    minimum = 0.5
    high = 40
    sos = signal.butter(10, [minimum, high], btype='band', fs=fs, output='sos')
    bp_filtered_ecg = signal.sosfiltfilt(sos, signal_data)
    plt.figure(figsize=(24,8))
    plt.title("Filtered ECG Signal", fontsize=24)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.plot(t, bp_filtered_ecg, color='purple')
    plt.tight_layout()
    plt.show()
    
    #Comparison between filtered and unfiltered
    plt.figure(figsize=(12,8))
    plt.title("Comparison of Filtered and Unfiltered ECG", fontsize=24)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.plot(t, unfiltered, color='pink')
    plt.plot(t, bp_filtered_ecg, color='purple')
    plt.show()
    
    return bp_filtered_ecg
    
#****************************************************Temperature**********************************************
def temp_lowpass_filter(data, fs, order, unfiltered, t):
    nyquist = 0.5 * fs
    cutoff = 0.9 * nyquist
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    lp_filtered = signal.filtfilt(b, a, data)

    plt.figure(figsize=(12,8))
    plt.title("Filtered ECG Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.plot(t, lp_filtered, color='blue')
    plt.show()
    
    #Comparison between filtered and unfiltered
    plt.figure(figsize=(12,8))
    plt.title("Comparison of Filtered and Unfiltered ECG")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.plot(t, unfiltered, color='pink')
    plt.plot(t, lp_filtered, color='blue')
    plt.show()
    
    return signal.filtfilt(b, a, data)
    
#def resp_bandpass_filter(fs, signal_data, t) :
    
#def motion_comp_filter(fs, signal_data, t) :

if __name__ == "__main__":
    app = GUI()
    app.mainloop()