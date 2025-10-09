
import sounddevice as sd
import numpy as np

def test_audio():
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

def get_audio_devices():
    """Print available audio devices"""
    print("\nAvailable audio devices:")
    for devide_id, name in enumerate(sd.query_devices()):
        print(f"{devide_id}: {name['name']}")
    print()
    # Select a device from user input
    # device_id = int(input("Select a device ID: "))
    # print(f"Using device ID {device_id}: {sd.query_devices(device_id)['name']}")


def test_audio_io():
    """
    Test audio io by routing the input from a device to a selected output device.
    On MacOS, you can use BlackHole as a virtual audio device.
    """
    # Select an input device
    # print("Available input audio devices:")
    # for device_id, name in enumerate(sd.query_devices(kind= 'input')):
    #     print(f"{device_id}: {name}")
    get_audio_devices()
    input_device_id = int(input("Select an input device ID: "))

    # Select an output device
    # print("Avaliable output audio devices:")
    # for device_id, name in enumerate(sd.query_devices(kind= 'output')):
    #     print(f"{device_id}: {name}")
    get_audio_devices()
    output_device_id = int(input("Select an output device ID: "))

    samplerate = 44100
    blocksize = 1024

    def callback(indata, outdata, frames, time, status):
        if status:
            print(status)
        outdata[:] = indata  # copia la entrada directamente a la salida

    try:
        with sd.Stream(
            samplerate=samplerate,
            blocksize=blocksize,
            dtype='float32',
            channels=2,
            callback=callback,
            device=(input_device_id, output_device_id)
        ):
            print("Press Ctrl+C to stop the stream")
            while True:
                sd.sleep(1000)
    except KeyboardInterrupt:
        print("\nStream stopped")

if __name__ == "__main__":
    # test_audio()
    # get_audio_devices()
    test_audio_io()
