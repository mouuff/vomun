import sys

print sys.argv

class index:
    def __init__(self,request):
        self.request = request
    def index(self,*args):
        self.request.wfile.write("outasd")