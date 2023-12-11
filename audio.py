import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import  QFileDialog
from classes import *
import sounddevice as sd
import pygame
from scipy.io import wavfile
import time

def save_as_wav(self, amplitude):
  self.generated_audio_file = True
  amplitude_array = np.array(amplitude)

  wavfile.write(f"dataset/outputs/output_{self.output_num}.wav", self.output_signal.sample_rate, amplitude_array.astype(np.int16))
  print(f"output_{self.output_num}")
  self.output_num = self.output_num + 1

def browse_audio(self):
  options = QFileDialog.Options()
  file_name, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.mp3 *.wav);;All Files (*)", options=options)

  if file_name:
    self.audio_file = file_name
    audio_data(self, file_name)
    self.started = False 

def audio_data(self, filename):
  if filename.lower().endswith('.wav'):
      sample_rate, amplitude = wavfile.read(filename)
  else:
      QtWidgets.QMessageBox.warning(self, 'Warning', "Unsupported file format. Please select a valid MP3 or WAV file.")
      return

  # Convert to mono if stereo
  if len(amplitude.shape) > 1:
      amplitude = np.mean(amplitude, axis=1)

  # Create time array
  time = np.arange(0, len(amplitude)) / sample_rate

  self.input_signal.time = time
  self.input_signal.t_amplitude = amplitude
  self.input_signal.sample_rate = sample_rate
  self.output_signal.sample_rate = sample_rate
  
def play_audio(self, audio_file):
  if self.current_mode != "Musical Instruments Mode" and self.current_mode != "Animals Sound Mode":
     return
  if self.generated_audio_file:
    _play_audio(self)
    if self.playing:
      pause_audio(self)
    elif not self.playing:
      resume_audio(self)
     
  elif self.started == False:
    if audio_file:
        _play_audio(self)
        self.playing = True
        self.started = True
    else:
        QtWidgets.QMessageBox.warning(self, 'Warning', "No audio file loaded.")
  else:
    if self.playing:
      pause_audio(self)
    elif not self.playing:
      resume_audio(self)

def _play_audio(self):
  if self.generated_audio_file:
    # amplitude_array = list(self.output_signal.t_amplitude)

    # # Normalize the amplitude array to be in the range [-1, 1]
    # amplitude_array = np.array(amplitude_array)
    # amplitude_array = amplitude_array / np.max(np.abs(amplitude_array))

    # # Play the audio using sounddevice
    # sd.play(amplitude_array, self.output_signal.sample_rate)
    
    # # time.sleep(10)
    # # sd.stop()
    # self.ui.play_pause_btn.setText("Play")
    # # sd.wait()  # Wait for the audio to finish playing

    pygame.mixer.music.load(f'dataset/outputs/output_{self.output_num - 1}.wav')
    pygame.mixer.music.play()
  else:
    pygame.mixer.music.load(self.audio_file)
    pygame.mixer.music.play()
    
  

def pause_audio(self):
  pygame.mixer.music.pause()
  self.playing = False
  
def resume_audio(self):
  pygame.mixer.music.unpause()
  self.playing = True


  
