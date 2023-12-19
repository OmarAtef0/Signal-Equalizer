import csv
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from task3 import Ui_MainWindow
import pyqtgraph as pg
from classes import *
import pygame
import qdarkstyle


#IMPORT MODULES
import audio
import controls
import spectogram
import fourier
class SignalEqualizer(QMainWindow):
  
  def __init__(self):
    super().__init__()
    # Set up the UI
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)  

    self.browsed_signal = SampledSignal()
    self.input_signal = Signal()
    self.output_signal = Signal()
    self.original_signal_f_amplitude = []
    
    #browse
    self.ui.actionOpen.triggered.connect(self.open_signal) 
    
    # modes
    self.current_mode = "Uniform Range Mode"
    self.ui.actionUniform_Range_Mode.triggered.connect(self.change_mode)
    self.ui.actionMusical_Instruments_Mode.triggered.connect(self.change_mode)
    self.ui.actionAnimals_Sound_Mode.triggered.connect(self.change_mode)
    self.ui.actionECG_Mode.triggered.connect(self.change_mode)

    # SLIDERS DICTIONARY
    self.sliders_dict = {
    "Uniform Range Mode": 10,
    "Musical Instruments Mode": 4,
    "Animals Sound Mode": 4,
    "ECG Mode": 4
    }
    
    self.num_of_sliders = self.sliders_dict[self.current_mode]

    # mouse
    # self.ui.plot_1.setMouseEnabled(x=False, y=False)
    # self.ui.plot_2.setMouseEnabled(x=False, y=False)
    # self.ui.plot_3.setMouseEnabled(x=False, y=False)
    # self.ui.plot_5.setMouseEnabled(x=False, y=False)

    # zoom
    self.ui.ZoomIn.clicked.connect(self.update_zoom_in)
    self.ui.ZoomOut.clicked.connect(self.update_zoom_out)

    # reset
    self.ui.reset_btn.clicked.connect(self.reset_plots)

    # x ranges
    self.x_range = [0.0, 4.0]

    # speed
    self.x_range_speed = 0.05
    self.ui.speed_slider.valueChanged.connect(self.update_playback_speed)

    # timer
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.update_plots)

    self.audio_file = ""
    self.generated_audio_file = False

    self.playing = False
    self.started = False

    #play/pause
    self.ui.play_pause_btn.clicked.connect(self.toggle_playback)
    self.ui.play_pause_btn.clicked.connect(lambda: audio.play_audio(self, self.audio_file))
  
    self.MaxX, self.MinX, self.MaxY, self.MinY = 0, 0, 0, 0

    self.ui.plot_1.setLabel('left', 'Amplitude')
    self.ui.plot_1.setLabel('bottom', 'Time (s)')
    self.ui.plot_2.setLabel('left', 'Amplitude')
    self.ui.plot_2.setLabel('bottom', 'Time (s)')
    self.ui.plot_3.setLabel('left', 'Amplitude')
    self.ui.plot_3.setLabel('bottom', 'Frequency (Hz)')
    self.csv_file = ""

    self.ui.comboBox.currentIndexChanged.connect(lambda: controls.visualize_window(self))
    self.Gaussian_std = 5
    self.output_num = 1
    self.sliders_on_off = False
    self.smooth = False

    self.axes1, self.figure1 = None, None
    self.axes2, self.figure2 = None, None

    self.current_range = []
    self.window_type = ""

    self.uniform_freq_ranges =[
      [0,1000],
      [1000, 2000], 
      [2000, 3000],
      [3000, 4000],
      [4000, 5000],
      [5000, 6000],
      [6000, 7000],
      [7000, 8000],
      [8000, 9000],
      [9000, 10000],
    ]

    self.music_freq_ranges = [
      [0, 600], 
      [601, 1000], 
      [1001, 2000], 
      [2001, 25000] 
      ]
    self.music_names = ["piano", "glockspiel" , "guitar" ,"violin"]

    self.animal_freq_ranges = [
      [0, 1000], 
      [1001, 1800], 
      [1801, 4000], 
      [4001, 24000]
      ]
    self.animal_names = [ "dog", "cow", "cat", "bird" ]

    self.arrythmia_freq_ranges = [
      [20, 100], 
      [30, 75], 
      [50, 60],  
      [0, 0]    
      ]
    self.arryhtmia_names = [ "atrial premature beat", "atrial flutter", "atrial fibrillation", "normal" ]
    
    self.ui.ShowHide_1.stateChanged.connect(lambda: spectogram.toggle_spectrogram(self, self.ui.Spectrogram_1))
    self.ui.ShowHide_2.stateChanged.connect(lambda: spectogram.toggle_spectrogram(self, self.ui.Spectrogram_2))
    self.target_indices = []

    self.window_function = []
    self.x_overlay = []

    # Initialize pygame mixer
    pygame.mixer.init()
    
  def draw_spectrograms(self):
    spectogram.CreateSpectrogram(self.axes1, self.figure1, self.ui.Spectrogram_1, self.input_signal.t_amplitude, self.input_signal.time)
    spectogram.CreateSpectrogram(self.axes2, self.figure2, self.ui.Spectrogram_2, self.output_signal.t_amplitude, self.output_signal.time)
  
  def draw(self):
    self.ui.plot_1.clear()
    self.ui.plot_2.clear()
    self.ui.plot_3.clear()

    self.ui.plot_1.plot(self.input_signal.time, self.input_signal.t_amplitude)
    self.ui.plot_2.plot(self.output_signal.time, self.output_signal.t_amplitude)
    self.ui.plot_3.plot(self.output_signal.frequency, self.output_signal.f_amplitude)
    
    self.ui.plot_1.plotItem.enableAutoRange(pg.ViewBox.YAxis, enable=False)
    self.ui.plot_2.plotItem.enableAutoRange(pg.ViewBox.YAxis, enable=False)
    self.ui.plot_3.plotItem.enableAutoRange(pg.ViewBox.YAxis, enable=False)
    
    self.draw_spectrograms()

  def toggle_playback(self):
    if self.ui.play_pause_btn.text() == "Pause":
      self.ui.play_pause_btn.setText("Play")
      self.timer.stop()
    else:
      self.timer.start(100)
      self.ui.play_pause_btn.setText("Pause")

  def reset_plots(self):
    self.x_range = [0.0, 4.0]
    self.ui.speed_slider.setValue(4)
    self.x_range_speed = 0.04
    
    self.ui.plot_1.setXRange(self.x_range[0], self.x_range[1])
    self.ui.plot_2.setXRange(self.x_range[0], self.x_range[1])

  def update_plots(self):
    self.x_range = [self.x_range[0] + self.x_range_speed, self.x_range[1] + self.x_range_speed]

    self.ui.plot_1.setXRange(self.x_range[0], self.x_range[1])
    self.ui.plot_2.setXRange(self.x_range[0], self.x_range[1])

  def update_zoom_in(self):    
    self.ui.plot_1.plotItem.getViewBox().scaleBy((0.75, 0.75))  
    self.ui.plot_2.plotItem.getViewBox().scaleBy((0.75, 0.75))  

  def update_zoom_out(self):
    self.ui.plot_1.plotItem.getViewBox().scaleBy((1.25, 1.25))  
    self.ui.plot_2.plotItem.getViewBox().scaleBy((1.25, 1.25))  

  def update_playback_speed(self, value):
    self.x_range_speed = (value / 100.0) + 0.10

  def clear(self):
    self.ui.plot_1.clear() 
    self.ui.plot_2.clear()
    self.ui.plot_3.clear()
    self.ui.plot_5.clear()

    for slider_number in range(1, 11):
      slider = getattr(self.ui, f"verticalSlider_{slider_number}")
      slider.setValue(0)

    self.browsed_signal = SampledSignal()
    self.input_signal = Signal()
    self.output_signal = Signal()

    self.generated_audio_file = False
    self.current_range = []
    self.window_type = ""
    self.output_num = 1
    self.audio_file = ""

    spectogram.clear_spectrogram(self.ui.Spectrogram_1)
    spectogram.clear_spectrogram(self.ui.Spectrogram_2)

  def change_mode(self):
    self.clear()
    _action = self.sender()
    if _action.isChecked():
      self.current_mode = _action.text()
      
      for action in self.ui.menuModes.actions():
        if action.text() != self.current_mode:
          action.setChecked(False)
    
    print("current mode: ",self.current_mode)
    if self.current_mode == "ECG Mode":
      self.sliders_on_off = True

    self.ui.mode_title.setText(self.current_mode)

    self.num_of_sliders = self.sliders_dict[self.current_mode]

    for slider_number in range(1, 11):
      slider = getattr(self.ui, f"verticalSlider_{slider_number}")
      label1 = getattr(self.ui, f"label_{slider_number}")
      label2 = getattr(self.ui, f"label_{10 + slider_number}")
      label3 = getattr(self.ui, f"label_{20 + slider_number}")

      if self.current_mode == "ECG Mode":
        label1.setText("0")
        label2.setText("1")
      else:
        label1.setText("10^(-5)")
        label2.setText("10^(3)")

      if self.sliders_on_off:
        slider.setMinimum(0)
        slider.setMaximum(1)
        slider.setValue(1)
      else:
        slider.setMinimum(-5)
        slider.setMaximum(3)
        slider.setValue(0)

      # initialize vertical sliders
      if slider_number <= self.num_of_sliders:
        slider.valueChanged.connect(lambda value, slider_number=slider_number-1: controls.update_plot(self, slider_number, value))
        slider.setVisible(True)
        label1.setVisible(True)
        label2.setVisible(True)
        label3.setVisible(True)

        if slider_number <= self.sliders_dict[self.current_mode]:
          if self.current_mode == "Uniform Range Mode":
            label3.setText(f"{self.uniform_freq_ranges[slider_number-1][0]}-{self.uniform_freq_ranges[slider_number-1][1]}")
          elif self.current_mode == "Musical Instruments Mode":
            label3.setText(f"{self.music_names[slider_number-1]}")
          elif self.current_mode == "Animals Sound Mode":
            label3.setText(f"{self.animal_names[slider_number-1]}")
          else: # ECG Mode
            label3.setText(f"{self.arryhtmia_names[slider_number-1]}")
            
      # hiding unused sliders
      if slider_number > self.num_of_sliders:
        slider.setVisible(False)
        label1.setVisible(False)
        label2.setVisible(False)
        label3.setVisible(False)
  
  def browse_csv(self):
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly

    file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
    self.csv_file = file_path
    print(file_path)

    if file_path:
        time = []
        amplitude = []

        with open(file_path, 'r') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            # neglect the first line in the csv file
            next(csvReader)
            for line in csvReader:
                amplitude.append(-float(line[1]))
                time.append(float(line[0]))

        self.fsample = 1 / (time[1] - time[0])
        self.browsed_signal = SampledSignal(self.fsample, amplitude)
        self.browsed_signal.amplitude = [x * (-1) for x in self.browsed_signal.amplitude]
        self.input_signal = Signal(self.browsed_signal.time, self.browsed_signal.amplitude)
        self.output_signal = Signal(self.browsed_signal.time, self.browsed_signal.amplitude)
        
  def open_signal(self):
    self.change_mode()
    if self.current_mode == "Uniform Range Mode" or self.current_mode == "ECG Mode":
      self.browse_csv()
    else:
      audio.browse_audio(self)
      
    # first time to make fourier
    if len(self.input_signal.frequency) == 0:
      fourier.fourier_transfrom(self, self.input_signal.time, self.input_signal.t_amplitude)  
      self.draw()
      controls.visualize_window(self)
      
if __name__ == "__main__":
  app = QApplication(sys.argv)
  app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
  window = SignalEqualizer()
  window.setWindowTitle("Signal Equalizer")
  app.setWindowIcon(QIcon("assets/logo.jpg"))
  window.resize(1450,950)
  window.show()
  sys.exit(app.exec_())
