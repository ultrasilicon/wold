from wold.utils import Utils

import simplejson

from http.server import HTTPServer, BaseHTTPRequestHandler
import asyncio
import websockets
import queue 
import threading
import time


msg_buf = queue.Queue(100)

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

        if 'device' not in json:
            return
        global msg_buf
        msg_buf.put(json['device'])
        print(list(msg_buf.queue))


class HttpServer(threading.Thread):
    def __init__(self, port, group=None, target=None,
                 args=(), kwargs=None, verbose=None):
        super(HttpServer,self).__init__()
        self.port = port

    def run(self):
        httpd = HTTPServer(('0.0.0.0', self.port), SimpleHTTPRequestHandler)
        httpd.serve_forever()


class WebSocketServer(threading.Thread):
    def __init__(self, port, group=None, target=None,
                 args=(), kwargs=None, verbose=None):
        super(WebSocketServer,self).__init__()
        self.port = port

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(self._listen, '0.0.0.0', self.port)
        loop.run_until_complete(start_server)
        loop.run_forever()

    async def _listen(self, websocket, path):
        while True:
            global msg_buf
            while not msg_buf.empty():
                target_name = msg_buf.get()
                await websocket.send(target_name)
                Utils.log('info', f'Sent wakeup signal to: {target_name}')
            time.sleep(1)


class Server():
    def __init__(self, config):
        self.config = config
        global msg_buf
        msg_buf.put('aa')
        msg_buf.put('bb')
        msg_buf.put('cc')
        msg_buf.put('dd')

    def start(self):
        ws_server = WebSocketServer(self.config.ws_port)
        http_server = HttpServer(self.config.http_port)

        ws_server.start()
        http_server.start()
        
