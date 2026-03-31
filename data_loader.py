import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

from pandas.errors import EmptyDataError

import preprocessing

def data_load(filename, choice, x, y, unit):
        
    try:
        df = pd.read_csv(filename)
        
        #Checking for empty csv file
        if df.empty:
            messagebox.showwarning("Empty CSV File", f"The file '{filename}' contains no data.")
            return None, None
        
        #Checking for invalid column names
        if x not in df.columns or y not in df.columns:
            messagebox.showerror("Column Error", f"Columns '{x}' or '{y}' not found in CSV.")
            return None, None  
        
        #Checking for empty entries if column names given
        if df[y].isnull().all():
            print(f"Error: Column '{y}' is entirely empty (all NaNs).")
            messagebox.showwarning("No data to display, all entries empty")
            return None, None
        
        #Checking for invalid filenames
      
        time = np.array(df[x])
        signal_data = np.array(df[y])
        
        if (unit == "Milliseconds") :
            time = time/1000.0
        
        #Only call preprocess if there are no errors with the csv
        pck = preprocessing.preprocess(choice, signal_data, time)
        return pck
    
    except EmptyDataError:
        # This catches a 0-byte file before the 'if df.empty' can even run
        messagebox.showerror("Empty File", f"The file '{filename}' is completely empty.")
        return None, None

    except FileNotFoundError:
        # This triggers specifically if the file doesn't exist
        messagebox.showerror("File Not Found", f"The file '{filename}' could not be found.")
        return None, None
        
    except Exception as e:
        print(f"Error: {e}")
        return None, None
    
def motion_data_load(filename, time_col, x_col, y_col, z_col):
    try:
        df = pd.read_csv(filename)

        if df.empty:
            messagebox.showwarning("Empty CSV File", f"The file '{filename}' contains no data.")
            return None, None, None, None
        
        for col in [time_col, x_col, y_col, z_col]:
            if col not in df.columns:
                messagebox.showerror("Column Error", f"Column '{col}' not found in CSV.")
                return None, None, None, None
            
            if df[col].isnull().all():
                print(f"Error: Column '{col}' is entirely empty (all NaNs).")
                messagebox.showwarning("No data to display, all entries empty")
                return None, None, None, None
        
        time = np.array(df[time_col])
        x_data = np.array(df[x_col])
        y_data = np.array(df[y_col])
        z_data = np.array(df[z_col])

        raw_magnitude = np.sqrt(x_data**2 + y_data**2 + z_data**2)   
        
        return raw_magnitude, time
        
    except Exception as e:
        print(f"Error: {e}")
        
        return None, None