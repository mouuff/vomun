#! /usr/bin/env python

import string,cgi,time
from os import getcwd, sep,system
from os.path import normpath
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import libs.threadmanager
from libs.globals import globalVars

class MyHandler(BaseHTTPRequestHandler):

    endings = {}
    handlers = {}

    def setVars(self):
        self.endings = {
            "html"  :   "text/html",
            "css"   :   "text/css"
        }

        self.handlers = {
            "py"    :   self.do_py
        }

    def do_py(self,filename):
        f = open(filename, "r")
        src = f.read()
        CompiledSrc = compile(src,filename,"exec")
        eval (CompiledSrc,globalVars,{"request":self})

    def do_raw(self,filename,ending="None"):
        f = open(filename) 
        self.send_response(200)
        if ending in self.endings:
            self.send_header("Content-type",self.endings[ending])
        else:
            self.send_header('Content-type',    'text/plain')
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
        return

    def do_GET(self):
        self.setVars()
        try:
            #set default path
            if self.path == "/":
                self.path = "/index/index"
            basepath = getcwd() + sep + "webui"
            filename =  normpath(basepath + self.path)

            print filename
            if not filename.startswith(basepath):
                self.send_error(500,"File inclusion detected") 

            extension = self.path.split(".")[-1]
            if extension in self.handlers.keys():
                handler = self.handlers[extension]
                handler(filename)
            else:
                handler = self.do_raw
                handler(filename)
                
        except IOError as error:
            #try MVC
            print "trying MVC"
            try:
                filename = basepath + "/ui.py"
                handler = self.handlers["py"]
                print filename
                handler(filename)
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


class WebUI(libs.threadmanager.Thread):
    def __init__(self):
        libs.threadmanager.Thread.__init__(self)
        globalVars["server"] = HTTPServer(('', 7777), MyHandler)
        
    def run(self):
        while globalVars["running"] == True and not self._stop.isSet():
            globalVars["server"].handle_request()

if __name__ == '__main__':
    ui = WebUI()
    ui.start()
