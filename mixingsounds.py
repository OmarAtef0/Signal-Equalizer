import numpy as np
import matplotlib.pyplot as plt
import librosa
import soundfile as sf
from scipy.io import wavfile
from scipy import fft
import pygame
import time

def play_wav_file(file_path):
    pygame.init()

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        time.sleep(6)

    except Exception as e:
        print(f"Error playing the audio: {e}")

    finally:
        pygame.mixer.quit()

def read(wav_file, ok):
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
    plt.plot(positive_frequencies, np.abs(f_amp[frequency >= 0]))
    if ok:
        plt.title('Input Frequency Spectrum')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        # plt.ylim(0, 30000)    
        plt.show()
    else:
        plt.title('Output Frequency Spectrum')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        # plt.ylim(0, 30000)
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
# lst = ["accordion", "accordion2","clarinet","flute","guitar","guitar2","harmonica","piano","piano2","sax","sax2","violin","drums","drums2"]
# lst = ["bird","cat","cow","elephant","lion","sheep","dolphin","horse","dinasour","crow","chicken","goat","fly"]/
lst = ["bird"]

for inst in lst:
    print(inst)
    input_file_path = f"dataset/Animals/anis/{inst}.wav"
    output_file_path = f'dataset/Animals/anis/output/output-{inst}.wav'

    # Set the frequency range to cut
    low_freq = 4000
    high_freq = 24000

    # Cut bandwidth and play the modified audio%
    cut_bandwidth(input_file_path, output_file_path, low_freq, high_freq)

    read(input_file_path, True)
    read(output_file_path, False)
    play_wav_file(output_file_path)
