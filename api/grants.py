# api/grants.py
from http.server import BaseHTTPRequestHandler
import json

GRANTS = {
    'farming-investment-fund': {'name': 'Farming Investment Fund', 'amount': '£25k-£500k', 'deadline': '2026-03-31', 'category': ['equipment']},
    'sfi': {'name': 'Sustainable Farming Incentive', 'amount': '£20-£450/ha', 'deadline': None, 'category': ['environmental']}
}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length else b'{}'
        
        try:
            user_data = json.loads(post_data)
            interests = user_data.get('interests', [])
            matches = [g for g in GRANTS.values() if any(i in g['category'] for i in interests)]
            response = {'success': True, 'matches': matches}
        except:
            response = {'success': False, 'matches': list(GRANTS.values())}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()