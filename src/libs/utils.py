import os
import sys
import signal
import libs.globals
import libs.threadmanager

def readLine(prompt = ">>>", f = sys.stdin):
    return f.readline()

def signal_handler(signal, frame):
        print 'please press enter'
        libs.threadmanager.killall()
        libs.globals.global_vars["running"] = False
        #globalVars["server"].socket.close()

signal.signal(signal.SIGINT, signal_handler)
