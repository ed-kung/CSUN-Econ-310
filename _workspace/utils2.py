import numpy as np
import pandas as pd
from sympy import nsimplify
from matplotlib import pyplot as plt
from econtools.documents import MCQ, generate_distractors

rng = np.random.default_rng()

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

def sign(x):
    if x>0: return '+'
    else: return '-'

def is_divisible(p,q):
    d = nsimplify(p/q).q
    return (d==1)

def asfrac(x, inline=False, maxdenom=5, rmplus=True, rmneg=False):
    d = nsimplify(x).q
    assert d<=maxdenom
    n = np.abs(nsimplify(x).p)
    out = sign(x)
    if d==1: out+=f'{n}'
    elif inline: out+=fr'{n}/{d}'
    else: out+=fr'\frac{{{n}}}{{{d}}}'
    if out[0]=='+' and rmplus: out=out[1:]
    elif out[0]=='-' and rmneg: out=out[1:]
    return out
    
class PTerm:
    # cx^p
    def __init__(self,c=1,x='x',p=0.5):
        self.c = c
        self.x = x
        self.p = p
    def print(self, maxdenom=5, rmplus=True, rmneg=False):
        c = asfrac(self.c, inline=False, maxdenom=maxdenom, rmplus=rmplus, rmneg=rmneg)
        p = asfrac(self.p, inline=True, maxdenom=maxdenom, rmplus=True, rmneg=False)
        if self.c==0: return ''
        elif self.p==0: return c
        if self.p==1: xp = fr'{self.x}'
        else: xp = fr'{self.x}^{{{p}}}'
        if self.c==-1: out = fr'-{xp}'
        elif self.c==1: out = fr'+{xp}'
        else: out = fr'{c}{xp}'
        if out[0]=='+' and rmplus: out=out[1:]
        elif out[0]=='-' and rmneg: out=out[1:]
        return out
    def __repr__(self):
        return self.print()

class PolyEq:
    def __init__(self, c=[1,1,1], x='x', p=[0,1,2]):
        assert len(c)==len(p)
        assert type(x)==str or len(x)==len(c)
        if type(x)==str:
            x = [x]*len(c)
        self.c = c
        self.x = x
        self.p = p
    def print(self, maxdenom=5, rmplus=True, rmneg=False):
        out = ''
        for i in range(len(self.c)):
            pterm = PTerm(self.c[i], self.x[i], self.p[i])
            out+=fr'{pterm.print(maxdenom=maxdenom, rmplus=False, rmneg=False)}'
        if out[0]=='+' and rmplus: out=out[1:]
        elif out[0]=='-' and rmneg: out=out[1:]
        return out
    def __repr__(self):
        return self.print()

class Axis:
    def __init__(self, xn=13, yn=13, xunit=1, yunit=1):
        self.xn = xn
        self.yn = yn
        self.xunit = xunit
        self.yunit = yunit
        self.xmax = xn*xunit
        self.ymax = yn*yunit
        self.objects = []
    def add(self, *args):
        for obj in args:
            self.objects.append(obj)
    def get_figax(self, xlab=r'$x$', ylab=r'$y$', alpha=0.4, legend=None):
        fig, ax = plt.subplots()
        for obj in self.objects:
            if type(obj)==Line:
                xg = np.arange(0, self.xmax, self.xunit/10)
                obj.plot(ax, xg)
        ax.set_xticks(np.arange(0, self.xmax, self.xunit))
        ax.set_yticks(np.arange(0, self.ymax, self.yunit))
        ax.set_xlim([0, self.xmax])
        ax.set_ylim([0, self.ymax])
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        ax.set_axisbelow(True)
        ax.grid(alpha=alpha)
        if legend:
            ax.legend()
        return fig, ax
    def on_grid(self,x,y):
        x_on_grid = is_divisible(x,self.xunit) and (x<self.xmax)
        y_on_grid = is_divisible(y,self.yunit) and (y<self.ymax)
        return x_on_grid and y_on_grid

