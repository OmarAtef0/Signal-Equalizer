import neurokit2 as nk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate synthetic ECG signal
simulated_ecg = nk.ecg_simulate(duration=8, sampling_rate=200)

# Create a time vector
time = np.arange(0, len(simulated_ecg)) / 200

# Create a DataFrame
ecg_data = pd.DataFrame({"Time": np.arange(0, len(simulated_ecg)) / 200, "ECG": simulated_ecg})

# Plot the synthetic ECG signal using Matplotlib
plt.figure(figsize=(10, 4))
plt.plot(time, simulated_ecg, label='Synthetic ECG')
plt.title('Synthetic ECG Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.show()

# Save to CSV
csv_filename = "normal_ecg.csv"
ecg_data.to_csv(csv_filename, index=False)

# Plot the synthetic ECG signal
nk.signal_plot(simulated_ecg, sampling_rate=200)
