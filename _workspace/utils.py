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



SUPPLYPOLY_SETUP = r"""
A price-taking firm produces a commodity that it can sell at price $p$. The firm's cost function is:

$$ c(q) = {} $$
"""
SUPPLYPOLY_SOLUTION = r"""
The supply curve is:

$$ q = \left( \frac{p - b}{kc} \right)^{\frac{1}{k-1}} $$
"""
class SupplyPoly:
    def __init__(self, params=None):
        if not params:
            params = {'a':0,'b':0,'c':0.5,'k':2}
        params = {k:params[k] for k in ['a','b','c','k']}
        self.params = params

    def general_setup(self):
        return SUPPLYPOLY_SETUP.format(
            'a + bq + cq^k'
        )
    def general_solution(self):
        return SUPPLYPOLY_SOLUTION
    def setup(self):
        k = self.params['k']
        coefs = np.zeros(k+1)
        coefs[0] = self.params['a']
        coefs[1] = self.params['b']
        coefs[k] = self.params['c']
        return SUPPLYPOLY_SETUP.format(
            polyeq('q', coefs=coefs)
        )
    def eval(self, p):
        a = self.params['a']
        b = self.params['b']
        c = self.params['c']
        k = self.params['k']
        q = ((p-b)/(k*c))**(1/(k-1))
        profit = p*q - a - b*q - c*q**k
        producer_surplus = profit - a
        assert q>0
        assert p>b
        assert profit>0
        return {'q':q, 'profit':profit, 'producer_surplus':producer_surplus}
        

DEMANDPOLY_SETUP = r"""
A price-taking consumer with income ${}$ has utility over numeraire consumption $c$ and a commodity $q$ given by:

$$ u(c,q) = c + {} $$
"""
DEMANDPOLY_SOLUTION = r"""
The demand curve is:

$$ q = \left( \frac{a-p}{kb} \right)^{\frac{1}{k-1}} $$
"""
class DemandPoly:
    def __init__(self, params=None):
        if not params:
            params = {'a':10,'b':0.5,'k':2,'Y':100}
        params = {k:params[k] for k in ['a','b','k','Y']}
        self.params = params
        
    def general_setup(self):
        return DEMANDPOLY_SETUP.format(
            'Y','aq - bq^k'
        )
    def general_solution(self):
        return DEMANDPOLY_SOLUTION
    def setup(self):
        k = self.params['k']
        coefs = np.zeros(k+1)
        coefs[0] = 0
        coefs[1] = self.params['a']
        coefs[k] = -self.params['b']
        return DEMANDPOLY_SETUP.format(
            f"Y = {self.params['Y']:.0f}",
            polyeq('q', coefs=coefs)
        )
    def eval(self, p):
        a = self.params['a']
        b = self.params['b']
        k = self.params['k']
        Y = self.params['Y']
        q = ((a-p)/(k*b))**(1/(k-1))
        c = Y - p*q
        utility = Y - p*q + a*q - b*q**k
        consumer_surplus = utility - Y
        assert q>0
        assert c>0
        assert p<a
        return {'q':q, 'utility':utility, 'consumer_surplus':consumer_surplus}
        

DEMANDCE_SETUP = r"""
A price-taking consumer with income ${}$ has utility over numeraire consumption $c$ and a commodity $q$ given by:

$$ u(c,q) = c + {} $$
"""
DEMANDCE_SOLUTION = r"""
The demand curve is:

$$ q = \left( \frac{p}{ka} \right)^{\frac{1}{k-1}} $$
"""
class DemandCE:
    def __init__(self, params=None):
        if not params:
            params = {'numer_k':1,'denom_k':2,'a':1,'Y':100}
        params = {k:params[k] for k in ['numer_k', 'denom_k', 'a', 'Y']}
        self.params = params
        
    def general_setup(self):
        return DEMANDCE_SETUP.format(
            'Y','aq^k'
        )
    def general_solution(self):
        return DEMANDCE_SOLUTION
    def setup(self):
        numer_k = self.params['numer_k']
        denom_k = self.params['denom_k']
        a = self.params['a']
        if a==1:
            coef = ''
        else:
            coef = f"{a}"
        return DEMANDCE_SETUP.format(
            f"Y = {self.params['Y']:.0f}",
            f"{coef}q^{{ \\frac{{ {numer_k} }}{{ {denom_k} }} }}"
        )
    def eval(self, p):
        a = self.params['a']
        k = self.params['numer_k'] / self.params['denom_k']
        Y = self.params['Y']
        q = (p/(k*a))**(1/(k-1))
        c = Y - p*q
        utility = Y - p*q + a*q**k
        consumer_surplus = utility - Y
        assert q>0
        assert c>0
        return {'q':q, 'utility':utility, 'consumer_surplus':consumer_surplus}


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


