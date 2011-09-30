#! /usr/bin/env python
VERSION = 'v0.0.0b0pre'
BUILD = 0
print('''
======================
= Anon+ %s
= Build: %s
======================
''' % (VERSION, BUILD))

import time
from code import InteractiveConsole
import rlcompleter
import readline
readline.parse_and_bind("tab: complete")



import libs.threadmanager
import libs.events
import libs.logs as logs

import libs.friends as friends
friends.load_friends()

import tunnels.directudp
tunnels.directudp.start()

#for friend in friends.friends.values():
#    friend.sendMessage("SUP")


running = True

console = InteractiveConsole(locals())

while running:
    try:
        console.push(raw_input(">>>"))
    except KeyboardInterrupt:
        running = False
libs.threadmanager.killall()
friends.save_friends()

exit()

