import numpy as np
from scipy import fft 
import audio

def fourier_transfrom(self, time, amplitude):
  # Perform FFT 
  fft_coef = fft.rfft(amplitude)
  fft_amplitudes = np.abs(fft_coef)
  fft_angle= np.angle(fft_coef)
  
  # Calculate frequencies corresponding to the FFT result
  # This line calculates the frequencies corresponding to the FFT result. fft.fftfreq function is used to 
  # generate an array of frequency values based on the length of the time array and the time step between samples.
  frequency = fft.rfftfreq(len(time), time[1] - time[0])

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
  self.output_signal.time = self.input_signal.time  
  fft_complex_amplitudes = fft.irfft(np.array(self.output_signal.f_amplitude) * np.exp(1j * np.array(self.output_signal.f_angle)))
  inverse_fft_amplitudes = np.abs(fft_complex_amplitudes)
  
  print("time amp before inverse ",self.output_signal.t_amplitude[0:5])
  self.output_signal.t_amplitude = list(inverse_fft_amplitudes)
  print("time amp after inverse: ",self.output_signal.t_amplitude[0:5])
  
  # Calculate time corresponding to the IFFT result
  # time = fft.rfftfreq(len(self.output_signal.frequency), self.output_signal.frequency[1] - self.output_signal.frequency[0])
  # self.output_signal.time = list(time)
  
  self.draw()
  
  if self.current_mode == "Musical Instruments Mode" or self.current_mode == "Animals Sound Mode":
    audio.save_as_wav(self, self.output_signal.t_amplitude) 

  