from dotenv import load_dotenv
load_dotenv()
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

PORT = 3010
RC_URL = os.getenv('RC_URL')
RC_API_KEY = os.getenv('RC_API_KEY')

class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/rc':
            if not RC_URL or not RC_API_KEY:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'Missing RC_URL or RC_API_KEY in environment')
                return
            try:
                response = requests.post(RC_URL, headers={'x-api-key': RC_API_KEY})
                self.send_response(response.status_code)
                self.end_headers()
                self.wfile.write(response.content)
                print(response.text)
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def run():
    server = HTTPServer(('0.0.0.0', PORT), SimpleHandler)
    print(f'Serving on port {PORT}')
    server.serve_forever()

if __name__ == '__main__':
    run()
