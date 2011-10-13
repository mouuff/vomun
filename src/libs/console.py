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

    def run(self):
        while globalVars["running"] == True and not self._stop.isSet():
            try:
                self.console.push(raw_input(">>>"))
            except KeyboardInterrupt:
                globalVars["running"] = False
