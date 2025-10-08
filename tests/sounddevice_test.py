
import sounddevice as sd
import numpy as np

def main():
    """Generate a 3-second sine wave at 440 Hz"""

    # Sampling frequency
    sampling_frequency = 44100
    # Duration in seconds
    duration = 3
    # Frequency of the sine wave
    frequency = 440
    # Time
    t = np.linspace(0, duration, int(sampling_frequency * duration), endpoint=False)

    audio = 0.5 * np.cos(2 * np.pi * frequency * t)

    # Play the audio and wait until it finishes
    sd.play(audio, samplerate= sampling_frequency)
    sd.wait()

if __name__ == "__main__":
    main()