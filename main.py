from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from endpoints_parser import parse_endpoints

PORT = 3010

# Load and process endpoints using the parser
endpoints = parse_endpoints()
if not endpoints:
    print("Failed to load endpoints configuration")
    raise SystemExit(1)

# Create a mapping of endpoint paths to their configurations
endpoint_map = {f'/{endpoint["name"]}': endpoint['target'] for endpoint in endpoints}
print(f'Available endpoints: {list(endpoint_map.keys())}')

class Handler(BaseHTTPRequestHandler):
    def handle_request(self, received_method):
        if self.path not in endpoint_map:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(f'Not Found. Available endpoints: {list(endpoint_map.keys())}'.encode())
            return

        target = endpoint_map[self.path]
        expected_method = target.get('method', 'POST')

        # Validate HTTP method
        if received_method != expected_method:
            self.send_response(405)  # Method Not Allowed
            self.end_headers()
            error_msg = f'Method {received_method} not allowed for {self.path}. Expected: {expected_method}'
            self.wfile.write(error_msg.encode())
            return

        try:
            response = requests.request(
                method=expected_method,
                url=target['url'],
                headers=target['headers']
            )
            self.send_response(response.status_code)
            self.end_headers()
            self.wfile.write(response.content)
            print(f'{expected_method} request to {self.path} -> {target["url"]} returned {response.status_code}')
            if response.text:
                print(f'Response: {response.text}')
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            error_msg = f'Error calling {target["url"]}: {str(e)}'
            print(error_msg)
            self.wfile.write(error_msg.encode())

    # def do_GET(self):
    #     self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    # def do_PUT(self):
    #     self.handle_request('PUT')

    # def do_DELETE(self):
    #     self.handle_request('DELETE')

    # def do_PATCH(self):
    #     self.handle_request('PATCH')

def run():
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    print(f'Serving on port {PORT}')
    server.serve_forever()

if __name__ == '__main__':
    run()
