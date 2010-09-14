addoper = lambda x,y : x+y
suboper = lambda x,y : x-y
muloper = lambda x,y : x*y
divoper = lambda x,y : x/y


class MissingRule(object):
    pass

class SkipMissing(MissingRule):
    '''The most straightforward of all the rules. Just skip missing points.'''


def addts(ts1, ts2, MissingRule = None):
    pass
    