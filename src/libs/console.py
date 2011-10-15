'''Manage the current console interface. This will later be replaced with a
stand alone console application.'''

from code import InteractiveConsole
# import rlcompleter # unused import
import readline
readline.parse_and_bind("tab: complete")
from libs.globals import global_vars
import libs.threadmanager



class console(libs.threadmanager.Thread):
    def __init__(self):
        libs.threadmanager.Thread.__init__(self)
        self.console = InteractiveConsole(global_vars)

    initscript = [
    "from libs.globals import global_vars",
    'other = global_vars["friends"]["0"]',
    "other.send('test')"
    ]

    def run(self):
        while global_vars['running'] == True and not self._stop.isSet():
            try:
                line = raw_input(">>>")
                if line == "runscript":
                    for line in self.initscript:
                        self.console.push(line)
                else:
                    self.console.push(line)
            except KeyboardInterrupt:
                global_vars["running"] = False
