import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

SMALL_SIZE = 14
MEDIUM_SIZE = 16
LARGE_SIZE = 18
HUGE_SIZE = 20

plt.rcdefaults()
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'Helvetica'
plt.rcParams['font.size'] = MEDIUM_SIZE
plt.rcParams['axes.titlesize'] = LARGE_SIZE
plt.rcParams['axes.labelsize'] = MEDIUM_SIZE
plt.rcParams['xtick.labelsize'] = MEDIUM_SIZE
plt.rcParams['ytick.labelsize'] = MEDIUM_SIZE
plt.rcParams['legend.fontsize'] = MEDIUM_SIZE
plt.rcParams['figure.titlesize'] = LARGE_SIZE
plt.rcParams['figure.figsize'] = [7.2, 7.2]
plt.rcParams['figure.dpi'] = 60
plt.rcParams['figure.facecolor'] = (1.0, 1.0, 1.0, 0.0)


def is_divisible(a,b):
    return (np.abs(a/b - np.round(a/b))<0.0001)

class Number:
    def __init__(self, n, d=1):
        self.v = n/d
        if is_divisible(n,1) and is_divisible(d,1):
            gcd = np.gcd(int(n),int(d))
            self.n = n/gcd
            self.d = d/gcd
        elif is_divisible(n,d):
            self.n = n/d
            self.d = 1
        elif is_divisible(d,n):
            self.n = 1
            self.d = d/n
        elif d<1:
            self.n = n/d
            self.d = 1
        else:
            self.n = n
            self.d = d
    def as_decimal(self,rmplus=False):
        t=''
        if self.v<0:
            t+='-'
        else:
            t+='+'
        t+=f'{self.v:g}'
        if rmplus and t[0]=='+':
            t=t[1:]
        return t
    def as_frac(self, inline=True, rmplus=False):
        t=''
        if self.v<0:
            t+='-'
        else:
            t+='+'
        if is_divisible(self.v, 1):
            t+=f'{np.abs(self.v):.0f}'
        elif self.d==1:
            t+=f'{np.abs(self.v):g}'
        else:
            if inline:
                t+=f'{np.abs(self.n):g} / {np.abs(self.d):g}'
            else:
                t+=fr'\frac{{ {np.abs(self.n):g} }}{{ {np.abs(self.d):g} }}'
        if rmplus and t[0]=='+':
            t=t[1:]
        return t

def print_exponentiated_numbers(x,y):
    if type(x)!=Number:
        x = Number(x)
    if type(y)!=Number:
        y = Number(y)
    if y.v==1:
        return x.as_frac(inline=False,rmplus=True)
    if y.v==-1:
        return Number(x.d, x.n).as_frac(inline=False,rmplus=True)
    if x.v==1:
        return '1'
    if x.v==0:
        return '0'
    if y.v==0:
        return '1'
    if is_divisible(x.v**y.v,1):
        return fr"{x.v**y.v:g}"
    if x.v>0 and is_divisible(x.v,1):
        return fr"{x.v:g}^{{ {y.as_frac(inline=True,rmplus=True)} }}"
    else:
        return fr"\left( {x.as_frac(inline=False,rmplus=True)} \right)^{{ {y.as_frac(inline=True,rmplus=True)} }}"

def term(c,x,p,asfrac=True,rmplus=False):
    if type(c)!=Number:
        c = Number(c)
    if type(p)!=Number:
        p = Number(p)
    if asfrac:
        cstr = c.as_frac(inline=False,rmplus=False)
        pstr = p.as_frac(inline=True,rmplus=True)
    else:
        cstr = c.as_decimal(rmplus=False)
        pstr = p.as_decimal(rmplus=True)
    t=''
    if c.v==0:
        return ''
    if p.v==0:
        t+=cstr
    elif p.v==1:
        if c.v==1:
            t+=f"+{x}"
        elif c.v==-1:
            t+=f"-{x}"
        else:
            t+=f"{cstr}{x}"
    else:
        if c.v==1:
            t+=fr"+{x}^{{ {pstr} }}"
        elif c.v==-1:
            t+=fr"-{x}^{{ {pstr} }}"
        else:
            t+=fr"{cstr}{x}^{{ {pstr} }}"
    if rmplus and t[0]=='+':
        t = t[1:]
    return t
    
def polyeq(var='x', coefs=[1,1,1], powers=[0,1,2], rmplus=True):
    t = ''
    for i in range(len(coefs)):
        c = coefs[i]
        p = powers[i]
        t+=term(c,var,p,asfrac=True,rmplus=False)
    if rmplus and t[0]=='+':
        return t[1:]
    return t

