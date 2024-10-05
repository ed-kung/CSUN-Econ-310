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
            (x>0.1) and (y>0.1) and 
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
        maxU = gmax**a * gmax**b
        minU = (gmax/12)**a * (gmax/12)**b
        dU = (maxU - minU)/12
        minU = U - np.floor((U - minU)/dU)*dU
        for myU in np.arange(minU, maxU+dU, dU):
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
        

"""
Perfect Substitutes
"""
class PerfectSubstitutes:
    def __init__(self, params=None):
        if not params:
            params = {'I':100,'a':1,'b':1,'px':1,'py':2,'gmax':120}
        params = {k:params[k] for k in ['I','a','b','px','py','gmax']}
        I,a,b,px,py,gmax = params['I'], params['a'], params['b'], params['px'], params['py'], params['gmax']
        xmax = I/px
        ymax = I/py
        if (a*py - b*px)>0:
            x = xmax
            y = 0
        elif (a*py - b*px)<0:
            x = 0
            y = ymax
        else:
            x = 0.5*I/px
            y = 0.5*I/py
        U = a*x + b*y
        sol = {'x':x, 'y':y, 'xmax':xmax, 'ymax':ymax, 'U':U}
        self.params = params
        self.sol = sol
    def check_solution(self):
        params = self.params
        sol = self.sol
        I,a,b,px,py,gmax = params['I'], params['a'], params['b'], params['px'], params['py'], params['gmax']
        x,y,xmax,ymax,U = sol['x'], sol['y'], sol['xmax'], sol['ymax'], sol['U']
        return (
            (x>=0) and (y>=0) and (a*py - b*px!=0) and
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

$$ u(x,y) = ax + by $$

The price of good \(x\) is \(p_x\) and the price of good \(y\) is \(p_y\).

The general solutions are:\\

If \(ap_y - bp_x > 0\) then \(x = I/p_x\) and \(y=0\). \\

If \(ap_y - bp_y < 0\) then \(x=0\) and \(y = I/p_y\). \\

Otherwise, \(x\) and \(y\) could be anything.
"""
    def setup(self):
        params = self.params
        I,a,b,px,py,gmax = params['I'], params['a'], params['b'], params['px'], params['py'], params['gmax']
        return fr"""
A consumer with income \(I={I:g}\) has a utility function over two goods, \(x\) and \(y\):

$$ u(x,y) = {term(a,'x',1,rmplus=True)} {term(b,'y',1,rmplus=False)}  $$

The price of good \(x\) is \(p_x={px:g}\) and the price of good \(y\) is \(p_y={py:g}\).
"""
    def graph_with_IC(self, with_solution=False, saveas=None, show=False):
        params = self.params
        sol = self.sol
        I,a,b,px,py,gmax = params['I'], params['a'], params['b'], params['px'], params['py'], params['gmax']
        x,y,xmax,ymax,U = sol['x'], sol['y'], sol['xmax'], sol['ymax'], sol['U']
        fig, ax = plt.subplots()
        xg = np.arange(0, gmax + 2*gmax/12, 0.1)

        maxU = a*gmax + b*gmax
        myx = 0
        myy = 0
        myU = 0
        if x==0:
            dx = 0
            dy = gmax/12
        else:
            dy = 0
            dx = gmax/12
        while myU < maxU:
            myx += dx
            myy += dy
            myU = a*myx + b*myy
            indifference_curve = (myU - a*xg)/b
            ax.plot(xg, indifference_curve, color='green', alpha=0.3)
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
    
    
"""
Leontieff
"""
class Leontieff:
    def __init__(self, params=None):
        if not params:
            params = {'I':100,'px':1,'py':1,'gmax':120}
        params = {k:params[k] for k in ['I','px','py','gmax']}
        I,px,py,gmax = params['I'], params['px'], params['py'], params['gmax']
        xmax = I/px
        ymax = I/py
        x = I/(px+py)
        y = I/(px+py)
        U = x
        sol = {'x':x, 'y':y, 'xmax':xmax, 'ymax':ymax, 'U':U}
        self.params = params
        self.sol = sol
    def check_solution(self):
        params = self.params
        I,px,py,gmax = params['I'], params['px'], params['py'], params['gmax']
        sol = self.sol
        x,y,xmax,ymax,U = sol['x'], sol['y'], sol['xmax'], sol['ymax'], sol['U']
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

$$ u(x,y) = \min (x, y) $$

The price of good \(x\) is \(p_x\) and the price of good \(y\) is \(p_y\).

The general solutions are:\\

$$ x = y = \frac{{I}}{{p_x + p_y}} $$
"""
    def setup(self):
        params = self.params
        I,px,py,gmax = params['I'], params['px'], params['py'], params['gmax']
        return fr"""
A consumer with income \(I={I:g}\) has a utility function over two goods, \(x\) and \(y\):

$$ u(x,y) = \min (x, y) $$

The price of good \(x\) is \(p_x={px:g}\) and the price of good \(y\) is \(p_y={py:g}\).
"""
    def graph_with_IC(self, with_solution=False, saveas=None, show=False):
        params = self.params
        I,px,py,gmax = params['I'], params['px'], params['py'], params['gmax']
        sol = self.sol
        x,y,xmax,ymax,U = sol['x'], sol['y'], sol['xmax'], sol['ymax'], sol['U']
        fig, ax = plt.subplots()
        xg = np.arange(0, gmax + 2*gmax/12, 0.1)
        
        for myU in np.arange(gmax/12, gmax+gmax/12, gmax/12):
            hline = np.arange(myU, gmax+2*gmax/12, 0.1)
            vline = np.arange(myU, gmax+2*gmax/12, 0.1)
            ax.plot(hline, myU*np.ones(hline.shape), color='green', alpha=0.3)
            ax.plot(myU*np.ones(vline.shape), vline, color='green', alpha=0.3)
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
    
    
"""
Quasilinear CE 
"""
class QuasilinearCE:
    def __init__(self, params=None):
        if not params:
            params = {'I':60,'a':10,'n':1,'d':2,'px':1,'py':1,'gmax':60,'numeraire':'x'}
        params = {k:params[k] for k in ['I','a','n','d','px','py','gmax','numeraire']}
        I,a,n,d,px,py,gmax,numeraire = params['I'], params['a'], params['n'], params['d'], params['px'], params['py'], params['gmax'], params['numeraire']
        if numeraire=='x':
            y = ((d*py)/(a*n*px))**(d/(n-d))
            x = (I - py*y)/px
            U = x + a*y**(n/d)
        elif numeraire=='y':
            x = ((d*px)/(a*n*py))**(d/(n-d))
            y = (I - px*x)/py
            U = a*x**(n/d) + y
        xmax = I/px
        ymax = I/py
        sol = {'x':x, 'y':y, 'xmax':xmax, 'ymax':ymax, 'U':U}
        self.params = params
        self.sol = sol
    def check_solution(self):
        params = self.params
        I,a,n,d,px,py,gmax,numeraire = params['I'], params['a'], params['n'], params['d'], params['px'], params['py'], params['gmax'], params['numeraire']
        sol = self.sol
        x,y,xmax,ymax,U = sol['x'], sol['y'], sol['xmax'], sol['ymax'], sol['U']
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

$$ u(x,y) = x + ay^{{n/d}} $$

or

$$ u(x,y) = ax^{{n/d}} + y $$

The price of good \(x\) is \(p_x\) and the price of good \(y\) is \(p_y\).

The general solutions are:\\

$$ y = \left( \frac{{ dp_y }}{{ anp_x }} \right)^{{ \frac{{d}}{{n-d}} }} $$

or

$$ x = \left( \frac{{ dp_x }}{{ anp_y }} \right)^{{ \frac{{d}}{{n-d}} }} $$
"""
    def setup(self):
        params = self.params
        I,a,n,d,px,py,gmax,numeraire = params['I'], params['a'], params['n'], params['d'], params['px'], params['py'], params['gmax'], params['numeraire']
        if numeraire=='x':
            myeq = fr"x + {term(a,'y',Number(n,d),rmplus=True)}"
        elif numeraire=='y':
            myeq = fr"{term(a,'x',Number(n,d),rmplus=True)} + y"
        return fr"""
A consumer with income \(I={I:g}\) has a utility function over two goods, \(x\) and \(y\):

$$ u(x,y) = {myeq} $$

The price of good \(x\) is \(p_x={px:g}\) and the price of good \(y\) is \(p_y={py:g}\).
"""
    def graph_with_IC(self, with_solution=False, saveas=None, show=False):
        params = self.params
        I,a,n,d,px,py,gmax,numeraire = params['I'], params['a'], params['n'], params['d'], params['px'], params['py'], params['gmax'], params['numeraire']
        sol = self.sol
        x,y,xmax,ymax,U = sol['x'], sol['y'], sol['xmax'], sol['ymax'], sol['U']
        fig, ax = plt.subplots()
        yg = np.arange(0, gmax+2*gmax/12, 0.1)
        xg = np.arange(0, gmax+2*gmax/12, 0.1)
        maxU = gmax + a*gmax**(n/d)
        minU = (gmax/12) + a*(gmax/12)**(n/d)
        dU = (maxU - minU)/12
        minU = U - np.floor((U - minU)/dU)*dU
        for myU in np.arange(minU, maxU+dU, dU):
            if numeraire=='x':
                indifference_curve = (myU - a*yg**(n/d))
                ax.plot(indifference_curve, yg, color='green', alpha=0.3)
            elif numeraire=='y':
                indifference_curve = (myU - a*xg**(n/d))
                ax.plot(xg, indifference_curve, color='green', alpha=0.3)
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
    
        
        
"""
CPI and Deflators
"""
class CobbDouglasDeflator:
    def __init__(self, params=None):
        if not params:
            params = {'nx':1,'dx':2,'ny':1,'dy':2,'I':100,'px1':1,'py1':1,'px2':1,'py2':2,'gmax':120}
        params = {k:params[k] for k in ['nx','dx','ny','dy','I','px1','py1','px2','py2','gmax']}
        nx, dx, ny, dy, I, px1, py1, px2, py2, gmax = params['nx'], params['dx'], params['ny'], params['dy'], params['I'], params['px1'], params['py1'], params['px2'], params['py2'], params['gmax']
        a = nx/dx
        b = ny/dy
        CPI = ((1/(1+b/a))*(px2/px1) + (1/(1+a/b))*(py2/py1)) * 100
        CONST_UTIL_DEFLATOR = ((px2/px1)**(a/(a+b))*(py2/py1)**(b/(a+b))) * 100
        # Base period
        params1 = params.copy()
        params1['px'] = px1
        params1['py'] = py1
        cb1 = CobbDouglasConsumer(params1)
        # Comparison period without COLA
        params2_no_cola = params.copy()
        params2_no_cola['px'] = px2
        params2_no_cola['py'] = py2
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
            self.cb2_no_colas.check_solution()
        )
    def general_setup(self):
        return fr"""
A consumer has a utility function over two goods, \(x\) and \(y\), given by:

$$ u(x,y) = x^a y^b $$

In the base period, the consumer has income \(I\), the price of \(x\) is \(p_x\), and the price of \(y\) is \(p_y\).

In the comparison period, the price of \(x\) changes to \(p_x^\prime\), and the price of \(y\) changes to \(p_y^\prime\).

The general solutions are:

The general solutions are:

$$ \text{{CPI}} = \frac{{1}}{{1+b/a}} \left(\frac{{p_x^\prime}}{{p_x}}\right) + \frac{{1}}{{1+a/b}}\left(\frac{{p_y^\prime}}{{p_y}}\right) $$

$$ \text{{Constant Utility Deflator}} = \left(\frac{{p_x^\prime}}{{p_x}}\right)^{{\frac{{a}}{{a+b}} }} \left(\frac{{p_y^\prime}}{{p_y}}\right)^{{ \frac{{b}}{{a+b}} }} $$
"""
    def setup(self):
        params = self.params
        nx, dx, ny, dy, I, px1, py1, px2, py2, gmax = params['nx'], params['dx'], params['ny'], params['dy'], params['I'], params['px1'], params['py1'], params['px2'], params['py2'], params['gmax']
        return fr"""
A consumer has a utility function over two goods, \(x\) and \(y\), given by:

$$ u(x,y) = {cbeq(1,'x',Number(nx,dx),'y',Number(ny,dy))} $$

In the base period, the consumer has income \(I={I:g}\), the price of \(x\) is \(p_x={px1:g}\), and the price of \(y\) is \(p_y={py1:g}\).

In the comparison period, the price of \(x\) is \(p_x^\prime={px2:g}\), and the price of \(y\) is \(p_y^\prime={py2:g}\).
"""
    
        

"""
Food Stamps
"""
class FoodStamps:
    def __init__(self, params=None):
        if not params:
            params = {'val':20,'nx':1,'dx':2,'ny':1,'dy':2,'I':100,'px':1,'py':1,'gmax':120}
        params = {k:params[k] for k in ['val','nx','dx','ny','dy','I','px','py','gmax']}
        val, nx, dx, ny, dy, I, px, py, gmax = params['val'], params['nx'], params['dx'], params['ny'], params['dy'], params['I'], params['px'], params['py'], params['gmax']
        a = nx/dx
        b = ny/dy
        cb_base = CobbDouglasConsumer(params)
        params_tfr = params.copy()
        params_tfr['I'] = I + val
        cb_tfr = CobbDouglasConsumer(params_tfr)
        U_base = cb_base.sol['U']
        U_tfr = cb_tfr.sol['U']
        x_tfr = cb_tfr.sol['x']
        y_tfr = cb_tfr.sol['y']
        U_corner = (val/px)**a * (I/px)**b
        if x_tfr >= val/px:
            U_ink = U_tfr
            x_ink = x_tfr
            y_ink = y_tfr
            corner = False
        else:
            U_ink = U_corner
            x_ink = val/px
            y_ink = I/py
            corner = True
        sol = {'U_base':U_base, 'U_tfr':U_tfr, 'U_corner':U_corner, 'corner':corner, 'U_ink':U_ink, 'x_ink':x_ink, 'y_ink':y_ink}
        self.params = params
        self.sol = sol
        self.cb_base = cb_base
        self.cb_tfr = cb_tfr
    def check_solution(self):
        return (
            self.cb_base.check_solution() and
            self.cb_tfr.check_solution() 
        )
    def graph_with_IC(self, base=False, inkind=False, tfr=False, saveas=None, show=False):
        params = self.params
        val, nx, dx, ny, dy, I, px, py, gmax = params['val'], params['nx'], params['dx'], params['ny'], params['dy'], params['I'], params['px'], params['py'], params['gmax']
        a = nx/dx
        b = ny/dy
        xmax = I/px
        ymax = I/py
        x_base = self.cb_base.sol['x']
        y_base = self.cb_base.sol['y']
        U_base = self.cb_base.sol['U']
        x_tfr = self.cb_tfr.sol['x']
        y_tfr = self.cb_tfr.sol['y']
        U_tfr = self.cb_tfr.sol['U']
        x_ink = self.sol['x_ink']
        y_ink = self.sol['y_ink']
        corner = self.sol['corner']
        fig, ax = plt.subplots()
        xg = np.arange(0, gmax + 2*gmax/12, 0.1)
        maxU = gmax**a * gmax**b
        minU = (gmax/12)**a * (gmax/12)**b
        dU_target = (maxU - minU)/12
        dU_n = np.ceil((U_tfr - U_base)/dU_target)
        dU = (U_tfr - U_base)/dU_n
        minU = U_base - np.floor((U_base - minU)/dU)*dU
        for myU in np.arange(minU, maxU+dU, dU):
            indifference_curve = (myU /(xg[1:]**a))**(1/b)
            ax.plot(xg[1:], indifference_curve, color='green', alpha=0.3, label='_nolegend_')
        legend = []
        if base:
            budget_constraint = (I - px*xg)/py
            ax.plot(xg, budget_constraint, color='black',linewidth=2)
            ax.plot(x_base,y_base,'o',color='black',markersize=12, label='_nolegend_')
            ax.text(x_base-0.2*gmax/12, y_base-0.2*gmax/12, 'A', color='black', horizontalalignment='right', verticalalignment='top')
            legend.append('No transfers')
        if inkind:
            budget_constraint = (I+val - px*xg)/py
            budget_constraint = np.minimum(budget_constraint, I/py)
            ax.plot(xg, budget_constraint, color='blue', linewidth=2)
            ax.plot(x_ink, y_ink, 'o', color='blue', markersize=12, label='_nolegend_')
            ax.text(x_ink+0.0*gmax/12, y_ink+0.4*gmax/12, 'B', color='blue')
            legend.append('Food stamps')
        if tfr:
            budget_constraint = (I+val - px*xg)/py
            ax.plot(xg, budget_constraint, color='red',linewidth=2,linestyle='dashed')
            ax.plot(x_tfr,y_tfr,'o',color='red',markersize=12, label='_nolegend_')
            ax.text(x_tfr+0.4*gmax/12, y_tfr+0.0*gmax/12, 'C', color='red')
            legend.append('Monetary transfers')
        if len(legend)>0:
            plt.legend(legend, loc='upper right')
        ax.set_ylabel('Other Consumption')
        ax.set_xlabel('Food Consumption')
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
        
    
"""
Public School
"""
class PublicSchool:
    def __init__(self, params=None):
        if not params:
            params = {'val':20,'nx':1,'dx':2,'ny':1,'dy':2,'I':100,'px':1,'py':1,'gmax':120}
        params = {k:params[k] for k in ['val','nx','dx','ny','dy','I','px','py','gmax']}
        val, nx, dx, ny, dy, I, px, py, gmax = params['val'], params['nx'], params['dx'], params['ny'], params['dy'], params['I'], params['px'], params['py'], params['gmax']
        a = nx/dx
        b = ny/dy
        cb_base = CobbDouglasConsumer(params)
        params_tfr = params.copy()
        params_tfr['I'] = I + val
        cb_tfr = CobbDouglasConsumer(params_tfr)
        U_base = cb_base.sol['U']
        x_base = cb_base.sol['x']
        y_base = cb_base.sol['y']
        U_tfr = cb_tfr.sol['U']
        x_tfr = cb_tfr.sol['x']
        y_tfr = cb_tfr.sol['y']
        U_corner = (val/px)**a * (I/px)**b
        if x_tfr >= val/px:
            U_voucher = U_tfr
            x_voucher = x_tfr
            y_voucher = y_tfr
            corner = False
        else:
            U_voucher = U_corner
            x_voucher = val/px
            y_voucher = I/py
            corner = True
        U_public = U_corner
        if U_corner >= U_base:
            U_public = U_corner
            x_public = val/px
            y_public = I/py
            public = True
        else:
            U_public = U_base
            x_public = x_base
            y_public = y_base
            public = False
        sol = {'U_base':U_base, 'U_public':U_public, 'U_voucher':U_voucher, 'corner':corner, 'public':public,
               'x_voucher':x_voucher, 'y_voucher':y_voucher, 'x_public':x_public, 'y_public':y_public}
        self.params = params
        self.sol = sol
        self.cb_base = cb_base
        self.cb_tfr = cb_tfr
    def check_solution(self):
        return (
            self.cb_base.check_solution() and
            self.cb_tfr.check_solution() 
        )
    def graph_with_IC(self, base=False, public=False, voucher=False, saveas=None, show=False):
        params = self.params
        val, nx, dx, ny, dy, I, px, py, gmax = params['val'], params['nx'], params['dx'], params['ny'], params['dy'], params['I'], params['px'], params['py'], params['gmax']
        a = nx/dx
        b = ny/dy
        xmax = I/px
        ymax = I/py
        x_base = self.cb_base.sol['x']
        y_base = self.cb_base.sol['y']
        U_base = self.cb_base.sol['U']
        x_tfr = self.cb_tfr.sol['x']
        y_tfr = self.cb_tfr.sol['y']
        U_tfr = self.cb_tfr.sol['U']
        x_public = self.sol['x_public']
        y_public = self.sol['y_public']
        chose_public = self.sol['public']
        x_voucher = self.sol['x_voucher']
        y_voucher = self.sol['y_voucher']
        corner = self.sol['corner']
        fig, ax = plt.subplots()
        xg = np.arange(0, gmax + 2*gmax/12, 0.1)
        maxU = gmax**a * gmax**b
        minU = (gmax/12)**a * (gmax/12)**b
        dU_target = (maxU - minU)/12
        dU_n = np.ceil((U_tfr - U_base)/dU_target)
        dU = (U_tfr - U_base)/dU_n
        minU = U_base - np.floor((U_base - minU)/dU)*dU
        for myU in np.arange(minU, maxU+dU, dU):
            indifference_curve = (myU /(xg[1:]**a))**(1/b)
            ax.plot(xg[1:], indifference_curve, color='green', alpha=0.3, label='_nolegend_')
        legend = []
        if base:
            budget_constraint = (I - px*xg)/py
            ax.plot(xg, budget_constraint, color='black',linewidth=2)
            ax.plot(x_base,y_base,'o',color='black',markersize=12, label='_nolegend_')
            ax.text(x_base-0.2*gmax/12, y_base-0.2*gmax/12, 'A', color='black', horizontalalignment='right', verticalalignment='top')
            legend.append('No public education')
        if public:
            ax.plot(val/px,I/py,'s',color='blue',markersize=14)
            legend.append('Public school')
            ax.plot(x_public, y_public, 'o', color='blue', markersize=12, label='_nolegend_')
            ax.text(x_public+0.0*gmax/12, y_public+0.4*gmax/12, 'B', color='blue')
        if voucher:
            budget_constraint = (I+val - px*xg)/py
            budget_constraint = np.minimum(budget_constraint, I/py)
            ax.plot(xg, budget_constraint, color='red', linewidth=2)
            legend.append('School vouchers')
            ax.plot(x_voucher, y_voucher, 'o', color='red', markersize=12, label='_nolegend_')
            ax.text(x_voucher+0.4*gmax/12, y_voucher+0.0*gmax/12, 'C', color='red')
        if len(legend)>0:
            plt.legend(legend, loc='upper right')
        ax.set_ylabel('Other Consumption')
        ax.set_xlabel('Education Consumption')
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
    

"""
LeisureCB
"""
class LeisureCB:
    def __init__(self, params=None):
        if not params:
            params = {'nx':2,'dx':3,'ny':1,'dy':3,'w':30,'cmax':1800}
        nx, dx, ny, dy, w, cmax = params['nx'], params['dx'], params['ny'], params['dy'], params['w'], params['cmax']
        a = nx/dx
        b = ny/dy
        h = 60/(1+b/a)
        l = 60 - h
        c = w*h
        U = c**a * l**b
        sol = {'c':c,'l':l,'h':h,'U':U}
        self.params = params
        self.sol = sol
    def check_solution(self):
        params = self.params
        nx, dx, ny, dy, w, cmax = params['nx'], params['dx'], params['ny'], params['dy'], params['w'], params['cmax']
        sol = self.sol
        c, l, h, U = sol['c'], sol['l'], sol['h'], sol['U']
        return (
            (c>0) and (l>0) and
            is_divisible(cmax, 12) and
            is_divisible(60*w, cmax/12) and
            is_divisible(c, cmax/12) and
            is_divisible(h, 60/12)
        )
    def general_setup(self):
        return fr"""
An individual can work for up to 60 hours a week at an hourly wage of \(w\). The person has utility over weekly consumption \(c\) and weekly leisure hours \(\ell\) given by:

$$ u(c, \ell) = c^a \ell^b $$

The general solution is:

$$ c = \frac{{60w}}{{1+b/a}} $$

$$ h = \frac{{60}}{{1+b/a}} $$
"""
    def setup(self):
        params = self.params
        nx, dx, ny, dy, w, cmax = params['nx'], params['dx'], params['ny'], params['dy'], params['w'], params['cmax']
        ell = r'\ell'
        return fr"""
An individual can work for up to 60 hours a week at an hourly wage of \(w={w:g}\). The person has utility over weekly consumption \(c\) and weekly leisure hours \(\ell\) given by:

$$ u(c, \ell) = {cbeq(1,'c',Number(nx,dx),ell,Number(ny,dy))} $$
"""
    def graph_with_IC(self, with_solution=False, saveas=None, show=False):
        params = self.params
        nx, dx, ny, dy, w, cmax = params['nx'], params['dx'], params['ny'], params['dy'], params['w'], params['cmax']
        sol = self.sol
        c, l, h, U = sol['c'], sol['l'], sol['h'], sol['U']
        a = nx/dx
        b = ny/dy
        fig, ax = plt.subplots()
        lg = np.arange(0, 65.1, 0.1)
        maxU = cmax**a * 60**b
        minU = (cmax/12)**a * 5**b
        dU = (maxU - minU)/12
        minU = U - np.floor((U - minU)/dU)*dU
        for myU in np.arange(minU, maxU+dU, dU):
            indifference_curve = (myU /(lg[1:]**b))**(1/a)
            ax.plot(lg[1:], indifference_curve, color='green', alpha=0.3)
        if with_solution:
            budget_constraint = (60*w - w*lg)
            ax.plot(lg, budget_constraint, color='black',linewidth=2)
            ax.plot(l,c,'o',color='black',markersize=12)
        ax.set_ylabel(r'Weekly Consumption')
        ax.set_xlabel(r'Weekly Leisure Hours')
        ax.set_xticks(np.arange(0, 65, 5))
        ax.set_yticks(np.arange(0, cmax+cmax/12, cmax/12))
        ax.set_xlim([0, 65])
        ax.set_ylim([0, cmax+cmax/12])
        ax.set_axisbelow(True)
        plt.grid(alpha=0.2)
        if saveas is not None:
            plt.savefig(saveas, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()
        return True

"""
WageChangeCB
"""
class WageChangeCB:
    def __init__(self, params=None):
        if not params:
            params = {'nx':2,'dx':3,'ny':1,'dy':3,'w1':15,'w2':30,'cmax':1800}
        nx, dx, ny, dy, w1, w2, cmax = params['nx'], params['dx'], params['ny'], params['dy'], params['w1'], params['w2'], params['cmax']
        params1 = params.copy()
        params1['w'] = params['w1']
        prob1 = LeisureCB(params1)
        params2 = params.copy()
        params2['w'] = params['w2']
        prob2 = LeisureCB(params2)
        c1, l1 = prob1.sol['c'], prob1.sol['l']
        c2, l2 = prob2.sol['c'], prob2.sol['l']
        sol = {'c1':c1, 'l1':l1, 'c2':c2, 'l2':l2}
        self.params = params
        self.prob1 = prob1
        self.prob2 = prob2
        self.sol = sol
    def check_solution(self):
        return (
            self.prob1.check_solution() and
            self.prob2.check_solution()
        )
    def setup(self):
        return self.prob1.setup()
    def graph_with_IC(self, period1=False, period2=False, saveas=None, show=False):
        params = self.params
        nx, dx, ny, dy, w1, w2, cmax = params['nx'], params['dx'], params['ny'], params['dy'], params['w1'], params['w2'], params['cmax']
        c1 = self.prob1.sol['c']
        c2 = self.prob2.sol['c']
        l1 = self.prob1.sol['l']
        l2 = self.prob2.sol['l']
        U1 = self.prob1.sol['U']
        U2 = self.prob2.sol['U']
        a = nx/dx
        b = ny/dy
        fig, ax = plt.subplots()
        lg = np.arange(0, 65.1, 0.1)
        maxU = cmax**a * 60**b
        minU = (cmax/12)**a * 5**b
        dU_target = (maxU - minU)/12
        dU_n = np.ceil(np.abs(U2-U1)/dU_target)
        dU = np.abs(U2-U1)/dU_n
        minU = min(U1,U2) - np.floor((min(U1,U2)-minU)/dU)*dU
        for myU in np.arange(minU, maxU+dU, dU):
            indifference_curve = (myU /(lg[1:]**b))**(1/a)
            ax.plot(lg[1:], indifference_curve, color='green', alpha=0.3, label='_nolegend_')
        legend = []
        if period1:
            budget_constraint = (60*w1 - w1*lg)
            ax.plot(lg, budget_constraint, color='black',linewidth=2)
            ax.plot(l1,c1,'o',color='black',markersize=12,label='_nolegend_')
            ax.text(l1+1,c1+0.2*cmax/12,'A',color='black')
            legend.append(f'Wage Rate = {w1:g}')
        if period2:
            budget_constraint = (60*w2 - w2*lg)
            ax.plot(lg, budget_constraint, color='red',linewidth=2)
            ax.plot(l2,c2,'o',color='red',markersize=12,label='_nolegend_')
            ax.text(l2+1,c2+0.2*cmax/12,'B',color='red')
            legend.append(f'Wage Rate = {w2:g}')
        ax.set_ylabel(r'Weekly Consumption')
        ax.set_xlabel(r'Weekly Leisure Hours')
        ax.set_xticks(np.arange(0, 65, 5))
        ax.set_yticks(np.arange(0, cmax+cmax/12, cmax/12))
        ax.set_xlim([0, 65])
        ax.set_ylim([0, cmax+cmax/12])
        ax.set_axisbelow(True)
        plt.grid(alpha=0.2)
        plt.legend(legend, loc='upper right')
        if saveas is not None:
            plt.savefig(saveas, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()
        return True
    
        
"""
LeisureExp
"""
class LeisureExp:
    def __init__(self, params=None):
        if not params:
            params = {'a':270,'kn':1,'kd':2,'w':30,'cmax':1800}
        a, kn, kd, w, cmax = params['a'], params['kn'], params['kd'], params['w'], params['cmax']
        k = kn/kd
        l = (w/(a*k))**(1/(k-1))
        h = 60 - l
        c = w*h
        U = c + a*l**k
        sol = {'c':c,'l':l,'h':h,'U':U}
        self.params = params
        self.sol = sol
    def check_solution(self):
        params = self.params
        a, kn, kd, w, cmax = params['a'], params['kn'], params['kd'], params['w'], params['cmax']
        sol = self.sol
        c, l, h, U = sol['c'], sol['l'], sol['h'], sol['U']
        return (
            (c>cmax/12) and (c<cmax*11/12) and (l>5) and (l<55) and
            is_divisible(cmax, 12) and
            is_divisible(60*w, cmax/12) and
            is_divisible(c, cmax/12) and
            is_divisible(h, 60/12)
        )
    def general_setup(self):
        return fr"""
An individual can work for up to 60 hours a week at an hourly wage of \(w\). The person has utility over weekly consumption \(c\) and weekly leisure hours \(\ell\) given by:

$$ u(c, \ell) = c + a \ell^k $$

The general solution is:

$$ \ell = \left( \frac{{w}}{{ak}} \right)^{{\frac{{1}}{{k-1}} }} $$
"""
    def setup(self):
        params = self.params
        a, kn, kd, w, cmax = params['a'], params['kn'], params['kd'], params['w'], params['cmax']
        ell = r'\ell'
        return fr"""
An individual can work for up to 60 hours a week at an hourly wage of \(w={w:g}\). The person has utility over weekly consumption \(c\) and weekly leisure hours \(\ell\) given by:

$$ u(c, \ell) = c + {term(a,ell,Number(kn,kd),rmplus=True)} $$
"""
    def graph_with_IC(self, with_solution=False, saveas=None, show=False):
        params = self.params
        a, kn, kd, w, cmax = params['a'], params['kn'], params['kd'], params['w'], params['cmax']
        sol = self.sol
        c, l, h, U = sol['c'], sol['l'], sol['h'], sol['U']
        k = kn/kd
        fig, ax = plt.subplots()
        lg = np.arange(0, 65.1, 0.1)
        maxU = cmax + a*60**k 
        minU = (cmax/12) + a*5**k
        dU = (maxU - minU)/12
        minU = U - np.floor((U - minU)/dU)*dU
        for myU in np.arange(minU, maxU+dU, dU):
            indifference_curve = myU - a*lg[1:]**k
            ax.plot(lg[1:], indifference_curve, color='green', alpha=0.3, label='_nolegend_')
        if with_solution:
            budget_constraint = (60*w - w*lg)
            ax.plot(lg, budget_constraint, color='black',linewidth=2)
            ax.plot(l,c,'o',color='black',markersize=12)
        ax.set_ylabel(r'Weekly Consumption')
        ax.set_xlabel(r'Weekly Leisure Hours')
        ax.set_xticks(np.arange(0, 65, 5))
        ax.set_yticks(np.arange(0, cmax+cmax/12, cmax/12))
        ax.set_xlim([0, 65])
        ax.set_ylim([0, cmax+cmax/12])
        ax.set_axisbelow(True)
        plt.grid(alpha=0.2)
        if saveas is not None:
            plt.savefig(saveas, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()
        return True


"""
WageChangeExp
"""
class WageChangeExp:
    def __init__(self, params=None):
        if not params:
            params = {'a':270,'kn':1,'kd':2,'w1':30,'w2':35,'cmax':3600}
        a, kn, kd, w1, w2, cmax = params['a'], params['kn'], params['kd'], params['w1'], params['w2'], params['cmax']
        params1 = params.copy()
        params1['w'] = params['w1']
        prob1 = LeisureExp(params1)
        params2 = params.copy()
        params2['w'] = params['w2']
        prob2 = LeisureExp(params2)
        c1, l1 = prob1.sol['c'], prob1.sol['l']
        c2, l2 = prob2.sol['c'], prob2.sol['l']
        sol = {'c1':c1, 'l1':l1, 'c2':c2, 'l2':l2}
        self.params = params
        self.prob1 = prob1
        self.prob2 = prob2
        self.sol = sol
    def check_solution(self):
        params = self.params
        a, kn, kd, w1, w2, cmax = params['a'], params['kn'], params['kd'], params['w1'], params['w2'], params['cmax']
        sol = self.sol
        c1, l1, c2, l2 = sol['c1'], sol['l1'], sol['c2'], sol['l2']
        return (
            is_divisible(cmax,12) and
            is_divisible(60*w1, cmax/12) and
            is_divisible(60*w2, cmax/12) and
            (l1>5) and (l2>5) and (l1<55) and (l2<55) and
            (np.abs(l1 - l2)>=5)
        )
    def setup(self):
        return self.prob1.setup()
    def graph_with_IC(self, period1=False, period2=False, saveas=None, show=False):
        params = self.params
        a, kn, kd, w1, w2, cmax = params['a'], params['kn'], params['kd'], params['w1'], params['w2'], params['cmax']
        k = kn/kd
        c1 = self.prob1.sol['c']
        c2 = self.prob2.sol['c']
        l1 = self.prob1.sol['l']
        l2 = self.prob2.sol['l']
        U1 = self.prob1.sol['U']
        U2 = self.prob2.sol['U']
        fig, ax = plt.subplots()
        lg = np.arange(0, 65.1, 0.1)
        maxU = cmax + a*60**k
        minU = (cmax/12) + a*5**k
        dU_target = (maxU - minU)/12
        dU_n = np.ceil(np.abs(U2-U1)/dU_target)
        dU = np.abs(U2-U1)/dU_n
        minU = min(U1,U2) - np.floor((min(U1,U2)-minU)/dU)*dU
        for myU in np.arange(minU, maxU+dU, dU):
            indifference_curve = myU - a*lg[1:]**k
            ax.plot(lg[1:], indifference_curve, color='green', alpha=0.3, label='_nolegend_')
        legend = []
        if period1:
            budget_constraint = (60*w1 - w1*lg)
            ax.plot(lg, budget_constraint, color='black',linewidth=2)
            ax.plot(l1,c1,'o',color='black',markersize=12,label='_nolegend_')
            ax.text(l1+1,c1+0.2*cmax/12,'A',color='black')
            legend.append(f'Wage Rate = {w1:g}')
        if period2:
            budget_constraint = (60*w2 - w2*lg)
            ax.plot(lg, budget_constraint, color='red',linewidth=2)
            ax.plot(l2,c2,'o',color='red',markersize=12,label='_nolegend_')
            ax.text(l2+1,c2+0.2*cmax/12,'B',color='red')
            legend.append(f'Wage Rate = {w2:g}')
        ax.set_ylabel(r'Weekly Consumption')
        ax.set_xlabel(r'Weekly Leisure Hours')
        ax.set_xticks(np.arange(0, 65, 5))
        ax.set_yticks(np.arange(0, cmax+cmax/12, cmax/12))
        ax.set_xlim([0, 65])
        ax.set_ylim([0, cmax+cmax/12])
        ax.set_axisbelow(True)
        plt.grid(alpha=0.2)
        plt.legend(legend, loc='upper right')
        if saveas is not None:
            plt.savefig(saveas, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()
        return True
        
"""
LeisureSate
"""
class LeisureSate:
    def __init__(self, params=None):
        if not params:
            params = {'a':60*30,'b':20*900,'w':30,'cmax':1800}
        a, b, w, cmax = params['a'], params['b'], params['w'], params['cmax']
        c = a - b/w
        h = c/w
        l = 60 - h
        U = a*c - 0.5*c**2 + b*l
        sol = {'c':c,'l':l,'h':h,'U':U}
        self.params = params
        self.sol = sol
    def check_solution(self):
        params = self.params
        a, b, w, cmax = params['a'], params['b'], params['w'], params['cmax']
        sol = self.sol
        c, l, h, U = sol['c'], sol['l'], sol['h'], sol['U']
        return (
            (c>cmax/12) and (c<cmax*11/12) and (l>5) and (l<55) and
            is_divisible(cmax, 12) and
            is_divisible(60*w, cmax/12) 
        )
    def general_setup(self):
        return fr"""
An individual can work for up to 60 hours a week at an hourly wage of \(w\). The person has utility over weekly consumption \(c\) and weekly leisure hours \(\ell\) given by:

$$ u(c, \ell) = ac - \frac{{1}}{{2}}c^2 + b \ell $$

The general solution is:

$$ c = a - b/w $$

Hours worked decreases with wage when \(w > 2b/a\)
"""
    def setup(self):
        params = self.params
        a, b, w, cmax = params['a'], params['b'], params['w'], params['cmax']
        ell = r'\ell'
        return fr"""
An individual can work for up to 60 hours a week at an hourly wage of \(w={w:g}\). The person has utility over weekly consumption \(c\) and weekly leisure hours \(\ell\) given by:

$$ u(c, \ell) = {term(a,'c',1,rmplus=True)} - {term(0.5,'c',2,rmplus=True)} + {term(b,ell,1,rmplus=True)} $$
"""
    def graph_with_IC(self, with_solution=False, saveas=None, show=False):
        params = self.params
        a, b, w, cmax = params['a'], params['b'], params['w'], params['cmax']
        sol = self.sol
        c, l, h, U = sol['c'], sol['l'], sol['h'], sol['U']
        fig, ax = plt.subplots()
        lg = np.arange(0, 65.1, 0.1)
        cg = np.arange(0, cmax+cmax/12+0.1, 0.1)
        maxU = a*a - 0.5*a**2 + b*60
        minU = min(a*(cmax/12) - 0.5*(cmax/12)**2 + b*5, a*cmax - 0.5*cmax**2 + b*5)
        dU = (maxU - minU)/12
        minU = U - np.floor((U - minU)/dU)*dU
        for myU in np.arange(minU, maxU+dU, dU):
            indifference_curve = (myU - a*cg + 0.5*cg**2)/b
            ax.plot(indifference_curve, cg, color='green', alpha=0.3, label='_nolegend_')
        if with_solution:
            budget_constraint = (60*w - w*lg)
            ax.plot(lg, budget_constraint, color='black',linewidth=2)
            ax.plot(l,c,'o',color='black',markersize=12)
        ax.set_ylabel(r'Weekly Consumption')
        ax.set_xlabel(r'Weekly Leisure Hours')
        ax.set_xticks(np.arange(0, 65, 5))
        ax.set_yticks(np.arange(0, cmax+cmax/12, cmax/12))
        ax.set_xlim([0, 65])
        ax.set_ylim([0, cmax+cmax/12])
        ax.set_axisbelow(True)
        plt.grid(alpha=0.2)
        if saveas is not None:
            plt.savefig(saveas, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()
        return True
        
"""
WageChangeSate
"""
class WageChangeSate:
    def __init__(self, params=None):
        if not params:
            params = {'a':60*30,'b':20*900,'w1':20,'w2':30,'cmax':1800}
        a, b, w1, w2, cmax = params['a'], params['b'], params['w1'], params['w2'], params['cmax']
        params1 = params.copy()
        params1['w'] = params['w1']
        prob1 = LeisureSate(params1)
        params2 = params.copy()
        params2['w'] = params['w2']
        prob2 = LeisureSate(params2)
        c1, l1 = prob1.sol['c'], prob1.sol['l']
        c2, l2 = prob2.sol['c'], prob2.sol['l']
        sol = {'c1':c1, 'l1':l1, 'c2':c2, 'l2':l2}
        self.params = params
        self.prob1 = prob1
        self.prob2 = prob2
        self.sol = sol
    def check_solution(self):
        params = self.params
        a, b, w1, w2, cmax = params['a'], params['b'], params['w1'], params['w2'], params['cmax']
        sol = self.sol
        c1, l1, c2, l2 = sol['c1'], sol['l1'], sol['c2'], sol['l2']
        return (
            is_divisible(cmax,12) and
            is_divisible(60*w1, cmax/12) and
            is_divisible(60*w2, cmax/12) and
            (l1>5) and (l2>5) and (l1<55) and (l2<55) and
            (np.abs(l1 - l2)>=5)
        )
    def setup(self):
        return self.prob1.setup()
    def graph_with_IC(self, period1=False, period2=False, saveas=None, show=False):
        params = self.params
        a, b, w1, w2, cmax = params['a'], params['b'], params['w1'], params['w2'], params['cmax']
        c1 = self.prob1.sol['c']
        c2 = self.prob2.sol['c']
        l1 = self.prob1.sol['l']
        l2 = self.prob2.sol['l']
        U1 = self.prob1.sol['U']
        U2 = self.prob2.sol['U']
        fig, ax = plt.subplots()
        lg = np.arange(0, 65.1, 0.1)
        cg = np.arange(0, cmax+cmax/12+0.1, 0.1)
        maxU = a*a - 0.5*a**2 + b*60
        minU = min(a*(cmax/12) - 0.5*(cmax/12)**2 + b*5, a*cmax - 0.5*cmax**2 + b*5)
        dU_target = (maxU - minU)/12
        dU_n = np.ceil(np.abs(U2-U1)/dU_target)
        dU = np.abs(U2-U1)/dU_n
        minU = min(U1,U2) - np.floor((min(U1,U2)-minU)/dU)*dU
        for myU in np.arange(minU, maxU+dU, dU):
            indifference_curve = (myU - a*cg + 0.5*cg**2)/b
            ax.plot(indifference_curve, cg, color='green', alpha=0.3, label='_nolegend_')
        legend = []
        if period1:
            budget_constraint = (60*w1 - w1*lg)
            ax.plot(lg, budget_constraint, color='black',linewidth=2)
            ax.plot(l1,c1,'o',color='black',markersize=12,label='_nolegend_')
            ax.text(l1+1,c1+0.2*cmax/12,'A',color='black')
            legend.append(f'Wage Rate = {w1:g}')
        if period2:
            budget_constraint = (60*w2 - w2*lg)
            ax.plot(lg, budget_constraint, color='red',linewidth=2)
            ax.plot(l2,c2,'o',color='red',markersize=12,label='_nolegend_')
            ax.text(l2+1,c2+0.2*cmax/12,'B',color='red')
            legend.append(f'Wage Rate = {w2:g}')
        ax.set_ylabel(r'Weekly Consumption')
        ax.set_xlabel(r'Weekly Leisure Hours')
        ax.set_xticks(np.arange(0, 65, 5))
        ax.set_yticks(np.arange(0, cmax+cmax/12, cmax/12))
        ax.set_xlim([0, 65])
        ax.set_ylim([0, cmax+cmax/12])
        ax.set_axisbelow(True)
        plt.grid(alpha=0.2)
        plt.legend(legend, loc='upper right')
        if saveas is not None:
            plt.savefig(saveas, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()
        return True


"""
Welfare
"""
class Welfare:
    def __init__(self, params=None):
        if not params:
            params = {'nx':2,'dx':3,'ny':1,'dy':3,'w':30,'cmax':1800,'minc':600}
        nx, dx, ny, dy, w, cmax, minc = params['nx'], params['dx'], params['ny'], params['dy'], params['w'], params['cmax'], params['minc']
        a = nx/dx
        b = ny/dy
        params1 = params.copy()
        prob_no_welfare = LeisureCB(params1)
        U_no_welfare = prob_no_welfare.sol['U']
        c_no_welfare = prob_no_welfare.sol['c']
        h_no_welfare = prob_no_welfare.sol['h']
        l_no_welfare = prob_no_welfare.sol['l']
        U_welfare = minc**a * 60**b
        if U_welfare > U_no_welfare:
            U = U_welfare
            c = minc
            l = 60
            h = 0
        else:
            U = U_no_welfare
            c = prob_no_welfare.sol['c']
            h = prob_no_welfare.sol['h']
            l = prob_no_welfare.sol['l']
        sol = {'c':c, 'l':l, 'h':h, 'U':U, 'c_no_welfare':c_no_welfare, 'h_no_welfare':h_no_welfare, 'l_no_welfare':l_no_welfare}
        self.params = params
        self.sol = sol
        self.prob_no_welfare = prob_no_welfare
    def check_solution(self):
        params = self.params
        nx, dx, ny, dy, w, cmax, minc = params['nx'], params['dx'], params['ny'], params['dy'], params['w'], params['cmax'], params['minc']
        sol = self.sol
        c, l, h, U = sol['c'], sol['l'], sol['h'], sol['U']
        return (
            self.prob_no_welfare.check_solution() and
            is_divisible(minc, cmax/12) and
            (minc < 60*w)
        )
    def graph_with_IC(self, with_solution=False, saveas=None, show=False):
        params = self.params
        nx, dx, ny, dy, w, cmax, minc = params['nx'], params['dx'], params['ny'], params['dy'], params['w'], params['cmax'], params['minc']
        sol = self.sol
        c, l, h, U, l_no_welfare, c_no_welfare = sol['c'], sol['l'], sol['h'], sol['U'], sol['l_no_welfare'], sol['c_no_welfare']
        U_no_welfare = self.prob_no_welfare.sol['U']
        a = nx/dx
        b = ny/dy
        fig, ax = plt.subplots()
        lg = np.arange(0, 65.1, 0.1)
        maxU = cmax**a * 60**b
        minU = (cmax/12)**a * 5**b
        dU = (maxU - minU)/12
        minU = U_no_welfare - np.floor((U_no_welfare - minU)/dU)*dU
        for myU in np.arange(minU, maxU+dU, dU):
            indifference_curve = (myU /(lg[1:]**b))**(1/a)
            ax.plot(lg[1:], indifference_curve, color='green', alpha=0.3)
        if with_solution:
            lg1 = np.arange(0, (60*w-minc)/w + 0.1, 0.1)
            lg2 = np.arange((60*w-minc)/w, 60.1, 0.1)
            bc1 = (60*w - w*lg1)
            bc2 = minc*np.ones(lg2.shape)
            bc3 = (60*w - w*lg2)
            ax.plot(lg1, bc1, color='black',linewidth=2)
            ax.plot(lg2, bc2, color='black',linewidth=2)
            ax.plot(lg2, bc3, color='black', linestyle='dashed', linewidth=2)
            ax.plot(l,c,'o',color='red',markersize=12)
            ax.text(l+1,c+0.2*cmax/12,'B',color='red')
            ax.plot(l_no_welfare, c_no_welfare, 'o', color='black', markersize=12)
            ax.text(l_no_welfare-1, c_no_welfare-0.2*cmax/12,'A',color='black',horizontalalignment='right',verticalalignment='top')
        ax.set_ylabel(r'Weekly Consumption')
        ax.set_xlabel(r'Weekly Leisure Hours')
        ax.set_xticks(np.arange(0, 65, 5))
        ax.set_yticks(np.arange(0, cmax+cmax/12, cmax/12))
        ax.set_xlim([0, 65])
        ax.set_ylim([0, cmax+cmax/12])
        ax.set_axisbelow(True)
        plt.grid(alpha=0.2)
        if saveas is not None:
            plt.savefig(saveas, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()
        return True
       

"""
Monopoly
"""
class Monopoly:
    def __init__(self, params=None):
        if not params:
            params = {'Y':100,'alpha':12,'beta':1,'gamma':0,'delta':0,'eta':1}
        params = {k:params[k] for k in ['Y','alpha','beta','gamma','delta','eta']}
        self.params = params
        Y, alpha, beta, gamma, delta, eta = params['Y'], params['alpha'], params['beta'], params['gamma'], params['delta'], params['eta']
        Q = (alpha - delta)/(2*beta + eta)
        p = alpha - beta * Q
        c = 100 - p*Q
        U = c + alpha*Q - 0.5*beta*Q**2
        Profit = p*Q - gamma - delta*Q - 0.5*eta*Q**2
        
        Q_eff = (alpha - delta)/(beta + eta)
        p_eff = alpha - beta*Q_eff
        c_eff = 100 - p_eff*Q_eff
        U_eff = c_eff + alpha*Q_eff - 0.5*beta*Q_eff**2
        Profit_eff = p_eff*Q_eff - gamma - delta*Q_eff - 0.5*eta*Q_eff**2
        
        DWL = (U_eff + Profit_eff) - (U + Profit)
        
        sol = {
            'Q':Q, 'p':p, 'U':U, 'Profit':Profit, 'c':c,
            'Q_eff':Q_eff, 'p_eff':p_eff, 'U_eff':U_eff, 'Profit_eff':Profit_eff, 'c_eff':c_eff,
            'DWL':DWL
        }
        self.sol = sol
        
    def general_setup(self):
        return fr"""
A commodity \(q\) is supplied by a monopolist with total cost function: 

$$ c(q) = \gamma + \delta q + \frac{{1}}{{2}} \eta q^2 $$

A representative consumer with income \(Y\) has a utility function over numeraire consumption \(c\) and commodity \(q\) given by:

$$u(c,q) = c + \alpha q - \frac{{1}}{{2}} \beta q^2 $$

The inverse demand curve is:

$$ p = \alpha - \beta Q $$

The profit maximizing quantity is:

$$ Q = \frac{{\alpha - \delta}}{{ 2\beta + \eta }} $$

The efficient quantity is:

$$ Q = \frac{{\alpha - \delta}}{{ \beta + \eta}} $$
"""
    def setup(self):
        params = self.params
        Y, alpha, beta, gamma, delta, eta = params['Y'], params['alpha'], params['beta'], params['gamma'], params['delta'], params['eta']
        return fr"""
A commodity \(q\) is supplied by a monopolist with cost function: 

$$c(q) = {polyeq('q',[gamma,delta,0.5*eta],[0,1,2])} $$

A representative consumer with income \(Y={Y:g}\) has a utility function over numeraire consumption \(c\) and commodity \(q\) given by:

$$u(c,q) = c + {polyeq('q',[alpha, -0.5*beta],[1,2])} $$
"""
    def check_solution(self):
        sol = self.sol
        return (
            (sol['Q']>0) and 
            (sol['Q_eff']>sol['Q']) and 
            (sol['p']>0) and
            (sol['p_eff']>0) and 
            (sol['c']>0) and
            (sol['c_eff']>0) and 
            (is_divisible(sol['p'],1)) and 
            (is_divisible(sol['Q'],1)) and
            (is_divisible(sol['p_eff'],1)) and 
            (is_divisible(sol['Q_eff'],1))
        )

"""
Price Discrimination
"""
class PriceDiscrimination:
    def __init__(self, params=None):
        if not params:
            params = {'Y1':500,'Y2':500,'alpha1':25,'alpha2':13,'beta1':1,'beta2':1,'gamma':0,'delta':1}
        params = {k:params[k] for k in ['Y1','Y2','alpha1','alpha2','beta1','beta2','gamma','delta']}
        self.params = params
        Y1, Y2, alpha1, alpha2, beta1, beta2, gamma, delta = params['Y1'], params['Y2'], params['alpha1'], params['alpha2'], params['beta1'], params['beta2'], params['gamma'], params['delta']
        q1 = (alpha1 - delta)/(2*beta1)
        q2 = (alpha2 - delta)/(2*beta2)
        p1 = alpha1 - beta1*q1
        p2 = alpha2 - beta2*q2
        profit = p1*q1 + p2*q2 - gamma - delta*(q1+q2)
        c1 = Y1 - p1*q1
        c2 = Y2 - p2*q2
        
        A = (alpha1*beta2 + alpha2*beta1)/(beta1 + beta2)
        B = (beta1*beta2)/(beta1+beta2)
        Q_npd = (A - delta)/(2*B)
        p_npd = A - B*Q_npd
        profit_npd = p_npd*Q_npd - gamma - delta*Q_npd
        q1_npd = alpha1/beta1 - 1/beta1 * p_npd
        q2_npd = alpha2/beta2 - 1/beta2 * p_npd
        c1_npd = Y1 - p_npd * q1_npd
        c2_npd = Y2 - p_npd * q2_npd
        
        corner = False
        if alpha1>alpha2:
            qcorner = q1
            pcorner = alpha1 - beta1*qcorner
            if pcorner>alpha2:
                profit_corner = pcorner*qcorner - gamma - delta*qcorner
                if profit_corner > profit_npd:
                    corner = True
        elif alpha2>alpha1:
            qcorner = q2
            pcorner = alpha2 - beta2*qcorner
            if pcorner>alpha1:
                profit_corner = pcorner*qcorner - gamma - delta*qcorner
                if profit_corner > profit_npd:
                    corner = True
        
        sol = {'q1':q1, 'q2':q2, 'p1':p1, 'p2':p2, 'c1':c1, 'c2':c2, 'profit':profit, 'A':A, 'B':B, 'Q_npd':Q_npd, 'p_npd':p_npd, 'profit_npd':profit_npd, 'q1_npd':q1_npd, 'q2_npd':q2_npd, 'c1_npd':c1_npd, 'c2_npd':c2_npd, 'corner':corner}
        self.sol = sol
    
    def general_setup(self):
        return fr"""
A commodity \(q\) is supplied by a monopolist with total cost function:

$$ c(q) = \gamma + \delta q $$

There are two representative consumers.

Representative consumer 1 has income \(Y\) and utility function over their numeraire consumption \(c\) and their commodity consumption \(q\) given by:

$$ u(c,q) = c + \alpha q - \frac{{1}}{{2}} \beta_1 q^2 $$

Representative consumer 2 has income \(Y\) and utility function over their numeraire consumption \(c\) and their commodity consumption \(q\) given by:

$$ u(c,q) = c + \alpha q - \frac{{1}}{{2}} \beta_2 q^2 $$

The consumers' inverse demand curves are:

$$ p_1 = \alpha_1 - \beta_1 q_1 $$

$$ p_2 = \alpha_2 - \beta_2 q_2 $$

The market inverse demand curve is:

$$ p = \left( \frac{{ \alpha_1 \beta_2 + \alpha_2 \beta_1 }}{{ \beta_1 + \beta_2 }}\right) - \left(\frac{{ \beta_1 \beta_2 }}{{ \beta_1 + \beta_2 }}\right) Q $$

With price discrimination, the solutions are:

$$ q_1 = \frac{{ \alpha_1 - \delta }}{{ 2 \beta_1 }} $$

$$ q_2 = \frac{{ \alpha_2 - \delta }}{{ 2 \beta_2 }} $$

Without price discrimination, the solutions are:

$$ Q = \frac{{ \left( \frac{{ \alpha_1 \beta_2 + \alpha_2 \beta_1 }}{{ \beta_1 + \beta_2 }}\right) - \delta }}{{ 2 \left(\frac{{ \beta_1 \beta_2 }}{{ \beta_1 + \beta_2 }}\right) }} $$
"""
    def setup(self):
        params = self.params
        Y1, Y2, alpha1, alpha2, beta1, beta2, gamma, delta = params['Y1'], params['Y2'], params['alpha1'], params['alpha2'], params['beta1'], params['beta2'], params['gamma'], params['delta']
        return fr"""
A commodity \(q\) is supplied by a monopolist with total cost function:

$$ c(Q) = {polyeq('Q',[gamma,delta],[0,1])} $$

There are two representative consumers.

Representative consumer 1 has income \(Y_1={Y1:g}\) and utility function over their numeraire consumption \(c_1\) and their commodity consumption \(q_1\) given by:

$$ u_1(c_1,q_1) = c_1 + {polyeq('q_1',[alpha1,-0.5*beta1],[1,2])} $$

Representative consumer 2 has income \(Y_2={Y2:g}\) and utility function over their numeraire consumption \(c_2\) and their commodity consumption \(q_2\) given by:

$$ u_2(c_2,q_2) = c_2 + {polyeq('q_2',[alpha2,-0.5*beta2],[1,2])} $$
"""        
    def check_solutions(self):
        sol = self.sol
        return (
            (sol['q1']>0) and (sol['q2']>0) and (sol['p1']>0) and (sol['p2']>0) and
            (sol['c1']>0) and (sol['c2']>0) and 
            (sol['Q_npd']>0) and (sol['p_npd']>0) and (sol['q1_npd']>0) and (sol['q2_npd']>0) and
            (sol['c1_npd']>0) and (sol['c2_npd']>0) and
            (is_divisible(sol['q1'],1)) and 
            (is_divisible(sol['p1'],1)) and 
            (is_divisible(sol['q2'],1)) and
            (is_divisible(sol['p2'],1)) and
            (is_divisible(sol['A'],1)) and
            (sol['corner']==False)
        )

