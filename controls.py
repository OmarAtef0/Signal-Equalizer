import numpy as np
import fourier
from scipy.signal.windows import boxcar, hamming, hann, gaussian
from PyQt5.QtWidgets import *
import pyqtgraph as pg


def update_plot(self, index, value):
  self.value = value
  self.index = index

  update_frequency_range(self, self.current_range[index], 10**(value))
  fourier.inverse_fourier(self)

def update_frequency_range(self, target_frequency_range, value):
  self.window_type = self.ui.comboBox.currentText()
  self.target_indices = []

  for i, frequency in enumerate(self.output_signal.frequency):
    if target_frequency_range[0] < frequency <= target_frequency_range[1]:
      self.target_indices.append(i)

  window_function = create_window_function(self, len(self.target_indices))
  window_function *= value

  for index, target_i in enumerate(self.target_indices):
    if target_i >= 0 and target_i < len(self.output_signal.f_amplitude): 
      self.output_signal.f_amplitude[target_i] = self.original_signal_f_amplitude[target_i] * window_function[index]

  self.ui.plot_3.clear()
  self.ui.plot_3.plot(self.output_signal.frequency, self.output_signal.f_amplitude)
  
  for index, rng in enumerate(self.current_range):
    length = rng[1] - rng[0]
    self.x_overlay = np.arange(rng[0], rng[1])

    self.window_function = create_window_function(self, length)

    slider = getattr(self.ui, f"verticalSlider_{index + 1}")
    if slider.value() == 0:
       self.window_function *= 1
    else:
      self.window_function *= max(self.output_signal.f_amplitude) 

    self.ui.plot_3.plot(self.x_overlay, self.window_function, pen=pg.mkPen(color='r'))
     
def visualize_window(self):
  self.ui.plot_5.clear()

  # Get window type from the UI
  self.window_type = self.ui.comboBox.currentText()
  if self.window_type == "Gaussian":
    get_guassian_std(self)
  
  # Create and visualize the window
  window_function = create_window_function(self, 100)
  x_values = np.arange(len(window_function))
  self.ui.plot_5.plot(x_values, window_function)

def create_window_function(self, length):
  window_function = None
  if self.window_type == "Rectangle":
      window_function = boxcar(length)
  elif self.window_type == "Hamming":
      window_function = hamming(length)
  elif self.window_type == "Hanning":
      window_function = hann(length)
  elif self.window_type == "Gaussian":
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