class Line:
    # y = mx + b
    def __init__(self, m, b, linewidth=1, color='black', label='_nolegend_'):
        self.m, self.b = m, b
        self.linewidth = linewidth
        self.color = color
        self.label = label
    def plot(self, ax, xg, color='black', linewidth=2):
        return ax.plot(xg, self.m*xg + self.b, color=self.color, linewidth=self.linewidth, label=self.label)
    
class LinearDemand:
    # p = a - bq
    # q = (a/b) - (1/b)*p
    def __init__(self, a=12, b=1):
        assert a>0
        assert b>0
        self.a = a
        self.b = b
        self.line = Line(-b,a)
    def print(self, x='p', maxdenom=5):
        return PolyEq(c=[self.a/self.b, -1/self.b], x=x, p=[0,1]).print(maxdenom=maxdenom, rmplus=True)
    def print_inverse(self, x='q', maxdenom=5):
        return PolyEq(c=[self.a, -self.b], x=x, p=[0,1]).print(maxdenom=maxdenom, rmplus=True)
    def eval_at_p(p):
        return self.a/self.b - (1/self.b)*p
    def eval_at_q(q):
        return self.a - self.b*q
        
class ExponentialDemand:
    # p = a*q^k
    # q = (1/a)^(1/k) p^(1/k)
    def __init__(self, a=1, k=-1):
        assert a>0
        assert k<0
        self.a = a
        self.k = k
    def print(self, x='p', maxdenom=36):
        c = (1/self.a)**(1/self.k)
        p = 1/self.k
        return PTerm(c=c,x=x,p=p).print(rmplus=True,maxdenom=maxdenom)
    def print_inverse(self, x='q', maxdenom=36):
        c = self.a
        p = self.k
        return PTerm(c=c,x=x,p=p).print(rmplus=True,maxdenom=maxdenom)
    def eval_at_p(p):
        return (1/self.a)**(1/self.k) * p**(1/self.k)
    def eval_at_q(q):
        return self.a * q**self.k
    
class LinearSupply:
    # p = a + bq
    # q = (1/b)*p - (a/b)
    def __init__(self, a=0, b=1):
        assert a>=0
        assert b>0
        self.a = a
        self.b = b
        self.line = Line(b,a)
    def print(self, x='p', maxdenom=5):
        return PolyEq(c=[1/self.b, -self.a/self.b], x=x, p=[1,0]).print(maxdenom=maxdenom, rmplus=True)
    def print_inverse(self, x='q', maxdenom=5):
        return PolyEq(c=[self.a, self.b], x=x, p=[0,1]).print(maxdenom=maxdenom, rmplus=True)
    def eval_at_p(p):
        return (1/self.b)*p - (self.a/self.b)
    def eval_at_q(q):
        return self.a + self.b*q
        
class ExponentialSupply:
    # p = aq^k
    # q = (1/a)^(1/k) p^(1/k)
    def __init__(self, a=1, k=1):
        assert a>0
        assert k>0
        self.a = a
        self.k = k
    def print(self, x='p', maxdenom=36):
        c = (1/self.a)**(1/self.k)
        p = 1/self.k
        return PTerm(c=c,x=x,p=p).print(rmplus=True,maxdenom=maxdenom)
    def print_inverse(self, x='q', maxdenom=36):
        c = self.a
        p = self.k
        return PTerm(c=c,x=x,p=p).print(rmplus=True,maxdenom=maxdenom)
    def eval_at_p(p):
        return (1/self.a)**(1/self.k) * p**(1/self.k)
    def eval_at_q(q):
        return self.a * q**self.k

class LinearMarket:
    # p = ad - bd*q
    # p = as + bs*q
    # q = (ad-as)/(bd+bs)
    def __init__(self, demand=LinearDemand(), supply=LinearSupply()):
        self.demand = demand
        self.supply = supply
        q = (demand.a - supply.a)/(demand.b + supply.b)
        p1 = demand.a - demand.b*q
        p2 = supply.a + supply.b*q
        assert p1==p2
        p = p1
        self.eq = {'q':q, 'p':p}

