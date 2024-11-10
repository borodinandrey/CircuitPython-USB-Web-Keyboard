import usb_hid
import wifi
import socketpool
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_httpserver import Server, Request, Response
from keycodes import keycode_map

# Configuration
NETWORK_CONFIG = {
    "client_mode": False,  # Set to False to force AP mode
    "ap_ssid": "Keyboard-AP",  # Wi-Fi SSID in AP mode
    "ap_password": "APPassword",  # Wi-Fi Password in AP mode
    "client_ssid": "YourSSID",  # Wi-Fi SSID to connect to in Client mode
    "client_password": "YourPassword",  # Wi-Fi Passwrd to connect to in Client mode
    "port": 80,  # Port for the HTTP server where the web keyboard will be served
}


def initialize_wifi(config):
    """
    Initialize Wi-Fi in either client or AP mode based on the configuration.
    If client mode connection fails it will fallback to AP mode.
    """
    if config["client_mode"]:
        try:
            print("Connecting in client mode...")
            wifi.radio.connect(config["client_ssid"], config["client_password"])
            ip = str(wifi.radio.ipv4_address)
            print(f"Connected to {config['client_ssid']}, IP: {ip}")
            return ip
        except Exception as e:
            print(f"Client mode failed: {e}. Switching to AP mode.")

    print("Starting Access Point...")
    wifi.radio.start_ap(config["ap_ssid"], config["ap_password"])
    ip = str(wifi.radio.ipv4_address_ap)
    print(f"Access Point started: {config['ap_ssid']}, IP: {ip}")
    return ip


def send_key(key_label, keyboard):
    """
    Send a keypress using the HID keyboard.
    """
    if key_code := keycode_map.get(key_label):
        try:
            keyboard.send(key_code)
            print(f"Key '{key_label}' sent.")
        except Exception as e:
            print(f"Error sending key '{key_label}': {e}")
    else:
        print(f"Unsupported key: {key_label}")


def load_file(filepath):
    """
    Load the content of a file and return it.
    """
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return None


def handle_post(request, keyboard):
    """
    Handle POST requests to send keypresses.
    """
    content_length = int(request.headers.get("Content-Length", 0))
    if content_length > 0:
        try:
            form_data = request.body.decode("utf-8")
            key_value = dict(pair.split("=") for pair in form_data.split("&")).get(
                "key", ""
            )
            send_key(key_value.replace("+", " ").upper(), keyboard)
        except Exception as e:
            print(f"Error processing POST request: {e}")
    return Response(request, body="OK", content_type="text/plain")


def start_server(ip, server, port):
    """
    Start the HTTP server on the specified IP and port.
    """
    print(f"Starting server at http://{ip}:{port}...")
    try:
        server.start(ip, port=port)
        print("Server started successfully.")
    except Exception as e:
        print(f"Failed to start server: {e}")


# Initialize system
ip_address = initialize_wifi(NETWORK_CONFIG)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool)
keyboard = Keyboard(usb_hid.devices)


# Define server routes
@server.route("/", methods=["GET", "POST"])
def index(request: Request):
    if request.method == "POST":
        return handle_post(request, keyboard)

    html_content = load_file("/index.html")
    return Response(
        request, body=html_content or "Error loading page", content_type="text/html"
    )


@server.route("/style.css", methods=["GET"])
def style(request: Request):
    css_content = load_file("/style.css")
    return Response(
        request, body=css_content or "Error loading stylesheet", content_type="text/css"
    )


# Start server
start_server(ip_address, server, NETWORK_CONFIG["port"])

while True:
    try:
        server.poll()
    except Exception as e:
        print(f"Server error: {e}")
        time.sleep(0.005)