LAFFER_SOLUTION = r"""
The general solutions are:

$$ p = \frac{\alpha N / M}{1 + N/M - t} $$

$$ Q = \alpha N \left( \frac{1-t}{1+N/M-t} \right) $$
"""
class Laffer:
    def __init__(self, params=None):
        if not params:
            params = {'N':400,'M':200,'alpha':15,'tp':0.5}
        params = {k:params[k] for k in ['N','M','alpha','tp']}
        self.params = params.copy()
        params['beta'] = 1
        params['gamma'] = 0
        params['delta'] = 0
        params['eta'] = 1
        params['Y'] = 100
        params['tc'] = 0
        av = AdValoremSR(params)
        sreq = SREQ(params)
        self.av = av
        self.sreq = sreq
        
        sol = {}
        sol['p'] = self.formula_p()
        sol['Q'] = self.formula_q()
        self.sol = sol
    
    def check_solution(self):
        N = self.params['N']
        M = self.params['M']
        alpha = self.params['alpha']
        return (
            ((alpha*N/M)%1 < 0.001) and
            ((alpha*N)%1 < 0.001) and
            (self.av.check_solution()) and
            (self.sreq.check_solution())
        )
    
    def general_setup(self):
        setup = SREQ_SETUP.format(
            'N', 'Y', '\\alpha q - \\tfrac{1}{2} q^2', 'M', '\\tfrac{1}{2} q^2'
        )
        setup += "An ad valorem tax rate of $t$ is placed on the producers."
        return setup
    
    def general_solution(self):
        return LAFFER_SOLUTION
    
    def setup(self):
        setup = self.sreq.setup()
        setup += "An ad valorem tax rate of $t$ is placed on the producers."
        return setup
    
    def formula_p(self):
        N = self.params['N']
        M = self.params['M']
        alpha = self.params['alpha']
        return fr"$$ p = \frac{{ {alpha*N/M:.0f} }}{{ {1+N/M:.0f} - t }} $$"
    
    def formula_q(self):
        N = self.params['N']
        M = self.params['M']
        alpha = self.params['alpha']
        return fr"$$ Q = {alpha*N:,.0f} \left( \frac{{ 1-t }}{{ {1+N/M:.0f} - t }} \right) $$"
        

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


    
CB_SETUP = r"""
A consumer with income ${}$ has a utility function over two goods, $x$ and $y$, given by:

$$ u(x,y) = x^{} y^{} $$

The price of good $x$ is ${}$ and the price of good $y$ is ${}$.
"""
CB_SOLUTION = r"""
The general solutions are:

$$ x = \frac{I}{p_x(1+b/a)} $$

$$ y = \frac{I}{p_y(1+a/b)} $$

The indifference curves are:

$$ y = \left( \frac{U}{x^a} \right)^{\frac{1}{b}} $$

The budget constraint is:

$$ y = \frac{I - p_x x}{p_y } $$
"""
class CobbDouglasConsumer:
    def __init__(self, params=None):
        if not params:
            params = {'numer_a':1,'denom_a':2,'numer_b':1,'denom_b':2,'I':100,'px':1,'py':1}

        params = {k:params[k] for k in ['numer_a','denom_a','numer_b','denom_b','I','px','py']}

        a = params['numer_a']/params['denom_a']
        b = params['numer_b']/params['denom_b']
        I = params['I']
        px = params['px']
        py = params['py']

        x = I/(px*(1+b/a))
        y = I/(py*(1+a/b))
        U = x**a * y**b

        sol = {}
        sol['x'] = x
        sol['y'] = y
        sol['U'] = U
        sol['xmax'] = params['I']/params['px']
        sol['ymax'] = params['I']/params['py']

        self.params = params
        self.sol = sol
        
    def check_solution(self):
        sol = self.sol
        return (
            (sol['x']>0) and
            (sol['y']>0) and
            (np.abs(sol['x']%1)<0.001) and
            (np.abs(sol['y']%1)<0.001) and
            (np.abs(sol['xmax']%1)<0.001) and
            (np.abs(sol['ymax']%1)<0.001)
        )
        
    def general_setup(self):
        return CB_SETUP.format(
            'I', 'a', 'b', 'p_x', 'p_y'
        ) 
    def general_solution(self):
        return CB_SOLUTION

    def setup(self):
        return CB_SETUP.format(
            f"I = {self.params['I']:.0f}", 
            f"\\tfrac{{ {self.params['numer_a']:.0f} }}{{ {self.params['denom_a']:.0f} }}",
            f"\\tfrac{{ {self.params['numer_b']:.0f} }}{{ {self.params['denom_b']:.0f} }}",
            f"p_x = {self.params['px']:.0f}", 
            f"p_y = {self.params['py']:.0f}"
        )


