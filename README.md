# CircuitPython / Raspberry Pi Pico W USB HID Keyboard with Web Interface

## About

I needed a keyboard to navigate the BIOS of an old PC, but I didn't have any keyboards at home. So, I decided to create one! This is a **CircuitPython-based USB HID Keyboard with a Web UI**.

<img width="1438" alt="image" src="<img width="1440" alt="image" src="https://github.com/user-attachments/assets/40628f6e-8c1e-4f07-9588-699af144afe3" />
">

### How It Works:
1. **Plug your Wi-Fi-enabled CircuitPython device** into a USB port.
2. **Connect to the device's Wi-Fi** using your phone or computer.
3. **Open a browser and start typing** by pressing keys on the web interface.

### Why This Might Be Useful:
- You only need a keyboard to **press a few buttons** and don’t want to buy one.
- You want a **credit card-sized USB keyboard** in your backpack, always ready to go.
- Just-in-case

### What it can do

- **On-Screen Keyboard**: Send single key presses via web browser interface
- **Wi-Fi Connectivity**: Work in both client (if you want to connect to the existing network) and access point (when you want you controller to create wifi network) modes.

### What it can't do (yet)

- **Shortcuts** like CTRL+Z and any others, only single key presses are supported but you can use sticky keys in windows

---

## Installation Guide

### Prerequisites

#### Hardware:
- A Wi-Fi-enabled CircuitPython-compatible microcontroller (e.g., Raspberry Pi Pico W and others)
- USB cable

#### Software:
- [CircuitPython](https://circuitpython.org/)
- Web browser for testing.

---

### Step 1: Install CircuitPython

1. Go to the [CircuitPython Downloads](https://circuitpython.org/downloads) page.
2. Download the latest `.uf2` file for your microcontroller.
3. Put your board in bootloader mode:
   - Press the reset button twice quickly (or follow board-specific instructions).
4. Drag and drop the `.uf2` file onto the `CIRCUITPY` drive.

---

### Step 2: Set Up Project Files

1. **Copy the  files** to the `CIRCUITPY` drive:

2. **Rename `boot_rename.py` to `boot.py` and copy** to the `CIRCUITPY` drive. WARNING: This is needed to support keyboard in BIOSes, but will disable the storage drive mode.

3. **Download the [CircuitPython Library Bundle](https://circuitpython.org/libraries)** for your specific CircuitPython version.

4. **From the bundle archive**, copy the following folder and files to the `lib` folder on the `CIRCUITPY` drive:
   - **Folder**:
     - `adafruit_hid`
     - `adafruit_httpserver`
   - **Files**:
     - `adafruit_connection_manager.mpy`
     - `adafruit_requests.mpy`
     - `simpleio.mpy`


### Step 3: Edit Network Config (If Needed)

The network configuration is located in the `code.py` file. You can modify the `NETWORK_CONFIG` dictionary as needed:

```python
NETWORK_CONFIG = {
    "client_mode": False,              # Set to False to force AP mode
    "ap_ssid": "Keyboard-AP",          # Wi-Fi SSID in AP mode
    "ap_password": "APPassword",       # Wi-Fi Password in AP mode
    "client_ssid": "YourSSID",         # Wi-Fi SSID to connect to in Client mode
    "client_password": "YourPassword", # Wi-Fi Password in Client mode
    "port": 80                         # Port for the HTTP server where the web keyboard will be served
}
```

### Step 4: Connect and Access the Keyboard
##### Wi-Fi Client Mode

1. The device connects to your specified Wi-Fi network.
2. Use a serial monitor or check your Wi-Fi router to identify IP address
3. Open your browser and navigate to the IP address (e.g., http://192.168.1.10).

##### Access Point Mode

1. The device creates a Wi-Fi network (SSID: Keyboard-AP).
2. Connect your computer or phone to this network.
3. Open your browser and navigate to http://192.168.4.1.

### Step 5: Debug

You can use serial terminal to check logs. More details in [this guide](https://learn.adafruit.com/welcome-to-circuitpython/kattni-connecting-to-the-serial-console) 

## Acknowledgements 
HTML+CSS Keyboard layout by [Aref Norouzzadeh](https://codepen.io/arefn/pen/wbzxpd)
