# encoding: UTF-8

import csv
from util import Util

class BasicInfo:
  def __init__(self, total, start_at, end_at):
    self.__total = total
    self.__start_at = start_at
    self.__end_at = end_at

  def get(self):
    __result = {}
    __result['total'] = self.__total
    __result['start_at'] = self.__start_at
    __result['end_at'] = self.__end_at
    return __result

class Extract:
  def __init__(self, filename):
    self.__filename = filename
    self.__rows = []
    self.__total = 0
    self.__start_at = ''
    self.__end_at = ''

  def __extract_rows(self):
    with open(self.__filename, 'rU') as f:
        reader = csv.reader(f, delimiter=';')
        row_with_date = ''
        for row in reader:
          if len(row) == 1:
            continue
          if 'SALDO ANTERIOR' in row[1]:
            continue
          if 'Total' in row[1]:
            self.__total = Util.convert_to_float(row[5])
            self.__total = Util.get_as_reais(self.__total)
            break
          if '/' in row[0]:
            row_with_date = row
          elif '' == row[0]:
            row_with_date[1] = row_with_date[1].lstrip() + ' ' + row[1]
            self.__rows.append(row_with_date)
    self.__start_at = self.__rows[0][0]
    self.__end_at = self.__rows[-1][0]

  def get_rows(self):
    self.__extract_rows()
    return self.__rows

  def get_basic_info(self):
    basic_info = BasicInfo(self.__total, self.__start_at, self.__end_at)
    return basic_info.get()
