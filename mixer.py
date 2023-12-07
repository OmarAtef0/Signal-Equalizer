# DONT RUN
# DONT RUN
from pydub import AudioSegment
from pydub.playback import play

# Load audio samples for each instrument
instrument1 = AudioSegment.from_file("dataset/Animals/anis/lion.wav", format="wav")
instrument2 = AudioSegment.from_file("dataset/Animals/anis/cat.wav", format="wav")
instrument3 = AudioSegment.from_file("dataset/Animals/anis/dog.wav", format="wav")
instrument4 = AudioSegment.from_file("dataset/Animals/anis/bird.wav", format="wav")


# Find the minimum duration among all instruments
min_duration = min(
    instrument1.duration_seconds,
    instrument2.duration_seconds,
    instrument3.duration_seconds,
    instrument4.duration_seconds
)

# Set the frame rate of each instrument to match the minimum duration
instrument1 = instrument1.set_frame_rate(instrument1.frame_rate)
instrument2 = instrument2.set_frame_rate(instrument2.frame_rate)
instrument3 = instrument3.set_frame_rate(instrument3.frame_rate)
instrument4 = instrument4.set_frame_rate(instrument4.frame_rate)

# Trim each instrument to the minimum duration
instrument1 = instrument1[:min_duration * 1000]  # in milliseconds
instrument2 = instrument2[:min_duration * 1000]
instrument3 = instrument3[:min_duration * 1000]
instrument4 = instrument4[:min_duration * 1000]

# Combine the instruments simultaneously
combined = instrument1.overlay(instrument2).overlay(instrument3).overlay(instrument4)

combined.export("dataset/animals/animals_sounds.wav", format="wav")