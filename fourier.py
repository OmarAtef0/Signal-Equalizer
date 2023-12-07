import numpy as np
from numpy.fft import fft, rfftfreq
from scipy import fft
import audio
import spectogram

def fourier_transfrom(self, time, amplitude):
  # Perform FFT - This line computes the FFT of the input signal amplitude using NumPy's fft function.
  fft_coef = fft.rfft(amplitude)
  fft_amplitudes = np.abs(fft_coef)
  fft_angle= np.angle(fft_coef)
  
  # Calculate frequencies corresponding to the FFT result
  # This line calculates the frequencies corresponding to the FFT result. The np.fft.fftfreq function is used to generate an array of frequency values based on the length of the time array and the time step between samples.
  frequency = rfftfreq(len(time), time[1] - time[0])

  self.input_signal.frequency = list(frequency)
  self.input_signal.f_amplitude = list(fft_amplitudes)
  self.input_signal.f_angle = list(fft_angle)
  self.input_signal.f_coef = list(fft_coef)

  self.output_signal.frequency = list(frequency)
  self.output_signal.f_amplitude = list(fft_amplitudes)
  self.output_signal.f_angle = list(fft_angle)
  self.output_signal.f_coef = list(fft_coef)

  self.draw()

  if self.ok:
    self.ok = False
    self.draw_spectrograms()

def inverse_fourier(self):
  fft_complex_amplitudes = fft.irfft(np.array(self.output_signal.f_amplitude) * np.exp(1j * np.array(self.output_signal.f_angle)))
  # fft_complex_amplitudes = fft.irfft(self.output_signal.f_amplitude * np.exp(1j * self.output_signal.f_angle))
  inverse_fft_amplitudes = np.abs(fft_complex_amplitudes)
  
  # Calculate time corresponding to the IFFT result
  # time = fft.rfftfreq(len(self.output_signal.frequency), self.output_signal.frequency[1] - self.output_signal.frequency[0])
  # self.output_signal.time = list(time)

  print("time before inverse ",self.output_signal.t_amplitude[0:5])
  self.output_signal.t_amplitude = list(inverse_fft_amplitudes)

  self.draw()
  spectogram.CreateSpectrogram(self.axes2, self.figure2, self.ui.Spectrogram_2, self.output_signal.t_amplitude, self.output_signal.time)
  audio.save_as_wav(self, self.output_signal.t_amplitude)

  print("time after inverse: ",self.output_signal.t_amplitude[0:5])

  

