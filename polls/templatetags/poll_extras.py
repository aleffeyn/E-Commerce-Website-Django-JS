from django import template
from jalali_date import date2jalali

register = template.Library()

@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg,'')

@register.filter(name='show_jalaali_date')
def show_jalaali_date(value):
    return date2jalali(value)

@register.filter(name='three_digits_currency')
def three_digits_currency(value):
    return '{:,}'.format(value) + ' تومان '