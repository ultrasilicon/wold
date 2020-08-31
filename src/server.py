from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import simplejson
import subprocess

def wake(label):
    if label == 'tornado':
        subprocess.run(['wakeonlan', '-p', '40000', 'a8:5e:45:50:6c:71'])
        print(f'magic packet sent to: {label}')
    else:
        print(f'device not recognized: {label}')



class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        self.send_response(200)
        self.end_headers()
        body = self.rfile.read(content_length)
        json = simplejson.loads(body)
        wake(json['device'])


httpd = HTTPServer(('0.0.0.0', 58293), SimpleHTTPRequestHandler)
httpd.serve_forever()
