from code import InteractiveConsole
import rlcompleter
import readline
readline.parse_and_bind("tab: complete")
import threading
from libs.globals import globalVars
import libs.threadmanager

from libs.utils import readLine as readAFuckingLine
import sys


class console(libs.threadmanager.Thread):
    def __init__(self):
        libs.threadmanager.Thread.__init__(self)
        self.console = InteractiveConsole(globalVars)

    initscript = [
    "from libs.globals import globalVars",
    'other = globalVars["friends"]["0"]',
    "other.send('test')"
    ]

    def run(self):

        while globalVars["running"] == True and not self._stop.isSet():
            try:
                line = raw_input(">>>")
                if line == "runscript":
                    for line in self.initscript:
                        self.console.push(line)
                else:
                    self.console.push(line)
            except KeyboardInterrupt:
                globalVars["running"] = False
