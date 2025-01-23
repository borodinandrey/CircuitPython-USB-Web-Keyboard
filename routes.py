# routes.py
import json
from adafruit_httpserver import Response

from bios_keys import save_bios_keys, load_bios_keys
from utils import load_file
from keyboard_manager import handle_post

def initialize_routes(server, keyboard):
    """
    Initialize server routes.

    :param server: HTTP server instance.
    :param keyboard: HID Keyboard object.
    """
    
    @server.route("/", methods=["GET", "POST"])
    def index(request):
        if request.method == "POST":
            return handle_post(request, keyboard)
        html_content = load_file("/index.html")
        if html_content:
            return Response(request, body=html_content, content_type="text/html")
        print("Failed to load index.html")
        return Response(request, body="Error loading page", status=500, content_type="text/plain")

    @server.route("/style.css", methods=["GET"])
    def style(request):
        css_content = load_file("/style.css")
        if css_content:
            return Response(request, body=css_content, content_type="text/css")
        print("Failed to load style.css")
        return Response(request, body="Error loading stylesheet", status=500, content_type="text/plain")

    @server.route("/save_bios", methods=["POST"])
    def save_bios(request):
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
                        key, value = pair.split("=")
                        data[key] = value
                key_combination = data.get("key", "").strip()
                repetitions_str = data.get("repetitions", "1").strip()
                repetitions = int(repetitions_str) if repetitions_str.isdigit() else 1

                if key_combination and repetitions > 0:
                    save_bios_keys(key_combination, repetitions)
                    return Response(request, body="BIOS configuration saved.", content_type="text/plain")
                else:
                    print("Invalid BIOS configuration data received.")
                    return Response(request, body="Invalid data.", status=400, content_type="text/plain")
            except Exception as e:
                print("Error saving BIOS configuration:", e)
                return Response(request, body="Error saving BIOS configuration.", status=500, content_type="text/plain")
        
        print("save_bios endpoint received POST request with no content.")
        return Response(request, body="No data received.", status=400, content_type="text/plain")

    @server.route("/load_bios", methods=["GET"])
    def load_bios(request):
        bios_config = load_bios_keys()
        if bios_config:
            key, repetitions = bios_config
            response_data = {"key": key, "repetitions": repetitions}
            return Response(request, body=json.dumps(response_data), content_type="application/json")
        print("No BIOS configuration found.")
        return Response(request, body=json.dumps({"key": "", "repetitions": 0}), content_type="application/json")
