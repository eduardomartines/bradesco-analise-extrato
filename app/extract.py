# encoding: UTF-8

import csv

class Extract:
  def __init__(self, filename):
    self.__filename = filename
    self.__rows = []
    self.__extract_rows()

  def __extract_rows(self):
    with open(self.__filename, 'rU') as f:
        reader = csv.reader(f, delimiter=';')
        row_with_date = ''
        for row in reader:
          if '/' in row[0]:
            row_with_date = row
          elif '' == row[0]:
            row_with_date[1] = row_with_date[1].lstrip() + ' ' + row[1]
            self.__rows.append(row_with_date)

  def get_rows(self):
    return self.__rows
