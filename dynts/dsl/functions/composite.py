from .registry import composeFunction
from .simple import ScalarWindowFunction


composeFunction(
    'sdd',
    'sd(delta(x1),window=20)',
    docs='''\
This is a shortcut function for calculating the standard deviation
of changes. Therefore:

.. math::

    {\\tt sdd}(y_t,w) = {\tt sd}({\\tt delta}(y_t),w)
''',
    description='standard deviation of changes'
)


composeFunction(
    'vol',
    '15.874*sd(delta(x1),window=20)',
    docs='''\
    a''',
    description='Annualised volatility'
)


composeFunction(
    'psdd',
    'sd(ldelta(x1),window=20)',
    docs='''\
This is a shortcut function for calculating the standard deviation
of log-changes. Therefore:

.. math::

    {\\tt sdd}(y_t,w) = {\tt sd}({\\tt ldelta}(y_t),w)
''',
    description='log standard deviation'
)


composeFunction(
    'avol',
    '15.874*sd(ldelta(x1),window=20)',
    description='annualised volatility',
    docs=('''Function for evaluating the annualized percentage
volatility of an asset. The asset price must be positive.

This function is equivalent to::

    15.874*sd(ldelta(x1),...)
''')
)

# Annualized sharpe on changes
composeFunction(
    'asharpe',
    '15.874*sharpe(delta(x1),window=20)',
    docs='''\
a''',
    description='Annualised volatility'
)

# Annualized sharpe on log-changes
composeFunction(
    'alsharpe',
    '15.874*sharpe(ldelta(x1),window=20)',
    docs='''\
a''',
    description='Annualised volatility'
)


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
