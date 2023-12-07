from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *

# # Set global plot parameters for a dark background
plt.rcParams['axes.facecolor'] = 'black'       # Background color of the plot area
plt.rc('axes', edgecolor='w')                  # Edge color of the plot area
plt.rc('xtick', color='w')                     # X-axis tick color
plt.rc('ytick', color='w')                     # Y-axis tick color
plt.rcParams['savefig.facecolor'] = 'black'    # Background color when saving figures
plt.rcParams["figure.autolayout"] = True       # Automatically adjust subplot parameters to fit the figure

def toggle_spectrogram(self, spectrogram_box):

    # spectrogram_box.setVisibility(not spectrogram_box.isVisible())
    for i in range(spectrogram_box.count()):
        item = spectrogram_box.itemAt(i)
        if item is not None and item.widget():
            item.widget().setVisible(not item.widget().isVisible())
    # if self.ui.ShowHide_1.isChecked():
    #     print("clear")
    #     
    # else:
    #     self.draw_spectrograms()

def CreateSpectrogram(axes, figure, spectrogram_box, amplitude_list, time_list):

    for i in range(spectrogram_box.count()):
        item = spectrogram_box.itemAt(i)
        if item is not None and item.widget():
            spectrogram_box.removeWidget(item.widget())
            
    # Set the backend explicitly
    matplotlib.use('Agg')

    # Turn off interactive mode
    matplotlib.interactive(False)   

    # Create a new figure with a black background
    figure = plt.figure()
    figure.patch.set_facecolor('black')

    # Add a subplot (axes) to the self.figure
    axes = figure.add_subplot()

    # Create a Canvas widget to embed the self.figure
    spectrogram = Canvas(figure)

    # Add the Canvas widget to the layout
    spectrogram_box.addWidget(spectrogram)

    # Convert to numpy arrays to ensure compatibility
    amplitude_list = np.array(amplitude_list)
    
    # Plot the spectrogram
    axes.specgram(amplitude_list, NFFT=256, Fs=1 / (time_list[1] - time_list[0]), cmap='viridis')
    axes.set_xlabel('Time (s)', color='white')
    axes.set_ylabel('Frequency (Hz)', color='white')
    figure.colorbar(axes.images[0], ax=axes, label='Intensity (dB)')

    return axes, figure

def update_spectrogram(self):
    self.axes2.clear()

    # Create a new spectrogram using imshow
    spec = self.axes2.specgram(self.output_signal.t_amplitude, NFFT=256, Fs=1 / (self.output_signal.time[1] - self.output_signal.time[0]), cmap='viridis')

    # Update the data of the existing Axes with the new spectrogram
    self.axes2.imshow(np.abs(spec[0]), aspect='auto', cmap='viridis', extent=(spec[1][0], spec[1][-1], spec[2][0], spec[2][-1]))
    self.axes2.set_xlabel('Time (s)', color='white')
    self.axes2.set_ylabel('Frequency (Hz)', color='white')
    self.figure2.colorbar(self.axes2.images[0], ax=self.axes2, label='Intensity (dB)')
    # Redraw the canvas
    self.figure2.canvas.draw()