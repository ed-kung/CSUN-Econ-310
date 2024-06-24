import numpy as np
import pandas as pd

def polyeq(var='x', coefs=[1,1,1], remove_first_plus_minus=True):
    t = ''
    for p in range(len(coefs)):
        c = coefs[p]
        if c!=0:
            if c>0:
                t+='+ '
            else:
                t+='- '
            if p==0:
                t+=f'{np.abs(c):g} '
            else:
                if np.abs(c)!=1:
                    t+=f'{np.abs(c):g}'
                if p==1:
                    t+=f'{var} '
                else:
                    t+=f'{var}^{p}'
    if remove_first_plus_minus:
        return t[2:]
    else:
        return t

def select_rows(df, params):
    idx = True
    for k, v in params.items():
        idx = (idx) & (df[k]==v)
    return df.loc[idx]


SREQ_SETUP = r"""
A commodity $q$ is traded at price $p$ in a competitive market with price-taking consumers and firms. \\
        
There are ${}$ identical consumers each with income ${}$. Each consumer has a utility function over numeraire consumption $c$ and commodity $q$ given by:

$$u(c,q) = c + {}$$

There are ${}$ identical firms each with cost function given by:

$$c(q) = {}$$

"""
SREQ_SOLUTION = r"""
The general solutions are:

$$Q = \frac{\alpha - \delta}{\beta/N + \eta/M}$$

$$p = \frac{N \eta \alpha + M \beta \delta}{N \eta + M \beta}$$
"""
class SREQ:
    def __init__(self, params=None):
        if not params:
            params = {'N':3000, 'M':200, 'Y':100, 'alpha':10, 'beta':2, 'gamma':0, 'delta':0, 'eta':0.2}

        params = {k:params[k] for k in ['N','M','Y','alpha','beta','gamma','delta','eta']}
        
        N = params['N']
        M = params['M']
        Y = params['Y']
        alpha = params['alpha']
        beta = params['beta']
        gamma = params['gamma']
        delta = params['delta']
        eta = params['eta']
        
        Q = (alpha - delta)/(beta/N + eta/M)
        p = (N*eta*alpha + M*beta*delta)/(N*eta + M*beta)

        sol = {}
        sol['Q'] = Q
        sol['p'] = p
        sol['qd'] = Q/N
        sol['qs'] = Q/M
        sol['c'] = Y - p*sol['qd']
        sol['revenue'] = p*sol['qs']
        sol['cost'] = gamma + delta*sol['qs'] + 0.5*eta*sol['qs']**2
        sol['profit'] = sol['revenue'] - sol['cost']
        sol['total_profit'] = M*sol['profit']
        sol['utility'] = sol['c'] + alpha * sol['qd'] - 0.5 * beta * sol['qd']**2
        sol['total_utility'] = N*sol['utility']
        sol['total_surplus'] = sol['total_profit'] + sol['total_utility']

        self.params = params
        self.sol = sol
        
    def check_solution(self):
        sol = self.sol
        return (
            (sol['c']>0) and
            (sol['qd']>0) and
            (sol['qs']>0) and
            (sol['p']>0) and
            (np.abs(sol['p']%1)<0.001) and
            (np.abs(sol['qd']%1)<0.001) and
            (np.abs(sol['qs']%1)<0.001)
        )

    def general_setup(self):
        return SREQ_SETUP.format(
            'N', 'Y', '\\alpha q - \\tfrac{1}{2} \\beta q^2', 'M', '\\gamma + \\delta q + \\tfrac{1}{2} \\eta q^2'
        ) 
    def general_solution(self):
        return SREQ_SOLUTION
        
    def setup(self):
        return SREQ_SETUP.format(
            f"{self.params['N']:,.0f}", 
            f"Y={self.params['Y']:,.0f}",
            polyeq('q', [0, self.params['alpha'], -0.5*self.params['beta']]),
            f"{self.params['M']:,.0f}",
            polyeq('q', [self.params['gamma'], self.params['delta'], 0.5*self.params['eta']])
        )



