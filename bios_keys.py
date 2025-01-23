# bios_keys.py
import microcontroller

from keyboard_manager import send_keys

# Constants for NVM storage
NVM_KEY_OFFSET = 0
NVM_REPETITIONS_OFFSET = 32  # Assuming first 32 bytes for key, next for repetitions
NVM_MAX_KEY_LENGTH = 32

def load_bios_keys():
    """
    Load BIOS keys configuration from non-volatile memory (NVM).
    Returns a tuple of (key combination, repetitions), or None if no valid data.
    
    :return: Tuple containing key combination and repetitions, or None.
    """
    try:
        # Read key combination
        raw_key = microcontroller.nvm[NVM_KEY_OFFSET:NVM_KEY_OFFSET + NVM_MAX_KEY_LENGTH]
        key_combination = ''.join([chr(b) for b in raw_key if b not in (0x00, 0xFF)]).strip()

        # Read repetitions
        raw_reps = microcontroller.nvm[NVM_REPETITIONS_OFFSET:NVM_REPETITIONS_OFFSET + 8]  # Assuming max 8 digits
        repetitions_str = ''.join([chr(b) for b in raw_reps if b not in (0x00, 0xFF)]).strip()

        if key_combination and repetitions_str.isdigit():
            repetitions = int(repetitions_str)
            print("Loaded BIOS keys:", key_combination, ",", repetitions, "times")
            return key_combination, repetitions
    except Exception as e:
        print("Error loading BIOS keys:", e)
    return None

def save_bios_keys(key_combination, repetitions):
    """
    Save or delete BIOS keys configuration in NVM.
    """
    try:
        # Encode key and repetitions
        key_encoded = key_combination.encode("utf-8")[:NVM_MAX_KEY_LENGTH]
        repetitions_encoded = str(repetitions).encode("utf-8")

        # Clear existing NVM (default behavior)
        microcontroller.nvm[NVM_KEY_OFFSET:NVM_KEY_OFFSET + NVM_MAX_KEY_LENGTH] = b'\x00' * NVM_MAX_KEY_LENGTH
        microcontroller.nvm[NVM_REPETITIONS_OFFSET:NVM_REPETITIONS_OFFSET + 8] = b'\x00' * 8

        if key_combination and repetitions > 0:
            # Save key and repetitions if valid
            microcontroller.nvm[NVM_KEY_OFFSET:NVM_KEY_OFFSET + len(key_encoded)] = key_encoded
            microcontroller.nvm[NVM_REPETITIONS_OFFSET:NVM_REPETITIONS_OFFSET + len(repetitions_encoded)] = repetitions_encoded
            print(f"Saved BIOS keys: {key_combination}, {repetitions} times")
        else:
            # Just clear configuration for deletion
            print("BIOS keys configuration removed.")
    except TypeError as te:
        print(f"Type error in save_bios_keys: {te}")
    except Exception as e:
        print(f"Error saving BIOS keys: {e}")




def send_bios_keys(bios_keys, keyboard):
    """
    Send the configured BIOS keys upon startup.
    
    :param bios_keys: Tuple containing key combination and repetitions.
    :param keyboard: HID Keyboard object.
    """
    if bios_keys:
        bios_key, repetitions = bios_keys
        print("Sending BIOS key '{}', {} time(s)...".format(bios_key, repetitions))
        send_keys(bios_key, keyboard, repetitions=repetitions, delay=0.1)
