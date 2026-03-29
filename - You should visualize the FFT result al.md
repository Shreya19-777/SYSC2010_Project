- You should visualize the FFT result alongside the time-domain signal
- Statistical results are displayed in a dedicated panel alongside the plots.
- 8.6 Testing and Debugging

• Compare raw vs filtered signals visually and numerically.
• Validate statistical metrics against expected values.


- should handle Large datasets without performance lag

- Apply LPF, HPF, BPF on test signals. Compare filtered signals
against expected outcomes. Check FIR vs IIR behavior

- Verify that raw and processed signals are displayed accurately. Test
zoom, pan, and overlay functions-

- test with multiple CSV files (correctly formatted, missing data,
corrupted entries). Check error handling and warnings

- maybe add units for extraction if applicable
- Filters, FFT, and feature extraction are triggered via GUI actions



examples 1. Filters Triggered via GUI
The user should be able to load a noisy signal and then "decide" to clean it.

GUI Action: The user selects "Low-Pass Filter" from a dropdown menu and clicks a button labeled "Apply Filter."

Result: The filters.py logic runs, and the plot on the screen updates from a jagged line to a smooth line.

Example: If you are looking at an ECG signal with high-frequency muscle noise, clicking the button triggers the filter that removes that "fuzz," leaving only the clear heartbeat pulses.

2. FFT Triggered via GUI
Since computing an FFT can be computationally expensive for very large datasets, you trigger it only when needed.

GUI Action: The user clicks a checkbox or a tab labeled "Show Frequency Spectrum."

Result: The analysis.py module takes the current time-domain data, calculates the Fast Fourier Transform, and generates the second plot alongside the original.

Example: A user looking at Motion (IMU) data might trigger the FFT to see if there is a dominant "shaking" frequency, which would appear as a sharp spike at a specific Hz value.

3. Feature Extraction Triggered via GUI
These are the specific "answers" or "stats" derived from the data.

GUI Action: After loading a file, the user clicks a button labeled "Calculate Heart Rate" or "Analyze Statistics."

Result: The analysis.py module scans the peaks of the signal and calculates a number (e.g., "72 BPM"). This number is then displayed in a text label or a dedicated "Statistics" panel in your GUI.

Example: For a Temperature sensor, the user clicks "Analyze" and the GUI displays the Mean Temperature and the Trend Slope (e.g., "Temperature is rising at 0.5°C/hour").


