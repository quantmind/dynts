
__all__ = ['isnumeric']

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