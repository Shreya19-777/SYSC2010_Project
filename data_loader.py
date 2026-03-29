import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from tkinter import messagebox

def data_load (filename, choice, x, y) :
    try:
        df = pd.read_csv(filename)

        time = np.array(df[x])
        signal_data = np.array(df[y])
        
        #Checking for completely empty csv file
        if df.empty:
            messagebox.showwarning("Empty CSV File", f"The file '{filename}' contains no data.")
            return None, None
        
        #Checking for empty entries if column names given
        if df[y].isnull().all():
            print(f"Error: Column '{y}' is entirely empty (all NaNs).")
            messagebox.showwarning("No data to display, all entries empty")
            return None, None
        
        #checking for invalid filenames
        if x not in df.columns or y not in df.columns:
            messagebox.showerror("Column Error", f"Columns '{x}' or '{y}' not found in CSV.")
            return None, None
        
        print("1- preprocessing data loaded successfully")      
        #-------------------------------------PLOTTING RAW DATA---------------------------
        plt.figure(figsize=(12,8))
        plt.tight_layout()
        plt.plot(df[x], df[y], color='pink')
        plt.title(f"Unfiltered plot of {choice} : {y} vs {x}")
        plt.xlabel(x)
        plt.ylabel(y)
        plt.grid(True)
        plt.show()
        print("2- preprocessing data plotted successfully")
        
        return signal_data, time
        
    except Exception as e :
        print({e})
        return None, None