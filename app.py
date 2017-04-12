from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json,re,urllib,simplejson
import cgi
import pdb

class LocalData(object):
    products = {
    'product1':{
    'id': 'product1',
    'company' : 'company1',
    'cost': '25',
    'count': '40'
    },
    }



# HTTPRequestHandler class
class HTTP_RequestHandler(BaseHTTPRequestHandler):
    def send_ok_response(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()


    def do_GET(self):
        break_path = re.findall('\/?(\w+)\/?',self.path)
        if len(break_path) ==1 :
            if break_path[0] == 'products':
                data = json.dumps(LocalData.products)
                self.send_ok_response()
                self.wfile.write(bytes(data,'utf8'))
                return
        elif len(break_path) == 2:
            if break_path[1] in LocalData.products.keys():
                data = json.dumps(LocalData.products[break_path[1]])
                self.send_ok_response()
                self.wfile.write(bytes(data,'utf8'))
                return
            else:
                self.send_response(404)
                self.end_headers()
                return
        # if self.path == '/favicon.io':
        #     data = json.dumps(LocalData.products[0])
        #     self.send_ok_response()
        #     self.wfile.write(bytes(data,'utf8'))
        return

    def do_POST(self):
        if self.path == '/products':
            if self.headers.get('Content-Type') == 'application/json':
                length = int(self.headers['Content-Length'])
                data = json.loads(self.rfile.read(length))
                recordID = data['id']
                LocalData.products[recordID] = data
                self.send_ok_response()
                self.wfile.write(bytes(json.dumps({'record_added': data}),'utf8'))
                return
            else:
                self.send_response(415)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return



    def do_PUT(self):
        break_path = re.findall('\/?(\w+)\/?',self.path)
        if len(break_path) == 2 :
            if break_path[0] == 'products':
                if self.headers.get('Content-Type') == 'application/json':
                    length = int(self.headers['Content-Length'])
                    data = json.loads(self.rfile.read(length))
                    LocalData.products[break_path[1]] = data
                    self.send_ok_response()
                    self.wfile.write(bytes(json.dumps({'record_replaced': data}),'utf8'))
                else:
                    self.send_response(415)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return

    def do_DELETE(self):
        break_path = re.findall('\/?(\w+)\/?',self.path)
        if len(break_path) == 2 :
            if break_path[0] == 'products':
                if break_path[1] in LocalData.products.keys():
                    del LocalData.products[break_path[1]]
                    self.send_ok_response()
                    self.wfile.write(bytes('record_deleted','utf8'))
                else:
                    self.send_response(415)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return


def run():
  print('starting server...')
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
