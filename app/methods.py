# encoding: UTF-8

import re

class Methods:

  def __init__(self, rows):
    self.__rows = rows

  def months(self):
    __months = {}
    for row in self.__rows:
      month = re.search('(\d{2}\/\d{2})$', row[0]).group(1)
      if month in __months:
        __months[month].append(row)
      else:
        __months[month] = [row]
    return __months

  def keys(self):
    __keys = {}
    for row in self.__rows:
      key = row[1]
      if key in __keys:
        __keys[key].append(row)
      else:
        __keys[key] = [row]
    return __keys
