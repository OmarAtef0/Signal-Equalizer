# Signal Equalizer Application

## Overview

The Signal Equalizer is a versatile desktop application designed for manipulating signals in the music, speech, and biomedical domains. It empowers users to adjust frequency components and explore various modes catering to different use cases. The application offers a user-friendly interface and supports real-time signal processing for enhanced user experience.

## Features

1. **Uniform Range Mode**
   - Divide the total frequency range into 10 equal parts controlled by sliders.
   - Prepare synthetic signal files for validation and analysis.

2. **Musical Instruments Mode**
   - Control the magnitude of specific musical instruments in a signal with at least four instruments.

3. **Animal Sounds Mode**
   - Adjust the magnitude of specific animal sounds in a mixture of at least four sounds.

4. **ECG Abnormalities Mode**
   - Analyze ECG signals with one normal and three arrhythmia types.
   - Adjust the magnitude of arrhythmia components in the signal.

5. **Equalizer Options**
   - Choose from four multiplication/smoothing windows (Rectangle, Hamming, Hanning, Gaussian).
   - Customize window parameters visually before applying to the equalizer.

6. **Mode Switching**
   - Easily switch between modes through an intuitive option menu or combobox.
   - Minimal UI changes ensure a seamless transition.

7. **UI Components**
   - Sliders for frequency component magnitude adjustment.
   - Linked cine signal viewers (input and output) with a comprehensive functionality panel.
   - Synchronous display of signals in time.
   - Two spectrograms (input and output) for detailed frequency analysis.
   - Option to toggle show/hide spectrograms.

## Information for the User

### Usage

1. Open the application and load your desired signal.
2. Choose the mode based on your signal type (Uniform Range, Musical Instruments, Animal Sounds, ECG Abnormalities).
3. Adjust sliders to modify the magnitude of frequency components.
4. Select a multiplication/smoothing window and customize its parameters visually.
5. Visualize your customizations before applying them to the equalizer.
6. Utilize the cine signal viewers and spectrograms for detailed signal analysis.
7. Toggle the option to show/hide spectrograms.

### Requirements

- Ensure your system has sufficient computational resources for real-time signal processing.
- Connect and configure audio and visual display devices appropriately.

### Dependencies

- The application relies on standard libraries for signal processing and graphical user interface development.

## Run App

1. Clone the repository: `git clone https://github.com/OmarAtef0/Signal-Equalizer.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## Team Members

- Ibrahim Emad
- Omar Atef
- Hazem Rafaat
- Ahmed Khaled