def cbeq(A=1,x='x',a=Number(1,2),y='y',b=Number(1,2)):
    if a.v==0 and b.v==0:
        return f'{A:g}'
    elif a.v==0:
        return term(A,y,b,asfrac=True,rmplus=True)
    elif b.v==0:
        return term(A,x,a,asfrac=True,rmplus=True)
    else:
        return term(A,x,a,asfrac=True,rmplus=True) + term(1,y,b,asfrac=True,rmplus=True)

def get_random_prob(ProbClass, CsvFile):
    df = pd.read_csv(CsvFile)
    params = dict(df.sample(1).reset_index(drop=True).loc[0])
    return ProbClass(params)


"""
Linear Supply and Demand
"""
class LinearSD:
    def __init__(self, params=None):
        if not params:
            params = {'a':120,'b':1,'c':2,'d':30}
        params = {k:params[k] for k in ['a','b','c','d']}
        a,b,c,d = params['a'],params['b'],params['c'],params['d']
        p = (a+d)/(b+c)
        q = a - b*p
        sol = {'p':p, 'q':q}
        self.params = params
        self.sol = sol
    def general_setup(self):
        return fr"""
Supply and demand are given by the following equations:

$$\begin{{align}}
q_d &= a - bp \\
q_s &= cp - d
\end{{align}}$$

The general solution is:

$$p = \frac{{ a+d }}{{ b + c }}$$
"""
    def setup(self):
        params = self.params
        a,b,c,d = params['a'],params['b'],params['c'],params['d']
        deq = polyeq('p',[a,-b],[0,1])
        seq = polyeq('p',[c,-d],[1,0])
        return fr"""
Supply and demand are given by the following equations:

$$\begin{{align}}
q_d &= {deq} \\
q_s &= {seq}
\end{{align}}$$
"""
    def check_solution(self):
        p, q = self.sol['p'], self.sol['q']
        return (
            (is_divisible(p,1)) and
            (is_divisible(q,1)) and
            (p>0) and (q>0)
        )


"""
Constant Elasticity Supply and Demand
"""
class CESSD:
    def __init__(self, params=None):
        if not params:
            params = {'A':120,'B':60,'a':1,'b':2,'d':3}
        params = {k:params[k] for k in ['A','B','a','b','d']}
        A,B,a,b,d = params['A'],params['B'],params['a'],params['b'],params['d']
        self.params = params
        p = (A/B)**(d/(a+b))
        q = A*p**(-a/d)
        self.sol = {'p':p, 'q':q}
    def general_setup(self):
        return fr"""
Supply and demand are given by the following equations:

$$\begin{{align}}
q_d &= Ap^{{ -a/d }}  \\
q_s &= Bp^{{ b/d }}
\end{{align}}$$

The general solution is:

$$p = \left( \frac{{A}}{{B}} \right)^{{ \frac{{d}}{{a+b}} }}$$
"""
    def setup(self):
        params = self.params
        A,B,a,b,d = params['A'],params['B'],params['a'],params['b'],params['d']
        return fr"""
Supply and demand are given by the following equations:

$$\begin{{align}}
q_d &= {term(A,'p',Number(-a,d),rmplus=True)}  \\
q_s &= {term(B,'p',Number(b,d),rmplus=True)}
\end{{align}}$$
"""
    def check_solution(self):
        params = self.params
        A,B,a,b,d = params['A'],params['B'],params['a'],params['b'],params['d']
        p,q = self.sol['p'], self.sol['q']
        return (
            (is_divisible(A/B,1)) and
            (p>0.1) and (q>0.1)
        )


