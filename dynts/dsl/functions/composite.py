from dynts.dsl import ComposeFunction
from .simple import ScalarWindowFunction


ComposeFunction('sdd','sd(delta(x1),window=20)')
ComposeFunction('asdd','15.874*sd(delta(x1),window=20)')
ComposeFunction('sdld','sd(ldelta(x1),window=20)')
ComposeFunction('avol','15.874*sd(ldelta(x1),window=20)')

# Annualized sharpe on changes
ComposeFunction('asharpe','15.874*sharpe(delta(x1),window=20)')
# Annualized sharpe on log-changes
ComposeFunction('alsharpe','15.874*sharpe(ldelta(x1),window=20)')


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