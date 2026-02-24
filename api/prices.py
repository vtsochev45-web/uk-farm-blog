# api/prices.py
from http.server import BaseHTTPRequestHandler
import json

PRICES = {
    'wheat_feed': {'price': 165.0, 'unit': '£/t', 'change': 2.5, 'trend': 'up'},
    'barley': {'price': 155.0, 'unit': '£/t', 'change': -1.0, 'trend': 'down'},
    'rapeseed': {'price': 420.0, 'unit': '£/t', 'change': 5.0, 'trend': 'up'},
    'lamb': {'price': 2.85, 'unit': '£/kg', 'change': 0.15, 'trend': 'up'},
    'milk': {'price': 0.38, 'unit': '£/L', 'change': 0.01, 'trend': 'up'}
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {'timestamp': '2026-02-24T18:00:00Z', 'source': 'AHDB', 'data': PRICES}
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()