"""
Simply Cobb Douglas
"""
class SimplifyCB:
    def __init__(self, params=None):
        if not params:
            params = {'A':4,'B':12,'D':3,'a':1,'b':-2,'c':-2,'d':1}
        params = {k:params[k] for k in ['A','B','D','a','b','c','d']}
        A,B,D,a,b,c,d = params['A'],params['B'],params['D'],params['a'],params['b'],params['c'],params['d']
        C = Number(A,B)
        numerC = C.n
        denomC = C.d
        xp = a-c
        yp = b-d
        numer = ''
        denom = ''
        if numerC>1:
            numer += term(numerC,'',0,rmplus=True)
        if denomC>1:
            denom += term(denomC,'',0,rmplus=True)
        if xp>0:
            numer += term(1,'x',Number(xp,D),rmplus=True)
        elif xp<0:
            denom += term(1,'x',Number(np.abs(xp),D),rmplus=True)
        if yp>0:
            numer += term(1,'y',Number(yp,D),rmplus=True)
        elif yp<0:
            denom += term(1,'y',Number(np.abs(yp),D),rmplus=True)
        sol = {'numerC':numerC,'denomC':denomC,'xp':xp,'yp':yp}
        self.numer = numer
        self.denom = denom
        self.params = params
        self.sol = sol
    def general_setup(self):
        return fr"""
Simplify:

$$ \frac{{ Ax^{{a/D}}y^{{b/D}} }}{{ Bx^{{c/D}}y^{{d/D}} }} $$
"""
    def setup(self):
        params = self.params
        A,B,D,a,b,c,d = params['A'],params['B'],params['D'],params['a'],params['b'],params['c'],params['d']
        return fr"""
Simplify:

$$ \frac{{ {cbeq(A,'x',Number(a,D),'y',Number(b,D))} }}{{ {cbeq(B,'x',Number(c,D),'y',Number(d,D))} }} $$
"""
    def check_solution(self):
        params = self.params
        A,B,D,a,b,c,d = params['A'],params['B'],params['D'],params['a'],params['b'],params['c'],params['d']
        return (
            (is_divisible(A,1)) and
            (is_divisible(B,1)) and
            ((a==0)+(b==0)+(c==0)+(d==0)<=1)
        )
    def solution(self):
        if len(self.denom)==0:
            return fr"$$ {self.numer} $$"
        elif len(self.numer)==0:
            return fr"$$ \frac{{1}}{{ {self.denom} }} $$"
        else:
            return fr"$$ \frac{{ {self.numer} }}{{ {self.denom} }} $$"

        
"""
Cobb Douglas Indifference Curve
"""
class CobbDouglasIC:
    def __init__(self, params=None):
        if not params:
            params = {'A':1,'x':'x','a':1,'b':2,'y':'y','c':1,'d':2,'U':2}
        params = {k:params[k] for k in ['A','x','a','b','y','c','d','U']}
        A,x,a,b,y,c,d,U=params['A'],params['x'],params['a'],params['b'],params['y'],params['c'],params['d'],params['U']
        self.params = params
    def general_setup(self):
        return fr"""
A consumer has utility function over goods \(x\) and \(y\) given by:

$$ u(x,y) = Ax^{{a/b}}y^{{c/d}} $$

Find the indifference curve with \( u(x,y) = U \).

Solution:

$$ y = \left( \frac{{U}}{{A}} \right)^{{d/c}} x^{{ -\frac{{ ad }}{{ bc }} }}  $$
"""
    def setup(self):
        params = self.params
        A,x,a,b,y,c,d,U=params['A'],params['x'],params['a'],params['b'],params['y'],params['c'],params['d'],params['U']
        return fr"""
A consumer has utility function over goods \({x}\) and \({y}\) given by:

$$ u({x},{y}) = {cbeq(A,x,a,b,y,c,d)} $$

Find the indifference curve with \( u({x},{y}) = {U} \).
"""
    def solution(self):
        params = self.params
        A,x,a,b,y,c,d,U=params['A'],params['x'],params['a'],params['b'],params['y'],params['c'],params['d'],params['U']
        if U/A==1:
            cons = ''
        else:
            cons = print_exponentiated_numbers(Number(U,A), Number(d,c))
        return fr"$$ y = {cons}{term(1,x,Number(-a*d,b*c),rmplus=True)} $$"
    def check_solution(self):
        params = self.params
        A,x,a,b,y,c,d,U=params['A'],params['x'],params['a'],params['b'],params['y'],params['c'],params['d'],params['U']
        return (
            (a>0) and (b>0) and (c>0) and (d>0)
        )



