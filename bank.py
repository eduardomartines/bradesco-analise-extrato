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
mouth_partial_values =[]

with open(file_name, 'rU') as f:
    reader = csv.reader(f, delimiter=';')

    for row in reader:
      if search in str(row).lower():
        if '/' in row[0]:
          prev_line = row
        partial_total_match = prev_line[5]
        partial_total = partial_total_match.replace('.', '')
        partial_total = partial_total.replace(',', '.')
        if '.' in partial_total:
          partial_total = float(partial_total)
        mouth_year = prev_line[0].split('/')[1] + '/' + prev_line[0].split('/')[2]
        amount_match = prev_line[3] or prev_line[4]
        amount = amount_match.replace('.', '')
        amount = amount.replace(',', '.')
        amount = float(amount)
        if mouth_year not in mouth_year_keys:
          mouth_year_lines.append(''.join(row) + '; ' + ' '.join(prev_line))
          mouth_year_keys.append(mouth_year)
          mouth_year_values.append(amount)
          mouth_partial_values.append(partial_total)
        else:
          index = mouth_year_keys.index(mouth_year)
          mouth_year_values[index] = mouth_year_values[index] + amount
          mouth_partial_values[index] = partial_total
      else:
        prev_line = row

print '\nResultados para "' + search + '":'

total = 0
for value in mouth_year_values:
  total = total + value
  total_text = 'R$ {:,.2f}'.format(total)

for i in xrange(0, len(mouth_year_keys)):
  mouth = mouth_year_keys[i]
  mouth_text = mouth + ': '
  value = mouth_year_values[i]
  value_text = 'R$ {:,.2f}'.format(value).replace(',', '|').replace('.', ',').replace('|', '.')
  partial_total = mouth_partial_values[i]
  if partial_total:
    partial_total_text = 'R$ {:,.2f}'.format(partial_total)
    bla = (float(value)*100/float(partial_total))
    bla_text = '{:,.2f}%'.format(bla)
  percentage = (float(value)*100/float(total))
  percentage_text = '\t\t{:,.2f}%'.format(percentage) + ' (' + total_text + ')     ' + bla_text + ' (' + partial_total_text + ')'
  print '\t' + mouth_text + value_text + percentage_text

print '\nTotal:'
print '\t' + total_text

print '\nRegistros:'
for item in mouth_year_lines:
  print '\t' + item
