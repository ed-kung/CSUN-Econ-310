import numpy as np
import pandas as pd
import sympy
from sympy import nsimplify
from matplotlib import pyplot as plt
from econtools.documents import Multipart, MCQ, generate_distractors, RawLatex

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

###################################################################
# MATH UTILITIES
###################################################################
def sign(x):
    if x>0: return '+'
    else: return '-'

def equals(x,y,tol=1e-4):
    return np.abs(x-y)<tol

def is_rational(x, maxdenom=8):
    try:
        d = nsimplify(x).q
        return (d<=maxdenom)
    except:
        return False

def is_divisible(p,q):
    if not is_rational(p/q,30):
        return False
    d = nsimplify(p/q).q
    return (d==1)

def asfrac(x, inline=False, maxdenom=8, rmplus=True, rmneg=False):
    if not is_rational(x, maxdenom):
        return f'{x:g}'
    d = nsimplify(x).q
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
    def print(self, maxdenom=8, rmplus=True, rmneg=False):
        c = asfrac(self.c, inline=False, maxdenom=maxdenom, rmplus=rmplus, rmneg=rmneg)
        p = asfrac(self.p, inline=True, maxdenom=maxdenom, rmplus=True, rmneg=False)
        if self.c==0: return ''
        if self.p==0: return c
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
    def print(self, maxdenom=8, rmplus=True, rmneg=False):
        out = ''
        for i in range(len(self.c)):
            pterm = PTerm(self.c[i], self.x[i], self.p[i])
            out+=fr'{pterm.print(maxdenom=maxdenom, rmplus=False, rmneg=False)}'
        if out[0]=='+' and rmplus: out=out[1:]
        elif out[0]=='-' and rmneg: out=out[1:]
        return out
    def __repr__(self):
        return self.print()

class CobbDouglas:
    def __init__(self, A=1, x='x', a=1/2, y='y', b=1/2):
        self.A, self.x, self.a, self.y, self.b = A, x, a, y, b
    def print(self, maxdenom=8, rmplus=True, rmneg=False):
        out = PTerm(self.A, self.x, self.a).print(maxdenom=maxdenom,rmplus=rmplus,rmneg=rmneg)
        out+= PTerm(1, self.y, self.b).print(maxdenom=maxdenom,rmplus=True,rmneg=True)
        return out
    def __repr__(self):
        return self.print()

def simplifyCB(cbtop, cbbot):
    assert cbtop.a!=0
    assert cbtop.b!=0
    assert equals( np.abs(cbtop.a)+np.abs(cbbot.a), 1)
    assert equals( np.abs(cbtop.b)+np.abs(cbbot.b), 1)
    assert sign(cbtop.a)!=sign(cbtop.b)
    assert cbtop.x==cbbot.x
    assert cbtop.y==cbbot.y
    assert is_rational(cbtop.A/cbbot.A, maxdenom=cbbot.A)
    x = cbtop.x
    y = cbtop.y
    a = cbtop.a
    n = nsimplify(cbtop.A/cbbot.A).p
    d = nsimplify(cbtop.A/cbbot.A).q
    if a>0:
        return fr"\(\frac{{{PTerm(n,x,1).print()}}}{{{PTerm(d,y,1).print()}}}\)"
    else:
        return fr"\(\frac{{{PTerm(n,y,1).print()}}}{{{PTerm(d,x,1).print()}}}\)"

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
    def get_figax(self, xlab=r'$x$', ylab=r'$y$', alpha=0.4, saveas=None):
        fig, ax = plt.subplots()
        ax.set_xticks(np.arange(0, self.xmax, self.xunit))
        ax.set_yticks(np.arange(0, self.ymax, self.yunit))
        ax.set_xlim([0, self.xmax])
        ax.set_ylim([0, self.ymax])
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        ax.set_axisbelow(True)
        ax.grid(alpha=alpha)
        if saveas is not None:
            plt.savefig(saveas, bbox_inches='tight')
        return fig, ax
    def draw(self, xlab=r'$x$', ylab=r'$y$', alpha=0.4, legend=None, saveas=None):
        fig, ax = self.get_figax(xlab=xlab, ylab=ylab, alpha=alpha)
        for obj in self.objects:
            if type(obj)==Line:
                xg = np.arange(0, self.xmax, self.xunit/10)
                obj.plot(ax, xg)
        if legend:
            ax.legend()
        if saveas is not None:
            plt.savefig(saveas, bbox_inches='tight')
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
    
###################################################################
# ECONOMIC MODELS
###################################################################

