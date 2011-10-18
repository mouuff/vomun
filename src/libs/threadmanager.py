'''This module manages running threads and kills them all when the program
needs to exist. Threads should stop when thread.stop() is called.
'''
import threading
from libs.errors import UsageError
import socket
# Lists of managed threads
threads = []
joinlist = []
sockets = []
def register(thread):
    '''Register a thread for tracking. Threads registered here will be told to
    stop() when the program is told to exit. Threads must be a subclass of
    libs.threadmanager.Thread
    '''
    if isinstance(thread, Thread):
        threads.append(thread)
    else:
        raise UsageError('Must be a subclass of libs.threadmanager.Thread')
    
def register_for_join(thread):
    if isinstance(thread, Thread):
        joinlist.append(thread)
    else:
        raise UsageError('Must be a subclass of libs.threadmanager.Thread')

def joinall(timeout=None):
    '''Tell all thread objects to join. Wait for each one up to the `timeout`
    parameter.
    '''
    for thread in joinlist:
        thread.join(timeout)

    #thread with stop function

def register_socket(sock):

    if isinstance(sock,socket.socket):
        sockets.append(sock)
    else:
        raise UsageError('Must be a subclass of socket')

def close_sockets():
    for sock in sockets:
        sock.shutdown(socket.SHUT_RDWR)

def killall():
    '''Tell all threads to stop'''
    for thread in threads:
        thread.stop()
        
class Thread(threading.Thread):
    '''Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition.'''
    def __init__(self):
        super(Thread, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
