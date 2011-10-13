out = ""
for friend in friends.values():
    out += str(friend)
request.send_response(200)
request.send_header('Content-type',    'text/css')
request.end_headers()
request.wfile.write(out)