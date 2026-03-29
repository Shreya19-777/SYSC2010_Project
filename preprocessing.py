import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

#file imports
import data_loader
import filters

def preprocess (filename, choice, x, y) :
    signal_data, time = data_loader.data_load(filename, choice, x, y)
    raw_data = (signal_data, time)
    #------------------------------------PREPROCESSING--------------------------------
    cleaned_data = handle_missing_data(signal_data)
    if (choice != "Temperature") :
        cleaned_data = remove_drift(cleaned_data)
        cleaned_data = normalize(cleaned_data)
    print("3- preprocessing data cleaned successfully")  
        
    #Getting the sampling frequency
    time_diff = np.diff(time)
    sampling_period = np.median(time_diff)
    fs = (1/sampling_period)
 
    #Applying correct filter for the given data type
    extract = filters.apply_filter(choice, cleaned_data, time, fs, signal_data)
    print("4- preprocessing dataextracted successfully")  
    return raw_data, extract
                
            
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

#normalization
def normalize(signal):
    min_val = np.min(signal)
    max_val = np.max(signal)
    if max_val - min_val == 0:
        return signal - min_val
    return (signal - min_val) / (max_val - min_val)