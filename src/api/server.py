'''Run a server on 127.0.0.1:3451 for the localhost API. Parse the packets
with api.packets when we get them.
'''

import libs.threadmanager
import libs.globals
import xmlrpclib
import api.functions
from SimpleXMLRPCServer import SimpleXMLRPCServer

class APIServer(libs.threadmanager.Thread):
    calls = []
    '''Contains the APIServer within a stopable and registered thread'''
    def __init__(self):
        libs.threadmanager.Thread.__init__(self)
        self.server = SimpleXMLRPCServer(("localhost", 3451),allow_none = True)

    def add_call(self,call):
        self.server.register_function(call,call.__name__)
        self.calls.append(call)

    def run(self):
        print('API-server running on port 3451 : Started')
        while not self._stop.isSet():
            try:
                # server.serve_forever()
                self.server.handle_request()
            except KeyboardInterrupt:
                print('^C received, shutting down web server')
                self.server.socket.close()
                self._stop.set()
            
## Start the server and handler            
def start():
    '''Start the user interface. Create the Server object and the listener
    we use to listen for events from this interface.
    '''
    libs.globals.global_vars["apiserver"] = APIServer()
    libs.threadmanager.register(libs.globals.global_vars["apiserver"])
    libs.globals.global_vars["apiserver"].start()
    api.functions.register()