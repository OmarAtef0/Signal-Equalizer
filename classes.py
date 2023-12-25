from scipy import fft
import numpy as np

class SampledSignal():
    '''An object containing sample points array'''
    def __init__(self, sampling_freq=1, amplitude=[]):
        self.sampling_freq = sampling_freq
        self.max_freq = 1/2 * sampling_freq
        self.amplitude = amplitude
        self.total_samples = len(amplitude)
        self.time = []
        self.generate_time_array()

    def generate_time_array(self):
        for index in range(self.total_samples):
            self.time.append(index/self.sampling_freq)

class Signal():
    '''An object containing the generic signal'''
    def __init__(self, time=[] ,t_amplitude=[], frequency=[], f_amplitude=[], fft_coef=[], fft_angle=[], sample_rate=44100):
        self.time = time
        self.t_amplitude = t_amplitude
        self.frequency = frequency 
        self.f_amplitude = f_amplitude
        self.fft_coef = fft_coef
        self.fft_angle = fft_angle
        self.sample_rate = sample_rate
        self.t_amp = []

