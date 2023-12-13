# DONT RUN
# DONT RUN
from pydub import AudioSegment
from pydub.playback import play

# Load audio samples for each instrument
instrument1 = AudioSegment.from_file("dataset\Music\instr\Final\output-accordion2.wav", format="wav")
instrument2 = AudioSegment.from_file("dataset\Music\instr\Final\output-clarinet.wav", format="wav")
instrument3 = AudioSegment.from_file("dataset\Music\instr\Final\output-drums.wav", format="wav")
instrument4 = AudioSegment.from_file("dataset\Music\instr\Final\output-sax.wav", format="wav")

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

instrument1 = instrument1 + 7
instrument2 = instrument2 + 7
instrument4 = instrument4 - 10

# Trim each instrument to the minimum duration
instrument1 = instrument1[:min_duration * 1000]  # in milliseconds
instrument2 = instrument2[:min_duration * 1000]
instrument3 = instrument3[:min_duration * 1000]
instrument4 = instrument4[:min_duration * 1000]

# Combine the instruments simultaneously
combined = instrument1.overlay(instrument2).overlay(instrument3).overlay(instrument4)

combined.export("dataset/Music/CocktailAnimal.wav", format="wav")