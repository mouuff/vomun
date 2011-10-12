import sys

print dir(sys.stdin)
#inpFile = open(sys.stdin,"r")
def readLine(prompt = ">>>", f = sys.stdin):
    return f.readline()