class LinearDemand:
    # p = a - bq
    # q = (a/b) - (1/b)*p
    def __init__(self, a=12, b=1):
        assert a>0
        assert b>0
        self.a = a
        self.b = b
        self.line = Line(-b,a)
    def print(self, x='p', maxdenom=8):
        return PolyEq(c=[self.a/self.b, -1/self.b], x=x, p=[0,1]).print(maxdenom=maxdenom, rmplus=True)
    def print_inverse(self, x='q', maxdenom=8):
        return PolyEq(c=[self.a, -self.b], x=x, p=[0,1]).print(maxdenom=maxdenom, rmplus=True)
    def eval_at_p(self, p):
        return self.a/self.b - (1/self.b)*p
    def eval_at_q(self, q):
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
    def eval_at_p(self, p):
        return (1/self.a)**(1/self.k) * p**(1/self.k)
    def eval_at_q(self, q):
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
    def print(self, x='p', maxdenom=8):
        return PolyEq(c=[1/self.b, -self.a/self.b], x=x, p=[1,0]).print(maxdenom=maxdenom, rmplus=True)
    def print_inverse(self, x='q', maxdenom=5):
        return PolyEq(c=[self.a, self.b], x=x, p=[0,1]).print(maxdenom=maxdenom, rmplus=True)
    def eval_at_p(self, p):
        return (1/self.b)*p - (self.a/self.b)
    def eval_at_q(self, q):
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
    def eval_at_p(self, p):
        return (1/self.a)**(1/self.k) * p**(1/self.k)
    def eval_at_q(self, q):
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
        assert equals(p1,p2)
        p = p1
        CS = 0.5*(demand.a - p)*q
        PS = 0.5*(p - supply.a)*q
        self.eq = {'q':q, 'p':p, 'CS': CS, 'PS': PS, 'TS':CS+PS}

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
        assert equals(p1,p2)
        p = p1
        assert p>0
        self.eq = {'q':q, 'p':p}

class LinearConsumer:
    # u(q) = aq - 0.5bq^2 - pq
    # inv.demand: p = a - bq
    def __init__(self, a=12, b=1):
        demand = LinearDemand(a=a,b=b)
        self.a, self.b = a, b
        self.demand = demand
    def print_utility(self, q='q'):
        a, b = self.a, self.b
        return fr"{PolyEq([a,-0.5*b],q,[1,2])} - p{q}"
    def setup(self):
        return fr"""
A representative, price-taking consumer decides how many units, \(q\), of a commodity to purchase at unit price \(p\). The utility
they receive for purchasing \(q\) units at price \(p\) is:
$$ u(q) = {self.print_utility()} $$
"""
    def utility_at(self, p,q):
        a, b = self.a, self.b
        return a*q - 0.5*b*q**2 - p*q

class LogConsumer:
    # u(q) = a ln(q) - pq
    # inv.demand: p = a - bq
    def __init__(self, a=1):
        demand = ExponentialDemand(a=a,k=-1)
        self.a = a
        self.demand = demand
    def print_utility(self, q='q'):
        a = self.a
        return fr"{PTerm(a,fr'\ln {q}',1)} - p{q}"
    def setup(self):
        return fr"""
A representative, price-taking consumer decides how many units, \(q\), of a commodity to purchase at unit price \(p\). The utility
they receive for purchasing \(q\) units at price \(p\) is:
$$ u(q) = {self.print_utility()} $$
"""
    def utility_at(self, p,q):
        a = self.a
        return a*np.log(q) - p*q

class QuadraticCostFirm:
    # c(q) = aq + 0.5*bq^2
    # inv.supply: p = a + bq
    def __init__(self, a=0, b=1):
        assert a>0 or b>0
        supply = LinearSupply(a=a,b=b)
        self.a, self.b = a, b
        self.supply = supply
    def print_cost_function(self, q='q'):
        a, b = self.a, self.b
        return fr"{PolyEq([a,0.5*b],q,[1,2])}"
    def setup(self):
        return fr"""
A representative, price-taking firm decides how many units, \(q\), of a commodity to produce and sell at unit price \(p\). The
firm's total cost function for producing \(q\) units is:
$$ c(q) = {self.print_cost_function()} $$
"""
    def profit_at(self,p,q):
        a, b = self.a, self.b
        return p*q - a*q - 0.5*b*q**2

class Worker:
    # u(L) = wL - d*L^k
    def __init__(self, d=0.5, k=2):
        self.d, self.k = d, k
        supply = ExponentialSupply(a=k*d, k=k-1)
        self.supply = supply
    def print_objective(self, w='w', L='L'):
        d, k = self.d, self.k
        wL = f'{w}{L}'
        return fr"{PolyEq([1,-d],[wL,L],[1,k])}"
    def setup(self):
        return fr"""
A representative, price-taking worker decides how many units, \(L\), of labor to supply (e.g. how many hours to work), at a unit wage \(w\).
The worker's utility function over working \(L\) labor-units at wage \(w\) is:

$$ u(L) = {self.print_objective()} $$
"""
    def utility_at(self, w, L):
        d, k = self.d, self.k
        return w*L - d*L**k

