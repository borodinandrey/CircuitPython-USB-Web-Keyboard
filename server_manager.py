# server_manager.py
from adafruit_httpserver import Server

def setup_server(ip, server, port):
    """
    Start and configure the HTTP server.

    :param ip: IP address to bind the server.
    :param server: HTTP server instance.
    :param port: Port number to listen on.
    """
    try:
        server.start(ip, port=port)
        print(f"Server started at http://{ip}:{port}")
    except Exception as e:
        print("Failed to start server:", e)
