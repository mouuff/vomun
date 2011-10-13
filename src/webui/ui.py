import sys
from os import getcwd, sep
import json
import subprocess
import traceback

sys.path.append(getcwd()+sep+"webui"+sep)

pathsegments = request.path.split("/")[1:]
if len(pathsegments) > 0:
    controller = pathsegments.pop(0)
else:
    controller = "index"

if len(pathsegments) > 0:
    action = pathsegments.pop(0)
else:
    action = "index"

if len(pathsegments)<1:
    pathsegments = {}

print pathsegments
out = str(pathsegments)
out += "<br>controller: %s <br>action: %s" % (controller,action)


try:
    serializable = {}
    for v in dir(request):
        try:
            json.dumps(getattr(request,v))
            serializable[v] = getattr(request,v)
        except:
            pass
    js = json.dumps(serializable)

    output = subprocess.check_output(["python",getcwd()+sep+"webui"+sep+"controllers/"+controller+".py",js])
    request.wfile.write(output)


except Exception as ex:

    request.send_response(500)
    request.send_header('Content-type',    'text/html')
    request.end_headers()
    request.wfile.write("<pre>")
    traceback.print_exc(file=request.wfile)
    request.wfile.write("</pre>")     
