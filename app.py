from http.server import BaseHTTPRequestHandler, HTTPServer
import os
# HTTPRequestHandler class
class HTTP_RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = "Hello world!"
        self.wfile.write(bytes(message, "utf8"))
        return
    def do_PUT(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = "Hello world!"
        self.wfile.write(bytes(message, "utf8"))
        return


def run():
  print('starting server...')
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  if 'PORT' in os.environ.keys() :
    port = os.environ['PORT']
  else:
    port = 8000
  server_address = ('0.0.0.0', port )
  httpd = HTTPServer(server_address, HTTP_RequestHandler)
  print('running server...')
  httpd.serve_forever()


if __name__ == '__main__':
    run()
