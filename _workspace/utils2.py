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
    def eval_at(self, x, y):
        A, a, b = self.A, self.a, self.b
        return A*(x**a)*(y**b)
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
    # x = (y-b)/m
    def __init__(self, m, b, linewidth=1, color='black', label='_nolegend_'):
        self.m, self.b = m, b
        self.linewidth = linewidth
        self.color = color
        self.label = label
    def plot(self, ax, xg):
        return ax.plot(xg, self.m*xg + self.b, color=self.color, linewidth=self.linewidth, label=self.label)
    def eval_at_x(self, x):
        return self.m*x + self.b
    def eval_at_y(self, y):
        return (y-self.b)/self.m

class Point:
    def __init__(self, x, y, color='black',text=None, position=None):
        self.x, self.y = x, y
        self.color = color
        self.text = text
        self.position = position
    def plot(self, ax, xg):
        x, y = self.x, self.y
        ax.plot(x,y,'o',color=self.color,markersize=12,label='_nolegend_')
        if self.text is not None:
            shift = xg[2]-xg[0]
            text_x = x
            text_y = y
            horizontalalignment = 'center'
            verticalalignment = 'center'
            if self.position=='sw':
                text_x = text_x - shift
                text_y = text_y - shift
                horizontalalignment = 'right'
                verticalalignment = 'top'
            elif self.position=='ne':
                text_x = text_x + shift
                text_y = text_y + shift
                horizontalalignment = 'left'
                verticalalignment = 'bottom'
            ax.text(text_x, text_y, self.text, color=self.color, horizontalalignment=horizontalalignment, verticalalignment=verticalalignment)
        return ax

class LineContours:
    # ax + by = z
    # y = -(a/b)*x + (z/b)
    def __init__(self, a, b, passing, linewidth=1, color='green', alpha=0.5):
        self.linewidth = linewidth
        self.color = color
        self.alpha = alpha
        contours = []
        for i in range(len(passing)):
            x = passing[i][0]
            y = passing[i][1]
            z = a*x + b*y
            contours.append(Line(-a/b, z/b))
        self.contours = contours
    def plot(self, ax, xg):
        for contour in self.contours:
            m = contour.m
            b = contour.b
            ax.plot(xg, m*xg+b, color=self.color, linewidth=self.linewidth, alpha=self.alpha, label='_nolegend_')
        return ax
    
class BudgetConstraint:
    def __init__(self, px, py, I, linewidth=2, color='black', alpha=1.0, label='_nolegend_'):
        self.px, self.py, self.I = px, py, I
        self.xint = I/px
        self.yint = I/py
        self.linewidth = linewidth
        self.color = color
        self.alpha = alpha
        self.label = label
    def plot(self, ax, xg):
        m = -self.px / self.py
        b = self.I / self.py
        ax.plot(xg, m*xg+b, color=self.color, linewidth=self.linewidth, alpha=self.alpha, label=self.label)
        return ax

class CobbDouglasContours:
    # A x^a y^b
    # y = (z/A)^(1/b) * x^(-a/b)
    def __init__(self, cobb_douglas, levels, linewidth=1, color='green', alpha=0.5):
        assert type(cobb_douglas)==CobbDouglas
        self.linewidth = linewidth
        self.color = color
        self.alpha = alpha
        self.levels = levels
        self.cobb_douglas = cobb_douglas
    def plot(self, ax, xg):
        A, a, b = self.cobb_douglas.A, self.cobb_douglas.a, self.cobb_douglas.b
        for z in self.levels:
            ax.plot(xg[1:], (z/A)**(1/b)*xg[1:]**(-a/b), color=self.color, linewidth=self.linewidth, alpha=self.alpha, label='_nolegend_')
        return ax