ADVALOREMSR_SOLUTION = r"""
The general solutions are:

$$Q = \frac{(1-t_p)\alpha - (1+t_c)\delta}{(1-t_p)\beta/N + (1+t_c)\eta/M}$$

$$p = \frac{N \eta \alpha + M \beta \delta}{(1+t_c) N \eta + (1-t_p) M \beta}$$
"""
class AdValoremSR:
    def __init__(self, params=None):
        if not params:
            params = {'N':3000, 'M':200, 'Y':100, 'alpha':10, 'beta':2, 'gamma':0, 'delta':0, 'eta':0.2, 'tc':0.1, 'tp':0}

        params = {k:params[k] for k in ['N','M','Y','alpha','beta','gamma','delta','eta','tc','tp']}

        no_tax = SREQ(params)
        
        N = params['N']
        M = params['M']
        Y = params['Y']
        alpha = params['alpha']
        beta = params['beta']
        gamma = params['gamma']
        delta = params['delta']
        eta = params['eta']
        tc = params['tc']
        tp = params['tp']

        Q = ((1-tp)*alpha - (1+tc)*delta)/((1+tc)*eta/M + (1-tp)*beta/N)
        p = (N*eta*alpha + M*beta*delta)/(N*eta*(1+tc) + M*beta*(1-tp))
        
        sol = {}
        sol['Q'] = Q
        sol['p'] = p
        sol['qd'] = Q/N
        sol['qs'] = Q/M
        sol['c'] = Y - (1+tc)*p*sol['qd']
        sol['revenue'] = (1-tp)*p*sol['qs']
        sol['cost'] = gamma + delta*sol['qs'] + 0.5*eta*sol['qs']**2
        sol['profit'] = sol['revenue'] - sol['cost']
        sol['total_profit'] = M*sol['profit']
        sol['utility'] = sol['c'] + alpha * sol['qd'] - 0.5 * beta * sol['qd']**2
        sol['total_utility'] = N*sol['utility']
        sol['tax_revenue'] = (tc+tp)*p*Q
        sol['total_surplus'] = sol['total_profit'] + sol['total_utility'] + sol['tax_revenue']
        sol['DWL'] = no_tax.sol['total_surplus'] - sol['total_surplus']

        self.params = params
        self.sol = sol
        self.no_tax = no_tax

        lumpsum_params = params.copy()
        lumpsum_params['Y'] = params['Y'] - sol['tax_revenue']/params['N']
        lumpsum = SREQ(lumpsum_params)
        lumpsum.sol['tax_revenue'] = sol['tax_revenue']
        lumpsum.sol['total_surplus'] = lumpsum.sol['total_profit'] + lumpsum.sol['total_utility'] + lumpsum.sol['tax_revenue']

        self.lump_sum = lumpsum

    def check_solution(self):
        return (
            (self.sol['c']>0) and
            (self.sol['p']>0) and
            (self.sol['qd']>0) and
            (self.sol['qs']>0) and
            (np.abs(self.sol['p']%1)<0.0001) and
            (np.abs(self.sol['qd']%1)<0.0001) and
            (np.abs(self.sol['qs']%1)<0.0001) and
            (self.no_tax.check_solution())
        )

    def general_setup(self):
        t = self.no_tax.general_setup()
        t+= r"An ad-valorem tax rate of $t_c$ is placed on the consumers and an ad-valorem tax rate of $t_p$ is placed on the producers."
        return t

    def general_solution(self):
        return ADVALOREMSR_SOLUTION

    def setup(self):
        t = self.no_tax.setup()
        if self.params['tc']>0:
            t+= r"An ad-valorem tax rate of ${}\%$ is placed on the consumers. ".format(f"{self.params['tc']*100:g}")
        if self.params['tp']>0:
            t+= r"An ad-valorem tax rate of ${}\%$ is placed on the producers. ".format(f"{self.params['tp']*100:g}")
        return t




