import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

def data_load (filename, choice, x, y) :
    try:
        df = pd.read_csv(filename)
        print(df[x])
        time = np.array(df[x])
        signal_data = np.array(df[y])
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