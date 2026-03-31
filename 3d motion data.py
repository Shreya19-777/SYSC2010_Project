import numpy as np
import pandas as pd

# Generate the Time and Signal Data
t = np.linspace(0, 20, 500)  
frequency = 0.5

# Parametric equations for a 3D spiral
x = np.cos(2 * np.pi * frequency * t)
y = np.sin(2 * np.pi * frequency * t)
z = t * 0.1

# Add random sensor noise
x_noisy = x + np.random.normal(0, 0.02, x.shape)
y_noisy = y + np.random.normal(0, 0.02, y.shape)
z_noisy = z + np.random.normal(0, 0.02, z.shape)

# 
df = pd.DataFrame({
    'timestamp': t,
    'x': x_noisy,
    'y': y_noisy,
    'z': z_noisy
})

# Export to CSV
file_name = "motion_signal.csv"
df.to_csv(file_name, index=False)

print(f"File '{file_name}' has been created successfully!")