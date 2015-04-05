# encoding: UTF-8

import json

class R:
  def __init__(self, name):
    self.name = name
    self.keys = []
    self.keys_values = []
    self.footer = []
    self.footer_values = []

  def get(self):
    __result = {}
    __result['name'] = self.name
    __result['keys'] = self.keys
    __result['keys_values'] = self.keys_values
    __result['footer'] = self.footer
    __result['footer_values'] = self.footer_values
    return __result

class Report:
  def __init__(self, rows_by_period):
    self.__rows_by_period = rows_by_period

  def __convert_to_float(self, _str):
    __amount = _str.replace('.', '')
    __amount = __amount.replace(',', '.')
    __amount = float(__amount)
    return __amount

  def __get_as_reais(self, amount):
    return 'R$ {:,.2f}'.format(amount)

  def simple(self, key):
    __key = key
    __r = R('simple')
    __r.keys.append('month')
    __r.keys.append('amount')
    __r.keys.append('grand_total')
    __r.keys.append('total')
    __r.footer.append('total')

    __filtered_rows = []

    for period in self.__rows_by_period:
      for row in self.__rows_by_period[period]:
        if key not in row[1].lower():
          self.__rows_by_period[period].remove(row)

    for period in self.__rows_by_period:
      __amount = 0
      __grand_total = 0
      for row in self.__rows_by_period[period]:
        #print row
        if row[3]:
          __amount += self.__convert_to_float(row[3])
        else:
          __amount += self.__convert_to_float(row[4])
        if row[5]:
          __grand_total = self.__convert_to_float(row[5])
      __key_value = [period, self.__get_as_reais(__amount), self.__get_as_reais(__grand_total), 0]
      __r.keys_values.append(__key_value)

    __r.footer_values = []

    return __r.get()
