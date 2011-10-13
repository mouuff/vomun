class asd:
    def __init__(self,request):
        self.request = request
    def index(self,*args):
        self.request.wfile.write("outasd")