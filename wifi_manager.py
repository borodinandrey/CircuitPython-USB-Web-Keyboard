# wifi_manager.py
import wifi

def initialize_wifi(config):
    """
    Initialize Wi-Fi in either client or AP mode based on the configuration.

    :param config: Configuration dictionary.
    :return: Assigned IP address as a string.
    """
    try:
        if config.get("client_mode"):
            print("Attempting to connect in client mode...")
            wifi.radio.connect(config["client_ssid"], config["client_password"])
            ip = str(wifi.radio.ipv4_address)
            print(f"Connected to {config['client_ssid']}. IP: {ip}")
            return ip
    except Exception as e:
        print("Client mode failed:", e, ". Switching to AP mode.")

    # Fallback to Access Point mode
    try:
        ap_ssid = config.get("ap_ssid", "Keyboard-AP")
        ap_password = config.get("ap_password", "APPassword")
        wifi.radio.start_ap(ap_ssid, ap_password)
        ip = str(wifi.radio.ipv4_address_ap)
        print(f"Access Point '{ap_ssid}' started. IP: {ip}")
        return ip
    except Exception as e:
        print("Failed to start Access Point:", e)
        raise
