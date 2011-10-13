#! /usr/bin/env python

import string,cgi,time
from os import getcwd, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import libs.threadmanager
from libs.globals import globalVars

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path == "/":
                self.path = "/index.py"
            # html file lets display it
            if self.path.endswith('.html'):
                f = open(getcwd() + sep + self.path,"r") 
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            #if its a css file lets display it
            if self.path.endswith('.css'):
                f = open(getcwd() + sep + self.path,"r") 
                self.send_response(200)
                self.send_header('Content-type',	'text/css')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            if self.path.endswith('.py'):
                filename = getcwd() + sep + "webui" + self.path
                f = open(filename, "r")
                src = f.read()
                CompiledSrc = compile(src,filename,"exec")
                eval (CompiledSrc,globalVars,{"request":self})
                #print dir(CompiledSrc)
      
                
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
        globalVars["server"] = HTTPServer(('', 7777), MyHandler)
        print('Webserver running on port 7777 : Started')
        while globalVars["running"] == True:
            globalVars["server"].handle_request()
            print "asd"
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        globalVars["server"].socket.close()


class WebUI(libs.threadmanager.Thread):
    def __init__(self):
        libs.threadmanager.Thread.__init__(self)
        globalVars["server"] = HTTPServer(('', 7777), MyHandler)
        
    def run(self):
        while globalVars["running"] == True and not self._stop.isSet():
            globalVars["server"].handle_request()

if __name__ == '__main__':
    main()
