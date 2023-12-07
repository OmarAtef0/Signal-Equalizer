import numpy as np
import matplotlib.pyplot as plt
import librosa
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import fft
import librosa
import soundfile as sf
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment
from pydub.playback import play

def read(wav_file):
    # Read the .wav file
    sample_rate, t_amp = wavfile.read(wav_file)

    # Generate time array
    time = np.arange(0, len(t_amp)) / sample_rate

    # Perform Fourier transform
    f_amp = fft.fft(t_amp)
    frequency = fft.fftfreq(len(t_amp), d=1/sample_rate)
    
    # Plot the frequency spectrum
    plt.figure(figsize=(12, 6))
    positive_frequencies = frequency[frequency >= 0]
    print("MAX Freq: ", max(positive_frequencies))
    plt.plot(positive_frequencies, np.abs(f_amp[frequency >= 0]))
    plt.title('Frequency Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.show()

def cut_bandwidth(input_file, output_file, low_freq, high_freq):
    # Load the audio file
    audio, sr = librosa.load(input_file, sr=None)

    # Calculate the frequency components corresponding to the FFT bins
    freqs = librosa.fft_frequencies(sr=sr)

    # Create a binary mask for the specified frequency range
    mask = np.logical_and(freqs >= low_freq, freqs <= high_freq)

    # Apply the mask to the magnitude spectrum of the audio
    stft = librosa.stft(audio)
    stft_filtered = stft * mask[:, np.newaxis]

    # Transform the modified spectrum back to the time domain
    audio_filtered = librosa.istft(stft_filtered)

    # Normalize the audio to bring its overall amplitude to 1
    audio_filtered = librosa.util.normalize(audio_filtered)

    # Save the modified audio using soundfile
    sf.write(output_file, audio_filtered, sr)

# Specify the input and output file paths
input_file_path = 'dataset/Music/instr/flute.wav'
output_file_path = 'dataset/Music/instr/output/output-flute.wav'

# Set the frequency range to cut
low_freq = 0 
high_freq = 12640

# Cut bandwidth and play the modified audio
cut_bandwidth(input_file_path, output_file_path, low_freq, high_freq)

# Plot spectrogram for both original and modified audio
read(input_file_path)
read(output_file_path)
