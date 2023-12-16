import sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QWidget, QLabel, \
    QLineEdit, QSlider
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq, irfft


def read_data(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    columns = df.columns
    time = df[columns[0]].values
    signal = df[columns[1]].values
    return time, signal


class FourierTransformApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.minimum = -999999999999999999
        self.maximum = 999999999999999999
        self.time, self.signal = None, None

        self.setWindowTitle('Fourier Transform App')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Push button to import CSV file data and get Fourier transform
        self.import_button = QPushButton('Import', self)
        self.import_button.clicked.connect(self.import_csv)
        self.layout.addWidget(self.import_button)

        # Push button to plot the data and its Fourier transform
        self.plot_button = QPushButton('Plot Data and FFT', self)
        self.plot_button.clicked.connect(self.plot_data)
        self.layout.addWidget(self.plot_button)

        # Slider (functionality to be implemented)
        self.slider_label = QLabel('Slider:', self)
        self.layout.addWidget(self.slider_label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self.slider_value_changed)
        self.slider.setRange(0, 500)
        self.slider.setValue(100)
        self.slider.setSingleStep(5)
        self.layout.addWidget(self.slider)

        # Line Edits (functionality to be implemented)
        self.line_edit1 = QLineEdit(self)
        self.line_edit2 = QLineEdit(self)

        self.layout.addWidget(self.line_edit1)
        self.layout.addWidget(self.line_edit2)

        self.line_edit1.textChanged.connect(self.line_edit1_changed)
        self.line_edit2.textChanged.connect(self.line_edit2_changed)

    def import_csv(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open CSV File', r'Data/arrythmia',
                                                   'CSV Files (*.csv);;All Files (*)')

        if file_path:
            try:
                self.time, self.signal = read_data(file_path)

            except Exception as e:
                print(f"Error: {e}")

    def plot_data(self):
        s_r = 500
        N = len(self.signal)
        T = 1.0 / s_r
        yf = 2 * rfft(self.signal)
        yf[0] = 0
        xf = rfftfreq(N, T)
        if len(xf) != len(yf):
            xf = xf[:len(yf)]

        plt.figure(figsize=(16, 8))

        plt.subplot(2, 2, 1)
        plt.plot(self.time[:len(self.time) // 2][0:1000], self.signal[:len(self.time) // 2][0:1000])
        plt.title('Original Data')

        plt.subplot(2, 2, 2)
        plt.plot(xf, 1.0 / N * np.abs(yf))
        plt.title('Fourier Transform')

        band = (xf > self.minimum) & (xf < self.maximum)
        yf[band] *= self.slider.value() / 100

        y = irfft(yf / 2)
        while len(y) != len(self.time):
            y = np.append(y, 0)

        plt.subplot(2, 2, 3)
        plt.plot(self.time[:len(self.time) // 2][0:1000], y[:len(self.time) // 2][0:1000])
        plt.title('Signal after Bandpass Filter')

        plt.subplot(2, 2, 4)
        plt.plot(xf, 1.0 / N * np.abs(yf))
        plt.title('Signal after Bandpass Filter')

        plt.tight_layout()
        plt.show()

    def slider_value_changed(self, value):
        # Placeholder function for slider value change
        print(f"Slider Value: {value}")

    def line_edit1_changed(self, text):
        try:
            self.minimum = float(text)
        except:
            print("Error in line_edit1_changed")

    def line_edit2_changed(self, text):
        try:
            self.maximum = float(text)
        except:
            print("Error in line_edit2_changed")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = FourierTransformApp()
    main_window.show()
    sys.exit(app.exec_())
