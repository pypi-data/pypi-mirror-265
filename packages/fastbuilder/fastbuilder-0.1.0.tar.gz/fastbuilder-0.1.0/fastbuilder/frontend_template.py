react_template = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8"/>
        <link rel="icon" href="{{{{prefix | safe}}}}/static/{favicon_file_name}"/>
        <meta name="viewport" content="width=device-width,initial-scale=1"/>
        <meta name="theme-color" content="#000000"/>
        <meta name="description" content="Web site created using create-react-app"/>
        <link rel="apple-touch-icon" href="{{{{prefix | safe}}}}/static/logo192.png"/>
        <link rel="manifest" href="{{{{prefix | safe}}}}/static/manifest.json"/>
        <title>{document_name}</title>
        <script defer="defer" src="{{{{prefix | safe}}}}/static/js/{js_file_name}"></script>
        <link href="{{{{prefix | safe}}}}/static/css/{css_file_name}" rel="stylesheet">
    </head>
    <body>
        <noscript>You need to enable JavaScript to run this app.</noscript>
        <div id="root"></div>
    </body>
</html>
"""


vue_template = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" href="{{{{prefix | safe}}}}/static/{favicon_file_name}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{document_name}</title>
    <script type="module" crossorigin src="{{{{prefix | safe}}}}/static/{js_file_name}"></script>
    <link rel="stylesheet" crossorigin href="{{{{prefix | safe}}}}/static/{css_file_name}">
  </head>
  <body>
    <div id="app"></div>
  </body>
</html>


"""


solidjs_template = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <link rel="shortcut icon" type="image/ico" href="{{{{prefix | safe}}}}/static/{favicon_file_name}" />
    <title>{document_name}</title>
    <script type="module" crossorigin src="{{{{prefix | safe}}}}/static/{js_file_name}"></script>
    <link rel="stylesheet" crossorigin href="{{{{prefix | safe}}}}/static/{css_file_name}">
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>

  </body>
</html>


"""