def get_cb_levels(cobb_douglas, axis, U1=None, U2=None):
    assert type(cobb_douglas)==CobbDouglas
    assert type(axis)==Axis
    xn = axis.xn
    yn = axis.yn
    xunit = axis.xunit
    yunit = axis.xunit
    umax = cobb_douglas.eval_at((xn-1)*xunit, (yn-1)*yunit)
    umin = cobb_douglas.eval_at(xunit, yunit)
    du_ideal = (umax - umin)/(xn-2)
    if U1 is None:
        return [umin+i*du_ideal for i in range(0,xn-1)]
    if U2 is None:
        U2 = umin
    if equals(U2,U1):
        U2 = umin
    du = np.abs(U2-U1)/np.maximum(np.round(np.abs(U2-U1)/du_ideal),1)
    levels = [U1+i*du for i in np.arange(-xn,xn) if U1+i*du>=umin and U1+i*du<=umax]
    return levels
                  
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
    # Pi = pAL^k - wL
    # c(q) = (1/A)^(1/k) wq^(1/k)
    # w = p*k*A*L^(k-1)
    def __init__(self, A=1, k=1/2):
        self.A, self.k = A, k
    def print_production_func(self, L='L'):
        A, k = self.A, self.k
        return fr"{PolyEq([A],L,[k])}"
    def setup(self):
        return fr"""
A representative, price-taking firm uses labor to produce and sell a commodity at unit price \(p\). The firm hires labor at a constant wage rate \(w\). If the firm employs \(L\) units of labor, it can produce \(f(L)\) units of commodity output, where:

$$ f(L) = {self.print_production_func()} $$
"""
    def profit_at(self, p, w, L):
        A, k = self.A, self.k
        return p*A*L**k - w*L
    def get_labor_demand(self, p):
        A, k = self.A, self.k
        return ExponentialDemand(p*k*A, k-1)
    def get_commodity_supply(self, p):
        A, k = self.A, self.k
        assert equals(k,1/2)
        b = 2*(1/A)**(1/k)
        return QuadraticCostFirm(0,b).supply

class GeneralEquilibrium:
    # f(L) = A*L^kf
    # u(L) = w*L - d*L^kw
    # u(q) = a*ln(q) - p*q
    # Commodity Demand: p = a*q^-1
    # Labor Demand: w = p*A*kf*L^(kf-1)
    # Labor Supply: w = d*kw*L^(kw-1)
    # Equilibrium Labor: L = (a*kf/d*kw)^(1/kw)
    # Equilibrium Wage: a*kf*L^-1
    def __init__(self, consumer, firm, worker):
        assert type(consumer)==LogConsumer
        assert type(firm)==ExponentialProductionFirm
        assert type(worker)==Worker
        self.consumer = consumer
        self.firm = firm
        self.worker = worker
        A = firm.A
        kf = firm.k
        d = worker.d
        kw = worker.k
        a = consumer.a
        L = (a*kf/(d*kw))**(1/kw)
        w = a*kf/L
        q = A*L**kf
        p = a/q
        U_consumer = consumer.utility_at(p,q)
        U_worker = worker.utility_at(w,L)
        profit = firm.profit_at(p, w, L)
        assert equals(consumer.demand.eval_at_p(p), q)
        assert equals(worker.supply.eval_at_p(w), L)
        assert equals(q, A*L**kf)
        self.eq = {'L':L, 'w':w, 'p':p, 'q':q, 'U_consumer':U_consumer, 'U_worker':U_worker, 'profit':profit}

class CobbDouglasConsumer:
    # u(x,y) = x^a y^b
    # px*x + py*y = I
    def __init__(self, cobb_douglas, budget_constraint):
        assert type(cobb_douglas)==CobbDouglas
        assert type(budget_constraint)==BudgetConstraint
        A, a, b = cobb_douglas.A, cobb_douglas.a, cobb_douglas.b 
        px, py, I = budget_constraint.px, budget_constraint.py, budget_constraint.I
        x = I/(px*(1+b/a))
        y = I/(py*(1+a/b))
        U = x**a * y**b
        self.x = x
        self.y = y
        self.U = U


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
        if self.sol['L']>50: return False
        return True
        
class ExponentialProductionFirmProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='exponential_production_firm_problem'):
        default_params = {'A':1,'k':1/2,'w':1,'p':1}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        A, k, w, p = params['A'], params['k'], params['w'], params['p']
        firm = ExponentialProductionFirm(A,k)
        labor_demand = firm.get_labor_demand(p)
        L = labor_demand.eval_at_p(w)
        profit = firm.profit_at(p, w, L)
        self.sol = {'L':L, 'profit':profit}

        c_ = k*A
        k_ = k-1
        demand_curve = fr"\(w = {PolyEq([c_],'p L_d',[k_])} \)"
        c_ = A
        k_ = k-1
        demand_curve_distractor1 = fr"\(w = {PolyEq([c_],'p L_d',[k_])} \)"
        c_ = 1/(k*A)
        k_ = 1-k
        demand_curve_distractor2 = fr"\(w = {PolyEq([c_],'p L_d',[k_])} \)"
        c_ = k*A
        k_ = 1/k
        demand_curve_distractor3 = fr"\(w = {PolyEq([c_],'p L_d',[k_])} \)"

        c_ = asfrac(1/A, inline=False, maxdenom=A)
        k_ = asfrac(1/k, inline=True)
        if A==1:
            cost_func = fr"\(c(q) = w q^{{{k_}}}\)"
        else:
            cost_func = fr"\(c(q) = \left({c_}\right)^{{{k_}}} w q^{{{k_}}}\)"
        c_ = asfrac(A/k, inline=False, maxdenom=A)
        k_ = asfrac(1/k, inline=True)
        cost_func_distractor1 = fr"\(c(q) = {c_} w q^{{{k_}}} \)"
        c_ = asfrac(A/k, inline=False, maxdenom=A)
        k_ = asfrac(1/k, inline=True)
        cost_func_distractor2 = fr"\(c(q) = \left({c_}\right)^{{{k_}}} w q^{{{k_}}} \)"
        c_ = asfrac(1/A, inline=False, maxdenom=A)
        k_ = asfrac(k, inline=True)
        if A==1:
            cost_func_distractor3 = fr"\(c(q) = w q^{{{k_}}}\)"
        else:
            cost_func_distractor3 = fr"\(c(q) = \left({c_}\right)^{{{k_}}} w q^{{{k_}}}\)"

        setup_list = []
        setup = firm.setup()
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"Write down the inverse labor demand curve in terms of \(p\) and \(L\)."
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
        question = fr"Write down the firm's total cost function, \(c(q)\), in terms of \(w\) and \(q\)."
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
        question = fr"Calculate the choice of \(L\) that maximizes profit when the wage rate is \(w={w:g}\) and the output price is \(p={p:g}\)."
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
        question = fr"What is the maximum profit attainable when the wage rate is \(w={w:g}\) and the output price is \(p={p:g}\)?"
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
        if self.sol['L']>50: return False
        return True
        
class ExponentialLaborMarketProblem(GenericProblem):
    # u(L) = wL - d*L^kw
    # f(L) = A*L^kf
    def __init__(self, params=None, rng=rng, name='exponential_labor_market_problem'):
        default_params = {'A':2,'kf':1/2,'d':1/2,'kw':3/2,'p':1}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        A, kf, d, kw, p = params['A'], params['kf'], params['d'], params['kw'], params['p']
        assert kf<1
        assert kw>1
        firm = ExponentialProductionFirm(A,kf)
        worker = Worker(d,kw)
        labor_demand = ExponentialDemand(p*A*kf, kf-1)
        labor_supply = ExponentialSupply(d*kw, kw-1)
        labor_market = ExponentialMarket(labor_demand, labor_supply)
        w = labor_market.eq['p']
        L = labor_market.eq['q']
        U = worker.utility_at(w, L)
        profit = firm.profit_at(p,w,L)
        self.sol = {'w':w, 'L':L, 'U':U, 'profit':profit}
        setup_list = []
        setup = fr"""
{worker.setup()}

{firm.setup()}

The current commodity price is \(p={p:g}\).
"""
        online_setup = fr"""
<p>{worker.setup()}</p>

<p>{firm.setup()}</p>

<p>The current commodity price is \(p={p:g}\).</p>
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"Calculate the equilibrium wage rate \(w\)."
        online_question = question
        answer = w
        online_answer = fr"\(w = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = fr"Calculate the equilibrium quantity of labor supplied, \(L\)."
        online_question = question
        answer = L
        online_answer = fr"\(L = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = fr"Calculate the equilibrium utility of the worker."
        online_question = question
        answer = U
        online_answer = fr"\(U = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = fr"Calculate the equilibrium profit of the firm."
        online_question = question
        answer = profit
        online_answer = fr"\(\Pi = {answer:g}\)"
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
    def check_solution(self):
        if self.sol['L']<=1: return False
        if self.sol['L']>50: return False
        if self.sol['w']<=1: return False
        if self.sol['w']>50: return False
        return True

class GeneralEquilibriumProblem(GenericProblem):
    # u(L) = wL - d*L^kw
    # f(L) = A*L^kf
    # u(q) = a*ln(q) - p*q
    def __init__(self, params=None, rng=rng, name='general_equilibrium_problem'):
        default_params = {'A':2,'kf':1/2,'d':1/2,'kw':3/2,'a':12}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        A, kf, d, kw, a = params['A'], params['kf'], params['d'], params['kw'], params['a']
        consumer = LogConsumer(a)
        firm = ExponentialProductionFirm(A,kf)
        worker = Worker(d,kw)
        equilibrium = GeneralEquilibrium(consumer, firm, worker)
        self.sol = equilibrium.eq.copy()
        L = self.sol['L']
        w = self.sol['w']
        p = self.sol['p']
        q = self.sol['q']
        U_consumer = self.sol['U_consumer']
        U_worker = self.sol['U_worker']
        profit = self.sol['profit']
        setup_list = []
        setup = fr"""
{consumer.setup()}

