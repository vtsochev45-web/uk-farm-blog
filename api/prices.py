from http.server import BaseHTTPRequestHandler
import json

PRICES = {
    'wheat': {'price': 165, 'unit': '£/t', 'change': 2.5},
    'barley': {'price': 155, 'unit': '£/t', 'change': -1.0},
    'lamb': {'price': 2.85, 'unit': '£/kg', 'change': 0.15}
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {'data': PRICES}
        self.wfile.write(json.dumps(response).encode())
        return