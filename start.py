# encoding: UTF-8

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import csv
import re
import sys
import operator
import json

rows = []
rows_group_by_month = {}
rows_group_by_month_sorted = ''
rows_group_by_key = {}
rows_group_by_key_sorted = ''

def extract_rows():
  with open('extrato.csv', 'rU') as f:
      reader = csv.reader(f, delimiter=';')
      row_with_date = ''
      for row in reader:
        if '/' in row[0]:
          row_with_date = row
        elif '' == row[0]:
          row_with_date[1] = row_with_date[1].lstrip() + ' ' + row[1]
          rows.append(row_with_date)

def group_rows_by_month():
  for row in rows:
    key = re.search('(\d{2}\/\d{2})$', row[0]).group(1)
    if key in rows_group_by_month:
      rows_group_by_month[key].append(row)
    else:
      rows_group_by_month[key] = [row]
  rows_group_by_month_sorted = sorted(rows_group_by_month.items(), key=operator.itemgetter(0))

def group_rows_by_key():
  for row in rows:
    key = row[1]
    if key in rows_group_by_key:
      rows_group_by_key[key].append(row)
    else:
      rows_group_by_key[key] = [row]
  rows_group_by_key_sorted = sorted(rows_group_by_key.items(), key=operator.itemgetter(0))

extract_rows()
group_rows_by_month()
group_rows_by_key()

PORT_NUMBER = 8000

class myHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path=='/':
      self.path='/index.html'
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
        if 'rows_group_by_month' in self.path:
          self.wfile.write(json.dumps(rows_group_by_month, ensure_ascii=False))
        elif 'rows_group_by_key' in self.path:
          self.wfile.write(json.dumps(rows_group_by_key, ensure_ascii=False))
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
