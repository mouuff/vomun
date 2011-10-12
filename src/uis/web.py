#! /usr/bin/env python

import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import libs.threadmanager

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # html file lets display it
            if self.path.endswith('.html'):
                f = open(curdir + sep + self.path,"r") 
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            #if its a css file lets display it
            if self.path.endswith('.css'):
                f = open(curdir + sep + self.path,"r") 
                self.send_response(200)
                self.send_header('Content-type',	'text/css')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

      
                
            return
                
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

def main():
    try:
        server = HTTPServer(('', 7777), MyHandler)
        print('Webserver running on port 7777 : Started')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()


class WebUI(libs.threadmanager.Thread):
    def run(self):
        main()

if __name__ == '__main__':
    main()
