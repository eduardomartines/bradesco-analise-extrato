# encoding: UTF-8

import csv
import re
import sys

search = sys.argv[1]
file_name = 'extrato.csv'
prev_line = ''
mouth_year_keys = []
mouth_year_values = []
mouth_year_lines = []

with open(file_name, 'rU') as f:
    reader = csv.reader(f, delimiter=';')

    for row in reader:
      if search in str(row).lower():
        if '/' in row[0]:
          prev_line = row
        mouth_year = prev_line[0].split('/')[1] + '/' + prev_line[0].split('/')[2]
        amount_match = prev_line[3] or prev_line[4]
        amount = amount_match.replace('.', '')
        amount = amount.replace(',', '.')
        amount = float(amount)
        if mouth_year not in mouth_year_keys:
          mouth_year_lines.append(' '.join(row) + '; ' + ' '.join(prev_line))
          mouth_year_keys.append(mouth_year)
          mouth_year_values.append(amount)
        else:
          index = mouth_year_keys.index(mouth_year)
          mouth_year_values[index] = mouth_year_values[index] + amount
      else:
        prev_line = row

print '\nResultados para "' + search + '":'

for i in xrange(0, len(mouth_year_keys)):
  print ' ' + mouth_year_keys[i] + ': ' + ('R$ {:,.2f}'.format(mouth_year_values[i]).replace(',', '|').replace('.', ',').replace('|', '.'))

total = 0
for value in mouth_year_values:
  total = total + value
print '\nTotal:'
print ' R$ {:,.2f}'.format(total)

print '\nRegistros:'
for item in mouth_year_lines:
  print item
