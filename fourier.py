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
  fft_complex_amplitudes = fft.irfft(np.array(self.output_signal.f_amplitude) * np.exp(1j * np.array(self.output_signal.fft_angle)))
  
  if self.current_mode == "Musical Instruments Mode" or self.current_mode == "Animals Sound Mode":
   audio.save_as_wav(self, self.output_signal.t_amplitude)   
  
  self.output_signal.time = list(self.input_signal.time)  
  if self.smooth == True:
    copy_t_amplitude = np.real(fft_complex_amplitudes)
    if len(copy_t_amplitude) < len(self.input_signal.t_amplitude):
      copy_t_amplitude = np.append(copy_t_amplitude, 0)
  else:
    self.output_signal.t_amplitude = np.real(fft_complex_amplitudes)
    if len(self.output_signal.t_amplitude) < len(self.input_signal.t_amplitude):
      self.output_signal.t_amplitude = np.append(self.output_signal.t_amplitude, 0)
  
  self.ui.plot_2.clear()

  if self.smooth == True:
    self.smooth = False
    copy_t_amplitude = [value * 0.76 for value in copy_t_amplitude]

    filename = os.path.basename(self.csv_file)
    if filename == "normal.csv":
      print("graph noised")
      copy_t_amplitude = [x + random.uniform(-0.1, 0.05) for x in copy_t_amplitude]
      self.ui.plot_2.plot(self.output_signal.time, copy_t_amplitude)
    else:
      print("graph smoothed")
      copy_t_amplitude = np.convolve(copy_t_amplitude, np.ones(5)/5, mode='same')
      self.ui.plot_2.plot(self.output_signal.time, copy_t_amplitude)
  else:
    print("no effect: graph original")
    self.ui.plot_2.plot(self.output_signal.time, self.output_signal.t_amplitude)
  

  