"""
Supply Curve from Polynomial Cost Function
"""
class SupplyPoly:
    def __init__(self, params=None):
        if not params:
            params = {'a':0,'b':0,'c':0.5,'k':2,'M':1}
        params = {k:params[k] for k in ['a','b','c','k','M']}
        self.params = params
    def general_setup(self):
        return fr"""
There are \(M\) identical, price-taking firms that can produce a commodity which sells at price \(p\). Each firm's cost function is:

$$ c(q) = a + bq + cq^k $$

The supply curve is:

$$ Q = M \left( \frac{{ p - b }}{{ kc }} \right)^{{ \frac{{1}}{{k-1}} }} $$
"""
    def setup(self):
        params = self.params
        a,b,c,k,M = params['a'],params['b'],params['c'],params['k'],params['M']
        cost_function = polyeq('q',[a,b,c],[0,1,k])
        if self.params['M']==1:
            return fr"""
A price-taking firm produces a commodity that sells at price \(p\). The firm's cost function is:

$$ c(q) = {cost_function} $$
"""
        else:
            return fr"""
There are \({M:g}\) identical, price-taking firms that can produce a commodity which sells at price \(p\). Each firm's cost function is:

$$ c(q) = {cost_function} $$
"""
    def solution(self):
        params = self.params
        a,b,c,k,M = params['a'],params['b'],params['c'],params['k'],params['M']
        
        c = Number(c,1)
        kc = Number(k*c.n, c.d)
        
        if kc.v==1:
            inner_equation = polyeq('p',[1,-b],[1,0])
        elif is_divisible(kc.v, 1):
            inner_equation = fr"\frac{{ {polyeq('p',[1,-b],[1,0])} }}{{ {kc.v:g} }}"
        else:
            inner_equation = fr"\frac{{ {polyeq('p',[c.d,-b*c.d],[1,0])} }}{{ {k*c.n:g} }}"
        if M>1:
            if k==2:
                return fr" {M:g} \left( {inner_equation} \right) "
            else:
                return fr" {M:g} \left( {inner_equation} \right)^{{ 1/{k-1:g} }}"
        if M==1:
            if k==2:
                return inner_equation
            else:
                return fr" \left( {inner_equation} \right)^{{ 1/{k-1:g} }}"
    def eval(self, p):
        params = self.params
        a,b,c,k,M = params['a'],params['b'],params['c'],params['k'],params['M']
        q = ((p-b)/(k*c))**(1/(k-1))
        Q = M*q
        profit = p*q - a - b*q - c*q**k
        total_profit = M*profit
        return {'p':p, 'q':q, 'Q':Q, 'profit':profit, 'total_profit':total_profit}

    
"""
Demand Curve from Polynomial Utility
"""
class DemandPoly:
    def __init__(self, params=None):
        if not params:
            params = {'Y':100,'a':10,'b':0.5,'k':2,'N':1}
        params = {k:params[k] for k in ['Y','a','b','k','N']}
        self.params = params
    def general_setup(self):
        return fr"""
There are \(N\) identical, price-taking consumers with income \(Y\). Each consumer has utility over numeraire consumption \(c\) and a commodity \(q\) given by:

$$ u(c,q) = c + aq - bq^k $$

The demand curve is:

$$ q = \left( \frac{{ a - p }}{{ kb }} \right)^{{ \frac{{1}}{{k-1}} }} $$
"""
    def setup(self):
        params = self.params
        Y,a,b,k,N = params['Y'],params['a'],params['b'],params['k'],params['N']
        utility_function = polyeq('q',[a,-b],[1,k])
        if self.params['N']==1:
            return fr"""
A price-taking consumer with income \(Y={Y:g}\) has utility over numeraire consumption \(c\) and a commodity \(q\) given by:

$$ u(c,q) = c + {utility_function} $$
"""
        else:
            return fr"""
There are \({N:g}\) identical, price-taking consumers with income \(Y={Y:g}\). Each consumer has utility over numeraire consumption \(c\) and a commodity \(q\) given by:

$$ u(c,q) = c + {utility_function} $$
"""
    def solution(self):
        params = self.params
        Y,a,b,k,N = params['Y'],params['a'],params['b'],params['k'],params['N']
        
        b = Number(b,1)
        kb = Number(k*b.n, b.d)
        
        if kb.v==1:
            inner_equation = polyeq('p',[a,-1],[0,1])
        elif is_divisible(kb.v, 1):
            inner_equation = fr"\frac{{ {polyeq('p',[a,-1],[0,1])} }}{{ {kb.v:g} }}"
        else:
            inner_equation = fr"\frac{{ {polyeq('p',[a*b.d, -b.d],[0,1])} }}{{ {k*b.n:g} }}"
        if N>1:
            if k==2:
                return fr" {N:g} \left( {inner_equation} \right) "
            else:
                return fr" {N:g} \left( {inner_equation} \right)^{{ 1/{k-1:g} }}"
        if N==1:
            if k==2:
                return inner_equation
            else:
                return fr" \left( {inner_equation} \right)^{{ 1/{k-1:g} }}"
    def eval(self, p):
        params = self.params
        Y,a,b,k,N = params['Y'],params['a'],params['b'],params['k'],params['N']
        q = ((a-p)/(k*b))**(1/(k-1))
        Q = N*q
        utility = Y - p*q + a*q - b*q**k
        total_utility = N*utility
        c = Y - p*q
        return {'p':p, 'q':q, 'Q':Q, 'utility':utility, 'total_utility':total_utility, 'c':c}
    
    
