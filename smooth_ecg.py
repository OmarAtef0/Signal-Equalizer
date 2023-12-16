import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

input_file_path = "dataset\ECG\data\\arrythmia_1.csv"

ecg_data = pd.read_csv(input_file_path)
time = ecg_data.iloc[:, 0].values
time *= 100
signal = ecg_data.iloc[:, 1].values

def moving_average(signal, window_size):
    return np.convolve(signal, np.ones(window_size)/window_size, mode='same')

window_size = 15
smoothed_ecg = moving_average(signal, window_size)

# temp = list(smoothed_ecg)
# smoothed_ecg = list(signal)
# smoothed_ecg = temp

plt.figure(figsize=(12, 12))

plt.subplot(1, 2, 1)
plt.plot(time[0:600], signal[0:600], label='Original Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.subplot(1, 2, 2)
plt.plot(time[0:600], smoothed_ecg[0:600], label='Smoothed Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
 
plt.tight_layout()
plt.show()

