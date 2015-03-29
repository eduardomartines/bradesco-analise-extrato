# encoding: UTF-8

import csv
import re
import sys
import operator

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