"""
Demand Curve with Constant Elasticity
"""
class DemandCE:
    def __init__(self, params=None):
        if not params:
            params = {'Y':100,'a':1,'kn':1,'kd':2,'N':1}
        params = {k:params[k] for k in ['Y','a','kn','kd','N']}
        self.params = params
    def general_setup(self):
        return fr"""
There are \(N\) identical, price-taking consumers with income \(Y\). Each consumer has utility over numeraire consumption \(c\) and a commodity \(q\) given by:

$$ u(c,q) = c + aq^{{ \frac{{ kn }}{{ kd }} }} $$

The demand curve is:

$$ q = \left( \frac{{ kd }}{{ kn \cdot a }} p \right)^{{ \frac{{kd}}{{kn - kd}} }} $$
"""
    def setup(self):
        params = self.params
        Y,a,kn,kd,N = params['Y'],params['a'],params['kn'],params['kd'],params['N']
        utility_function = term(a,'q',Number(kn,kd),rmplus=True)
        if self.params['N']==1:
            return fr"""
A price-taking consumer with income \(Y={Y:g}\) has utility over numeraire consumption \(c\) and a commodity \(q\) given by:

$$ u(c,q) = c + {utility_function} $$
"""
        else:
            return fr"""
There are \({N:g}\) identical, price-taking consumers with income \(Y={Y:g}\). Each consumer has utility over numeraire consumption \(c\) and a commodity \(q\) given by:

$$ u(c,q) = c + {utility_function} $$
"""
    def solution(self):
        params = self.params
        Y,a,kn,kd,N = params['Y'],params['a'],params['kn'],params['kd'],params['N']
        
        inner_equation = polyeq('p',[Number(kd,kn*a)],[1])
        
        if N>1:
            if kd/(kn*a)==1:
                return fr"{N:g} p^{{ {Number(kd,kn-kd).as_frac(inline=True,rmplus=True)} }}"
            else:
                return fr"{N:g} \left( {Number(kd,kn*a).as_frac(inline=False,rmplus=True)} p \right)^{{ {Number(kd,kn-kd).as_frac(inline=True,rmplus=True)} }}"
        else:
            if kd/(kn*a)==1:
                return fr"p^{{ {Number(kd,kn-kd).as_frac(inline=True,rmplus=True)} }}"
            else:
                return fr"\left( {Number(kd,kn*a).as_frac(inline=False,rmplus=True)} p \right)^{{ {Number(kd,kn-kd).as_frac(inline=True,rmplus=True)} }}"
    def eval(self, p):
        params = self.params
        Y,a,kn,kd,N = params['Y'],params['a'],params['kn'],params['kd'],params['N']
        q = ((kd/(kn*a))*p)**(kd/(kn-kd))
        Q = N*q
        utility = Y - p*q + a*q**(kn/kd)
        total_utility = N*utility
        c = Y - p*q
        return {'p':p, 'q':q, 'Q':Q, 'utility':utility, 'total_utility':total_utility, 'c':c}
    

"""
Short Run Equilibrium
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
    def general_setup(self):
        return fr"""
A commodity \(q\) is traded at price \(p\) in a competitive market with price-taking consumers and firms. \\
        
There are \(N\) identical consumers each with income \(Y\). Each consumer has a utility function over numeraire consumption \(c\) and commodity \(q\) given by:

$$u(c,q) = c + \alpha q - \frac{{1}}{{2}} \beta q^2 $$

There are \(M\) identical firms each with cost function given by:

$$c(q) = \gamma + \delta q + \frac{{1}}{{2}} \eta q^2 $$

The general solutions are:

$$ Q = \frac{{ \alpha - \delta }}{{ \beta/N + \eta/M }} $$

$$ p = \frac{{ N \eta \alpha + M \beta \delta }}{{ N \eta + M \beta }} $$
"""
    def setup(self):
        params = self.params
        N, M, Y, alpha, beta, gamma, delta, eta = params['N'], params['M'], params['Y'], params['alpha'], params['beta'], params['gamma'], params['delta'], params['eta']
        return fr"""
A commodity \(q\) is traded at price \(p\) in a competitive market with price-taking consumers and firms. \\
        
There are \({N:,g}\) identical consumers each with income \(Y={Y:g}\). Each consumer has a utility function over numeraire consumption \(c\) and commodity \(q\) given by:

$$u(c,q) = c + {polyeq('q',[alpha, -0.5*beta],[1,2])} $$

There are \({M:,g}\) identical firms each with cost function given by:

$$c(q) = {polyeq('q',[gamma,delta,0.5*eta],[0,1,2])} $$
"""
    def check_solution(self):
        sol = self.sol
        return (
            (sol['c']>0) and
            (sol['qd']>0) and
            (sol['qs']>0) and
            (sol['p']>0) and
            (is_divisible(sol['p'],1)) and
            (is_divisible(sol['qd'],1)) and
            (is_divisible(sol['qs'],1)) 
        )


ADVALOREMSR_SOLUTION = r"""
The general solutions are:

