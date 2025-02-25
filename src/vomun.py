#! /usr/bin/env python
'''Start the program. Load segments of the program that need to be started and
run them.'''
import time

import libs.globals

print(libs.globals.global_vars['anon+']['banner'] % 
        (libs.globals.global_vars['anon+']['VERSION'], 
        libs.globals.global_vars['anon+']['BUILD']))
        
import libs.threadmanager
import libs.events
import libs.logs
import libs.config

print('''
    == Warning! ==
This is a beta release
of Anon+, which means
that you should not
trust it to share
important info
as it is not
secure yet
''')

## Startup
if __name__ == '__main__':
    # Create the API Server. Used by external Applications.
    import api.server
    api.server.start()
    
    # Create the console. Later to be replaced with an extenal app
    from libs.console import console
    consoleO = console()
    libs.threadmanager.register(consoleO)
    #consoleO.start()
    
    # Load and prepare our list of friends
    import libs.friends as friends
    friends.load_friends()
    
    # Load connection handlers and start
    import tunnels.directudp
    tunnels.directudp.start()
    
    # Start the web interface
    import uis.web.manager
    uis.web.manager.start()
    
    # Start the API


    ## main loop
    while libs.globals.global_vars['running']:
        time.sleep(0.5)
    
    ## cleanup
    libs.threadmanager.killall()
    libs.threadmanager.close_sockets()
    friends.save_friends()
    libs.config.save_config()
    
    libs.globals.global_vars['running'] = False
    exit()

