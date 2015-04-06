# encoding: UTF-8

class Util:
  @staticmethod
  def convert_to_float(_str):
    _str = _str.replace(' ', '')
    _str = _str.replace('R$', '')
    amount = _str.replace('.', '')
    amount = amount.replace(',', '.')
    amount = float(amount)
    return amount

  @staticmethod
  def get_as_reais(amount):
    amount = 'R$ {:,.2f}'.format(amount)
    amount = amount.replace(',', '@')
    amount = amount.replace('.', ',')
    amount = amount.replace('@', '.')
    return amount