class ExponentialMarket:
    # p = ad * q^ kd
    # p = as * q^ ks
    # q = (ad/as)^(1/(ks - kd))
    def __init__(self, demand=ExponentialDemand(), supply=ExponentialSupply()):
        self.demand = demand
        self.supply = supply
        q = (demand.a / supply.a)**(1/(supply.k - demand.k))
        assert q>0
        p1 = demand.a * q**demand.k
        p2 = supply.a * q**supply.k
        assert np.abs(p1-p2)<0.001*np.abs(p1)
        p = p1
        assert p>0
        self.eq = {'q':q, 'p':p}

class GenericProblem:
    def __init__(self, params, default_params, rng=rng, name="generic_problem"):
        self.name = name
        if not params:
            params = default_params.copy()
        self.params = {}
        for k in default_params.keys():
            if k in params.keys():
                self.params[k] = params[k]
            else:
                self.params[k] = default_params[k]
    def show_setups(self):
        i=0
        for s in self.setup_list:
            print(f'{i}: ', end='')
            print(s)
            i+=1
    def show_questions(self):
        i=0
        for q in self.question_list:
            print(f'{i}: ', end='')
            print(q)
            i+=1

class LinearMarketProblem(GenericProblem):
    def __init__(self, params=None, rng=rng):
        default_params = {'ad':12,'bd':1,'as':0,'bs':1,'xunit':1,'yunit':1,'xn':13,'yn':13}
        GenericProblem.__init__(self, params, default_params, rng)
        params = self.params
        demand = LinearDemand(a=params['ad'], b=params['bd'])
        supply = LinearSupply(a=params['as'], b=params['bs'])
        market = LinearMarket(demand, supply)
        axis = Axis(xn=params['xn'],yn=params['yn'],xunit=params['xunit'],yunit=params['yunit'])
        demand.line.color = 'blue'
        supply.line.color = 'red'
        axis.add(demand.line, supply.line)
        setup_list = []
        setup = fr"""
Supply and demand in a market are defined by the following equations:
\begin{{align*}}
q_d &= {demand.print()} \\
q_s &= {supply.print()} 
\end{{align*}}
"""
        online_setup = fr"""
Supply and demand in a market are defined by the following equations:
$$\begin{{align}}
q_d &= {demand.print()} \\
q_s &= {supply.print()}
\end{{align*}}$$
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = "Calculate the equilibrium price."
        ans = market.eq['p']
        answers = generate_distractors(ans,rng=rng)
        question_list.append({
            "question": question,
            "answer": ans,
            "online_answer": fr"$$p = {ans:g}$$",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "Calculate the equilibrium quantity."
        ans = market.eq['q']
        answers = generate_distractors(ans,rng=rng)
        question_list.append({
            "question": question,
            "answer": ans,
            "online_answer": fr"$$q = {ans:g}$$",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list

class ExponentialMarketProblem(GenericProblem):
    def __init__(self, params=None, rng=rng):
        default_params = {'ad':6,'kd':-0.5,'as':1,'ks':2}
        GenericProblem.__init__(self, params, default_params, rng)
        params = self.params
        demand = ExponentialDemand(a=params['ad'], k=params['kd'])
        supply = ExponentialSupply(a=params['as'], k=params['ks'])
        market = ExponentialMarket(demand, supply)
        setup_list = []
        setup = fr"""
Supply and demand in a market are defined by the following equations:
\begin{{align*}}
q_d &= {demand.print()} \\
q_s &= {supply.print()} 
\end{{align*}}
"""
        online_setup = fr"""
Supply and demand in a market are defined by the following equations:
$$\begin{{align}}
q_d &= {demand.print()} \\
q_s &= {supply.print()}
\end{{align*}}$$
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = "Calculate the equilibrium price."
        ans = market.eq['p']
        answers = generate_distractors(ans,rng=rng)
        question_list.append({
            "question": question,
            "answer": ans,
            "online_answer": fr"$$p = {ans:g}$$",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "Calculate the equilibrium quantity."
        ans = market.eq['q']
        answers = generate_distractors(ans,rng=rng)
        question_list.append({
            "question": question,
            "answer": ans,
            "online_answer": fr"$$q = {ans:g}$$",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list


        


        
        
        