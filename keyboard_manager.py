# keyboard_manager.py

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import time

from keycodes import keycode_map  # You must provide this dict
from utils import blink_led        # Your existing LED blink helper
from adafruit_httpserver import Response

SHIFT = Keycode.SHIFT

# For symbols that require pressing SHIFT + some keycode to type them.
# Expand this dictionary if you need more punctuation.
shift_map = {
    "!": (SHIFT, Keycode.ONE),
    "@": (SHIFT, Keycode.TWO),
    "#": (SHIFT, Keycode.THREE),
    "$": (SHIFT, Keycode.FOUR),
    "%": (SHIFT, Keycode.FIVE),
    "^": (SHIFT, Keycode.SIX),
    "&": (SHIFT, Keycode.SEVEN),
    "*": (SHIFT, Keycode.EIGHT),
    "(": (SHIFT, Keycode.NINE),
    ")": (SHIFT, Keycode.ZERO),
    "_": (SHIFT, Keycode.MINUS),
    "+": (SHIFT, Keycode.EQUALS),
    "{": (SHIFT, Keycode.LEFT_BRACKET),
    "}": (SHIFT, Keycode.RIGHT_BRACKET),
    ":": (SHIFT, Keycode.SEMICOLON),
    "\"": (SHIFT, Keycode.QUOTE),
    "<": (SHIFT, Keycode.COMMA),
    ">": (SHIFT, Keycode.PERIOD),
    "?": (SHIFT, Keycode.FORWARD_SLASH),
    "|": (SHIFT, Keycode.BACKSLASH)
}

def send_keys(key_label, keyboard, repetitions=1, delay=0.1):
    """
    Send a keypress or combination using the HID keyboard.

    :param key_label: String of keys to send (e.g., 'CTRL+V', 'F8', or 'Hello!').
    :param keyboard: HID Keyboard object.
    :param repetitions: Number of times to repeat the key combination.
    :param delay: Delay between repetitions in seconds.
    """
    try:
        decoded_label = url_decode(key_label)

        # Check if it's a combination (CTRL+V, ALT+TAB, etc.)
        if "+" in decoded_label:
            combo_keys = []
            for part in decoded_label.split("+"):
                kc = keycode_map.get(part.strip().upper())
                if kc:
                    combo_keys.append(kc)

            if not combo_keys:
                print(f"Unsupported combo: {decoded_label}")
                return

            for i in range(repetitions):
                keyboard.press(*combo_keys)
                time.sleep(0.1)
                keyboard.release_all()
                print(f"Key combo '{decoded_label}' sent ({i + 1}/{repetitions})")
                blink_led(2, short_duration=0.1)
                time.sleep(delay)

        # Check if it's a single command key (e.g., ESC, F1, LEFT)
        elif decoded_label.upper() in keycode_map:
            kc = keycode_map[decoded_label.upper()]
            for i in range(repetitions):
                keyboard.press(kc)
                time.sleep(0.05)
                keyboard.release_all()
                print(f"Command key '{decoded_label}' sent ({i + 1}/{repetitions})")
                blink_led(1, short_duration=0.1)

        # Otherwise, treat it as a multi-character string
        else:
            for char in decoded_label:
                # Handle SHIFT+symbol mappings (e.g., !, @)
                if char in shift_map:
                    key_tuple = shift_map[char]
                    keyboard.press(*key_tuple)
                    time.sleep(0.05)
                    keyboard.release_all()

                # Handle uppercase letters
                elif char.isalpha() and char.isupper():
                    lower_char = char.lower()
                    sc = keycode_map.get(lower_char.upper())
                    if sc:
                        keyboard.press(SHIFT, sc)
                        time.sleep(0.05)
                        keyboard.release_all()

                # Handle lowercase letters, digits, and common symbols
                else:
                    scancode = keycode_map.get(char.upper(), None)
                    if scancode:
                        keyboard.press(scancode)
                        time.sleep(0.05)
                        keyboard.release_all()
                    else:
                        print(f"No scancode for: {char}")

            print(f"Typed string: '{decoded_label}'")
            blink_led(2, short_duration=0.1)

    except Exception as e:
        print(f"Error sending key '{key_label}': {e}")


def handle_post(request, keyboard):
    """
    Handle POST requests. Expects 'key=' in form data for single combos or entire strings.

    :param request: HTTP request object.
    :param keyboard: HID Keyboard object.
    :return: HTTP response object.
    """
    try:
        content_length = int(request.headers.get("Content-Length", 0))
    except ValueError:
        content_length = 0

    if content_length > 0:
        try:
            form_data = request.body.decode("utf-8")
            data = {}
            for pair in form_data.split("&"):
                if "=" in pair:
                    k, v = pair.split("=")
                    data[k] = v
            key = data.get("key", "")
            # Send the keys (or type the string)
            send_keys(key, keyboard)
            return Response(request, body="OK", content_type="text/plain")
        except Exception as e:
            print("Error processing POST request:", e)
            return Response(request, body="Error processing request.", status=500, content_type="text/plain")

    print("POST request received with no content.")
    return Response(request, body="No data received.", status_code=400, content_type="text/plain")

def url_decode(encoded_str):
    """
    Decode a URL-encoded string (e.g. "Hello%21" -> "Hello!").
    """
    try:
        result = []
        i = 0
        while i < len(encoded_str):
            if encoded_str[i] == '%' and (i + 2) < len(encoded_str):
                hex_value = encoded_str[i+1:i+3]
                try:
                    result.append(chr(int(hex_value, 16)))
                    i += 3
                except ValueError:
                    # If it's not valid hex, just append '%'
                    result.append('%')
                    i += 1
            else:
                result.append(encoded_str[i])
                i += 1
        return ''.join(result)
    except Exception as e:
        print("Error decoding URL:", e)
        return encoded_str  # Return as-is if decoding fails
