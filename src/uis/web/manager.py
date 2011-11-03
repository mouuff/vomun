import string
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import libs.threadmanager
import libs.globals
import libs.events

# Import our other files
import uis.web.content


class MyHandler(BaseHTTPRequestHandler):
    '''Handles events from the web server and passes them out as events to
    libs.events via the broadcast function. The event is sent to the
    web_ui_request method of all registered event handlers.'''
    
    def do_GET(self):
        '''Handle GET requests'''
        libs.events.broadcast('web_ui_request', self.path, self)

    def do_POST(self):
        '''Handle POST requests'''
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query=cgi.parse_multipart(self.rfile, pdict)
            self.send_response(301)
            
            self.end_headers()
            upfilecontent = query.get('upfile')
            print('filecontent', upfilecontent[0])
            self.wfile.write('<html>POST OK.<br /><br />');
            self.wfile.write(upfilecontent[0]);
            
        except:
            pass

class Server(libs.threadmanager.Thread):
    '''Contains the webserver within a stopable and registered thread'''
    def run(self):
        self.server = HTTPServer(('', 7777), MyHandler)
        libs.threadmanager.register_socket(self.server.socket)
        print('Webserver running on port 7777 : Started')
        while not self._stop.isSet():
            try:
                # server.serve_forever()
                self.server.handle_request()
            except KeyboardInterrupt:
                print('^C received, shutting down web server')
                self.server.socket.close()
                self._stop.set()
            
class Handler(libs.events.Handler):
    '''A demonstration of how event handlers can serve pages on the localhost
    web server. This can be used easily accross the entire project.
    '''
    def web_ui_request(self, path, connection):
        if path == '/':
            connection.send_response(200)
            connection.send_header('Content-type',	'text/html')
            connection.end_headers()
            connection.wfile.write(uis.web.content.template.format(
                    title = 'Anon+ News Feed',
                    pagetitle = 'Anon+ News Feed',
                    main = uis.web.content.post_box + self.__generate_news_feed(),
                    sidecontent = self.__friends2html()
            ))
        elif path == '/global.css':
            connection.send_response(200)
            connection.send_header('Content-type',	'text/css')
            connection.end_headers()
            connection.wfile.write(uis.web.content.globalcss)
        elif path == '/settings.html':
            connection.send_response(200)
            connection.send_header('Content-type',	'text/html')
            connection.end_headers()
            connection.wfile.write('Connections page')
        elif path == '/shutdown.html':
            connection.send_response(200)
            connection.send_header('Content-type',	'text/html')
            connection.end_headers()
            print('Got shutdown request from web server')
            connection.wfile.write(uis.web.content.template.format(
                    title = 'Shutting down',
                    pagetitle = 'Shutdown',
                    main = 'We are quitting now. Threads are being killed.',
                    sidecontent = 'Goodbye :)'
            ))
            libs.globals.global_vars['running'] = False
            libs.threadmanager.killall()
        elif path == '/keys.html':
            connection.send_response(200)
            connection.send_header('Content-type', 'text/html')
            connection.end_headers()
            connection.wfile.write(uis.web.content.template.format(
                    title = 'Key management',
                    pagetitle = 'Key management',
                    main = uis.web.content.key_form,
                    sidecontent = self.__friends2html()
            ))
            
    def __friends2html(self):
        '''Convert our friends list into some nice HTML'''
        return uis.web.content.friends_box.format(
                friends = 'Our friend detector tells me you have no friends!'
        )
        
    def __generate_news_feed(self):
        '''Return the post elements in HTML'''
        content = ''
        content += uis.web.content.post.format(
                user = 'aj00200',
                body = 'Yeah, we are almost ready!',
                hash = 'lskjdf'
        )
        content += uis.web.content.mention.format(
                user = 'Anonymous1234',
                body = '<a class="tag" href="#!/u/aj00200">@aj00200</a> Ready for the Nov 5th beta?',
                hash = 'lzu89k'
        )
        return content
            
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
