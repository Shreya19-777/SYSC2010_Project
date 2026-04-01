import numpy as np 
import pandas as pd 
num_samples = 1000
interval_sec = 60
seconds = np.arange(0, num_samples * interval_sec, interval_sec)
temperatures = np.random.normal(loc=36.7, scale=0.2, size = num_samples)
baseline = 36.7
noise = np.random.normal(0, 0.1, size=num_samples)
temperatures =  baseline + noise

drift = np.random.normal(0, 0.05, size=num_samples)
temperatures = 36.7 + np.cumsum(drift)

df = pd.DataFrame({
    'seconds' : seconds,
    'temperature' : np.round(temperatures, 2)
})

df.to_csv("temp.csv")
