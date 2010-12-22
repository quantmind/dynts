from jflow.lib import tablefunction
from .data import qpqn

__all__ = ['qp','qn','calmar','calmarnorm']

qn = tablefunction('qn',qpqn.qn)
qp = tablefunction('qp',qpqn.qp)

def calmar(sharpe, T = 1.0):
    '''
    Calculate the Calmar ratio for a Weiner process
    
    @param sharpe:    Annualized Sharpe ratio
    @param T:         Time interval in years
    '''
    x = 0.5*T*sharpe*sharpe
    return x/qp(x)


def calmarnorm(sharpe, T, tau = 1.0):
    '''
    Multiplicator for normalizing calmar ratio to period tau
    '''
    return calmar(sharpe,tau)/calmar(sharpe,T)