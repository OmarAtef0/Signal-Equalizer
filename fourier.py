import numpy as np
from scipy import fft 
import audio

def set_signal_attributes(self, signal, frequencies, fourier_coefficients):
  signal.frequency = frequencies
  signal.f_ampltiude = np.abs(fourier_coefficients)
  signal.angel = np.angle(fourier_coefficients)
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
  self.input_signal.f_angle = list(fft_angle)
  self.input_signal.f_coef = list(fft_coef)

  self.output_signal.frequency = list(frequency)
  self.output_signal.f_amplitude = list(fft_amplitudes)
  self.output_signal.f_angle = list(fft_angle)
  self.output_signal.f_coef = list(fft_coef)

  self.original_signal_f_amplitude = list(self.output_signal.f_amplitude)

def inverse_fourier(self):
  #perform Inverse Fourier Transform
  fft_complex_amplitudes = fft.irfft(np.array(self.output_signal.f_amplitude) * np.exp(1j * np.array(self.output_signal.f_angle)))
  
  if self.current_mode == "Musical Instruments Mode" or self.current_mode == "Animals Sound Mode":
   audio.save_as_wav(self, self.output_signal.t_amplitude)   
  
  print(fft_complex_amplitudes)
  self.output_signal.time = self.input_signal.time  
  self.output_signal.t_amplitude = np.real(fft_complex_amplitudes)

  # print("time amp before inverse ",self.output_signal.t_amplitude[0:5])
  # print("time amp after inverse: ",self.output_signal.t_amplitude[0:5])
  print("time_len_in", len(self.input_signal.time))
  print("amp_len_in", len(self.input_signal.t_amplitude))
  
  print("time_len_out", len(self.output_signal.time))
  print("amp_len_out", len(self.output_signal.t_amplitude))
  
  self.draw()
  

  