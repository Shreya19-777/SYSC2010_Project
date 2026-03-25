import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

#file imports
import filter_functions

def preprocess (filename, choice, x, y) :
    try:
        df = pd.read_csv(filename)
        print(df[x])
        time = np.array(df[x])
        signal_data = np.array(df[y])
                
        #-------------------------------------PLOTTING RAW DATA---------------------------
        plt.figure(figsize=(12,8))
        plt.tight_layout()
        plt.plot(df[x], df[y], color='pink')
        plt.title(f"Unfiltered plot of {choice} : {y} vs {x}")
        plt.xlabel(x)
        plt.ylabel(y)
        plt.grid(True)
        plt.show()
        #------------------------------------PREPROCESSING--------------------------------
        cleaned_data = handle_missing_data(signal_data)
        if (choice != "Temperature") :
            cleaned_data = remove_drift(cleaned_data)
        cleaned_data = normalize(cleaned_data)
            
        #Getting the sampling frequency
        time_diff = np.diff(time)
        sampling_period = np.median(time_diff)
        fs = (1/sampling_period)
 
        #Applying correct filter for the given data type
        extract = filter_functions.apply_filter(choice, cleaned_data, time, fs, signal_data)
        
        return extract
                
    #Error message for incorrect inputted values from user
    except Exception as e:
        print("Error", str(e))
            
def handle_missing_data(signal):

    s = pd.Series(signal, dtype=float)  #convert to series for easier handling of missing data

    missing_count = s.isna().sum()
    if missing_count > 0:
        print(f"[handle_missing_data] Found {missing_count}  missing values. ")

    if s.isna().all():
        raise ValueError("Signal is entirely NaN — cannot interpolate.")

    cleaned = s.interpolate(method='linear').bfill().ffill()
    
    return cleaned.to_numpy() #convert back to numpy array

def remove_drift(signal):
    mean_val = np.mean(signal)
    return signal - mean_val

#normalization IMU
def normalize(signal):
    min_val = np.min(signal)
    max_val = np.max(signal)
    if max_val - min_val == 0:
        return signal - min_val
    return (signal - min_val) / (max_val - min_val)