from django import template 
import math
register = template.Library()

@register.filter
def round_number(number):
    return round(number, 2)

@register.filter
def math_ceil(number):
    return math.ceil(number)

@register.filter
def format_2digital(number) :
    return format(number, '.2f')

@register.filter
def covert_date(date) :
    return date.strftime("%d/%m/%Y")