{worker.setup()}

{firm.setup()}
"""
        online_setup = fr"""
<p>{consumer.setup()}</p>
        
<p>{worker.setup()}</p>

<p>{firm.setup()}</p>
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"Calculate the equilibrium quantity of labor supplied, \(L\)."
        online_question = question
        answer = L
        online_answer = fr"\(L = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = fr"Calculate the equilibrium quantity of commodity produced, \(q\)."
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
        question = fr"Calculate the equilibrium wage rate \(w\)."
        online_question = question
        answer = w
        online_answer = fr"\(w = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = fr"Calculate the equilibrium commodity price \(p\)."
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
        question = fr"Calculate the equilibrium utility of the consumer."
        online_question = question
        answer = U_consumer
        online_answer = fr"\(U_c = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = fr"Calculate the equilibrium utility of the worker."
        online_question = question
        answer = U_worker
        online_answer = fr"\(U_w = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = fr"Calculate the equilibrium profit of the firm."
        online_question = question
        answer = profit
        online_answer = fr"\(\Pi = {answer:g}\)"
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
    def check_solution(self):
        if self.sol['p']<=1: return False
        if self.sol['p']>50: return False
        if self.sol['q']<=1: return False
        if self.sol['q']>50: return False
        if self.sol['w']<=1: return False
        if self.sol['w']>50: return False
        if self.sol['L']<=1: return False
        if self.sol['L']>50: return False
        if self.sol['U_consumer']<0: return False
        return True

class ProductivityShockProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='productivity_shock_problem'):
        default_params = {'A1':2,'A2':1,'kf':1/2,'d':1/2,'kw':3/2,'a':12}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        A1, A2, kf, d, kw, a = params['A1'], params['A2'], params['kf'], params['d'], params['kw'], params['a']
        assert A1!=A2
        consumer = LogConsumer(a)
        firm1 = ExponentialProductionFirm(A1,kf)
        firm2 = ExponentialProductionFirm(A2,kf)
        worker = Worker(d,kw)
        equilibrium1 = GeneralEquilibrium(consumer, firm1, worker)
        equilibrium2 = GeneralEquilibrium(consumer, firm2, worker)
        self.eq1 = equilibrium1
        self.eq2 = equilibrium2
        dU_consumer = equilibrium2.eq['U_consumer'] - equilibrium1.eq['U_consumer']
        dU_worker = equilibrium2.eq['U_worker'] - equilibrium1.eq['U_worker']
        dprofit = equilibrium2.eq['profit'] - equilibrium1.eq['profit']
        assert equals(dprofit, 0)
        assert equals(dU_worker, 0)
        dprofit=0
        dU_worker=0
        self.sol = {'dU_consumer':dU_consumer, 'dU_worker':dU_worker, 'dprofit':dprofit}
        firm_setup = fr"""
A representative, price-taking firm uses labor to produce and sell a commodity at unit price \(p\). The firm hires labor at a constant wage rate \(w\). If the firm employs \(L\) units of labor, it can produce \(f(L)\) units of commodity output, where:

$$ f(L) = A L^{{{asfrac(kf,inline=True)}}} $$
"""
        setup_list = []
        setup = fr"""
{consumer.setup()}

{worker.setup()}

{firm_setup}

Suppose the labor productivity, \(A\), changes from {A1:g} to {A2:g}.
"""
        online_setup = fr"""
<p>{consumer.setup()}</p>
        
<p>{worker.setup()}</p>

<p>{firm_setup}</p>

<p>Suppose the total factor productivity, \(A\), changes from {A1:g} to {A2:g}.</p>
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"How much does the utility of the consumer change?"
        online_question = question
        answer = dU_consumer
        online_answer = fr"\(\Delta U_c = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = fr"How much does the utility of the worker change?"
        online_question = question
        answer = dU_worker
        online_answer = fr"\(\Delta U_w = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,sort=True,horz=True,numerical=True,rng=rng)
        })
        question = fr"How much does the profit of the firm change?"
        online_question = question
        answer = dprofit
        online_answer = fr"\(\Delta \Pi = {answer:g}\)"
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
        question = fr"Who is the greatest beneficiary of the growth in labor productivity?"
        online_question = question
        answer = "consumers"
        online_answer = answer
        answers = ['workers', 'firms', 'consumers']
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,2,shuffle=False,sort=False,horz=True,numerical=False,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if self.eq1.eq['U_consumer']<0: return False
        if self.eq2.eq['U_consumer']<0: return False
        if np.abs(self.sol['dU_consumer'])<0.1: return False
        return True

class LinearContourProblem(GenericProblem):
    # ax + by = z
    # y = z/b - (a/b)x
    def __init__(self, params=None, rng=rng, name='linear_contour_line_problem'):
        default_params = {'a':1,'b':1,'z':5,'x':'x','y':'y','xunit':1,'yunit':1,'xn':13,'yn':13}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        a, b, z, x, y, xunit, yunit, xn, yn = params['a'], params['b'], params['z'], params['x'], params['y'], params['xunit'], params['yunit'], params['xn'], params['yn']
        yint = z/b
        xint = z/a
        self.sol = {'yint':yint, 'xint':xint}
        axis = Axis(xn=xn, yn=yn, xunit=xunit, yunit=yunit)
        passing = [(i*xunit, i*yunit) for i in range(1,xn)]
        contours = LineContours(a,b,passing)
        axis.add(contours)
        setup_list = []
        setup = fr"$$ f({x},{y}) = {PolyEq([a,b],[x,y],[1,1])} $$"
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"What is the y-intercept of the contour line for \(f(x)={z:g}\)?"
        online_question = question
        answer = yint
        online_answer = fr"{answer:g}"
        answers = generate_distractors(answer,delta=yunit,type='add',rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"What is the x-intercept of the contour line for \(f(x)={z:g}\)?"
        online_question = question
        answer = xint
        online_answer = fr"{answer:g}"
        answers = generate_distractors(answer,delta=xunit,type='add',rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"""
Using the grid below, draw multiple contour lines for \(f(x)\).
\begin{{center}}
\includegraphics[width=3in]{{{name}_setup.png}}
\end{{center}}
"""
        online_question = fr"""
Using the grid below, draw multiple contour lines for \(f(x)\).
<p><img src="/CSUN-Econ-310/assets/images/graphs/{name}_setup.png"></p>
"""
        answer = fr"""
\begin{{center}}
\includegraphics[width=3in]{{{name}_sol.png}}
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
        self.setup_list = setup_list
        self.question_list = question_list
        self.axis = axis
    def check_solution(self):
        if not is_divisible(self.sol['yint'], self.params['yunit']): return False
        if not is_divisible(self.sol['xint'], self.params['xunit']): return False
        if self.sol['yint'] >= self.params['yunit']*self.params['yn']: return False
        if self.sol['xint'] >= self.params['xunit']*self.params['xn']: return False
        return True
    
