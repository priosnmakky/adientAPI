from django import template 
import math
register = template.Library()

@register.filter
def round_number(number):

    if number is None :
        
        return 00.00

    else:

        return round(number, 2)

@register.filter
def math_ceil(number):
    if number is None :
        
        return 00.00

    else:

        return math.ceil(number)

@register.filter
def format_2digital(number) :

    if number is None :
        
        return 00.00

    else:
            
        return format(number, '.2f')

@register.filter
def covert_none(data) :

    if data is None :
        
        return ''
    
    else :

        return data

@register.filter
def covert_date(date) :
    
    if date is None :

        return ""

    else :

        return date.strftime("%d/%m/%Y")

@register.filter
def covert_time(date) :

    if date is None :

        return ""

    else :

        return date.strftime("%H:%M")

