template = '''
<!DOCTYPE html>
<html>
  <head>
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="global.css" />
  </head>
  <body>
    <div id="header">
      <div id="title">
        <h1>Project Vomun</h1>
      </div>
      <div id="nav">
        <a href="/">Anon+</a> | 
        <a href="/settings.html">Settings</a> | 
        <a href="/shutdown.html">Shutdown</a>
      </div>
    </div>
    <div id="main">
      <h2>{pagetitle}</h2>
      {main}
    </div>
    <div id="side">
      <h3>{sidecontent}</h3>
    </div>
  </body>
</html>'''

globalcss = '''
#header {
  border-bottom: 1px solid gray;
  letter-spacing: 3x;
  color: gray;
}
'''