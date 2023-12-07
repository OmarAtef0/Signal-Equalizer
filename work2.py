import numpy as np
import matplotlib.pyplot as plt
import librosa
import soundfile as sf

def cut_most_significant_bandwidth(input_file, output_file, max_bandwidth_length):
    # Load the audio file
    audio, sr = librosa.load(input_file, sr=None)

    # Calculate the frequency components corresponding to the FFT bins
    freqs = librosa.fft_frequencies(sr=sr)

    # Perform Fourier transform
    stft = librosa.stft(audio)
    magnitude = np.abs(stft)

    # Sum the magnitudes along the time axis to find the frequency importance
    freq_importance = np.sum(magnitude, axis=1)

    # Find the frequency range with the most significant components
    most_significant_range = np.argmax(freq_importance)
    
    # Determine the frequency range (centered and adjusted if it exceeds 5000 Hz)
    center_freq = freqs[most_significant_range]
    low_freq = max(0, center_freq - max_bandwidth_length / 2)
    high_freq = min(sr / 2, center_freq + max_bandwidth_length / 2)

    # Adjust the range if the difference exceeds 5000 Hz
    if high_freq - low_freq > max_bandwidth_length:
        low_freq = center_freq - max_bandwidth_length / 2
        high_freq = center_freq + max_bandwidth_length / 2

    # Print the determined frequency range
    print(f"Determined Frequency Range: {low_freq} Hz to {high_freq} Hz")

    # Create a binary mask for the specified frequency range
    mask = np.logical_and(freqs >= low_freq, freqs <= high_freq)

    # Apply the mask to the magnitude spectrum of the audio
    stft_filtered = stft * mask[:, np.newaxis]

    # Transform the modified spectrum back to the time domain
    audio_filtered = librosa.istft(stft_filtered)

    # Save the modified audio using soundfile
    sf.write(output_file, audio_filtered, sr)

# Specify the input and output file paths
input_file_path = 'dataset/Music/instr/flute.wav'
output_file_path = 'dataset/Music/instr/output/output-flute.wav'

# Set the maximum bandwidth length to 5000 Hz
max_bandwidth_length = 23500

# Cut the most significant bandwidth and save the modified audio
cut_most_significant_bandwidth(input_file_path, output_file_path, max_bandwidth_length)


# guitar: 0 Hz to 2734 Hz
# flute: 2735 Hz to 4336 Hz


