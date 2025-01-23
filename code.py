# main.py
import usb_hid
import time
import socketpool
import wifi

from adafruit_hid.keyboard import Keyboard
from adafruit_httpserver import Server

from bios_keys import load_bios_keys, send_bios_keys
from wifi_manager import initialize_wifi
from server_manager import setup_server
from routes import initialize_routes
from utils import blink_led

# Configuration
NETWORK_CONFIG = {
    "client_mode": False,  # Set to False to force AP mode
    "ap_ssid": "Keyboard-AP",  # Wi-Fi SSID in AP mode
    "ap_password": "APPassword",  # Wi-Fi Password in AP mode
    "client_ssid": "YourSSID",  # Wi-Fi SSID to connect to in Client mode
    "client_password": "YourPassword",  # Wi-Fi Passwrd to connect to in Client mode
    "port": 80,  # Port for the HTTP server where the web keyboard will be served
}

def main():
    try:
        # Initialize network-related components
        pool = socketpool.SocketPool(wifi.radio)
        server = Server(pool)
        keyboard = Keyboard(usb_hid.devices)
        
        blink_led(3)

        # Load and send BIOS keys before initializing Wi-Fi and server
        bios_keys = load_bios_keys()
        if bios_keys:
            send_bios_keys(bios_keys, keyboard)

        # Initialize Wi-Fi and get IP address
        ip_address = initialize_wifi(NETWORK_CONFIG)
        print("IP Address:", ip_address)

        # Initialize server routes
        initialize_routes(server, keyboard)

        # Setup and start the HTTP server
        setup_server(ip_address, server, NETWORK_CONFIG["port"])

        print("Initialization complete. Entering main loop.")

        # Main loop to poll server
        while True:
            try:
                server.poll()
            except Exception as e:
                print("Server polling error:", e)
                time.sleep(0.005)

    except Exception as e:
        print("Critical Error: Failed to initialize the system:", e)

if __name__ == "__main__":
    main()
