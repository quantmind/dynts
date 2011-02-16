from dynts.dsl import ComposeFunction
from .simple import ScalarWindowFunction


ComposeFunction('sdd','sd(delta(x1),window=20)',docs='''\
This is a shortcut function for calculating the standard deviation
of changes. Therefore:

.. math::

    {\\tt sdd}(y_t,w) = {\tt sd}({\\tt delta}(y_t),w)
''',description = 'standard deviation of changes')

ComposeFunction('vol','15.874*sd(delta(x1),window=20)',docs='''\
a''',description='Annualised volatility')

ComposeFunction('psdd','sd(ldelta(x1),window=20)',docs='''\
This is a shortcut function for calculating the standard deviation
of log-changes. Therefore:

.. math::

    {\\tt sdd}(y_t,w) = {\tt sd}({\\tt ldelta}(y_t),w)
''',description='log standard deviation')

ComposeFunction('avol','15.874*sd(ldelta(x1),window=20)',docs='''\
a''',description='annualised volatility')

# Annualized sharpe on changes
ComposeFunction('asharpe','15.874*sharpe(delta(x1),window=20)',docs='''\
a''',description='Annualised volatility')
# Annualized sharpe on log-changes
ComposeFunction('alsharpe','15.874*sharpe(ldelta(x1),window=20)',docs='''\
a''',description='Annualised volatility')


class zscore(ScalarWindowFunction):
    """\
Rolling Z-Score function:

.. math::

    zs_{n,w} = \\frac{y_n - y_{n-w}}{\sigma_{n,w}}
    
"""
    def apply(self, ts, **kwargs):
        return tsfunctions.zscore(ts, **kwargs)
    

class prange(ScalarWindowFunction):
    """\
Rolling Percentage range function.
"""
    def apply(self, ts, **kwargs):
        return tsfunctions.prange(ts, **kwargs)