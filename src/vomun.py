#! /usr/bin/env python
import sys
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
consoleO.start()

import libs.friends as friends
friends.load_friends()

import tunnels.directudp
tunnels.directudp.start()

#main
from uis.web import WebUI
web = WebUI()
web.start()

while globalVars["running"]: pass

# cleanup
libs.threadmanager.killall()
friends.save_friends()

exit()

