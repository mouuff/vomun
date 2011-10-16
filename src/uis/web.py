#! /usr/bin/env python

import string,cgi,time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import libs.threadmanager
import libs.events


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # TODO: report connection with libs.events
            #f = open(curdir + sep + self.path,"r") 
##            self.send_response(200)
##            self.send_header('Content-type',	'text/html')
##            self.end_headers()            
            libs.events.broadcast('web_ui_request', self.path, self)
##            if self.path == '/':
##                self.wfile.write('200, OK. The server is working')
##            elif self.path == '/settings.html':
##                self.wfile.write('200, OK. Settings file')
                
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
     

    def do_POST(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query=cgi.parse_multipart(self.rfile, pdict)
            self.send_response(301)
            
            self.end_headers()
            upfilecontent = query.get('upfile')
            print('filecontent', upfilecontent[0])
            self.wfile.write('<HTML>POST OK.<BR><BR>');
            self.wfile.write(upfilecontent[0]);
            
        except :
            pass

class Server(libs.threadmanager.Thread):
    def run(self):
        try:
            server = HTTPServer(('', 7777), MyHandler)
            print('Webserver running on port 7777 : Started')
            server.serve_forever()
        except KeyboardInterrupt:
            print('^C received, shutting down server')
            server.socket.close()
            
class Handler(libs.events.Handler):
    def web_ui_request(self, path, connection):
        connection.send_response(200) # Woah, we shouldn't reply globally
        connection.send_header('Content-type',	'text/html')
        connection.end_headers()
        if path == '/':
            connection.wfile.write('Default interface.')
        elif path == '/settings.html':
            connection.wfile.write('Connections page')
            
## Start the server and handler            
def start():
    '''Start the user interface. Create the Server object and the listener
    we use to listen for events from this interface.
    '''
    server = Server()
    handler = Handler()

    libs.threadmanager.register(server)
    server.start()

    libs.events.register_handler(handler)