class CBDerivativeProblem(GenericProblem):
    # f(x,y) = Ax^a y^b
    # f_x = a Ax^(a-1) y^b
    # f_y = b Ax^a y^(b-1)
    def __init__(self, params=None, rng=rng, name='cb_derivative_problem'):
        default_params = {'A':1,'a':1/2,'b':1/2}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        A, a, b = params['A'], params['a'], params['b']

        A_, a_, b_ = a*A, a-1, b
        fx    = fr"\(f_x(x,y) = {CobbDouglas(A_,'x',a_,'y',b_)} \)"
        A_, a_, b_ = A, a-1, b
        fx_d1 = fr"\(f_x(x,y) = {CobbDouglas(A_,'x',a_,'y',b_)} \)"
        A_, a_, b_ = a*b*A, a-1, b-1
        fx_d2 = fr"\(f_x(x,y) = {CobbDouglas(A_,'x',a_,'y',b_)} \)"
        A_, a_, b_ = b*A, a, b-1
        fx_d3 = fr"\(f_x(x,y) = {CobbDouglas(A_,'x',a_,'y',b_)} \)"

        A_, a_, b_ = b*A, a, b-1
        fy    = fr"\(f_y(x,y) = {CobbDouglas(A_,'x',a_,'y',b_)} \)"
        A_, a_, b_ = A, a, b-1
        fy_d1 = fr"\(f_y(x,y) = {CobbDouglas(A_,'x',a_,'y',b_)} \)"
        A_, a_, b_ = a*b*A, a-1, b-1
        fy_d2 = fr"\(f_y(x,y) = {CobbDouglas(A_,'x',a_,'y',b_)} \)"
        A_, a_, b_ = a*A, a-1, b
        fy_d3 = fr"\(f_y(x,y) = {CobbDouglas(A_,'x',a_,'y',b_)} \)"

        setup_list = []
        setup = fr"""
$$ f(x,y) = {CobbDouglas(A,'x',a,'y',b)} $$
"""
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"Write the partial derivative of \(f(x,y)\) with respect to \(x\)."
        online_question = question
        answer = fx
        online_answer = answer
        answers = [answer, fx_d1, fx_d2, fx_d3]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        question = fr"Write the partial derivative of \(f(x,y)\) with respect to \(y\)."
        online_question = question
        answer = fy
        online_answer = answer
        answers = [answer, fy_d1, fy_d2, fy_d3]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list

class CobbDouglasConsumerProblem(GenericProblem):
    # u(x,y) = x^a y^b s.t. px x + py y = I
    def __init__(self, params=None, rng=rng, name='cobb_douglas_consumer_problem'):
        default_params = {'a':1/2,'b':1/2,'px':1,'py':1,'I':12,'xunit':1,'yunit':1,'xn':13,'yn':13}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        a, b, px, py, I, xunit, yunit, xn, yn = params['a'], params['b'], params['px'], params['py'], params['I'], params['xunit'], params['yunit'], params['xn'], params['yn']
        cobb_douglas = CobbDouglas(A=1, a=a, b=b)
        budget_constraint = BudgetConstraint(px=px, py=py, I=I)
        consumer = CobbDouglasConsumer(cobb_douglas, budget_constraint)
        setup_axis = Axis(xn=xn,yn=yn,xunit=xunit,yunit=yunit)
        setup_axis2 = Axis(xn=xn,yn=yn,xunit=xunit,yunit=yunit)
        solution_axis = Axis(xn=xn,yn=yn,xunit=xunit,yunit=yunit)
        x = consumer.x
        y = consumer.y
        U = consumer.U
        self.sol = {'x':x, 'y':y, 'U':U}
        self.consumer = consumer
        self.cobb_douglas = cobb_douglas
        self.budget_constraint = budget_constraint
        levels = get_cb_levels(cobb_douglas, setup_axis, U1=U)
        self.levels = levels
        contours = CobbDouglasContours(cobb_douglas, levels)
        point = Point(x,y,text='A',position='sw')
        setup_axis.add(contours)
        setup_axis2.add(contours)
        setup_axis2.add(budget_constraint)
        solution_axis.add(contours)
        solution_axis.add(budget_constraint)
        solution_axis.add(point)
        self.setup_axis = setup_axis
        self.setup_axis2 = setup_axis2
        self.solution_axis = solution_axis
        setup_list = []
        setup = fr"""
A consumer with income \(I = {I:g}\) has a utility function over two goods, \(x\) and \(y\):

$$ u(x,y) = {cobb_douglas} $$

The price of good \(x\) is \(p_x = {px:g}\) and the price of good \(y\) is \(p_y = {py:g}\).
"""
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        setup = fr"""
Solve:

$$ \max_{{x,y}} ~ {cobb_douglas} ~ \text{{s.t.}} ~ {PolyEq([px,py],['x','y'],[1,1])} = {I:g}$$
"""
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        setup = fr"""
A consumer with income \(I = {I:g}\) has a utility function over two goods, \(x\) and \(y\), represented
by the indifference curves shown below.
\begin{{center}}
\includegraphics[width=3in]{{{name}_setup.png}}
\end{{center}}
The price of good \(x\) is \(p_x = {px:g}\) and the price of good \(y\) is \(p_y = {py:g}\).
"""
        online_setup = fr"""
A consumer with income \(I = {I:g}\) has a utility function over two goods, \(x\) and \(y\), represented
by the indifference curves shown below.
<p>
<img src="/CSUN-Econ-310/assets/images/graphs/{name}_setup.png">
</p>
The price of good \(x\) is \(p_x = {px:g}\) and the price of good \(y\) is \(p_y = {py:g}\).
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        setup = fr"""
A consumer's indifference curves and budget constraint over two goods, \(x\) and \(y\), is shown below.
\begin{{center}}
\includegraphics[width=3in]{{{name}_setup2.png}}
\end{{center}}
"""
        online_setup = fr"""
