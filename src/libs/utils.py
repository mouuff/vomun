import sys
import os
import signal
from libs.globals import globalVars
import libs.threadmanager

def readLine(prompt = ">>>", f = sys.stdin):
    return f.readline()

def signal_handler(signal, frame):
        print 'please press enter'
        libs.threadmanager.killall()
        globalVars["running"] = False
        #globalVars["server"].socket.close()

signal.signal(signal.SIGINT, signal_handler)
