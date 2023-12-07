import numpy as np
import fourier
from scipy.signal.windows import boxcar, hamming, hann, gaussian

def split_into_ranges(self, max_frequency, num_of_sliders):
  range_size = max_frequency / num_of_sliders
  self.uniform_freq_ranges = [[i * range_size, (i + 1) * range_size] for i in range(num_of_sliders)]
  print("uniform_freq_ranges", self.uniform_freq_ranges)

def update_plot(self, index, value):
  print("index: ",index)
  print("value: ", (value))
  if self.current_mode == "Uniform Range Mode":
    print(self.uniform_freq_ranges[index])
    update_frequency_range(self, self.uniform_freq_ranges[index], 10**(value))
  
  elif self.current_mode == "Musical Instruments Mode":
    print("music range: ", self.music_dict[index])
    update_frequency_range(self , self.music_dict[index], 10**(value))

  elif self.current_mode == "Animals Sound Mode":
    update_frequency_range(self , [0,1000], 10**(value))

  # make dict to map slider index to its frequency range
  elif self.current_mode == "ECG Mode":
    update_frequency_range(self , [0,1000], 10**(value))
  

  # Apply IFFT to get the modified time-domain signal
  fourier.inverse_fourier(self)

def update_frequency_range(self, target_frequency_range, value):
  # Identify the indices corresponding to the target frequency range
  self.target_indices = []
  for i, frequency in enumerate(self.output_signal.frequency):
    if target_frequency_range[0] <= frequency <= target_frequency_range[1]:
      self.target_indices.append(i)

  window_type = self.ui.comboBox.currentText()
  window_function = create_window_function(window_type, len(self.target_indices))
  window_function *= value
  print("window_function: ",window_function)

  for target_i in self.target_indices[:5]:
    print(self.output_signal.f_amplitude[target_i])

  print()

  for index, target_i in enumerate(self.target_indices):
    if target_i >= 0 and target_i < len(self.output_signal.f_amplitude): 
      self.output_signal.f_amplitude[target_i] = self.original_signal_f_amplitude[target_i] * window_function[index]
  
  for target_i in self.target_indices[:5]:
    print(self.output_signal.f_amplitude[target_i])
      
def visualize_window(self):
    # Get window type from the UI
    window_type = self.ui.comboBox.currentText()

    # Create and visualize the window
    window_function = create_window_function(window_type, 100)
    self.ui.plot_5.clear()
    x = np.arange(len(window_function))
    self.ui.plot_5.plot(x, window_function)

def create_window_function(window_type, length):
    window_function = None
    if window_type == "Rectangle":
        window_function = boxcar(length)
    elif window_type == "Hamming":
        window_function = hamming(length)
    elif window_type == "Hanning":
        window_function = hann(length)
    elif window_type == "Gaussian":
        # Adjust window_params as needed
        window_function = gaussian(length, std=3)  # STD msh 3aref teb2a static wla eluser bydkhalha
    else:
        raise ValueError("Invalid window type")

    return window_function

    
    