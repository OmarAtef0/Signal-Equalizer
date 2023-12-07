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
    #Toggle Visibility of spectrogram
    for i in range(spectrogram_box.count()):
        item = spectrogram_box.itemAt(i)
        if item is not None and item.widget():
            item.widget().setVisible(not item.widget().isVisible())


def CreateSpectrogram(axes, figure, spectrogram_box, amplitude_list, time_list):

    clear_spectrogram(spectrogram_box)  
    
    # Set the backend explicitly
    matplotlib.use('Agg')

    # Turn off interactive mode
    matplotlib.interactive(False)   

    # Create a new figure with a black background
    figure = plt.figure()
    figure.patch.set_facecolor('black')
    axes = figure.add_subplot()
    spectrogram = Canvas(figure)
    spectrogram_box.addWidget(spectrogram)

    # Convert to numpy arrays to ensure compatibility
    amplitude_list = np.array(amplitude_list)
    
    # Plot the spectrogram
    axes.specgram(amplitude_list, NFFT=256, Fs=1 / (time_list[1] - time_list[0]), cmap='viridis')
    axes.set_xlabel('Time (s)', color='white')
    axes.set_ylabel('Frequency (Hz)', color='white')
    figure.colorbar(axes.images[0], ax=axes, label='Intensity (dB)')

    return axes, figure
    
def clear_spectrogram(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
