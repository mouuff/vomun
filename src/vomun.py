#! /usr/bin/env python
import sys
import time

import libs.globals

print(libs.globals.global_vars['anon+']['banner'] % 
        (libs.globals.global_vars['anon+']['VERSION'], 
        libs.globals.global_vars['anon+']['BUILD']))


import libs.threadmanager
import libs.events
import libs.logs
import libs.config

## Startup
# Create the console. Later to be replaced with an extenal app
from libs.console import console
consoleO = console()
libs.threadmanager.register(consoleO)
consoleO.start()

# Load and prepare our list of friends
import libs.friends as friends
friends.load_friends()

# Load connection handlers and start
import tunnels.directudp
tunnels.directudp.start()

# Start the web interface
import uis.web.manager
uis.web.manager.start()


## main loop
while libs.globals.global_vars['running']:
    time.sleep(0.5)

## cleanup
libs.threadmanager.killall()
friends.save_friends()
libs.config.save_config()

libs.globals.global_vars['running'] = False
exit()

