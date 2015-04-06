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
    reportView = R('simple')
    reportView.keys.append('month')
    reportView.keys.append('amount')
    reportView.keys.append('partial_total')
    reportView.keys.append('grand_total')
    reportView.footer.append('total')

    filtered_rows_by_period = {}

    for period in self.__rows_by_period:
      for row in self.__rows_by_period[period]:
        if key in row[1].lower():
          if period in filtered_rows_by_period:
            filtered_rows_by_period[period].append(row)
          else:
            filtered_rows_by_period[period] = [row]

    print filtered_rows_by_period

    for period in filtered_rows_by_period:
      amount = 0
      partial_total = 0

      for row in filtered_rows_by_period[period]:
        if row[3]:
          amount += self.__convert_to_float(row[3])
        else:
          amount += self.__convert_to_float(row[4])
        if row[5]:
          partial_total = self.__convert_to_float(row[5])

      key_value = []
      key_value.append(period)
      key_value.append(self.__get_as_reais(amount))
      key_value.append(self.__get_as_reais(partial_total))

      key_value.append(0) # TODO

      reportView.keys_values.append(key_value)

    reportView.footer_values = []

    return reportView.get()
