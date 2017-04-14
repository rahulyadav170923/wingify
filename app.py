from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json,re,urllib,simplejson
import cgi
import pdb
import base64

class LocalData(object):
    products = {
    'product1':{
    'id': 'product1',
    'company' : 'company1',
    'cost': '25',
    'count': '40'
    },
    }
    users = {
    'admin': 'cGFzc3dvcmQ='
    }

status_404 = {
    'status': '404',
    'msg':'Resource not found'
}


# HTTPRequestHandler class
class HTTP_RequestHandler(BaseHTTPRequestHandler):

    def authenticate(func):
        def authenticate_wrapper(self):
            if self.headers['Authorization'] and self.headers['username']:
                if self.headers['Authorization'] == 'Basic '+LocalData.users[self.headers['username']]:
                    return func(self)
                else:
                    self.send_200_response()
                    self.wfile.write(bytes(json.dumps({'status':'401','msg':'Unauthorised request'}),'utf-8'))
            else:
                self.do_AUTHHEAD()
                self.wfile.write(bytes(json.dumps({'status': '200','msg':'Username or Password header is missing'}),'utf-8'))
        return authenticate_wrapper

    def data_fields(func):
        def data_fields_wrapper(self):
            if self.headers['Content-Type'] == 'application/json' :
                length = int(self.headers['Content-Length'])
                data = json.loads(self.rfile.read(length))
                if 'id' in data.keys():
                    return func(self,data)
                else:
                    self.send_200_response()
                    self.wfile.write(bytes(json.dumps({'status':'422','msg':'Unprocessable Entity . Does not contain the minamal id field'}),'utf-8'))
            else:
                self.send_200_response()
                self.wfile.write(bytes(json.dumps({'status': '415','msg':' Media type is not supported'}),'utf-8'))
        return data_fields_wrapper


    def send_200_response(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()


    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    @authenticate
    def do_GET(self):
        break_path = re.findall('\/?(\w+)\/?',self.path)
        if len(break_path) ==1 :
            if break_path[0] == 'products':
                data = json.dumps(LocalData.products)
                self.send_200_response()
                self.wfile.write(bytes(data,'utf8'))
            else:
                self.send_200_response()
                self.wfile.write(bytes(json.dumps({'status':'404','msg':'Resource Not found'}),'utf8'))
        elif len(break_path) == 2:
            if break_path[1] in LocalData.products.keys():
                data = json.dumps(LocalData.products[break_path[1]])
                self.send_200_response()
                self.wfile.write(bytes(data,'utf8'))
            else:
                self.send_200_response()
                self.wfile.write(bytes(json.dumps({'status':'404','msg':'Resource Not found'}),'utf8'))
        return

    @authenticate
    @data_fields
    def do_POST(self,data):
        break_path = re.findall('\/?(\w+)\/?',self.path)
        if break_path[0] == 'products':
            length = int(self.headers['Content-Length'])
            # data = json.loads(self.rfile.read(length))
            recordID = data['id']
            LocalData.products[recordID] = data
            self.send_200_response()
            self.wfile.write(bytes(json.dumps({'record_added': data}),'utf8'))
        elif self.path == '/users':
            if self.headers['username'] and self.headers['password'] :
                key = base64.b64encode(self.headers['password'].encode()).decode()
                LocalData.users[self.headers['username']] = key
                self.send_200_response()
                self.wfile.write(bytes(json.dumps({'status': '200','msg':'user added','key':key}),'utf8'))
            else:
                self.send_200_response()
                self.wfile.write(bytes(json.dumps({'status': '200','msg':'Username or Password header is missing'}),'utf8'))
        else:
            self.send_200_response()
            self.wfile.write(bytes(json.dumps({'status':'404','msg':'Resource Not found'}),'utf8'))
        return

    @authenticate
    def do_PUT(self):
        break_path = re.findall('\/?(\w+)\/?',self.path)
        if len(break_path) == 2 :
            if break_path[0] == 'products':
                if self.headers.get('Content-Type') == 'application/json':
                    length = int(self.headers['Content-Length'])
                    data = json.loads(self.rfile.read(length))
                    LocalData.products[break_path[1]] = data
                    self.send_200_response()
                    self.wfile.write(bytes(json.dumps({'status':'200','msg':'record replaced','record': data}),'utf8'))
                else:
                    self.send_response(415)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(bytes(json.dumps({'status':'415','msg':'Media type not supported'}),'utf8'))
            else:
                self.send_200_response()
                self.wfile.write(bytes(json.dumps({'status':'404','msg':'Resource Not found'}),'utf8'))
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps({'status':'415','msg':'HTTP method not supported'}),'utf8'))
        return

    @authenticate
    def do_DELETE(self):
        break_path = re.findall('\/?(\w+)\/?',self.path)
        if len(break_path) == 2 :
            if break_path[0] == 'products':
                if break_path[1] in LocalData.products.keys():
                    del LocalData.products[break_path[1]]
                    self.send_200_response()
                    self.wfile.write(bytes(json.dumps({'status':'200','msg':'record_deleted'}),'utf8'))
                else:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(bytes(json.dumps({'status':'200','msg':'product does not exist'}),'utf8'))
        else:
            self.send_200_response()
            self.wfile.write(bytes(json.dumps({'status':'404','msg':'Resource Not found'}),'utf8'))
        return

def run():
  print('starting server...')
  if 'PORT' in os.environ.keys() :
    port = int(s.environ['PORT'])
  else:
    port = 8000
  server_address = ('0.0.0.0', port )
  httpd = HTTPServer(server_address, HTTP_RequestHandler)
  print('running server...')
  httpd.serve_forever()


if __name__ == '__main__':
    run()
