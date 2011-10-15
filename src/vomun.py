#! /usr/bin/env python
import sys
import time

import libs.globals
libs.globals.global_vars['input'] = sys.stdin
print(libs.globals.global_vars['anon+']['banner'] % 
        (libs.globals.global_vars['anon+']['VERSION'], 
        libs.globals.global_vars['anon+']['BUILD']))


import libs.threadmanager
import libs.events
import libs.logs

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

while libs.globals.global_vars['running']:
    time.sleep(0.5)

# cleanup
libs.threadmanager.killall()
friends.save_friends()

libs.globals.global_vars['running'] = False
exit()

