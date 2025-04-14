import http.server
import socketserver
import os

DIRECTORY = "webpage"

os.chdir(DIRECTORY)

Handler = http.server.SimpleHTTPRequestHandler
#Handler.directory = DIRECTORY

with socketserver.TCPServer(("", 80), Handler) as httpd:
    httpd.serve_forever()
