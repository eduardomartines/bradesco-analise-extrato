# encoding: UTF-8

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import json

from extract import Extract
from methods import Methods
from report import Report

extract = Extract('extrato.csv')
__rows = extract.get_rows()
basic_info = extract.get_basic_info()

methods = Methods(__rows)
report = Report(methods.months(), basic_info)

PORT_NUMBER = 8000

class myHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path=='/':
      self.path='/app/index.html'
    try:
      sendReply = False
      if self.path.endswith('.html'):
        mimetype='text/html'
        sendReply = True
      if self.path.endswith('.jpg'):
        mimetype='image/jpg'
        sendReply = True
      if self.path.endswith('.gif'):
        mimetype='image/gif'
        sendReply = True
      if self.path.endswith('.js'):
        mimetype='application/javascript'
        sendReply = True
      if self.path.endswith('.css'):
        mimetype='text/css'
        sendReply = True
      if self.path.endswith('.json'):
        mimetype='application/json'
        self.send_response(200)
        self.send_header('Content-type', mimetype)
        self.end_headers()
        if 'months' in self.path:
          self.wfile.write(json.dumps(methods.months(), ensure_ascii=False))
        elif 'keys' in self.path:
          self.wfile.write(json.dumps(methods.keys(), ensure_ascii=False))
        elif 'report' in self.path:
          key = self.path.split('/')[-1].split('.')[0]
          self.wfile.write(json.dumps(report.simple(key), ensure_ascii=False))
        elif 'basic_info' in self.path:
          self.wfile.write(json.dumps(basic_info, ensure_ascii=False))
        return
      if sendReply == True:
        f = open(curdir + sep + self.path)
        self.send_response(200)
        self.send_header('Content-type', mimetype)
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
      return
    except IOError:
      self.send_error(404,'File Not Found: %s' % self.path)

try:
  server = HTTPServer(('', PORT_NUMBER), myHandler)
  print 'Started httpserver on port ', PORT_NUMBER
  server.serve_forever()

except KeyboardInterrupt:
  print '^C received, shutting down the web server'
  server.socket.close()
