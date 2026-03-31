import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from tkinter import messagebox

def data_load(filename, choice, x, y):
    try:
        df = pd.read_csv(filename)

        #Checking for completely empty csv file
        if df.empty:
            messagebox.showwarning("Empty CSV File", f"The file '{filename}' contains no data.")
            return None, None
        
        if x not in df.columns or y not in df.columns:
            messagebox.showerror("Column Error", f"Columns '{x}' or '{y}' not found in CSV.")
            return None, None
        
        #Checking for empty entries if column names given
        if df[x].isnull().all():
            print(f"Error: Column '{y}' is entirely empty (all NaNs).")
            messagebox.showwarning("No data to display, all entries empty")
            return None, None
        
        #Checking for invalid filenames
      
        time = np.array(df[x])
        signal_data = np.array(df[y])
        
        return signal_data, time
        
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