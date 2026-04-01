import pandas as pd 
import numpy as np
'''
df = pd.read_csv('ecg_raw_sub4_seg3.csv')

time_column = np.linspace(0, 20, num=4999)

df.insert(0, 'Time', time_column)

# 4. Save the updated file
df.to_csv('high_intensity_ecg_data.csv', index=False)
'''

with open('high_intensity_ecg_data.csv', 'r') as f_in:
    with open('high_intensity_real_ecg.csv', 'w') as f_out:
        for line in f_in:
            # rstrip() removes the newline, then we strip the last comma, 
            # then we add the newline back.
            clean_line = line.rstrip().rstrip(',')
            f_out.write(clean_line + '\n')

print("CSV cleaned! Use 'cleaned_data.csv' in your GUI now.")


