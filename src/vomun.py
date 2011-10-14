#! /usr/bin/env python
import sys
import time

from libs.globals import globalVars
globalVars["running"] = True
globalVars["anon+"] = {}
globalVars["anon+"]["VERSION"] = 'v0.0.0b0pre'
globalVars["anon+"]["BUILD"] = 0
globalVars["input"] = sys.stdin
globalVars["anon+"]["Banner"] = '''
======================
= Anon+ %s
= Build: %s
======================
''' % ( globalVars["anon+"]["VERSION"], 
        globalVars["anon+"]["BUILD"])

print globalVars["anon+"]["Banner"]


import libs.threadmanager
import libs.events
import libs.logs as logs

#startup
from libs.console import console
consoleO = console()
libs.threadmanager.register(consoleO)
consoleO.start()

import libs.friends as friends
friends.load_friends()

import tunnels.directudp
tunnels.directudp.start()

#main
#from uis.web import WebUI
#web = WebUI()
#libs.threadmanager.register(web)
#web.start()

while globalVars["running"]:
    time.sleep(0.5)

# cleanup
libs.threadmanager.killall()
friends.save_friends()

"please press enter"
exit()

