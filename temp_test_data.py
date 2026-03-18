import numpy as np 
import pandas as pd 
num_samples = 100
interval_sec = 60
seconds = np.arange(0, num_samples * interval_sec, interval_sec)
temperatures = np.random.normal(loc=36.7, scale=0.2, size = num_samples)

df = pd.DataFrame({
    'seconds' : seconds,
    'temperature' : np.round(temperatures, 2)
})

df.to_csv("sample_temp.csv")