A consumer's indifference curves and budget constraint over two goods, \(x\) and \(y\), is shown below.
<p>
<img src="/CSUN-Econ-310/assets/images/graphs/{name}_setup2.png">
</p>
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"Draw the consumer's budget constraint and label the optimal point A."
        online_question = question
        answer = fr"\begin{{center}}\includegraphics[width=3in]{{{name}_sol.png}}\end{{center}}"
        online_answer = f'<img src = "/CSUN-Econ-310/assets/images/graphs/{name}_sol.png">'
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": None
        })
        question = fr"What is the consumer's optimal choice of \(x\)?"
        online_question = question
        answer = x
        online_answer = fr"\(x = {answer:g}\)"
        answers = generate_distractors(answer,delta=xunit,type='add',rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"What is the optimal value of \(x\)?"
        online_question = question
        answer = x
        online_answer = fr"\(x = {answer:g}\)"
        answers = generate_distractors(answer,delta=xunit,type='add',rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"What is the consumer's optimal choice of \(y\)?"
        online_question = question
        answer = y
        online_answer = fr"\(y = {answer:g}\)"
        answers = generate_distractors(answer,delta=yunit,type='add',rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"What is the optimal value of \(y\)?"
        online_question = question
        answer = y
        online_answer = fr"\(y = {answer:g}\)"
        answers = generate_distractors(answer,delta=yunit,type='add',rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"Calcualte the consumer's utility at the optimal choice."
        online_question = question
        answer = U
        online_answer = fr"\(U = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"What is the maximum value of the function?"
        online_question = question
        answer = U
        online_answer = fr"\(f(x,y) = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if len(self.levels)>=14: return False
        if len(self.levels)<=6: return False
        if not is_divisible(self.sol['x'], self.params['xunit']): return False
        if not is_divisible(self.sol['y'], self.params['yunit']): return False
        if not is_divisible(self.budget_constraint.xint, self.params['xunit']): return False
        if not is_divisible(self.budget_constraint.yint, self.params['yunit']): return False
        if self.sol['x'] >= self.setup_axis.xmax: return False
        if self.sol['y'] >= self.setup_axis.ymax: return False
        if self.budget_constraint.xint >= self.setup_axis.xmax: return False
        if self.budget_constraint.yint >= self.setup_axis.ymax: return False
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
    'ExponentialProductionFirmProblem': ExponentialProductionFirmProblem,
    'ExponentialLaborMarketProblem': ExponentialLaborMarketProblem,
    'GeneralEquilibriumProblem': GeneralEquilibriumProblem,
    'ProductivityShockProblem': ProductivityShockProblem,
    'LinearContourProblem': LinearContourProblem,
    'CBDerivativeProblem': CBDerivativeProblem,
    'CobbDouglasConsumerProblem': CobbDouglasConsumerProblem
}
def load_problem(problem_str, params=None, name='generic_problem', rng=rng):
    return PROBLEM_TYPES[problem_str](params=params, name=name, rng=rng)
    
def show_menu(problem_str, params=None, name='generic_problem', rng=rng):
    prob = load_problem(problem_str, params, name, rng=rng)
    setup_list = prob.setup_list
    question_list = prob.question_list
    for i in range(len(setup_list)):
        print(f"{i}: {setup_list[i]['setup']}".replace('\n',' '))
        print("")
    for i in range(len(question_list)):
        print(f"{i}: {question_list[i]['question']}".replace('\n',' '))
        print("")
    
        
        
        