out =  """
<html>
    <head>
        <title>Anon+</title>
        <style type="text/css">
            @import url("/css/anonplus.css");
        </style>
    </head>
    <body>
        <div class="container_12">%s</div>
    </body>
</html>
""" % "test"




request.send_response(200)
request.send_header('Content-type',    'text/html')
request.end_headers()
request.wfile.write(out)