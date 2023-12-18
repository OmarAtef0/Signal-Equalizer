import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import fft 

def cut_frequency_range_and_plot(csv_file, start_freq, end_freq, scale_factor=1):
    # Load ECG signal from CSV file
    ecg_data = pd.read_csv(csv_file)
    time = ecg_data.iloc[:, 0].values
    signal = ecg_data.iloc[:, 1].values

    # Calculate the Fourier transform of the signal
    signal_fft = fft.rfft(signal)

    # Get the frequencies corresponding to the Fourier transform
    frequencies = np.fft.rfftfreq(len(signal), d=(time[1] - time[0]))

    # Plot the original and filtered signals along with their spectra
    plt.figure(figsize=(12, 12))

    plt.subplot(4, 1, 1)
    plt.plot(time[0:1000], signal[0:1000], label='Original Signal')
    plt.title('Original ECG Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    plt.subplot(4, 2, 5)
    plt.plot(frequencies, np.abs(signal_fft), label='Original Spectrum')
    plt.title('Original Signal Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.ylim(0, 10000)  

    # Identify the indices corresponding to the frequency range to be scaled
    cut_indices = np.where((frequencies >= start_freq) & (frequencies <= end_freq))

    # Scale the amplitude in the specified frequency range
    signal_fft[cut_indices] *= scale_factor

    # Perform the inverse Fourier transform
    signal_filtered = fft.irfft(signal_fft)
    signal_filtered = np.append(signal_filtered, 0)

    signal_filtered = np.convolve(signal_filtered, np.ones(10)/10, mode='same')

    plt.subplot(4, 1, 2)
    plt.plot(time[0:1000], signal_filtered[0:1000], label=f'Filtered Signal ({start_freq} - {end_freq} Hz)')
    plt.title('Filtered ECG Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')


    plt.subplot(4, 2, 6)
    plt.plot(frequencies, np.abs(signal_fft), label='Filtered Spectrum')
    plt.title('Filtered Signal Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.ylim(0, 10000)  

    plt.tight_layout()
    plt.show()

# Example usage:
ecg_csv_file = "dataset\ECG\data\\arrythmia_1.csv"
cut_start_freq = 50
cut_end_freq = 170

cut_frequency_range_and_plot(ecg_csv_file, cut_start_freq, cut_end_freq, 0)
