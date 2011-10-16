'''This module manages running threads and kills them all when the program
needs to exist. Threads should stop when thread.stop() is called.
'''
import threading
from libs.errors import UsageError

# Lists of managed threads
threads = []
joinlist = []

def register(thread):
    '''Register a thread for tracking. Threads registered here will be told to
    stop() when the program is told to exit. Threads must be a subclass of
    libs.threadmanager.Thread
    '''
    if isinstance(thread, Thread):
        threads.append(thread)
    else:
        raise UsageError('Must be a subclass of libs.threadmanager.Thread')
    
def registerForJoin(thread):
    if isinstance(thread, Thread):
        joinlist.append(thread)
    else:
        raise UsageError('Must be a subclass of libs.threadmanager.Thread')

def doJoins(timeout=None):
    for thread in joinlist:
        thread.join(timeout)

    #thread with stop function
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