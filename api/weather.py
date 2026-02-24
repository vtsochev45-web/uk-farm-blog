from http.server import BaseHTTPRequestHandler
import json

REGIONS = {
    'scotland': {'temp': 8, 'rain': 18, 'wind': 45, 'condition': 'Rain', 'impact': 'Field work suspended', 'alert': 'Heavy rain'},
    'midlands': {'temp': 6, 'rain': 2, 'wind': 15, 'condition': 'Clear', 'impact': 'Frost risk tonight', 'alert': 'Frost warning'},
    'south_west': {'temp': 11, 'rain': 5, 'wind': 25, 'condition': 'Cloudy', 'impact': 'Good for field work', 'alert': None},
    'east_anglia': {'temp': 9, 'rain': 1, 'wind': 18, 'condition': 'Sunny', 'impact': 'Ideal conditions', 'alert': None}
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {'data': REGIONS}
        self.wfile.write(json.dumps(response).encode())
        return