$$Q = \frac{(1-t_p)\alpha - (1+t_c)\delta}{(1-t_p)\beta/N + (1+t_c)\eta/M}$$

$$p = \frac{N \eta \alpha + M \beta \delta}{(1+t_c) N \eta + (1-t_p) M \beta}$$
"""
"""
Ad Valorem Taxes
"""
class AdValoremSR:
    def __init__(self, params=None):
        if not params:
            params = {'N':3000, 'M':200, 'Y':100, 'alpha':10, 'beta':2, 'gamma':0, 'delta':0, 'eta':0.2, 'tc':0.1, 'tp':0}
        params = {k:params[k] for k in ['N','M','Y','alpha','beta','gamma','delta','eta','tc','tp']}
        no_tax = SREQ(params)
        N, M, Y, alpha, beta, gamma, delta, eta, tc, tp = params['N'], params['M'], params['Y'], params['alpha'], params['beta'], params['gamma'], params['delta'], params['eta'], params['tc'], params['tp']

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

    def general_setup(self):
        t = self.no_tax.general_setup()
        t+= r"""
An ad-valorem tax rate of \(t_c\) is placed on the consumers and an ad-valorem tax rate of \(t_p\) is placed on the producers.

The general solutions are:

$$Q = \frac{(1-t_p)\alpha - (1+t_c)\delta}{(1-t_p)\beta/N + (1+t_c)\eta/M}$$

$$p = \frac{N \eta \alpha + M \beta \delta}{(1+t_c) N \eta + (1-t_p) M \beta}$$
"""
        return t
    
    def setup(self):
        params = self.params
        N, M, Y, alpha, beta, gamma, delta, eta, tc, tp = params['N'], params['M'], params['Y'], params['alpha'], params['beta'], params['gamma'], params['delta'], params['eta'], params['tc'], params['tp']
        t = self.no_tax.setup()
        if tc>0:
            t+=fr"An ad-valorem tax rate of \({tc*100:g}\% \) is placed on the consumers. "
        if tp>0:
            t+=fr"An ad-valorem tax rate of \({tp*100:G}\% \) is placed on the producers. "
        return t
    
    def check_solution(self):
        return (
            (self.sol['c']>0) and
            (self.sol['p']>0) and
            (self.sol['qd']>0) and
            (self.sol['qs']>0) and
            is_divisible(self.sol['p'],1) and 
            is_divisible(self.sol['qd'],1) and 
            is_divisible(self.sol['qs'],1) and 
            self.no_tax.check_solution()
        )



"""
Laffer Curve
"""
class Laffer:
    def __init__(self, params=None):
        if not params:
            params = {'N':400,'M':200,'alpha':15}
        params = {k:params[k] for k in ['N','M','alpha']}
        self.params = params.copy()
        params['beta'] = 1
        params['gamma'] = 0
        params['delta'] = 0
        params['eta'] = 1
        params['Y'] = 100
        sreq = SREQ(params)
        self.sreq = sreq
    def general_setup(self):
        return fr"""
A commodity \(q\) is traded at price \(p\) in a competitive market with price-taking consumers and firms. \\
        
There are \(N\) identical consumers each with income \(Y\). Each consumer has a utility function over numeraire consumption \(c\) and commodity \(q\) given by:

$$u(c,q) = c + \alpha q - \frac{{1}}{{2}} q^2 $$

There are \(M\) identical firms each with cost function given by:

$$c(q) = \frac{{1}}{{2}} q^2 $$

An ad-valorem tax rate of \(t\) is levied on the producers.

The general solutions are:

$$ p = \frac{{\alpha N / M}}{{1 + N/M - t}} $$

$$ Q = \alpha N \left( \frac{{1-t}}{{1+N/M-t}} \right) $$
"""
    def setup(self):
        t = self.sreq.setup()
        t+=fr"""
