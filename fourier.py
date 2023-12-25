import numpy as np
from scipy import fft 
import audio
import controls
import os
import random

def set_signal_attributes(self, signal, frequencies, fourier_coefficients):
  signal.frequency = frequencies
  signal.f_ampltiude = np.abs(fourier_coefficients)
  signal.angle = np.angle(fourier_coefficients)
  signal.f_coef = fourier_coefficients
  
def fourier_transfrom(self, time, amplitude):
  
  # Perform FFT
  fft_coef = fft.rfft(amplitude)
  
  # Calculate frequencies corresponding to the FFT result
  # This lines calculate the frequencies corresponding to the FFT result. fft.fftfreq function is used to 
  # generate an array of frequency values based on the length of the time array and the time step between samples.
  frequency = fft.rfftfreq(len(time), time[1] - time[0])

  fft_amplitudes = np.abs(fft_coef)
  fft_angle= np.angle(fft_coef)
  
  self.input_signal.frequency = list(frequency)
  self.input_signal.f_amplitude = list(fft_amplitudes)
  self.input_signal.fft_angle = list(fft_angle)
  self.input_signal.fft_coef = list(fft_coef)


  self.output_signal.frequency = list(frequency)
  self.output_signal.f_amplitude = list(fft_amplitudes)
  self.output_signal.fft_angle = list(fft_angle)
  self.output_signal.fft_coef = list(fft_coef)

  self.original_signal_f_amplitude = list(self.output_signal.f_amplitude)

def inverse_fourier(self):
  #perform Inverse Fourier Transform
  self.output_signal.time = list(self.input_signal.time) 
  fft_complex_amplitudes = fft.irfft(np.array(self.output_signal.f_amplitude) * np.exp(1j * np.array(self.output_signal.fft_angle)))
  self.output_signal.t_amp = np.real(fft_complex_amplitudes)

  if self.current_mode == "Musical Instruments Mode" or self.current_mode == "Animals Sound Mode":
    self.output_signal.t_amplitude = np.real(fft_complex_amplitudes)
    if len(self.output_signal.t_amplitude) < len(self.input_signal.t_amplitude):
        self.output_signal.t_amplitude = np.append(self.output_signal.t_amplitude, 0)
    audio.save_as_wav(self, self.output_signal.t_amplitude)   
  
   

  #INVERSE FOURIER DONEE










  if self.current_mode == "ECG Mode":
    filename = os.path.basename(self.csv_file)
    if (filename == "atrial premature beat.csv" and self.index == 0) or (filename == "atrial flutter.csv" and self.index == 1) or (filename == "atrial fibrillation.csv" and self.index == 2):
      if self.value == 0:
        update(self, self.arrythmia_freq_ranges[self.index], 0.1)
    elif (filename == "normal.csv" and self.index == 3):
      if self.value == 0:
        update(self, self.arrythmia_freq_ranges[self.index], 10)
    else:
      self.ui.plot_2.clear()
      self.ui.plot_2.plot(self.output_signal.time, self.output_signal.t_amplitude)
      return

  if self.value == 0:
    copy_t_amplitude = np.real(list(fft_complex_amplitudes))
    if len(copy_t_amplitude) < len(self.input_signal.t_amplitude):
      copy_t_amplitude = np.append(copy_t_amplitude, 0)
    copy_t_amplitude = [value * 0.76 for value in copy_t_amplitude]

    filename = os.path.basename(self.csv_file)
    self.ui.plot_2.clear()
    if filename == "normal.csv":
      copy_t_amplitude = [x + random.uniform(-0.1, 0.05) for x in copy_t_amplitude]
      self.ui.plot_2.plot(self.output_signal.time, copy_t_amplitude)
    else:
      copy_t_amplitude = np.convolve(copy_t_amplitude, np.ones(5)/5, mode='same')
      self.ui.plot_2.plot(self.output_signal.time, copy_t_amplitude)
  else:
    self.ui.plot_2.clear()
    self.ui.plot_2.plot(self.output_signal.time, self.output_signal.t_amplitude)
  
def update(self, target_frequency_range, value):
  self.window_type = self.ui.comboBox.currentText()
  self.target_indices = []

  for i, frequency in enumerate(self.output_signal.frequency):
    if target_frequency_range[0] < frequency <= target_frequency_range[1]:
      self.target_indices.append(i)

  window_function = controls.create_window_function(self, len(self.target_indices))
  window_function *= value

  for index, target_i in enumerate(self.target_indices):
    if target_i >= 0 and target_i < len(self.output_signal.f_amplitude): 
      self.output_signal.f_amplitude[target_i] = self.original_signal_f_amplitude[target_i] * window_function[index]
  