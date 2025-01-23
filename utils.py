# utils.py
import digitalio
import board
import time


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

def blink_led(times, duration=0.2, short_duration=None):
    """
    Blink the LED a specified number of times.
    
    :param times: Number of blinks.
    :param duration: Duration of each blink.
    :param short_duration: Optional, shorter duration for different blink patterns.
    """

    for _ in range(times):
        led.value = True
        time.sleep(short_duration if short_duration else duration)
        led.value = False
        time.sleep(short_duration if short_duration else duration)


def load_file(filepath):
    """
    Load the content of a file and return it.

    :param filepath: Path to the file.
    :return: File content as a string, or None if not found/error.
    """
    try:
        with open(filepath, "r") as file:
            print("Loaded file:", filepath)
            return file.read()
    except OSError:
        print("File not found:", filepath)
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return None