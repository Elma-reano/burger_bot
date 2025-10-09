
import sounddevice as sd
import soundfile as sf
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

def select_audio_device(kind: str = None) -> int:
    """Print available audio devices"""

    assert kind in (None, "input", "output"), "type must be None, 'input', or 'output'"

    devices = tuple(enumerate(sd.query_devices()))
    if kind:
        devices = tuple(filter(lambda d: d[1]['max_' + kind + '_channels'] > 0, devices))
    
    print("\nAvailable audio devices:")
    for devide_id, name in devices:
        print(f"{devide_id}: {name['name']}")
    while True:
        try:
            device_id = int(input("Select a device ID: "))
            if device_id in dict(devices).keys():
                print(f"Using device ID {device_id}: {sd.query_devices(device_id)['name']}")
                return device_id
            else:
                print("Invalid device ID. Please try again.")
        except ValueError:
            print("Please enter a valid integer for the device ID.")
    # Select a device from user input
    # device_id = int(input("Select a device ID: "))
    # print(f"Using device ID {device_id}: {sd.query_devices(device_id)['name']}")


def test_audio_io():
    """
    Test audio io by routing the input from a device to a selected output device.
    On MacOS, you can use BlackHole as a virtual audio device.
    """
    # Select an input device
    input_device_id = select_audio_device(kind= 'input')

    # Select an output device
    output_device_id = select_audio_device(kind= 'output')

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

def test_read_audiofile(filename: str):
    import threading

    event = threading.Event()

    try:
        data, fs = sf.read(filename, always_2d=False)

        output_device = select_audio_device(kind= 'output')

        current_frame = 0

        def callback(outdata, frames, time, status):
            if status:
                print(status)
            nonlocal current_frame
            chunksize = min(len(data) - current_frame, frames)
            outdata[:chunksize] = data[current_frame:current_frame + chunksize]
            if chunksize < frames:
                outdata[chunksize:] = 0
                raise sd.CallbackStop()
            current_frame += chunksize

        stream = sd.OutputStream(
            samplerate=fs,
            device=output_device,
            channels=data.shape[1],
            callback=callback,
            finished_callback=event.set
        )
        with stream:
            event.wait()  # Wait until playback is finished
    except KeyboardInterrupt:
        print('\nInterrupted by user')
    except Exception as e:
        print(type(e).__name__ + ': ' + str(e))

if __name__ == "__main__":
    # test_audio()
    # get_audio_devices()
    # test_audio_io()
    test_read_audiofile("tests/sample_audios/test_1.mp3")
    # test_read_audiofile("tests/sample_audios/test_2.mp3")
    # test_read_audiofile("tests/sample_audios/test_3.mp3")
