import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
import pandas as pd

def generate_uniform_signal(duration, sample_rate, frequencies, amplitude):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = amplitude * np.sin(2 * np.pi * np.array(frequencies)[:, None] * t, dtype=np.float32)
    signal = np.sum(signal, axis=0)
    signal /= np.max(np.abs(signal))
    return signal, t

def save_csv(file_path, time, signal):
    df = pd.DataFrame({"Time": time, "Amplitude": signal})
    df.to_csv(file_path, index=False)

def save_wav(file_path, sample_rate, signal):
    wavfile.write(file_path, sample_rate, signal)

def plot_spectrum(sample_rate, signal):
    n = len(signal)
    spectrum = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(n, 1/sample_rate)

    plt.figure(figsize=(10, 4))
    plt.plot(frequencies[:n//2], np.abs(spectrum)[:n//2])
    plt.title('Frequency Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

# Parameters for the synthetic signal
duration = 10 # seconds
sample_rate = 20001  # Hz
frequencies = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
amplitude = 1.0

# Generate synthetic signal
synthetic_signal, time = generate_uniform_signal(duration, sample_rate, frequencies, amplitude)

# Save synthetic signal as CSV
csv_file_path = 'dataset/Uniform Range/uniform_synthetic_signal.csv'
save_csv(csv_file_path, time, synthetic_signal)
print(f"CSV file saved: {csv_file_path}")

# Save synthetic signal as WAV
# wav_file_path = 'dataset/Uniform Range/uniform_synthetic_signal.wav'
# save_wav(wav_file_path, sample_rate, synthetic_signal)
# print(f"WAV file saved: {wav_file_path}")

# Plot the synthetic signal
# plt.figure(figsize=(10, 4))
# plt.plot(time, synthetic_signal)
# plt.title('Uniform Synthetic Signal')
# plt.xlabel('Time (seconds)')
# plt.ylabel('Amplitude')
# plt.grid(True)
# plt.show()

# # Plot the frequency spectrum
# plot_spectrum(sample_rate, synthetic_signal)