CBD_SETUP = r"""
A consumer has a utility function over two goods, $x$ and $y$, given by:

$$ u(x,y) = x^{} y^{} $$

In the base period, the consumer has income ${}$, the price of $x$ is ${}$, and the price of $y$ is ${}$.

In the comparison period, the price of $x$ changes to ${}$ and the price of $y$ changes to ${}$.
"""
CBD_SOLUTION = r"""
The general solutions are:

$$ \text{CPI} = \frac{1}{1+b/a} \left(\frac{p_x^\prime}{p_x}\right) + \frac{1}{1+a/b}\left(\frac{p_y^\prime}{p_y}\right) $$

$$ \text{Constant Utility Deflator} = \left(\frac{p_x^\prime}{p_x}\right)^{\frac{a}{a+b}} \left(\frac{p_y^\prime}{p_y}\right)^{\frac{b}{a+b}} $$
"""
class CobbDouglasDeflator:
    def __init__(self, params=None):
        if not params:
            params = {'numer_a':1,'denom_a':2,'numer_b':1,'denom_b':2,'I':100,'px1':1,'py1':1,'px2':1,'py2':2}

        params = {k:params[k] for k in ['numer_a','denom_a','numer_b','denom_b','I','px1','py1','px2','py2']}

        a = params['numer_a']/params['denom_a']
        b = params['numer_b']/params['denom_b']
        px1 = params['px1']
        px2 = params['px2']
        py1 = params['py1']
        py2 = params['py2']
        I = params['I']

        CPI = ((1/(1+b/a))*(px2/px1) + (1/(1+a/b))*(py2/py1)) * 100
        CONST_UTIL_DEFLATOR = ((px2/px1)**(a/(a+b))*(py2/py1)**(b/(a+b))) * 100

        # Base period
        params1 = params.copy()
        params1['px'] = params['px1']
        params1['py'] = params['py1']
        cb1 = CobbDouglasConsumer(params1)

        # Comparison period without COLA
        params2_no_cola = params.copy()
        params2_no_cola['px'] = params['px2']
        params2_no_cola['py'] = params['py2']
        cb2_no_cola = CobbDouglasConsumer(params2_no_cola)

        # Comparison period with CPI colas
        params2_cpi = params2_no_cola.copy()
        params2_cpi['I'] = params['I'] * CPI/100
        cb2_cpi = CobbDouglasConsumer(params2_cpi)

        # Comparison period with constant utility cola
        params2_cons = params2_no_cola.copy()
        params2_cons['I'] = params['I'] * CONST_UTIL_DEFLATOR/100
        cb2_cons = CobbDouglasConsumer(params2_cons)

        assert np.abs( (cb1.sol['x']*px2 + cb1.sol['y']*py2)/(cb1.sol['x']*px1 + cb1.sol['y']*py1) - CPI/100) < 0.001
        assert np.abs( cb1.sol['U'] - cb2_cons.sol['U'] ) < 0.001

        self.params = params
        self.cb1 = cb1
        self.cb2_no_colas = cb2_no_cola
        self.cb2_cpi = cb2_cpi
        self.cb2_cons = cb2_cons

        sol = {}
        sol['CPI'] = CPI
        sol['CONST_UTIL_DEFLATOR'] = CONST_UTIL_DEFLATOR
        self.sol = sol

    def check_solution(self):
        return (
            self.cb1.check_solution() and
            (np.abs(self.cb1.sol['U']%1)<0.001)
        )

    def general_setup(self):
        return CBD_SETUP.format(
            'a', 'b', 'I', 'p_x', 'p_y', 'p_x^\\prime', 'p_y^\\prime'
        ) 
    def general_solution(self):
        return CBD_SOLUTION

    def setup(self):
        return CBD_SETUP.format(
            f"\\tfrac{{ {self.params['numer_a']:.0f} }}{{ {self.params['denom_a']:.0f} }}",
            f"\\tfrac{{ {self.params['numer_b']:.0f} }}{{ {self.params['denom_b']:.0f} }}",
            f"I = {self.params['I']:.0f}", 
            f"p_x = {self.params['px1']:.0f}", 
            f"p_y = {self.params['py1']:.0f}",
            f"p_x^\\prime = {self.params['px2']:.0f}", 
            f"p_y^\\prime = {self.params['py2']:.0f}",
        )
        
