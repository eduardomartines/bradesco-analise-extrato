# encoding: UTF-8

class Util:
  @staticmethod
  def convert_to_float(_str):
    amount = _str.replace('.', '')
    amount = amount.replace(',', '.')
    amount = float(amount)
    return amount

  @staticmethod
  def get_as_reais(amount):
    return 'R$ {:,.2f}'.format(amount)