LREQ_SETUP = r"""
A commodity $q$ is traded at price $p$ in a competitive market with price-taking consumers and firms. \\
        
There are ${}$ identical consumers each with income ${}$. Each consumer has a utility function over numeraire consumption $c$ and commodity $q$ given by:

$$u(c,q) = c + {}$$

There are ${}$ identical firms each with cost function given by:

$$c(q) = {}$$

The number of firms is fixed in the short run, but in the long run firms can freely enter or exit the market. Thus, the number of firms is flexible in the long run.
"""
LREQ_SOLUTION = r"""
The general solutions are:

$$q_s = \sqrt{2\gamma / \eta}$$

$$p = \delta + \eta q_s$$

$$q_d = \frac{\alpha - p}{\beta}$$
"""
class LREQ:
    def __init__(self, params=None):
        if not params:
            params = {'N':3000, 'Y':100, 'alpha':10, 'beta':1, 'gamma':32, 'delta':0, 'eta':1}
            
        params = {k:params[k] for k in ['N','Y','alpha','beta','gamma','delta','eta']}

        N = params['N']
        Y = params['Y']
        alpha = params['alpha']
        beta = params['beta']
        gamma = params['gamma']
        delta = params['delta']
        eta = params['eta']

        qs = np.sqrt(2*gamma/eta)
        p = delta + eta*qs
        qd = (alpha - p)/beta
        Q = N*qd
        M = Q/qs
        
        sol = {}
        sol['Q'] = Q
        sol['p'] = p
        sol['qd'] = qd
        sol['qs'] = qs
        sol['M'] = M
        sol['c'] = Y - p*sol['qd']
        sol['revenue'] = p*sol['qs']
        sol['cost'] = gamma + delta*sol['qs'] + 0.5*eta*sol['qs']**2
        sol['profit'] = sol['revenue'] - sol['cost']
        sol['total_profit'] = M*sol['profit']
        sol['utility'] = sol['c'] + alpha * sol['qd'] - 0.5 * beta * sol['qd']**2
        sol['total_utility'] = N*sol['utility']
        sol['total_surplus'] = sol['total_profit'] + sol['total_utility']

        self.params = params
        self.sol = sol
    
    def check_solution(self):
        sol = self.sol
        return (
            (sol['c']>0) and
            (sol['qd']>0) and
            (sol['qs']>0) and
            (sol['p']>0) and
            (np.abs(sol['p']%1)<0.001) and
            (np.abs(sol['qd']%1)<0.001) and
            (np.abs(sol['qs']%1)<0.001) and
            (np.abs(sol['M']%1)<0.001)
        )

    def general_setup(self):
        return LREQ_SETUP.format(
            'N', 'Y', '\\alpha q - \\tfrac{1}{2} \\beta q^2', 'M', '\\gamma + \\delta q + \\tfrac{1}{2} \\eta q^2'
        ) 
    def general_solution(self):
        return LREQ_SOLUTION
        
    def setup(self):
        return LREQ_SETUP.format(
            f"{self.params['N']:,.0f}", 
            f"Y={self.params['Y']:,.0f}",
            polyeq('q', [0, self.params['alpha'], -0.5*self.params['beta']]),
            "M",
            polyeq('q', [self.params['gamma'], self.params['delta'], 0.5*self.params['eta']])
        )

class CobbDouglasConsumer:
    def __init__(self,a=0.5,b=0.5,px=1,py=1,I=100):
        
        x = I/(px*(1+b/a))
        y = I/(py*(1+a/b))
        
        xmax = I/px
        ymax = I/py
        
        U = x**a * y**b
        
        self.a=a
        self.b=b
        self.px=px
        self.py=py
        self.I=I
        self.x=x
        self.y=y
        self.xmax=xmax
        self.ymax=ymax
        self.U = U
    
    def __repr__(self):
        return repr({
            'a': self.a,
            'b': self.b,
            'px': self.px, 
            'py': self.py,
            'I': self.I,
            'x': self.x,
            'y': self.y,
            'xmax': self.xmax,
            'ymax': self.ymax,
            'U': self.U
        })
    
    def is_integer(self):
        return (
            (self.x%1==0) and
            (self.y%1==0) and
            (self.xmax%1==0) and
            (self.ymax%1==0)
        )

class CobbDouglasDeflator:
    def __init__(self,a,b,I,px0,py0,px1,py1):
        CPI_DEFLATOR = (1/(1+b/a))*(px1/px0) + (1/(1+a/b))*(py1/py0)
        GOOD_DEFLATOR = (px1/px0)**(a/(a+b)) * (py1/py0)**(b/(a+b))
        
        cb0 = CobbDouglasConsumer(a=a,b=b,I=I,px=px0,py=py0)
        cb1 = CobbDouglasConsumer(a=a,b=b,I=I*GOOD_DEFLATOR,px=px1,py=py1)

        assert np.abs(CPI_DEFLATOR - (px1*cb0.x+py1*cb0.y)/(px0*cb0.x+py0*cb0.y))<0.0001
        assert np.abs(cb0.U - cb1.U)<0.0001

        self.a = a
        self.b = b
        self.I = I
        self.px0 = px0
        self.py0 = py0
        self.px1 = px1
        self.py1 = py1
        self.CPI_DEFLATOR = CPI_DEFLATOR
        self.GOOD_DEFLATOR = GOOD_DEFLATOR
        self.cb0 = cb0
        self.cb1 = cb1

    def __repr__(self):
        return repr({
            'a': self.a,
            'b': self.b,
            'I': self.I,
            'px0': self.px0,
            'py0': self.py0,
            'px1': self.px1,
            'py1': self.py1,
            'CPI_DEFLATOR': self.CPI_DEFLATOR,
            'GOOD_DEFLATOR': self.GOOD_DEFLATOR
        })

    def is_integer(self):
        return (
            (self.cb0.x%1==0) and
            (self.cb0.y%1==0) 
        )

