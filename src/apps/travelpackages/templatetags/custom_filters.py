from django import template

register = template.Library()

@register.filter
def indian_currency(value):
    """Convert a number into Indian style comma separated currency"""
    try:
        value = int(float(value))
        s = str(value)
        l = len(s)
        if l > 3:
            last_three = s[-3:]
            other_nums = s[:-3]
            if len(other_nums) > 0:
                formatted = ''
                for i, c in enumerate(reversed(other_nums)):
                    if i > 0 and i % 2 == 0:
                        formatted = ',' + formatted
                    formatted = c + formatted
                return formatted + ',' + last_three
        return s
    except:
        return value
