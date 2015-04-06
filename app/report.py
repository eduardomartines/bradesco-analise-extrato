# encoding: UTF-8

import json
from util import Util

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
  def __init__(self, rows_by_period, basic_info):
    self.__rows_by_period = rows_by_period
    self.__basic_info = basic_info

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

    total = 0

    for period in filtered_rows_by_period:
      amount = 0
      partial_total = 0

      for row in filtered_rows_by_period[period]:
        if row[3]:
          amount += Util.convert_to_float(row[3])
        else:
          amount += Util.convert_to_float(row[4])
        if row[5]:
          partial_total = Util.convert_to_float(row[5])

      total += amount
      grand_total = self.__basic_info['total']

      key_value = []
      key_value.append(period)
      key_value.append(Util.get_as_reais(amount))
      if partial_total:
        amount_percentage = (float(amount)*100/float(partial_total))
        key_value.append('{:,.2f}%'.format(amount_percentage) + ' (' + Util.get_as_reais(partial_total) + ')')
      else:
        key_value.append('')
      grand_total_percentage = (float(amount)*100/Util.convert_to_float(grand_total))
      key_value.append('{:,.2f}%'.format(grand_total_percentage) + ' (' + grand_total + ')')

      reportView.keys_values.append(key_value)

    reportView.footer_values = []
    reportView.footer_values.append(Util.get_as_reais(total))
    reportView.footer_values.append('')
    reportView.footer_values.append('')

    return reportView.get()