An ad-valorem tax rate of \(t\) is levied on the producers.
"""
        return t
    def check_solution(self):
        params = self.params
        N, M, alpha = params['N'], params['M'], params['alpha']
        return (
            is_divisible(alpha*N, M) and 
            is_divisible(alpha*N, 1) and
            is_divisible(N,M) 
        )
    def formula_p(self):
        params = self.params
        N, M, alpha = params['N'], params['M'], params['alpha']
        numer = alpha*N/M
        denom = 1 + N/M
        return fr"\frac{{ {numer:,g} }}{{ {denom:,g} - t }}"
    def formula_q(self):
        params = self.params
        N, M, alpha = params['N'], params['M'], params['alpha']
        denom = 1 + N/M
        return fr"{alpha*N:,g} \left( \frac{{ 1-t }}{{ {denom:,g} - t }} \right)"
    def get_plot_xy(self):
        params = self.params
        N, M, alpha = params['N'], params['M'], params['alpha']
        t = np.arange(0,1,0.01)
        p = (alpha*N/M)/(1 + N/M - t)
        Q = alpha*N*((1-t)/(1+N/M-t))
        revenue = t*p*Q
        return t, revenue
    

"""
Long Run Equilibrium
"""
class LREQ:
    def __init__(self, params=None):
        if not params:
            params = {'N':3000, 'Y':100, 'alpha':10, 'beta':1, 'gamma':32, 'delta':0, 'eta':1}
        params = {k:params[k] for k in ['N','Y','alpha','beta','gamma','delta','eta']}
        N, Y, alpha, beta, gamma, delta, eta = params['N'], params['Y'], params['alpha'], params['beta'], params['gamma'], params['delta'], params['eta']
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
        params = self.params
        sol = self.sol
        return (
            (sol['c']>0) and
            (sol['qd']>0) and
            (sol['qs']>0) and
            (sol['p']>0) and
            is_divisible(sol['p'],1) and
            is_divisible(sol['qd'],1) and
            is_divisible(sol['qs'],1) and
            is_divisible(sol['M'],1) and
            (params['N'] > sol['M'])
        )
    def general_setup(self):
        return fr"""
A commodity \(q\) is traded at price \(p\) in a competitive market with price-taking consumers and firms. \\
        
There are \(N\) identical consumers each with income \(Y\). Each consumer has a utility function over numeraire consumption \(c\) and commodity \(q\) given by:

$$u(c,q) = c + \alpha q - \frac{{1}}{{2}} \beta q^2$$

There are \(M\) identical firms each with cost function given by:

$$c(q) = \gamma + \delta q + \frac{{1}}{{2}} \eta q^2 $$

The number of firms is fixed in the short run, but in the long run firms can freely enter or exit the market. Thus, the number of firms is flexible in the long run.

The general solutions are:

$$q_s = \sqrt{{2\gamma / \eta}}$$

$$p = \delta + \eta q_s$$

$$q_d = \frac{{\alpha - p}}{{\beta}}$$
"""
    def setup(self):
        params = self.params
        N, Y, alpha, beta, gamma, delta, eta = params['N'], params['Y'], params['alpha'], params['beta'], params['gamma'], params['delta'], params['eta']
        return fr"""
A commodity \(q\) is traded at price \(p\) in a competitive market with price-taking consumers and firms. \\
        
There are \({N:,g}\) identical consumers each with income \(Y={Y:,g}\). Each consumer has a utility function over numeraire consumption \(c\) and commodity \(q\) given by:

$$u(c,q) = c + {polyeq('q',[alpha,-0.5*beta],[1,2])} $$

There are \(M\) identical firms each with cost function given by:

$$c(q) = {polyeq('q',[gamma,delta,0.5*eta],[0,1,2])} $$

The number of firms is fixed in the short run, but in the long run firms can freely enter or exit the market. Thus, the number of firms is flexible in the long run.
"""


    
"""
Cobb Douglas Consumer
"""
class CobbDouglasConsumer:
    def __init__(self, params=None):
        if not params:
            params = {'nx':1,'dx':2,'ny':1,'dy':2,'I':120,'px':1,'py':1,'gmax':120}
        params = {k:params[k] for k in ['nx','dx','ny','dy','I','px','py','gmax']}
        nx, dx, ny, dy, I, px, py, gmax = params['nx'], params['dx'], params['ny'], params['dy'], params['I'], params['px'], params['py'], params['gmax']
        a = nx/dx
        b = ny/dy
        x = I/(px*(1+b/a))
        y = I/(py*(1+a/b))
        U = x**a * y**b
        sol = {}
        sol['x'] = x
        sol['y'] = y
        sol['U'] = U
        sol['xmax'] = I/px
        sol['ymax'] = I/py
        self.params = params
        self.sol = sol
    def check_solution(self):
        params = self.params
        nx, dx, ny, dy, I, px, py, gmax = params['nx'], params['dx'], params['ny'], params['dy'], params['I'], params['px'], params['py'], params['gmax']
        sol = self.sol
        x, y, xmax, ymax = sol['x'], sol['y'], sol['xmax'], sol['ymax']
        return (
            (x>0) and (y>0) and 
            is_divisible(px,1) and
            is_divisible(py,1) and
            is_divisible(I,px) and
            is_divisible(I,py) and
            is_divisible(gmax,12) and
            is_divisible(xmax, gmax/12) and
            is_divisible(ymax, gmax/12) and
            is_divisible(x, gmax/12) and
            is_divisible(y, gmax/12)
        )
    def general_setup(self):
        return fr"""
