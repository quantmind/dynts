

__all__ = ['isnumeric','significant','significant_format']


def isnumeric(obj):
    '''
    Return true if obj is a numeric value
    '''
    from decimal import Decimal
    if type(obj) == Decimal:
        return True
    else:
        try:
            float(obj)
        except:
            return False
        return True
    

def significant(number, n = 3):
    '''Round a number up to a given number ``n`` of significant figures.
Rounding to ``n`` significant digits is a more general-purpose technique
than rounding to ``n`` decimal places, since it handles numbers
of different scales in a uniform way.'''
    r = '%.' + str(n) +'g'
    return r % number


def significant_format(number, decimal_sep = '.', thousand_sep=',', n = 3):
    """Format a number according to a given number of significant figures.
"""
    str_number = significant(number, n)
    
    # sign
    if float(number) < 0:
        sign = '-'
    else:
        sign = ''
    
    if str_number[0] == '-':
        str_number = str_number[1:]
    if '.' in str_number:
        int_part, dec_part = str_number.split('.')
    else:
        int_part, dec_part = str_number, ''
    if dec_part:
        dec_part = decimal_sep + dec_part
    if thousand_sep:
        int_part_gd = ''
        for cnt, digit in enumerate(int_part[::-1]):
            if cnt and not cnt % 3:
                int_part_gd += thousand_sep
            int_part_gd += digit
        int_part = int_part_gd[::-1]
    return sign + int_part + dec_part

