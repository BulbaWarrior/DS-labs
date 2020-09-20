import http.server
import socketserver
import redis

r = redis.Redis('redis') # 'redis'


PORT = 8080



class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        index = open('index.html', 'r')

        self.content = ''
        for line in index:
            self.content += line

        index.close()
        super(MyHandler, self).__init__(*args, **kwargs)
        
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            requests = r.incr('requests')
            s = f'<h4> a total of {requests} requests has been made </h4>'
            content = self.content + s
            self.wfile.write(content.encode())

        else:
            super(MyHandler, self).do_GET()


handler = MyHandler # http.server.SimpleHTTPRequestHandler

with http.server.ThreadingHTTPServer(("", PORT), handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