A consumer with income \(I\) has a utility function over two goods, \(x\) and \(y\):

$$ u(x,y) = x^a y^b $$

The price of good \(x\) is \(p_x\) and the price of good \(y\) is \(p_y\).

The general solutions are:

$$ x = \frac{{I}}{{p_x(1+b/a)}} $$

$$ y = \frac{{I}}{{p_y(1+a/b)}} $$

The indifference curves are:

$$ y = \left( \frac{{U}}{{x^a}} \right)^{{ 1/b }} $$

The budget constraint is:

$$ y = \frac{{I - p_x x}}{{p_y }} $$
"""
    def setup(self):
        params = self.params
        nx, dx, ny, dy, I, px, py, gmax = params['nx'], params['dx'], params['ny'], params['dy'], params['I'], params['px'], params['py'], params['gmax']
        return fr"""
A consumer with income \(I={I:g}\) has a utility function over two goods, \(x\) and \(y\):

$$ u(x,y) = {cbeq(1,'x',Number(nx,dx),'y',Number(ny,dy))} $$

The price of good \(x\) is \(p_x = {px:g} \) and the price of good \(y\) is \(p_y = {py:g} \).
"""
    def graph_schematic(self, saveas=None, show=False):
        params = self.params
        nx, dx, ny, dy, I, px, py, gmax = params['nx'], params['dx'], params['ny'], params['dy'], params['I'], params['px'], params['py'], params['gmax']
        a = nx/dx
        b = ny/dy
        sol = self.sol
        x, y, xmax, ymax, U = sol['x'], sol['y'], sol['xmax'], sol['ymax'], sol['U']
        mymax = max(xmax, ymax)
        fig, ax = plt.subplots()
        xg = np.arange(0, gmax + 2*gmax/12, 0.1)
        budget_constraint = (I - px*xg)/py
        indifference_curve = (U/(xg[1:]**a))**(1/b)
        ax.plot(xg, budget_constraint, color='black',linewidth=2)
        ax.plot(xg[1:], indifference_curve, color='blue')
        ax.plot(x,y,'o',color='black',markersize=12)
        ax.set_ylabel(r'$y$')
        ax.set_xlabel(r'$x$')
        ax.set_xticks(np.arange(0, mymax+gmax/12, gmax/12))
        ax.set_yticks(np.arange(0, mymax+gmax/12, gmax/12))
        ax.set_xlim([0, mymax+gmax/12])
        ax.set_ylim([0, mymax+gmax/12])
        ax.set_axisbelow(True)
        plt.grid(alpha=0.2)
        if saveas is not None:
            plt.savefig(saveas, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()
        return True
    def graph_with_IC(self, with_solution=False, saveas=None, show=False):
        params = self.params
        nx, dx, ny, dy, I, px, py, gmax = params['nx'], params['dx'], params['ny'], params['dy'], params['I'], params['px'], params['py'], params['gmax']
        a = nx/dx
        b = ny/dy
        sol = self.sol
        x, y, xmax, ymax, U = sol['x'], sol['y'], sol['xmax'], sol['ymax'], sol['U']
        fig, ax = plt.subplots()
        xg = np.arange(0, gmax + 2*gmax/12, 0.1)
        for xug in np.arange(gmax/12, gmax+gmax/12, gmax/12):
            yug = y/x*xug
            myU = xug**a * yug**b
            indifference_curve = (myU /(xg[1:]**a))**(1/b)
            ax.plot(xg[1:], indifference_curve, color='green', alpha=0.3)
        if with_solution:
            budget_constraint = (I - px*xg)/py
            ax.plot(xg, budget_constraint, color='black',linewidth=2)
            ax.plot(x,y,'o',color='black',markersize=12)
        ax.set_ylabel(r'$y$')
        ax.set_xlabel(r'$x$')
        ax.set_xticks(np.arange(0, gmax+gmax/12, gmax/12))
        ax.set_yticks(np.arange(0, gmax+gmax/12, gmax/12))
        ax.set_xlim([0, gmax+gmax/12])
        ax.set_ylim([0, gmax+gmax/12])
        ax.set_axisbelow(True)
        plt.grid(alpha=0.2)
        if saveas is not None:
            plt.savefig(saveas, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()
        return True
        


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
        
