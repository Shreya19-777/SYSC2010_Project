import numpy as np
import pandas as pd

num_samples = 1000
interval_sec = 60
seconds = np.arange(0, num_samples * interval_sec, interval_sec)

# Realistic slow drift (stays within normal body temp range)
drift = np.cumsum(np.random.normal(0, 0.005, size=num_samples))  # smaller drift
drift = np.clip(drift, -1.0, 1.0)  # clamp so it doesn't wander too far

# Add high frequency noise on top
noise = np.random.normal(0, 0.05, size=num_samples)

# Combine: baseline + slow drift + noise
temperatures = 36.7 + drift + noise
temperatures = np.clip(temperatures, 35.5, 38.5)  # keep within realistic range

df = pd.DataFrame({
    'time': seconds,
    'signal': np.round(temperatures, 2)
})

df.to_csv("temp.csv", index=False)

num_samples = 5000
fs = 100  # 100 Hz sampling rate
seconds = np.arange(0, num_samples / fs, 1/fs)

# Simulate walking motion (dominant frequency ~2 Hz)
motion = np.sin(2 * np.pi * 2 * seconds)  # 2 Hz walking signal

# Add higher frequency vibration noise
noise = np.random.normal(0, 0.1, size=num_samples)

# Add occasional spikes (motion artifacts)
spikes = np.zeros(num_samples)
spike_locations = np.random.choice(num_samples, size=20, replace=False)
spikes[spike_locations] = np.random.uniform(2, 4, size=20)

accelerometer_x = motion + noise + spikes

df_imu = pd.DataFrame({
    'time': seconds,
    'signal': np.round(accelerometer_x, 4)
})

df_imu.to_csv("imu.csv", index=False)

import numpy as np
import pandas as pd

num_samples = 5000
fs = 100  # 100 Hz sampling rate
seconds = np.arange(0, num_samples / fs, 1/fs)

# Normal breathing ~15 breaths/min = 0.25 Hz
breathing_rate = 0.25
respiration = np.sin(2 * np.pi * breathing_rate * seconds)

# Add baseline drift (slow wandering)
drift = np.cumsum(np.random.normal(0, 0.001, size=num_samples))
drift = np.clip(drift, -0.3, 0.3)

# Add high frequency noise
noise = np.random.normal(0, 0.05, size=num_samples)

respiration_signal = respiration + drift + noise

df_resp = pd.DataFrame({
    'time': seconds,
    'signal': np.round(respiration_signal, 4)
})

df_resp.to_csv("respiration.csv", index=False)