class ExponentialProductionFirm:
    # f(L) = AL^k 
    # Pi = AL^k - wL
    # c(q) = (1/A)^(1/k) q^(1/k)
    # w = k*A*L^(k-1)
    def __init__(self, A=1, k=1/2):
        self.A, self.k = A, k
        self.labor_demand = ExponentialDemand(a=k*A, k=k-1)
        if k==1/2:
            b = 2*(1/A)**(1/k)
            self.quadratic_firm = QuadraticCostFirm(0, b)
            self.commodity_supply = self.quadratic_firm.supply
    def print_production_func(self, L='L'):
        A, k = self.A, self.k
        return fr"{PolyEq([A],L,[k])}"
    def setup(self):
        return fr"""
A representative, price-taking firm hires labor at a constant wage rate \(w\). If the firm employs \(L\) units of labor, it can produce \(f(L)\) units of commodity output, where:

$$ f(L) = {self.print_production_func()} $$
"""
    def profit_at(self, w, L):
        A, k = self.A, self.k
        return A*L**k - w*L
        
###################################################################
# PROBLEM GENERATION UTILITIES
###################################################################

def get_online_format(problem, setup_id=None, question_ids=None):
    if setup_id is None or question_ids is None:
        print("Please select a setup_id and a list of question_ids:\n")
        print("Setups:")
        problem.show_setups()
        print("\nQuestions:")
        problem.show_questions()
        return None
    setup = problem.setup_list[setup_id]['online_setup']
    if len(setup)>0:
        setup = '<p>'+setup+'</p>\n'
    else:
        setup = ''
    solution = ''
    i=1
    for qid in question_ids:
        setup+=f'<p>{i}. ' + problem.question_list[qid]['online_question'] + '</p>\n'
        solution+=f'<p>{i}. ' + problem.question_list[qid]['online_answer'] + '</p>\n'
        i+=1
    return {'setup': setup, 'solution': solution}

def get_multipart(problem, setup_id=None, question_ids=None):
    if setup_id is None or question_ids is None:
        print("Please select a setup_id and a list of question_ids:\n")
        print("Setups:")
        problem.show_setups()
        print("\nQuestions:")
        problem.show_questions()
        return None
    multipart = Multipart()
    setup = problem.setup_list[setup_id]['setup']
    assert len(setup)>0
    multipart.add(RawLatex(setup))
    for qid in question_ids:
        multipart.add(problem.question_list[qid]['MCQ'])
    return multipart
    
def get_single(problem, setup_id=None, question_id=None):
    if setup_id is None or question_id is None:
        print("Please select a setup_id and a list of question_ids:\n")
        print("Setups:")
        problem.show_setups()
        print("\nQuestions:")
        problem.show_questions()
        return None
    setup = problem.setup_list[setup_id]['setup']
    mcq = problem.question_list[question_id]['MCQ']
    if len(setup)>0:
        mcq.question = setup + "\n\n" + mcq.question
    return mcq

class GenericProblem:
    def __init__(self, params, default_params, rng=rng, name="generic_problem"):
        self.name = name
        self.sol = {}
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
    def check_solution(self):
        return True

class LinearMarketProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='linear_market_problem'):
        default_params = {'ad':12,'bd':1,'as':0,'bs':1,'xunit':1,'yunit':1,'xn':13,'yn':13}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
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
\end{{align}}$$
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
            "online_question": question,
            "answer": ans,
            "online_answer": fr"\(p = {ans:g}\)",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "Calculate the equilibrium quantity."
        ans = market.eq['q']
        answers = generate_distractors(ans,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": ans,
            "online_answer": fr"\(q = {ans:g}\)",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"""
Draw the supply and demand diagram using the provided grid:
\begin{{center}}
\includegraphics[width=3in]{{{name}_blank.png}}
\end{{center}}
"""
        online_question = f'Draw the supply and demand diagram using the provided grid:<p><img src="/CSUN-Econ-310/assets/images/graphs/{name}_blank.png"></p>'
        answer = fr"""
\begin{{center}}
\includegraphics[width=3in]{{{name}.png}}
\end{{center}}
"""
        online_answer = f'<img src="/CSUN-Econ-310/assets/images/graphs/{name}_sol.png">'
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": None
        })
        question = "Calculate the consumer surplus."
        ans = market.eq['CS']
        answers = generate_distractors(ans,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": ans,
            "online_answer": fr"\(CS = {ans:g}\)",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "Calculate the producer surplus."
        ans = market.eq['PS']
        answers = generate_distractors(ans,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": ans,
            "online_answer": fr"\(PS = {ans:g}\)",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        self.demand = demand
        self.supply = supply
        self.market = market
        self.sol = market.eq.copy()
        self.axis = axis
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        ok = True
        ok = ok and self.axis.on_grid(self.market.eq['p'], self.market.eq['q'])
        ok = ok and self.axis.on_grid(0, self.demand.a)
        ok = ok and self.axis.on_grid(0, self.supply.a)
        return ok

class ExponentialMarketProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='exponential_market_problem'):
        default_params = {'ad':6,'kd':-0.5,'as':1,'ks':2}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
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
\end{{align}}$$
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        setup = fr"""
A market's inverse demand curve and inverse supply curve are defined by the following equations:
\begin{{align*}}
p &= {demand.print_inverse(x='q_d')} \\
p &= {supply.print_inverse(x='q_s')} 
\end{{align*}}
"""
        online_setup = fr"""
A market's inverse demand curve and inverse supply curve are defined by the following equations:
$$\begin{{align}}
p &= {demand.print_inverse(x='q_d')} \\
p &= {supply.print_inverse(x='q_s')}
\end{{align}}$$
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
            "online_question": question,
            "answer": ans,
            "online_answer": fr"\(p = {ans:g}\)",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "Calculate the equilibrium quantity."
        ans = market.eq['q']
        answers = generate_distractors(ans,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": ans,
            "online_answer": fr"\(q = {ans:g}\)",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        self.demand = demand
        self.supply = supply
        self.market = market
        self.sol = market.eq.copy()
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if not is_rational((1/self.demand.a)**(1/self.demand.k)): return False
        if not is_rational((1/self.supply.a)**(1/self.supply.k)): return False
        return True

class ExponentialRewriteProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='exponential_rewrite_problem'):
        default_params = {'a':2,'k':-0.5,'y':4}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        a, k, y = params['a'], params['k'], params['y']
        x = (1/a)**(1/k) * y**(1/k)
        self.sol = {'x':x}
        func = fr"y = {PolyEq([a],'x',[k])}"
        c = asfrac(1/a, inline=False)
        invk = asfrac(1/k, inline=True)
        inv =             fr"\(x = \left({c}\right)^{{{invk}}} y^{{{invk}}}\)"
        inv_distractor1 = fr"\(x = {c} y^{{{invk}}}\)"
        c = asfrac(1/a, inline=False)
        invk = asfrac(-1/k, inline=True)
        inv_distractor2 = fr"\(x = \left({c}\right)^{{{invk}}} y^{{{invk}}}\)"
        c = asfrac(a, inline=False)
        invk = asfrac(1/k, inline=True)
        inv_distractor3 = fr"\(x = \left({c}\right)^{{{invk}}} y^{{{invk}}}\)"
        setup_list = []
        setup = fr"""
$$ {func} $$
"""
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"Write \(x\) as a function of \(y\)."
        online_question = question
        answer = inv
        online_answer = answer
        answers = [inv, inv_distractor1, inv_distractor2, inv_distractor3]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        question = fr"Calculate \(x\) when \(y={params['y']:g}\)."
        online_question = question
        answer = x
        online_answer = fr"\(x = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,horz=True,sort=True,numerical=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if self.sol['x']<0.1: return False
        return True

class CobbDouglasSimplifyProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='cobbdouglas_simplify_problem'):
        default_params = {'x':'x','y':'y','A':4,'B':12,'a':1/3,'b':-2/3}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        x, y, A, B, a, b = self.params['x'], self.params['y'], self.params['A'], self.params['B'], self.params['a'], self.params['b']
        assert A!=B
        assert a!=0
        assert b!=0
        assert sign(a)!=sign(b)
        cbtop = CobbDouglas(A,x,a,y,b)
        if (a>0):
            cbbot = CobbDouglas(B,x,a-1,y,b+1)
        else:
            cbbot = CobbDouglas(B,x,a+1,y,b-1)
        answer = simplifyCB(cbtop,cbbot)
        distractor1 = simplifyCB(CobbDouglas(B,x,cbtop.a,y,cbtop.b),CobbDouglas(A,x,cbbot.a,y,cbbot.b))
        distractor2 = simplifyCB(CobbDouglas(A,x,cbtop.b,y,cbtop.a),CobbDouglas(B,x,cbbot.b,y,cbbot.a))
        distractor3 = simplifyCB(CobbDouglas(B,x,cbtop.b,y,cbtop.a),CobbDouglas(A,x,cbbot.b,y,cbbot.a))
        setup_list = []
        setup_list.append({
            'setup':'',
            'online_setup':''
        })
        question_list = []
        question = fr"""
Simplify:
$$ \frac{{{cbtop.print()}}}{{{cbbot.print()}}} $$
"""
        online_question = question
        answer = answer
        online_answer = answer
        answers = [
            answer,
            distractor1,
            distractor2,
            distractor3
        ]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,horz=True,rng=rng)
        })
        self.cbtop = cbtop
        self.cbbot = cbbot
        self.setup_list = setup_list
        self.question_list = question_list
        
class LogDifferencesProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='log_differences_problem'):
        default_params = {'delta':0.05}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        delta = params['delta']
        assert delta!=0
        setup_list = []
        setup = fr"$$\ln y - \ln x = {delta:g}$$"
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"Is \(y\) larger or smaller than \(x\)?"
        online_question = question
        answers = ["larger", "smaller"]
        if delta>0:
            answer = "larger"
            online_answer = "larger"
            sol = 0
        else:
            answer = "smaller"
            online_answer = "smaller"
            sol = 1
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,sol,shuffle=False,horz=True,rng=rng)
        })
        question = fr"By how much?"
        online_question = question
        answer = fr"\({np.abs(delta)*100:g}\%\)"
        online_answer = answer
        answers = [
            answer,
            fr"\({np.abs(delta):g}\%\)",
            fr"\({np.abs(delta)*10:g}\%\)",
            fr"\({np.abs(delta)*1000:g}\%\)"
        ]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,horz=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
        self.delta = delta
        
class LinearConsumerProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='linear_consumer_problem'):
        default_params = {'a':12,'b':1,'p':6}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        a, b, p = params['a'], params['b'], params['p']
        consumer = LinearConsumer(a,b)
        q = consumer.demand.eval_at_p(p)
        U = consumer.utility_at(p,q)
        self.sol = {'q':q, 'U':U}
        
        foc =             fr"\( {PolyEq([a,-b],'q',[0,1]).print()} - p = 0 \)"
        foc_distractor1 = fr"\( {PolyEq([a,-0.5*b],'q',[0,1]).print()} - p = 0 \)"
        foc_distractor2 = fr"\( {PolyEq([a,-b],'q',[0,1]).print()} = 0 \)"
        foc_distractor3 = fr"\( {PolyEq([a,b],'q',[0,1]).print()} - p = 0 \)"
        
        demand_curve =             fr"\( q_d = {PolyEq([a/b,-1/b],'p',[0,1])} \)"
        demand_curve_distractor1 = fr"\( q_d = {PolyEq([a/b,1/b],'p',[0,1])} \)"
        demand_curve_distractor2 = fr"\( q_d = {PolyEq([a],'p',[-1])}\)"
        demand_curve_distractor3 = rng.choice([
            fr"\(q_d = {PolyEq([2*a/b,-2/b],'p',[0,1])}\)",
            fr"\(q_d = {PolyEq([0.5*a/b,-0.5/b],'p',[0,1])}\)"
        ])
        
        setup_list = []
        setup = consumer.setup()
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = "Write down the consumer's first order condition."
        online_question = question
        answer = foc
        online_answer = answer
        answers = [foc, foc_distractor1, foc_distractor2, foc_distractor3]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        question = "Write down the consumer's demand curve."
        online_question = question
        answer = demand_curve
        online_answer = answer
        answers = [demand_curve, demand_curve_distractor1, demand_curve_distractor2, demand_curve_distractor3]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        question = fr"Calculate the choice of \(q\) that maximizes utility when price is \(p={p:g}\)."
        online_question = question
        answer = q
        online_answer = fr"\(q = {answer}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = fr"Calculate the maximum utility attained when price is \(p={p:g}\)."
        online_question = question
        answer = U
        online_answer = fr"\(U = {answer}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        self.consumer = consumer
        self.setup_list = setup_list
        self.question_list = question_list

class LogConsumerProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='log_consumer_problem'):
        default_params = {'a':12,'p':2}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        a, p = params['a'], params['p']
        consumer = LogConsumer(a)
        q = consumer.demand.eval_at_p(p)
        U = consumer.utility_at(p,q)
        self.sol = {'q':q, 'U':U}
        
        foc =             fr"\({PolyEq([a,-1],['q','p'],[-1,1])} = 0 \)"
        foc_distractor1 = fr"\({PolyEq([a,0],['q','p'],[-1,1])} = 0 \)"
        foc_distractor2 = fr"\({PolyEq([a,-1],['q','p'],[1,1])} = 0 \)"
        foc_distractor3 = fr"\({PolyEq([a,-1,-1],['q','q','p'],[0,1,1])} = 0 \)"

        demand_curve =             fr"\(q_d = {PolyEq([a],'p',[-1])}) \)"
        demand_curve_distractor1 = fr"\(q_d = {PolyEq([a,-1],'p',[0,1])} \)"
        demand_curve_distractor2 = fr"\(q_d = {PolyEq([1/a],'p',[-1]).print(maxdenom=a)} \)"
        demand_curve_distractor3 = fr"\(q_d = {PolyEq([a],'e^{-p}',[1])}\)"
        
        demand_curve = fr"\(q_d = {consumer.demand.print()}\)"
        setup_list = []
        setup = consumer.setup()
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = "Write down the consumer's first order condition."
        online_question = question
        answer = foc
        online_answer = answer
        answers = [foc, foc_distractor1, foc_distractor2, foc_distractor3]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        question = "Write down the consumer's demand curve."
        online_question = question
        answer = demand_curve
        online_answer = answer
        answers = [demand_curve, demand_curve_distractor1, demand_curve_distractor2, demand_curve_distractor3]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        question = fr"Calculate the choice of \(q\) that maximizes utility when price is \(p={p:g}\)."
        online_question = question
        answer = q
        online_answer = fr"\(q = {answer}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = fr"Calculate the maximum utility attained when price is \(p={p:g}\)."
        online_question = question
        answer = U
        online_answer = fr"\(U = {answer}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        self.consumer = consumer
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if self.sol['U']<=0: return False
        return True

class QuadraticCostFirmProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='quadratic_cost_firm_problem'):
        default_params = {'a':0,'b':1,'p':6}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        a, b, p = params['a'], params['b'], params['p']
        producer = QuadraticCostFirm(a,b)
        q = producer.supply.eval_at_p(p)
        profit = producer.profit_at(p,q)
        self.sol = {'q':q, 'profit':profit}

        obj =             fr"\(\Pi = {PolyEq([1,-a,-0.5*b],['pq','q','q'],[1,1,2])} \)"
        obj_distractor1 = fr"\(\Pi = {PolyEq([1,-a,0.5*b],['pq','q','q'],[1,1,2])} \)"
        obj_distractor2 = fr"\(\Pi = {PolyEq([1,-a,0.5*b],['p','q','q'],[1,1,2])} \)"
        obj_distractor3 = fr"\(\Pi = {PolyEq([1,-a,-0.5*b],['p','q','q'],[1,1,2])} \)"
        
        foc =             fr"\({PolyEq([1,-a,-b],['p','','q'],[1,0,1])} = 0 \)"
        foc_distractor1 = fr"\({PolyEq([1,-b],['p',''],[1,0])} = 0\)"
        foc_distractor2 = fr"\({PolyEq([1,-a,b],['p','','q'],[1,0,1])} = 0\)"
        foc_distractor3 = fr"\({PolyEq([1,-a,-b],['pq','','q'],[1,0,1])} = 0\)"

        supply_curve =             fr"\(q_s = {PolyEq([1/b,-a/b],'p',[1,0])}\)"
        supply_curve_distractor1 = fr"\(q_s = {PolyEq([a/b,-1/b],'p',[0,1])}\)"
        supply_curve_distractor2 = fr"\(q_s = {PolyEq([1/b,-a/b],'p',[-1,0])}\)"
        supply_curve_distractor3 = rng.choice([
            fr"\(q_s = {PolyEq([2/b,-2*a/b],'p',[1,0])}\)",
            fr"\(q_s = {PolyEq([0.5/b,-0.5*a/b],'p',[1,0])}\)"
        ])
        
        setup_list = []
        setup = producer.setup()
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = "Write down the firm's profit function."
        online_question = question
        answer = obj
        online_answer = answer
        answers = [obj, obj_distractor1, obj_distractor2, obj_distractor3]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        question = "Write down the firm's first order condition."
        online_question = question
        answer = foc
        online_answer = answer
        answers = [foc, foc_distractor1, foc_distractor2, foc_distractor3]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        question = "Write down the firm's supply curve."
        online_question = question
        answer = supply_curve
        online_answer = answer
        answers = [supply_curve, supply_curve_distractor1, supply_curve_distractor2, supply_curve_distractor3]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        question = fr"Calculate the choice of \(q\) that maximizes profit when price is \(p={p:g}\)."
        online_question = question
        answer = q
        online_answer = fr"\(q = {answer}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = fr"Calculate the maximum profit attained when price is \(p={p:g}\)."
        online_question = question
        answer = profit
        online_answer = fr"\(U = {answer}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        self.producer = producer
        self.setup_list = setup_list
        self.question_list = question_list

class QuadraticOptimizationProblem(GenericProblem):
    # f(x) = ax - 0.5*bx^2 + c
    def __init__(self, params=None, rng=rng, name='quadratic_optimization_problem'):
        default_params = {'a':12,'b':1,'c':0}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        a, b, c = params['a'], params['b'], params['c']
        x = a/b
        f = a*x - 0.5*x**2 + c
        self.sol = {'x':x, 'f':f}
        
        foc =             fr"\(f^\prime(x) = {PolyEq([a,    -b],'x',[0,1])} \)"
        foc_distractor1 = fr"\(f^\prime(x) = {PolyEq([a,     b],'x',[0,1])} \)"
        foc_distractor2 = fr"\(f^\prime(x) = {PolyEq([a+c,  -b],'x',[0,1])} \)"
        foc_distractor3 = fr"\(f^\prime(x) = {PolyEq([a,-0.5*b],'x',[0,1])} \)"

        setup_list = []
        setup = fr"""
$$f(x) = {PolyEq([a,-0.5*b,c],'x',[1,2,0])}$$
"""
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"What is the first derivative of \(f(x)\)?"
        online_question = question
        answer = foc
        online_answer = answer
        answers = [foc, foc_distractor1, foc_distractor2, foc_distractor3]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        question = fr"What is the value of \(x\) that maximizes \(f(x)\)?"
        online_question = question
        answer = x
        online_answer = fr"\(x = {x:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = fr"What is the maximum value of \(f(x)\)?"
        online_question = question
        answer = f
        online_answer = fr"\(f(x) = {f:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
        
class LinearCommodityMarketProblem(GenericProblem):
    # u = ac*q - 0.5*bcq^2 - pq
    # pi = p*q - af*q - 0.5*bf*q^2
    def __init__(self, params=None, rng=rng, name='linear_commodity_market_problem'):
        default_params = {'ac':12,'bc':1,'af':0,'bf':1}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        ac, bc, af, bf = params['ac'], params['bc'], params['af'], params['bf']
        consumer = LinearConsumer(ac, bc)
        producer = QuadraticCostFirm(af, bf)
        market = LinearMarket(consumer.demand, producer.supply)
        q = market.eq['q']
        p = market.eq['p']
        U = consumer.utility_at(p, q)
        profit = producer.profit_at(p, q)
        self.sol = {'q':q, 'p':p, 'U':U, 'profit':profit}
        linear_consumer_problem = LinearConsumerProblem(params={'a':ac,'b':bc,'p':p}, rng=rng)
        linear_producer_problem = QuadraticCostFirmProblem(params={'a':af,'b':bf,'p':p}, rng=rng)
        setup_list = []
        setup = fr"""
{consumer.setup()}

{producer.setup()}
"""
        online_setup = fr"""
<p>{consumer.setup()}</p>

<p>{producer.setup()}</p>
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question_list.append(linear_consumer_problem.question_list[1])
        question_list.append(linear_producer_problem.question_list[2])
        question = "Calculate the equilibrium price."
        online_question = question
        answer = p
        online_answer = fr"\(p = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = "Calculate the equilibrium quantity."
        online_question = question
        answer = q
        online_answer = fr"\(q = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = "Calculate the consumer surplus (i.e. utility) in equilibrium."
        online_question = question
        answer = U
        online_answer = fr"\(CS = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = "Calculate the producer surplus (i.e. profit) in equilibrium."
        online_question = question
        answer = profit
        online_answer = fr"\(PS = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        self.consumer = consumer
        self.producer = producer
        self.market = market
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if self.sol['q']<=0: return False
        if self.sol['p']<=0: return False
        return True
        
class ExponentialCommodityMarketProblem(GenericProblem):
    # u = a*ln(q) - pq
    # pi = p*q - 0.5*bf*q^2
    def __init__(self, params=None, rng=rng, name='linear_commodity_market_problem'):
        default_params = {'a':12,'b':1}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        a, b = self.params['a'], self.params['b']
        consumer = LogConsumer(a)
        producer = QuadraticCostFirm(0, b)
        producer.supply = ExponentialSupply(b, 1)
        market = ExponentialMarket(consumer.demand, producer.supply)
        q = market.eq['q']
        p = market.eq['p']
        U = consumer.utility_at(p, q)
        profit = producer.profit_at(p, q)
        self.sol = {'q':q, 'p':p, 'U':U, 'profit':profit}
        consumer_problem = LogConsumerProblem(params={'a':a,'p':p}, rng=rng)
        producer_problem = QuadraticCostFirmProblem(params={'a':0,'b':b,'p':p}, rng=rng)
        setup_list = []
        setup = fr"""
{consumer.setup()}

{producer.setup()}
"""
        online_setup = fr"""
<p>{consumer.setup()}</p>

<p>{producer.setup()}</p>
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question_list.append(consumer_problem.question_list[1])
        question_list.append(producer_problem.question_list[2])
        question = "Calculate the equilibrium price."
        online_question = question
        answer = p
        online_answer = fr"\(p = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = "Calculate the equilibrium quantity."
        online_question = question
        answer = q
        online_answer = fr"\(q = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = "Calculate the consumer surplus (i.e. utility) in equilibrium."
        online_question = question
        answer = U
        online_answer = fr"\(CS = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = "Calculate the producer surplus (i.e. profit) in equilibrium."
        online_question = question
        answer = profit
        online_answer = fr"\(PS = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        self.consumer = consumer
        self.producer = producer
        self.market = market
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if self.sol['q']<=0: return False
        if self.sol['p']<=0: return False
        if self.sol['U']<0: return False
        return True

class WorkerProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='worker_problem'):
        default_params = {'d':0.5,'k':2,'w':2}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        d, k, w = params['d'], params['k'], params['w']
        worker = Worker(d, k)
        L = worker.supply.eval_at_p(w)
        U = worker.utility_at(w, L)
        self.sol = {'L':L, 'U':U}

        c_ = k*d
        k_ = k-1
        supply_curve = fr"\(w = {PolyEq([c_],'L_s',[k_])} \)"
        
        c_ = d
        k_ = k-1
        supply_curve_distractor1 = fr"\(w = {PolyEq([c_],'L_s',[k_])} \)"

        c_ = 1/(k*d)
        k_ = 1-k
        supply_curve_distractor2 = fr"\(w = {PolyEq([c_],'L_s',[k_])} \)"
        
        c_ = k*d
        k_ = 1/k
        supply_curve_distractor3 = fr"\(w = {PolyEq([c_],'L_s',[k_])} \)"

        setup_list = []
        setup = worker.setup()
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = "Write down the inverse labor supply curve."
        online_question = question
        answer = supply_curve
        online_answer = answer
        answers = [answer, supply_curve_distractor1, supply_curve_distractor2, supply_curve_distractor3]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        question = fr"Calculate the choice of \(L\) that maximizes utility when the wage rate is \(w={w:g}\)."
        online_question = question
        answer = L
        online_answer = fr"\(L = {answer:g}\)"
        answers = generate_distractors(answer, rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = fr"What is the maximum utility attainable when the wage rate is \(w={w:g}\)?"
        online_question = question
        answer = U
        online_answer = fr"\(U = {answer:g}\)"
        answers = generate_distractors(answer, rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if self.sol['L']<1: return False
        return True
        
class ExponentialProductionFirmProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='exponential_production_firm_problem'):
        default_params = {'A':1,'k':1/2,'w':1}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        A, k, w = params['A'], params['k'], params['w']
        firm = ExponentialProductionFirm(A,k)
        L = firm.labor_demand.eval_at_p(w)
        profit = firm.profit_at(w, L)
        self.sol = {'L':L, 'profit':profit}

        c_ = k*A
        k_ = k-1
        demand_curve = fr"\(w = {PolyEq([c_],'L_d',[k_])} \)"
        c_ = A
        k_ = k-1
        demand_curve_distractor1 = fr"\(w = {PolyEq([c_],'L_d',[k_])} \)"
        c_ = 1/(k*A)
        k_ = 1-k
        demand_curve_distractor2 = fr"\(w = {PolyEq([c_],'L_d',[k_])} \)"
        c_ = k*A
        k_ = 1/k
        demand_curve_distractor3 = fr"\(w = {PolyEq([c_],'L_d',[k_])} \)"

        c_ = asfrac(1/A, inline=False, maxdenom=A)
        k_ = asfrac(1/k, inline=True)
        if A==1:
            cost_func = fr"\(c(q) = q^{{{k_}}}\)"
        else:
            cost_func = fr"\(c(q) = \left({c_}\right)^{{{k_}}} q^{{{k_}}}\)"
        c_ = asfrac(A/k, inline=False, maxdenom=A)
        k_ = asfrac(1/k, inline=True)
        cost_func_distractor1 = fr"\(c(q) = {c_} q^{{{k_}}} \)"
        c_ = asfrac(A/k, inline=False, maxdenom=A)
        k_ = asfrac(1/k, inline=True)
        cost_func_distractor2 = fr"\(c(q) = \left({c_}\right)^{{{k_}}} q^{{{k_}}} \)"
        c_ = asfrac(1/A, inline=False, maxdenom=A)
        k_ = asfrac(k, inline=True)
        if A==1:
            cost_func_distractor3 = fr"\(c(q) = q^{{{k_}}}\)"
        else:
            cost_func_distractor3 = fr"\(c(q) = \left({c_}\right)^{{{k_}}} q^{{{k_}}}\)"

        setup_list = []
        setup = firm.setup()
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = "Write down the inverse labor demand curve."
        online_question = question
        answer = demand_curve
        online_answer = answer
        answers = [answer, demand_curve_distractor1, demand_curve_distractor2, demand_curve_distractor3]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        question = fr"Write down the firm's total cost function, \(c(q)\)."
        online_question = question
        answer = cost_func
        online_answer = answer
        answers = [answer, cost_func_distractor1, cost_func_distractor2, cost_func_distractor3]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        question = fr"Calculate the choice of \(L\) that maximizes profit when the wage rate is \(w={w:g}\)."
        online_question = question
        answer = L
        online_answer = fr"\(L = {answer:g}\)"
        answers = generate_distractors(answer, rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = fr"What is the maximum profit attainable when the wage rate is \(w={w:g}\)?"
        online_question = question
        answer = profit
        online_answer = fr"\(\Pi = {answer:g}\)"
        answers = generate_distractors(answer, rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if self.sol['L']<1: return False
        return True
        

PROBLEM_TYPES = {
    'LinearMarketProblem': LinearMarketProblem,
    'ExponentialMarketProblem': ExponentialMarketProblem,
    'ExponentialRewriteProblem': ExponentialRewriteProblem,
    'CobbDouglasSimplifyProblem': CobbDouglasSimplifyProblem,
    'LogDifferencesProblem': LogDifferencesProblem,
    'LinearConsumerProblem': LinearConsumerProblem,
    'LogConsumerProblem': LogConsumerProblem,
    'QuadraticCostFirmProblem': QuadraticCostFirmProblem,
    'QuadraticOptimizationProblem': QuadraticOptimizationProblem,
    'LinearCommodityMarketProblem': LinearCommodityMarketProblem,
    'ExponentialCommodityMarketProblem': ExponentialCommodityMarketProblem,
    'WorkerProblem': WorkerProblem,
    'ExponentialProductionFirmProblem': ExponentialProductionFirmProblem
}
def load_problem(problem_str, params=None, name='generic_problem', rng=rng):
    return PROBLEM_TYPES[problem_str](params=params, name=name, rng=rng)
    

        
        
        