import numpy as np
import fourier
from scipy.signal.windows import boxcar, hamming, hann, gaussian
from PyQt5.QtWidgets import *

def update_plot(self, index, value):
  if self.current_mode == "Uniform Range Mode":
    print(self.uniform_freq_ranges[index])
    update_frequency_range(self, self.uniform_freq_ranges[index], 10**(value))
  
  elif self.current_mode == "Musical Instruments Mode":
    print("music range: ", self.music_freq_ranges[index])
    update_frequency_range(self , self.music_freq_ranges[index], 10**(value))

  elif self.current_mode == "Animals Sound Mode":
    update_frequency_range(self , self.animal_freq_ranges[index], 10**(value))

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
  window_function = create_window_function(self, window_type, len(self.target_indices))
  window_function *= value

  for index, target_i in enumerate(self.target_indices):
    if target_i >= 0 and target_i < len(self.output_signal.f_amplitude): 
      self.output_signal.f_amplitude[target_i] = self.original_signal_f_amplitude[target_i] * window_function[index]
     
def visualize_window(self):
    # Get window type from the UI
    window_type = self.ui.comboBox.currentText()
    if window_type == "Gaussian":
      get_guassian_std(self)
    
    # Create and visualize the window
    window_function = create_window_function(self, window_type, 100)
    self.ui.plot_5.clear()
    x = np.arange(len(window_function))
    self.ui.plot_5.plot(x, window_function)

def create_window_function(self, window_type, length):
    window_function = None
    if window_type == "Rectangle":
        window_function = boxcar(length)
    elif window_type == "Hamming":
        window_function = hamming(length)
    elif window_type == "Hanning":
        window_function = hann(length)
    elif window_type == "Gaussian":
        # Adjust window_params as needed
        window_function = gaussian(length, std=self.Gaussian_std)
    else:
        raise ValueError("Invalid window type")

    return window_function

def get_guassian_std(self):
    dialog = gaussain_std(self)
    result = dialog.exec()

    # Initialize dialog_input with an empty string or a default value
    dialog_input = ""

    if result == QDialog.Accepted:
        dialog_input = dialog.parameter_input.text()

    try:
        # Try to convert the entered value to an integer
        self.Gaussian_std = int(dialog_input)
        print("User entered parameter (as integer):", self.Gaussian_std)
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

class gaussain_std(QDialog):
    def __init__(self, parent=None):
        super(gaussain_std, self).__init__(parent)

        self.setWindowTitle("Gaussian Standrad Deviation")
        self.setGeometry(500, 500, 500, 150)

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Enter Standrad Deviation Value:")
        self.parameter_input = QLineEdit()

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.parameter_input)
        self.layout.addWidget(self.ok_button)