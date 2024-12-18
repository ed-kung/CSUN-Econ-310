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
        self.bad=False
    def print(self, maxdenom=8, rmplus=True, rmneg=False):
        out = PTerm(self.A, self.x, self.a).print(maxdenom=maxdenom,rmplus=rmplus,rmneg=rmneg)
        out+= PTerm(1, self.y, self.b).print(maxdenom=maxdenom,rmplus=True,rmneg=True)
        return out
    def eval_at(self, x, y):
        A, a, b = self.A, self.a, self.b
        return A*(x**a)*(y**b)
    def get_IC(self, U, xg):
        A, a, b = self.A, self.a, self.b
        return (U/A)**(1/b)*xg**(-a/b)
    def get_IC_from_point(self, x, y, xg):
        U = self.eval_at(x, y)
        return self.get_IC(U, xg)
    def __repr__(self):
        return self.print()

class CES:
    def __init__(self, a=0.5, rho=0.5):
        self.a = a
        self.rho = rho
        self.bad = False
        if self.a<=0.1 or self.a>=0.9:
            self.bad = True
        if self.rho>=0.8:
            self.bad = True
        if self.rho<-2:
            self.bad = True
        if np.abs(self.rho)<=0.1:
            self.bad = True
    def eval_at(self, x, y):
        a, rho = self.a, self.rho
        return (a*x**rho + (1-a)*y**rho)**(1/rho)
    def get_IC(self, U, xg):
        a, rho = self.a, self.rho
        numerator = U**rho - a*xg**rho
        ids = (numerator>0)
        return xg[ids], (numerator[ids]/(1-a))**(1/rho)
    def get_IC_from_point(self, x, y, xg):
        U = self.eval_at(x,y)
        return self.get_IC(U, xg)

def get_cb_from_point(x, y, budget_constraint, x_='x', y_='y'):
    px, py, I = budget_constraint.px, budget_constraint.py, budget_constraint.I
    assert equals(x*px + y*py, I)
    a = px*x/I
    b = py*y/I
    return CobbDouglas(A=1,a=a,b=b,x=x_,y=y_)

def get_ces_from_points(x1,y1,x2,y2,bc1,bc2):
    px1, py1, I1 = bc1.px, bc1.py, bc1.I
    px2, py2, I2 = bc2.px, bc2.py, bc2.I
    assert equals(px1*x1 + py1*y1, I1)
    assert equals(px2*x2 + py2*y2, I2)
    A1 = np.log((I1-px1*x1)/(py1*x1))
    A2 = np.log((I2-px2*x2)/(py2*x2))
    B1 = np.log(py1/px1)
    B2 = np.log(py2/px2)
    try:
        M = np.array([
            [A1, 1],
            [A2, 1]
        ])
        Y = np.array([B1, B2])
        X = np.linalg.solve(M,Y)
    except:
        return CES(rho=2,a=0)
    rho = X[0]+1
    a = 1/(1+np.exp(X[1]))
    if equals(rho, 0):
        return CobbDouglas(A=1, a=a, b=1-a)
    else:
        return CES(rho=rho, a=a)

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
    def __init__(self, xn=13, yn=13, xunit=1, yunit=1, xlab=r'$x$', ylab=r'$y$', noticklabels=False, title=None):
        self.xn = xn
        self.yn = yn
        self.xunit = xunit
        self.yunit = yunit
        self.xmax = xn*xunit
        self.ymax = yn*yunit
        self.objects = []
        self.xg = np.arange(0, self.xmax, self.xunit/10)
        self.xlab = xlab
        self.ylab = ylab
        self.noticklabels = noticklabels
        self.title = title
    def add(self, *args):
        for obj in args:
            self.objects.append(obj)
    def get_figax(self, alpha=0.4, saveas=None):
        fig, ax = plt.subplots()
        ax.set_xticks(np.arange(0, self.xmax, self.xunit))
        ax.set_yticks(np.arange(0, self.ymax, self.yunit))
        if self.noticklabels:
            ax.set_xticklabels([])
            ax.set_yticklabels([])
        ax.set_xlim([0, self.xmax])
        ax.set_ylim([0, self.ymax])
        ax.set_xlabel(self.xlab)
        ax.set_ylabel(self.ylab)
        ax.set_axisbelow(True)
        ax.grid(alpha=alpha)
        if self.title is not None:
            ax.set_title(self.title)
        if saveas is not None:
            plt.savefig(saveas, bbox_inches='tight')
        return fig, ax
    def draw(self, alpha=0.4, legend=None, saveas=None):
        fig, ax = self.get_figax(alpha=alpha)
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
    def __init__(self, m, b, linewidth=1, color='black', label='_nolegend_', linestyle='solid'):
        self.m, self.b = m, b
        self.linewidth = linewidth
        self.color = color
        self.label = label
        self.linestyle = linestyle
    def plot(self, ax, xg):
        return ax.plot(xg, self.m*xg + self.b, color=self.color, linewidth=self.linewidth, label=self.label, linestyle=self.linestyle)
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

class CESContours:
    def __init__(self, x1, y1, x2, y2, bc1, bc2, axis, color='green', alpha=0.5, linewidth=1):
        self.color = color
        self.alpha = alpha
        self.linewidth = linewidth
        xn, yn, xunit, yunit, xmax, ymax, xg = axis.xn, axis.yn, axis.xunit, axis.yunit, axis.xmax, axis.ymax, axis.xg
        ces = get_ces_from_points(x1,y1,x2,y2,bc1,bc2)
        self.ces = ces
        if not self.ces.bad:
            U1 = ces.eval_at(x1, y1)
            U2 = ces.eval_at(x2, y2)
            IC1 = ces.get_IC_from_point(x1,y1,xg[1:])
            IC2 = ces.get_IC_from_point(x2,y2,xg[1:])
            Umax = ces.eval_at((xn+1)*xunit, (yn+1)*yunit)
            Umin = ces.eval_at(xunit, yunit)
            du_ideal = (Umax - Umin)/(xn-2)
            du = np.abs(U2-U1)/np.maximum(np.round(np.abs(U2-U1)/du_ideal),1)
            levels = [U1+i*du for i in np.arange(-xn,xn) if U1+i*du>=Umin and U1+i*du<=Umax]
            self.levels = levels
    def plot(self, ax, xg):
        if not self.ces.bad:
            for u in self.levels:
                if type(self.ces)==CES:
                    myxg, ic = self.ces.get_IC(u, xg[1:])
                else: 
                    myxg = xg[1:]
                    ic = self.ces.get_IC(u, xg[1:])
                ax.plot(myxg, ic, color=self.color, alpha=self.alpha, linewidth=self.linewidth, label='_nolegend_')
        return ax

def get_cb_levels(cobb_douglas, axis, U1=None, U2=None):
    assert type(cobb_douglas)==CobbDouglas
    assert type(axis)==Axis
    xn = axis.xn
    yn = axis.yn
    xunit = axis.xunit
    yunit = axis.yunit
    umax = cobb_douglas.eval_at((xn)*xunit, (yn)*yunit)
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

class LeontieffContours:
    def __init__(self, xunit=1, yunit=1, xn=13, yn=13, linewidth=1, color='green', alpha=0.5):
        self.xunit = xunit
        self.xn = xn
        self.yunit = yunit
        self.yn = yn
        self.linewidth = linewidth
        self.color = color
        self.alpha = alpha
    def plot(self, ax, xg):
        for i in np.arange(1, self.xn):
            xmax = (self.xn+1)*self.xunit
            ymax = (self.yn+1)*self.yunit
            interval = xg[1]-xg[0]
            x = i*self.xunit
            y = i*self.yunit
            myxg = np.arange(x,xmax,interval)
            myyg = np.arange(y,ymax,interval)
            ax.plot(myxg, [y]*len(myxg), linewidth=self.linewidth, color=self.color, alpha=self.alpha, label='_nolegend_')
            ax.plot([x]*len(myyg), myyg, linewidth=self.linewidth, color=self.color, alpha=self.alpha, label='_nolegend_')
        return ax

###################################################################
# ECONOMIC MODELS
###################################################################

class LinearDemand:
    # p = a - bq
    # q = (a/b) - (1/b)*p
    def __init__(self, a=12, b=1,color='black',linewidth=1,label='_nolegend_',linestyle='solid'):
        assert a>0
        assert b>0
        self.a = a
        self.b = b
        self.line = Line(-b,a,linewidth=linewidth,color=color,label=label,linestyle=linestyle)
    def print(self, x='p', maxdenom=8):
        return PolyEq(c=[self.a/self.b, -1/self.b], x=x, p=[0,1]).print(maxdenom=maxdenom, rmplus=True)
    def print_inverse(self, x='q', maxdenom=8):
        return PolyEq(c=[self.a, -self.b], x=x, p=[0,1]).print(maxdenom=maxdenom, rmplus=True)
    def eval_at_p(self, p):
        return self.a/self.b - (1/self.b)*p
    def eval_at_q(self, q):
        return self.a - self.b*q
    def plot(self,ax, xg):
        return self.line.plot(ax,xg)
        
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
    def __init__(self, a=0, b=1,linewidth=1,color='black',label='_nolegend_',linestyle='solid'):
        assert a>=0
        assert b>0
        self.a = a
        self.b = b
        self.line = Line(b,a,linewidth=linewidth,color=color,label=label,linestyle=linestyle)
    def print(self, x='p', maxdenom=8):
        return PolyEq(c=[1/self.b, -self.a/self.b], x=x, p=[1,0]).print(maxdenom=maxdenom, rmplus=True)
    def print_inverse(self, x='q', maxdenom=5):
        return PolyEq(c=[self.a, self.b], x=x, p=[0,1]).print(maxdenom=maxdenom, rmplus=True)
    def eval_at_p(self, p):
        return (1/self.b)*p - (self.a/self.b)
    def eval_at_q(self, q):
        return self.a + self.b*q
    def plot(self,ax, xg):
        return self.line.plot(ax,xg)
        
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
        lnq = PTerm(a,fr'\ln {q}',1)
        return fr"{lnq} - p{q}"
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

class IncomeSupportBudget:
    def __init__(self, bc, min_y):
        self.bc = bc
        self.min_y = min_y
    def plot(self, ax, xg):
        m = - self.bc.px / self.bc.py
        b = self.bc.I / self.bc.py
        bc = m*xg + b
        ax.plot(xg, np.maximum(bc, self.min_y), color=self.bc.color, linewidth=self.bc.linewidth, alpha=self.bc.alpha, label=self.bc.label)
        return ax

class CobbDouglasFirm:
    # f(L,K) = A*L^a K^(1-a)
    def __init__(self, A, a, color='black', linewidth=2, label='_nolegend_', linestyle='solid', alpha=1.0):
        self.cb = CobbDouglas(A=A, a=a, b=1-a, x='L', y='K')
        self.color = color
        self.linewidth = linewidth
        self.label = label
        self.linestyle = linestyle
        self.alpha = alpha
    def print(self, maxdenom=8, rmplus=True, rmneg=False):
        return self.cb.print(maxdenom=maxdenom,rmplus=rmplus,rmneg=rmneg)
    def eval_at(self, L, K):
        return cb.eval_at(L, K)
    def get_isoquant(self, Q, xg):
        return self.cb.get_IC(Q, xg)
    def get_isoquant_from_point(self, L, K, xg):
        return self.cb.get_IC_from_point(L, K, xg)
    def __repr__(self):
        return self.print()
    def unit_cost_K(self, w, r):
        A, a = self.cb.A, self.cb.a
        return (1/A)*(((1-a)/a)**a)*(w/r)**a
    def unit_cost_L(self, w, r):
        A, a = self.cb.A, self.cb.a
        return (1/A)*((a/(1-a)))**(1-a)*(r/w)**(1-a)
    def unit_cost(self, w, r):
        K = self.unit_cost_K(w,r)
        L = self.unit_cost_L(w,r)
        return w*L + r*K
    def get_unit_isoquant(self, xg):
        return self.get_isoquant(1, xg)
    def plot(self, ax, xg):  # draw unit isoquant
        ic = self.get_unit_isoquant(xg[1:])
        ax.plot(xg[1:], ic, color=self.color, linewidth=self.linewidth, label=self.label, linestyle=self.linestyle, alpha=self.alpha)
        return ax

def get_cb_firm_from_point(L, K, w, r):
    a = w*L/(w*L + r*K)
    b = 1-a
    A = 1/(L**a*K**(1-a))
    return CobbDouglasFirm(A=A, a=a)

class NormalForm:
    def __init__(self, players, strategies, payoffs, gametype):
        assert len(players)==2
        assert len(strategies)==2
        assert len(strategies[0])==len(payoffs)
        assert len(payoffs[0])==len(strategies[1])
        _payoffs_ = payoffs
        # Initialize payoffs and best responses
        payoffs = {}
        payoffs[players[0]] = {}
        payoffs[players[1]] = {}
        br = {}
        br[players[0]] = {}
        br[players[1]] = {}
        for s in strategies[1]:
            payoffs[players[0]][s] = {}
            br[players[0]][s] = {}
        for s in strategies[0]:
            payoffs[players[1]][s] = {}
            br[players[1]][s] = {}

        # Populate payoffs
        for i in range(len(_payoffs_)):
            for j in range(len(_payoffs_[0])):
                strategy_1 = strategies[0][i]
                strategy_2 = strategies[1][j]
                payoffs[players[0]][strategy_2][strategy_1] = _payoffs_[i][j][0]
                payoffs[players[1]][strategy_1][strategy_2] = _payoffs_[i][j][1]

        # Find best responses
        for player, opp_strategies in payoffs.items():
            for opp_strategy, my_strategies in opp_strategies.items():
                my_payoffs = np.array([v for (k,v) in my_strategies.items()])
                #print(my_payoffs)
                #print(my_payoffs.shape)
                my_br = []
                my_br_ids = np.argwhere(my_payoffs==np.amax(my_payoffs)).flatten()
                #print(type(my_br_ids))
                #print(my_br_ids)
                #print(type(list(my_strategies.keys())))
                #print(list(my_strategies.keys()))
                for br_id in my_br_ids:
                    my_br.append(list(my_strategies.keys())[br_id] )
                br[player][opp_strategy] = my_br

        # Find Nash equilibria
        ne = []
        ne_payoffs = []
        ne_distractors = []
        for s1 in strategies[0]:
            for s2 in strategies[1]:
                if (s1 in br[players[0]][s2]) and (s2 in br[players[1]][s1]):
                    ne.append(fr"({s1},{s2})")
                    ne_payoffs.append((payoffs[players[0]][s1][s2], payoffs[players[1]][s1][s2]))
                else:
                    ne_distractors.append(fr"({s1},{s2})")
        
        self.players = players
        self.strategies = strategies
        self._payoffs_ = _payoffs_
        self.payoffs = payoffs
        self.br = br
        self.ne = ne
        self.ne_payoffs = ne_payoffs
        self.ne_distractors = ne_distractors
        self.gametype = gametype
    
    def table_as_html(self, circle_br=False):
        t = '<table border=1px align="center">'
        N = len(self.strategies[0])
        K = len(self.strategies[1])
        players = self.players
        strategies = self.strategies
        payoffs = self._payoffs_
        br = self.br
        t+=  '<tr>'
        t+=  '<td></td>'
        t+=  '<td></td>'
        t+= f'<td colspan={K} align="center">{players[1]}</td>'
        t+=  '</tr>'
        t+=  '<tr>'
        t+=  '<td></td>'
        t+=  '<td></td>'
        for k in range(K):
            t+= f'<td align="center">{strategies[1][k]}</td>'
        t+= '</tr>'
        for i in range(N):
            t+= '<tr>'
            if i==0:
                t+= f'<td rowspan={N}>{players[0]}</td>'
            t+= f'<td>{strategies[0][i]}</td>'
            for k in range(K):
                if circle_br and (strategies[0][i] in br[players[0]][strategies[1][k]]):
                    u1 = f'<span style="border-width:2px; border-style:solid; border-color:#FF0000;">{payoffs[i][k][0]}</span>'
                else:
                    u1 = f'{payoffs[i][k][0]}'
                if circle_br and (strategies[1][k] in br[players[1]][strategies[0][i]]):
                    u2 = f'<span style="border-width:2px; border-style:solid; border-color:#FF0000;">{payoffs[i][k][1]}</span>'
                else:
                    u2 = f'{payoffs[i][k][1]}'
                t+= f'<td align="center">{u1}, {u2}</td>'
            t+=  '</tr>'
        t+=  '</table>'
        return t

    def table_as_latex(self):
        players = self.players
        strategies = self.strategies
        payoffs = self._payoffs_
        N = len(strategies[0])
        K = len(strategies[1])
        t = fr"""
\begin{{center}}
\begin{{tabular}}{{|c|c|{'c|'*K}}} \hline
 & & \multicolumn{{{K}}}{{c|}}{{ {players[1]} }} \\ \hline
"""
        t+= " & "
        for k in range(K):
            t+= fr" & {strategies[1][k]}"
        t+= fr"\\ \hline" + '\n'
        for i in range(N):
            if i==0:
                t+= fr"\multirow{{{N}}}{{*}}{{{players[0]}}} "
            t+= fr" & {strategies[0][i]} "
            for k in range(K):
                t+= fr" & {payoffs[i][k][0]}, {payoffs[i][k][1]} "
            if i==N-1:
                t+= fr"\\ \hline" + '\n'
            else:
                t+= fr"\\ \cline{{2-{K+2}}}" + '\n'
        t+=fr"""
\end{{tabular}}
\end{{center}}
"""
        return t

class Monopoly:
    # c(q) = f + aq + b*q^2
    # demand is of class LinearDemand
    def __init__(self, demand, f=0, a=0, b=0.5):
        q = (demand.a - a)/(2*(demand.b + b))
        p = demand.a - demand.b*q
        profit = p*q - f - a*q - b*q**2
        CS = 0.5*(demand.a - p)*q
        q_eff = (demand.a - a)/(demand.b + 2*b)
        p_eff = demand.a - demand.b*q_eff
        profit_eff = p_eff*q_eff - f - a*q_eff - b*q_eff**2
        CS_eff = 0.5*(demand.a - p_eff)*q_eff
        DWL = (CS_eff + profit_eff) - (CS + profit)
        self.demand = demand
        self.f = f
        self.a = a
        self.b = b
        self.sol = {'q':q, 'p':p, 'CS':CS, 'profit':profit, 
                    'q_eff': q_eff, 'p_eff': p_eff, 'CS_eff':CS_eff, 'profit_eff':profit_eff,
                    'DWL':DWL}
    def print_cost_function(self, q='q'):
        f, a, b = self.f, self.a, self.b
        return fr"{PolyEq([f,a,b],q,[0,1,2])}"
    def setup(self):
        return fr"""
The market is supplied by a single monopolist, who can produce \(q\) units of the commodity at a total cost of:
$$ c(q) = {self.print_cost_function()} $$
"""

class Cournot2:
    def __init__(self, firm1, firm2, demand):
        a1 = firm1.a
        b1 = firm1.b
        a2 = firm2.a
        b2 = firm2.b
        alpha = demand.a
        beta = demand.b
        M = np.array([
            [2*beta+b1,      beta],
            [     beta, 2*beta+b2]
        ])
        y = np.array([alpha-a1, alpha-a2])
        x = np.linalg.solve(M, y)
        q1 = x[0]
        q2 = x[1]
        Q = q1 + q2
        p = alpha - beta*Q
        profit1 = firm1.profit_at(p, q1)
        profit2 = firm2.profit_at(p, q2)
        self.sol = {'p':p, 'q1':q1, 'q2':q2, 'Q':Q, 'profit1':profit1, 'profit2':profit2}
        self.firm1 = firm1
        self.firm2 = firm2
        self.demand = demand
    def setup(self):
        return fr"""
Price-taking consumers in the market for a commodity have a demand curve given by:
$$ Q = {self.demand.print()} $$
The market is supplied by two firms who produce identical products. Firm 1 has a cost function given by:
$$ c_1(q_1) = {self.firm1.print_cost_function(q='q_1')} $$
Firm 2 has a cost function given by:
$$ c_2(q_2) = {self.firm2.print_cost_function(q='q_2')} $$
The firms engage in Cournot competition, i.e. they choose the quantity they wish to produce and let the market determine the price.
"""

class CournotN:
    def __init__(self, mc, N, demand):
        alpha = demand.a
        beta = demand.b
        q = (alpha - mc)/((N+1)*beta)
        Q = N*q
        p = alpha - beta*Q
        profit = p*q - mc*q
        total_profit = N*profit
        self.N = N
        self.mc = mc
        self.demand = demand
        self.sol = {'q':q, 'Q':Q, 'p':p, 'profit':profit, 'total_profit':total_profit}
    def setup(self):
        return fr"""
Price-taking consumers in the market for a commodity have a demand curve given by:
$$ Q = {self.demand.print()} $$
The market is supplied by \(N={self.N:g}\) identical firms. Each firm has a constant average and marginal cost of production equal to \(c={self.mc:g}\). The firms engage in Cournot competition, i.e. they choose the quantity they wish to produce and let the market determine the price.
"""

class Insurance:
    def __init__(self, W0=1000, D=200, p=0.2, fun='ln'):
        self.W0 = W0
        self.D = D
        self.p = p
        self.fun = fun
        if fun=='ln':
            ufun = np.log
            uinv = np.exp
        elif fun=='sqrt':
            ufun = np.sqrt
            uinv = lambda x: x**2
        EX = (1-p)*W0 + p*(W0 - D)
        EU = (1-p)*ufun(W0) + p*ufun(W0 - D)
        CE = uinv(EU)
        WTP = W0 - CE
        FairCost = p*D
        self.sol = {'EX':EX, 'EU':EU, 'CE':CE, 'WTP':WTP, 'FairCost':FairCost}
    def setup(self):
        W0, D, p, fun = self.W0, self.D, self.p, self.fun
        if fun=='ln':
            funstr = fr"\ln X"
        elif fun=='sqrt':
            funstr = fr"\sqrt{{X}}"
        return fr"""
An individual has an initial wealth of \({W0:,g}\). There is a \({p*100:g}\%\) chance that the individual has an accident which would force them to pay \({D:,g}\) to fix the problem. Let \(X\) be a random variable representing the person's wealth at the end of the day. The individual's utility function over wealth is:
$$ u(X) = {funstr} $$
"""

class Savings:
    def __init__(self, Y, beta, p):
        self.Y = Y
        self.beta = beta
        self.p = p
        c2 = Y/(p*(1+1/beta))
        c1 = Y - p*c2
        r = (1-p)/p
        self.sol = {'c1':c1, 'c2':c2, 'r':r}
    def setup(self):
        Y, beta, p = self.Y, self.beta, self.p
        return fr"""
An individual lives for two periods. In period 1, they earn an income of \(Y={Y:,g}\). In period 2, they earn no income. In order to consume in period 2, they must buy bonds in period 1. One bond pays \(\$1\) in period 2, and can be purchased for price \(p={p:g}\) in period 1. The individual's objective is to maximize the present value of their utility:
$$u(c_1,c_2) = \ln c_1 + \beta \ln c_2$$
where \(c_1\) is consumption period 1, \(c_2\) is consumption in period 2, and \(\beta={beta:g}\) is the individual's subjective time discount factor.
"""

###################################################################
# PROBLEM GENERATION UTILITIES
###################################################################

def get_online_format(problem, setup_id=None, question_ids=None):
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

def get_multipart_sa(problem, setup_id=None, question_ids=None):
    setup = problem.setup_list[setup_id]['setup']
    assert len(setup)>0
    t = "\\begin{q}\n"
    t+= setup
    t+= "\\begin{enumerate}[a.]\n"
    for qid in question_ids:
        t+="\\item " + problem.question_list[qid]['question'] + "\n"
    t+= "\\end{enumerate}\n"
    t+= "\\end{q}\n"
    return RawLatex(t)

def get_multipart_mcq(problem, setup_id=None, question_ids=None):
    multipart = Multipart()
    setup = problem.setup_list[setup_id]['setup']
    assert len(setup)>0
    multipart.add(RawLatex(setup))
    for qid in question_ids:
        multipart.add(problem.question_list[qid]['MCQ'])
    return multipart
    
def get_single_sa(problem, setup_id=None, question_id=None):
    setup = problem.setup_list[setup_id]['setup']
    question = problem.question_list[question_id]['question']
    if len(setup)>0:
        question = setup + "\n\n" + question
    t = "\\begin{q}\n"
    t+= question
    t+= "\\end{q}\n"
    return RawLatex(t)

def get_single_mcq(problem, setup_id=None, question_id=None):
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
        axis = Axis(xn=params['xn'],yn=params['yn'],xunit=params['xunit'],yunit=params['yunit'],xlab=r'$q$',ylab=r'$p$')
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
        default_params = {'a':12,'b':1,'c':7}
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
        question = fr"Write an equation describing the contour line for \(f(x,y)=z\)."
        online_question = question
        answer = fr"\(y = {PolyEq([1/b,-a/b],'z',[0,1])}\)"
        online_answer = answer
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": None
        })
        question = fr"What is the y-intercept of the contour line for \(f(x,y)={z:g}\)?"
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
        question = fr"What is the x-intercept of the contour line for \(f(x,y)={z:g}\)?"
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
Using the grid below, draw contour lines for \(f(x,z)=z\) for multiple values of \(z\).
\begin{{center}}
\includegraphics[width=3in]{{{name}_setup.png}}
\end{{center}}
"""
        online_question = fr"""
Using the grid below, draw contour lines for \(f(x,z)=z\) for multiple values of \(z\).
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
        A_, a_, b_, px_ = a, a-1, b, px
        focx    = fr"\({CobbDouglas(A_,'x',a_,'y',b_)} = {px_:g} \lambda\)"
        A_, a_, b_, px_ = 1, a-1, b, px
        focx_d1 = fr"\({CobbDouglas(A_,'x',a_,'y',b_)} = \lambda\)"
        A_, a_, b_, px_ = a, a-1, b, px
        focx_d2 = fr"\({CobbDouglas(A_,'x',a_,'y',b_)} = {px_:g} \)"
        A_, a_, b_, px_ = b, a, b-1, py
        focx_d3 = fr"\({CobbDouglas(A_,'x',a_,'y',b_)} = {px_:g} \lambda\)"
        A_, a_, b_, py_ = b, a, b-1, py
        focy    = fr"\({CobbDouglas(A_,'x',a_,'y',b_)} = {py_:g} \lambda\)"
        A_, a_, b_, py_ = 1, a, b-1, py
        focy_d1 = fr"\({CobbDouglas(A_,'x',a_,'y',b_)} = \lambda\)"
        A_, a_, b_, py_ = b, a, b-1, py
        focy_d2 = fr"\({CobbDouglas(A_,'x',a_,'y',b_)} = {py_:g} \)"
        A_, a_, b_, py_ = a, a-1, b, px
        focy_d3 = fr"\({CobbDouglas(A_,'x',a_,'y',b_)} = {py_:g} \lambda\)"
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
        question = fr"Calculate the consumer's utility at the optimal choice."
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
        question = fr"Write the first order condition for \(x\)."
        online_question = question
        answer = focx
        online_answer = answer
        answers = [focx, focx_d1, focx_d2, focx_d3]
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        question = fr"Write the first order condition for \(y\)."
        online_question = question
        answer = focy
        online_answer = answer
        answers = [focy, focy_d1, focy_d2, focy_d3]
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
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

class PerfectSubstitutesProblem(GenericProblem):
    # u(x,y) = ax + by s.t. px x + py y = I
    def __init__(self, params=None, rng=rng, name='perfect_substitutes_problem'):
        default_params = {'a':2,'b':1,'px':1,'py':1,'I':12,'xunit':1,'yunit':1,'xn':13,'yn':13}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        a, b, px, py, I, xunit, yunit, xn, yn = params['a'], params['b'], params['px'], params['py'], params['I'], params['xunit'], params['yunit'], params['xn'], params['yn']
        budget_constraint = BudgetConstraint(px=px, py=py, I=I)
        self.budget_constraint = budget_constraint
        if (a*py - b*px)>0:
            x, y = I/px, 0
            passing = [(x_,0) for x_ in np.arange(xunit, xunit*5*xn, xunit)]
        elif (a*py - b*px)<0:
            x, y = 0, I/py
            passing = [(0,y_) for y_ in np.arange(yunit, yunit*5*yn, yunit)]
        else:
            x = 0.5*I/px
            y = 0.5*I/py
            passing = [(i*xunit,i*yunit) for i in np.arange(1, xn)]
        U = a*x + b*y
        self.sol = {'x':x, 'y':y, 'U':U}
        contours = LineContours(a,b,passing)
        point = Point(x,y,text='A',position='ne')
        setup_axis = Axis(xn=xn,yn=yn,xunit=xunit,yunit=yunit)
        solution_axis = Axis(xn=xn,yn=yn,xunit=xunit,yunit=yunit)
        setup_axis.add(contours)
        solution_axis.add(contours)
        solution_axis.add(budget_constraint)
        solution_axis.add(point)
        self.setup_axis = setup_axis
        self.solution_axis = solution_axis
        setup_list = []
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
        question = fr"What best describes the relationship between goods \(x\) and \(y\)?"
        online_question = question
        answer = "perfect substitutes"
        online_answer = answer
        answers = [answer, "perfect complements", "inferior goods", "Giffen goods"]
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if (self.sol['x']>0 and self.sol['y']>0): return False
        if not is_divisible(self.sol['x'], self.params['xunit']): return False
        if not is_divisible(self.sol['y'], self.params['yunit']): return False
        if not is_divisible(self.budget_constraint.xint, self.params['xunit']): return False
        if not is_divisible(self.budget_constraint.yint, self.params['yunit']): return False
        if self.sol['x'] >= self.setup_axis.xmax: return False
        if self.sol['y'] >= self.setup_axis.ymax: return False
        if self.budget_constraint.xint >= self.setup_axis.xmax: return False
        if self.budget_constraint.yint >= self.setup_axis.ymax: return False
        return True
        
class PerfectComplementsProblem(GenericProblem):
    # u(x,y) = min(x,y)
    def __init__(self, params=None, rng=rng, name='perfect_substitutes_problem'):
        default_params = {'px':1,'py':1,'I':12,'xunit':1,'yunit':1,'xn':13,'yn':13}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        px, py, I, xunit, yunit, xn, yn = params['px'], params['py'], params['I'], params['xunit'], params['yunit'], params['xn'], params['yn']
        budget_constraint = BudgetConstraint(px=px, py=py, I=I)
        self.budget_constraint = budget_constraint
        x = I/(px+py)
        y = I/(px+py)
        U = x
        self.sol = {'x':x, 'y':y, 'U':U}
        contours = LeontieffContours(xunit=xunit,yunit=yunit,xn=xn,yn=yn)
        point = Point(x,y,text='A',position='sw')
        setup_axis = Axis(xn=xn,yn=yn,xunit=xunit,yunit=yunit)
        solution_axis = Axis(xn=xn,yn=yn,xunit=xunit,yunit=yunit)
        setup_axis.add(contours)
        solution_axis.add(contours)
        solution_axis.add(budget_constraint)
        solution_axis.add(point)
        self.setup_axis = setup_axis
        self.solution_axis = solution_axis
        setup_list = []
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
        question = fr"What best describes the relationship between goods \(x\) and \(y\)?"
        online_question = question
        answer = "perfect complements"
        online_answer = answer
        answers = [answer, "perfect substitutes", "inferior goods", "quasilinear goods"]
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if not is_divisible(self.sol['x'], self.params['xunit']): return False
        if not is_divisible(self.sol['y'], self.params['yunit']): return False
        if not is_divisible(self.budget_constraint.xint, self.params['xunit']): return False
        if not is_divisible(self.budget_constraint.yint, self.params['yunit']): return False
        if self.sol['x'] >= self.setup_axis.xmax: return False
        if self.sol['y'] >= self.setup_axis.ymax: return False
        if self.budget_constraint.xint >= self.setup_axis.xmax: return False
        if self.budget_constraint.yint >= self.setup_axis.ymax: return False
        return True        
        
class PriceChangeProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='cobb_douglas_consumer_problem'):
        default_params = {'x1':7,'px1':1,'py1':1,'x2':8,'px2':1,'py2':2,'I':12,'xunit':1,'xn':13}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        x1, px1, py1, x2, px2, py2, I, xunit, xn = params['x1'], params['px1'], params['py1'], params['x2'], params['px2'], params['py2'], params['I'], params['xunit'], params['xn']
        y1 = (I - px1*x1)/py1
        y2 = (I - px2*x2)/py2
        bc1 = BudgetConstraint(px1,py1,I)
        bc2 = BudgetConstraint(px2,py2,I)
        setup_axis = Axis(xn=xn, xunit=xunit, yn=xn, yunit=xunit)
        solution_axis = Axis(xn=xn, xunit=xunit, yn=xn, yunit=xunit)
        contours = CESContours(x1,y1,x2,y2,bc1,bc2,setup_axis)
        self.contours = contours
        setup_axis.add(contours)
        solution_axis.add(contours)
        point1 = Point(x1,y1,text='A',position='sw')
        point2 = Point(x2,y2,text='B',position='sw')
        solution_axis.add(bc1, bc2, point1, point2)
        self.setup_axis = setup_axis
        self.solution_axis = solution_axis
        if px2!=px1:
            price_that_changed = 'x'
            myp2 = px2
            if (y2-y1)/(px2-px1) > 0:
                comp_or_sub = 'substitutes'
            elif (y2-y1)/(px2-px1) < 0:
                comp_or_sub = 'complements'
            else:
                comp_or_sub = 'neither'
        if py2!=py1:
            myp2 = py2
            price_that_changed = 'y'
            if (x2-x1)/(py2-py1) > 0:
                comp_or_sub = 'substitutes'
            elif (x2-x1)/(py2-py1) < 0:
                comp_or_sub = 'complements'
            else:
                comp_or_sub = 'neither'
        self.sol = {'y1':y1, 'y2':y2, 'price_that_changed':price_that_changed, 'comp_or_sub':comp_or_sub}
        setup_list = []
        setup = fr"""
A consumer with income \(I={I:g}\) has utility over two goods, \(x\) and \(y\), shown by the indifference curves below.
\begin{{center}}
\includegraphics[width=3in]{{{name}_setup.png}}
\end{{center}}
The prices of the goods are initially \(p_x = {px1:g}\) and \(p_y = {py1:g}\). One day, the price of good \({price_that_changed}\) changes to \(p_{price_that_changed}^\prime = {myp2:g}\).
"""
        online_setup = fr"""
A consumer with income \(I={I:g}\) has utility over two goods, \(x\) and \(y\), shown by the indifference curves below.
<p>
<img src="/CSUN-Econ-310/assets/images/graphs/{name}_setup.png">
</p>
The prices of the goods are initially \(p_x = {px1:g}\) and \(p_y = {py1:g}\). One day, the price of good \({price_that_changed}\) increases to \(p_{price_that_changed}^\prime = {myp2:g}\).
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"Draw the consumer's budget constraint in both periods. Label the optimal point in the initial period A. Label the optimal point after the prices change B."
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
        question = fr"Did consumption of \(x\) increase or decrease as a result of the price change?"
        online_question = question
        if x2>x1: answer = "increase"
        elif x2<x1: answer = "decrease"
        else: answer = "neither"
        online_answer = answer
        answers = ["increase", "decrease", "neither"]
        sol = answers.index(answer)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,sol,horz=True,shuffle=False,rng=rng)
        })
        question = fr"Did consumption of \(y\) increase or decrease as a result of the price change?"
        online_question = question
        if y2>y1: answer = "increase"
        elif y2<y1: answer = "decrease"
        else: answer = "neither"
        online_answer = answer
        answers = ["increase", "decrease", "neither"]
        sol = answers.index(answer)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,sol,horz=True,shuffle=False,rng=rng)
        })
        question = fr"Are \(x\) and \(y\) complements or substitutes at current price levels?"
        online_question = question
        answer = comp_or_sub
        online_answer = answer
        answers = ["complements", "substitutes","neither"]
        sol = answers.index(answer)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,sol,horz=True,shuffle=False,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if self.contours.ces.bad: return False
        if self.contours.ces.a<=0: return False
        if self.contours.ces.a>=1: return False
        if self.params['x1']==self.params['x2']: return False
        if (self.params['px1']==self.params['px2']) and (self.params['py1']==self.params['py2']): return False
        if (self.params['px1']!=self.params['px2']) and (self.params['py1']!=self.params['py2']): return False
        if not is_divisible(self.sol['y1'], self.setup_axis.yunit): return False
        if not is_divisible(self.sol['y2'], self.setup_axis.yunit): return False
        if not is_divisible(self.params['x1'], self.setup_axis.xunit): return False
        if not is_divisible(self.params['x2'], self.setup_axis.xunit): return False
        if not is_divisible(self.params['I']/self.params['py1'], self.setup_axis.yunit): return False
        if not is_divisible(self.params['I']/self.params['py2'], self.setup_axis.yunit): return False
        if not is_divisible(self.params['I']/self.params['px1'], self.setup_axis.xunit): return False
        if not is_divisible(self.params['I']/self.params['px2'], self.setup_axis.xunit): return False
        return True
        
class PublicSchoolProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='public_school_problem'):
        default_params = {'x_private':6,'x_public':4,'px':1,'py':1,'I':12,'xunit':1,'xn':13}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        x_private, x_public, px, py, I, xunit, xn = params['x_private'], params['x_public'], params['px'], params['py'], params['I'], params['xunit'], params['xn']
        y_private = (I-px*x_private)/py
        bc = BudgetConstraint(px,py,I)
        cb = get_cb_from_point(x_private, y_private, bc)
        U_private = cb.eval_at(x_private, y_private)
        U_public = cb.eval_at(x_public, I/py)
        if equals(U_private, U_public):
            choice = 'unknown'
            xchoice = None
            ychoice = None
        elif U_private>U_public: 
            choice = 'private'
            xchoice = x_private
            ychoice = y_private
        else:
            choice = 'public'
            xchoice = x_public
            ychoice = I/py
        self.sol = {'y_private':y_private,'U_private':U_private, 'U_public':U_public, 'choice':choice, 'xchoice':xchoice, 'ychoice':ychoice}
        setup_axis = Axis(xn=xn,yn=xn,xunit=xunit,yunit=xunit, xlab="Education", ylab="Other Goods")
        solution_axis = Axis(xn=xn,yn=xn,xunit=xunit,yunit=xunit, xlab="Education", ylab="Other Goods")
        levels = get_cb_levels(cb, setup_axis, U_private)
        contours = CobbDouglasContours(cb, levels)
        setup_axis.add(contours)
        solution_axis.add(contours)
        private_point = Point(x=x_private, y=y_private, text='A', position='sw')
        public_point = Point(x=x_public, y=I/py, text='B', position='ne')
        solution_axis.add(private_point)
        setup_axis.add(bc)
        solution_axis.add(bc)
        solution_axis.add(public_point)
        self.setup_axis = setup_axis
        self.solution_axis = solution_axis
        setup_list = []
        setup = fr"""
A family can spend their income on either education or other goods. The diagram below shows the family's budget constraint when only private school options are available, as well as their indifference curves over education and other consumption.
\begin{{center}}
\includegraphics[width=3in]{{{name}_setup.png}}
\end{{center}}
A public school option is also available which provides {x_public:g} units of education for free.
"""
        online_setup = fr"""
A family can spend their income on either education or other goods. The diagram below shows the family's budget constraint when only private school options are available, as well as their indifference curves over education and other consumption.
<p>
<img src="/CSUN-Econ-310/assets/images/graphs/{name}_setup.png">
</p>
A public school option is also available which provides {x_public:g} units of education for free.
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"On the diagram, label the optimal private school option A and label the public school option B."
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
        question = fr"Which option offers higher utility, public or private?"
        online_question = question
        if choice=="private": answer="private"
        elif choice=="public": answer="public"
        else: answer="they offer the same utility"
        online_answer = answer
        answers = ["public", "private", "they offer the same utility"]
        sol = answers.index(answer)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,sol,horz=True,shuffle=False,rng=rng)
        })
        question = fr"Which option will the family choose?"
        online_question = question
        if choice=="private": answer="private"
        elif choice=="public": answer="public"
        else: answer="not enough information"
        online_answer = answer
        answers = ["public", "private", "not enough information"]
        sol = answers.index(answer)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,sol,horz=True,shuffle=False,rng=rng)
        })
        question = fr"If the public school option were removed, would this increase or decrease the amount of education consumed?"
        online_question = question
        if choice=='private': answer="neither increase nor decrease"
        elif choice=='unknown': answer="not enough information"
        elif x_private>xchoice: answer="increase"
        elif x_private<xchoice: answer="decrease"
        else: answer="neither increase nor decrease"
        online_answer = answer
        answers = ["increase", "decrease", "neither increase nor decrease", "not enough information"]
        sol = answers.index(answer)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,sol,horz=False,shuffle=False,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if not is_divisible(self.sol['y_private'], self.params['xunit']): return False
        if np.abs(self.sol['U_public'] - self.sol['U_private'])/self.sol['U_private']<0.1: return False
        return True
    
class CobbDouglasWorkerProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='cobb_douglas_worker_problem'):
        default_params = {'x':6,'w':15,'yunit':15*5}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        x, w, yunit = self.params['x'], self.params['w'], self.params['yunit']
        T = 60 # time budget
        I = w*T
        y = I-w*x
        bc = BudgetConstraint(w,1,I)
        cb = get_cb_from_point(x, y, bc)
        U = cb.eval_at(x,y)
        self.sol = {'y':y, 'I':I}
        setup_axis = Axis(xn=13, yn=13, xunit=5, yunit=yunit, xlab='Leisure Hours', ylab='Income')
        solution_axis = Axis(xn=13, yn=13, xunit=5, yunit=yunit, xlab='Leisure Hours', ylab='Income')
        levels = get_cb_levels(cb, setup_axis, U)
        contours = CobbDouglasContours(cb, levels)
        self.contours = contours
        setup_axis.add(contours)
        solution_axis.add(contours)
        point = Point(x,y,text='A',position='sw')
        solution_axis.add(bc, point)
        self.setup_axis = setup_axis
        self.solution_axis = solution_axis
        setup_list = []
        setup = fr"""
A worker has up to 60 hours a week to spend on working or on leisure. If he works, he makes a wage rate of \(w={w:g}\) dollars per hour. The worker's 
indifference curves over leisure and income are shown in the diagram below.
\begin{{center}}
\includegraphics[width=3in]{{{name}_setup.png}}
\end{{center}}
"""
        online_setup = fr"""
A worker has up to 60 hours a week to spend on working or on leisure. If he works, he makes a wage rate of \(w={w:g}\) dollars per hour. The worker's 
indifference curves over leisure and income are shown in the diagram below.
<p>
<img src="/CSUN-Econ-310/assets/images/graphs/{name}_setup.png">
</p>
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"Draw the worker's budget constraint. Label the optimal point A."
        online_question = question
        answer = fr"\begin{{center}}\includegraphics[width=3in]{{{name}_sol.png}}\end{{center}}"
        online_answer = f'<img src = "/CSUN-Econ-310/assets/images/graphs/{name}_sol.png">'
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": None
        })
        question = fr"How many hours per week does the worker choose to work?"
        online_question = question
        answer = T - x
        online_answer = fr"\({answer:g}\) hours"
        answers = generate_distractors(answer,delta=5,type='add',rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })        
        question = fr"How income per week does the worker make?"
        online_question = question
        answer = y
        online_answer = fr"\({answer:g}\) dollars"
        answers = generate_distractors(answer,delta=setup_axis.yunit,type='add',rng=rng)
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
        if not is_divisible(self.params['x'], self.setup_axis.xunit): return False
        if not is_divisible(self.sol['y'], self.setup_axis.yunit): return False
        if not is_divisible(self.sol['I'], self.setup_axis.yunit): return False
        if not is_divisible(self.setup_axis.yunit, 1): return False
        return True

class WageChangeProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='wage_change_problem'):
        default_params = {'x1':6,'w1':15,'x2':6,'w2':30}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        x1, w1, x2, w2 = params['x1'], params['w1'], params['x2'], params['w2']
        T = 60 # time budget
        I1 = w1*T
        I2 = w2*T
        y1 = (I1 - w1*x1)
        y2 = (I2 - w2*x2)
        bc1 = BudgetConstraint(w1,1,I1)
        bc2 = BudgetConstraint(w2,1,I2)
        setup_axis = Axis(xn=13, yn=13, xunit=5, yunit=5*T, xlab='Leisure Hours', ylab='Income')
        solution_axis = Axis(xn=13, yn=13, xunit=5, yunit=5*T, xlab='Leisure Hours', ylab='Income')
        contours = CESContours(x1,y1,x2,y2,bc1,bc2,setup_axis)
        self.contours = contours
        setup_axis.add(contours)
        solution_axis.add(contours)
        point1 = Point(x1,y1,text='A',position='sw')
        point2 = Point(x2,y2,text='B',position='sw')
        solution_axis.add(bc1, bc2, point1, point2)
        self.setup_axis = setup_axis
        self.solution_axis = solution_axis
        if w1>w2:
            wage_inc_or_dec = 'decreases'
        elif w1<w2:
            wage_inc_or_dec = 'increases'
        else:
            wage_inc_or_dec = 'neither'
        if x1>x2:
            labor_inc_or_dec = 'increase'
        elif x1<x2:
            labor_inc_or_dec = 'decrease'
        else:
            labor_inc_or_dec = 'neither increase nor decrease'
        self.sol = {'y1':y1, 'y2':y2, 'I1':I1, 'I2':I2, 'wage_inc_or_dec':wage_inc_or_dec, 'labor_inc_or_dec':labor_inc_or_dec}
        setup_list = []
        setup = fr"""
A worker has up to 60 hours a week to spend on working or on leisure. If he works, he makes a wage rate of \(w={w1:g}\) dollars per hour. The worker's 
indifference curves over leisure and income are shown in the diagram below.
\begin{{center}}
\includegraphics[width=3in]{{{name}_setup.png}}
\end{{center}}
One day, the worker's hourly wage changes to \(w^\prime = {w2:g}\).
"""
        online_setup = fr"""
A worker has up to 60 hours a week to spend on working or on leisure. If he works, he makes a wage rate of \(w={w1:g}\) dollars per hour. The worker's 
indifference curves over leisure and income are shown in the diagram below.
<p>
<img src="/CSUN-Econ-310/assets/images/graphs/{name}_setup.png">
</p>
One day, the worker's hourly wage changes to \(w^\prime = {w2:g}\).
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"Draw the worker's budget constraint at both the initial wage and the subsequent wage. Label the optimal point at the initial wage A. Label the optimal point at the subsequent wage B."
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
        question = fr"How many hours per week does the worker work at the initial wage, \(w\)?"
        online_question = question
        answer = T - x1
        online_answer = fr"\({answer:g}\) hours"
        answers = generate_distractors(answer,delta=5,type='add',rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })        
        question = fr"How many hours per week does the worker work at the subsequent wage, \(w^\prime\)?"
        online_question = question
        answer = T - x2
        online_answer = fr"\({answer:g}\) hours"
        answers = generate_distractors(answer,delta=5,type='add',rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"Did the number of hours worked increase or decrease as a result of the wage change?"
        online_question = question
        if labor_inc_or_dec=='increase': answer = "increase"
        elif labor_inc_or_dec=='decrease': answer = "decrease"
        else: answer = "neither increase nor decrease"
        online_answer = answer
        answers = ["increase", "decrease", "neither increase nor decrease"]
        sol = answers.index(answer)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,sol,horz=True,shuffle=False,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if self.contours.ces.bad: return False
        if self.contours.ces.a<=0: return False
        if self.contours.ces.a>=1: return False
        if equals(self.params['w1'], self.params['w2']): return False
        if not is_divisible(self.setup_axis.yunit, 1): return False
        if not is_divisible(self.sol['I1'], self.setup_axis.yunit): return False
        if not is_divisible(self.sol['I2'], self.setup_axis.yunit): return False
        if not is_divisible(self.sol['y1'], self.setup_axis.yunit): return False
        if not is_divisible(self.sol['y2'], self.setup_axis.yunit): return False
        return True


class IncomeSupportProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='income_support_problem'):
        default_params = {'x':6,'w':15,'yunit':15*5,'ymin':15*5}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        x, w, yunit, ymin = self.params['x'], self.params['w'], self.params['yunit'], self.params['ymin']
        T = 60 # time budget
        I = w*T
        y = I-w*x
        bc = BudgetConstraint(w,1,I)
        ibc = IncomeSupportBudget(bc, ymin)
        cb = get_cb_from_point(x, y, bc)
        U_work = cb.eval_at(x,y)
        U_nowork = cb.eval_at(T,ymin)
        if U_work > U_nowork:
            work = 'yes'
            x_choice = x
            y_choice = y
        elif U_work < U_nowork:
            work = 'no'
            x_choice = T
            y_choice = ymin
        else:
            work = 'not enough information'
            x_choice = x
            y_choice = y
        self.sol = {'y':y, 'I':I, 'U_work':U_work, 'U_nowork':U_nowork, 'work':work, 'x_choice':x_choice, 'y_choice':y_choice}
        setup_axis = Axis(xn=13, yn=13, xunit=5, yunit=yunit, xlab='Leisure Hours', ylab='Income')
        solution_axis = Axis(xn=13, yn=13, xunit=5, yunit=yunit, xlab='Leisure Hours', ylab='Income')
        levels = get_cb_levels(cb, setup_axis, U_work)
        contours = CobbDouglasContours(cb, levels)
        self.contours = contours
        setup_axis.add(contours)
        solution_axis.add(contours)
        point = Point(x_choice,y_choice,text='A',position='sw')
        solution_axis.add(ibc, point)
        self.setup_axis = setup_axis
        self.solution_axis = solution_axis
        setup_list = []
        setup = fr"""
A worker has up to 60 hours a week to spend on working or on leisure. If he works, he makes a wage rate of \(w={w:g}\) dollars per hour. The worker's 
indifference curves over leisure and income are shown in the diagram below.
\begin{{center}}
\includegraphics[width=3in]{{{name}_setup.png}}
\end{{center}}
In addition, the government provides minimum income support of up to \({ymin:g}\) dollars a week. That is, if someone earns less than \({ymin:g}\) dollars a week, the government supplements their income until it reaches \({ymin:g}\) a week.
"""
        online_setup = fr"""
A worker has up to 60 hours a week to spend on working or on leisure. If he works, he makes a wage rate of \(w={w:g}\) dollars per hour. The worker's 
indifference curves over leisure and income are shown in the diagram below.
<p>
<img src="/CSUN-Econ-310/assets/images/graphs/{name}_setup.png">
</p>
In addition, the government provides minimum income support of up to \({ymin:g}\) dollars a week. That is, if someone earns less than \({ymin:g}\) dollars a week, the government supplements their income until it reaches \({ymin:g}\) a week.
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"Draw the worker's budget constraint. Label the optimal point A."
        online_question = question
        answer = fr"\begin{{center}}\includegraphics[width=3in]{{{name}_sol.png}}\end{{center}}"
        online_answer = f'<img src = "/CSUN-Econ-310/assets/images/graphs/{name}_sol.png">'
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": None
        })
        question = fr"How many hours per week does the worker choose to work?"
        online_question = question
        if work=='yes': answer = fr'{T-x:g}'
        elif work=='no': answer = fr'{0:g}'
        else: answer = 'not enough information'
        online_answer = fr"{answer} hours"
        answers = [fr'{0:g}', fr'{T-x:g}', fr'{60:g}', 'not enough information']
        sol = answers.index(answer)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,sol,horz=True,shuffle=False,rng=rng)
        })
        question = fr"If income support were removed, how many hours would the worker choose to work?"
        online_question = question
        answer = fr'{T-x:g}'
        online_answer = fr"{answer} hours"
        answers = [fr'{0:g}', fr'{T-x:g}', fr'{60:g}', 'not enough information']
        sol = answers.index(answer)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,sol,horz=True,shuffle=False,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if not is_divisible(self.params['x'], self.setup_axis.xunit): return False
        if not is_divisible(self.sol['y'], self.setup_axis.yunit): return False
        if not is_divisible(self.sol['I'], self.setup_axis.yunit): return False
        if not is_divisible(self.params['ymin'], self.setup_axis.yunit): return False
        if not is_divisible(self.setup_axis.yunit, 1): return False
        if np.abs(self.sol['U_work'] - self.sol['U_nowork'])/self.sol['U_work']<0.1: return False
        return True

class ReturnsToScaleProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='cobb_douglas_consumer_problem'):
        default_params = {'A':1,'a':1/2,'b':1/2,'delta':0.5}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        A, a, b, delta = params['A'], params['a'], params['b'], params['delta']
        if delta<0: 
            input_inc_dec = "reduces"
            output_inc_dec = "decrease"
        elif delta>0: 
            input_inc_dec = "increases"
            output_inc_dec = "increase"
        else: 
            input_inc_dec = "neither"
            output_inc_dec = "neither"
        if a+b==1: rts="constant returns to scale"
        elif a+b>1: rts="increasing returns to scale"
        else: rts="decreasing returns to scale"
        self.sol['rts'] = rts
        cb = CobbDouglas(A=A,a=a,b=b,x='L',y='K')
        setup_list = []
        setup = fr"""
A firm uses labor \(L\) and capital \(K\) to produce a commodity output. The firm's production function is:
$$f(L,K) = {cb}$$
"""
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"Does the firm exhibit increasing, decreasing, or constant returns to scale?"
        online_question = question
        answer = rts
        online_answer = answer
        answers = ["increasing returns to scale", "decreasing returns to scale", "constant returns to scale"]
        sol = answers.index(answer)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,sol,horz=True,rng=rng)
        })
        question = fr"Suppose the firm {input_inc_dec} both its labor and capital input by \({np.abs(delta)*100:g}\%\). This would cause the firm's output to {output_inc_dec} by a factor of:"
        online_question = fr"Suppose the firm {input_inc_dec} both its labor and capital input by \({np.abs(delta)*100:g}\%\). This would cause the firm's output to {output_inc_dec} by a factor of what?"
        answer = np.abs((1+delta)**(a+b)-1)
        online_answer = fr"\({answer*100:g}\%\)"
        answers = generate_distractors(answer,K=4,delta=1.25,type='mul')
        answers = [fr"\({ans*100:g}\%\)" for ans in answers]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,sort=True,rng=rng)
        })
        question = fr"Suppose the firm {input_inc_dec} its labor input by \({np.abs(delta)*100:g}\%\) without changing its capital input. This would cause the firm's output to {output_inc_dec} by a factor of:"
        online_question = fr"Suppose the firm {input_inc_dec} its labor input by \({np.abs(delta)*100:g}\%\) without changing its capital input. This would cause the firm's output to {output_inc_dec} by a factor of what?"
        answer = np.abs((1+delta)**a-1)
        online_answer = fr"\({answer*100:g}\%\)"
        answers = generate_distractors(answer,K=4,delta=1.25,type='mul')
        answers = [fr"\({ans*100:g}\%\)" for ans in answers]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,sort=True,rng=rng)
        })
        question = fr"Suppose the firm {input_inc_dec} its capital input by \({np.abs(delta)*100:g}\%\) without changing its labor input. This would cause the firm's output to {output_inc_dec} by a factor of:"
        online_question = fr"Suppose the firm {input_inc_dec} its capital input by \({np.abs(delta)*100:g}\%\) without changing its labor input. This would cause the firm's output to {output_inc_dec} by a factor of what?"
        answer = np.abs((1+delta)**b-1)
        online_answer = fr"\({answer*100:g}\%\)"
        answers = generate_distractors(answer,K=4,delta=1.25,type='mul')
        answers = [fr"\({ans*100:g}\%\)" for ans in answers]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,sort=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
        
class CobbDouglasFirmProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='cobb_douglas_firm_problem'):
        default_params = {'A':1, 'a':1/2, 'w':1, 'r':1}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        A, a, w, r = params['A'], params['a'], params['w'], params['r']
        firm = CobbDouglasFirm(A,a)
        L = firm.unit_cost_L(w,r)
        K = firm.unit_cost_K(w,r)
        unit_cost = firm.unit_cost(w,r)
        self.sol = {'L':L, 'K':K, 'unit_cost':unit_cost}
        setup_list = []
        setup = fr"""
A firm has a constant returns to scale production function over labor and capital given by:
$$ f(L,K) = {firm.cb} $$
The unit price of labor is \(w={w:g}\) and the unit price of capital is \(r={r:g}\).
"""
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"What choice of labor \(L\) minimizes the cost to produce one unit of output?"
        online_question = question
        answer = L
        online_answer = fr"\(L = {answer:g}\)"
        answers = generate_distractors(answer, type='add')
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"What choice of capital \(K\) minimizes the cost to produce one unit of output?"
        online_question = question
        answer = K
        online_answer = fr"\(K = {answer:g}\)"
        answers = generate_distractors(answer, type='add')
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"What is the firm's cost to produce one unit?"
        online_question = question
        answer = unit_cost
        online_answer = fr"\(MC = {answer:g}\)"
        answers = generate_distractors(answer, type='add')
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list        
        
class CobbDouglasFirmGraphicalProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='cobb_douglas_firm_problem'):
        default_params = {'L':4, 'K':4, 'w':1, 'r':1, 'xunit':1}
        xn = 13
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        L, K, w, r, xunit = params['L'], params['K'], params['w'], params['r'], params['xunit']
        unit_cost = w*L + r*K
        self.sol['unit_cost'] = unit_cost
        firm = get_cb_firm_from_point(L, K, w, r)
        setup_axis = Axis(xn=13,yn=13,xunit=xunit,yunit=xunit,xlab=r'$L$',ylab=r'$K$')
        passing = [(L+i*xunit, K+i*xunit) for i in np.arange(-xn,xn)]
        contours = LineContours(w, r, passing)
        self.contours = contours
        setup_axis.add(contours)
        setup_axis.add(firm)
        self.setup_axis = setup_axis
        setup_list = []
        setup = fr"""
A firm has a constant returns to scale production function. Its unit isoquant and isocost curves are shown in the diagram below:
\begin{{center}}
\includegraphics[width=3in]{{{name}_setup.png}}
\end{{center}}
The unit price of labor is \(w={w:g}\) and the unit price of capital is \(r={r:g}\).
"""
        online_setup = fr"""
A firm has a constant returns to scale production function. Its unit isoquant and isocost curves are shown in the diagram below:
<p>
<img src="/CSUN-Econ-310/assets/images/graphs/{name}_setup.png">
</p>
The unit price of labor is \(w={w:g}\) and the unit price of capital is \(r={r:g}\).
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"What choice of labor \(L\) minimizes the cost to produce one unit of output?"
        online_question = question
        answer = L
        online_answer = fr"\(L = {answer:g}\)"
        answers = generate_distractors(answer, delta=xunit, type='add')
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"What choice of capital \(K\) minimizes the cost to produce one unit of output?"
        online_question = question
        answer = K
        online_answer = fr"\(K = {answer:g}\)"
        answers = generate_distractors(answer, delta=xunit, type='add')
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"What is the firm's cost to produce one unit?"
        online_question = question
        answer = unit_cost
        online_answer = fr"\(MC = {answer:g}\)"
        answers = generate_distractors(answer, type='add')
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if not is_divisible(self.params['L'], self.setup_axis.xunit): return False
        if not is_divisible(self.params['K'], self.setup_axis.yunit): return False
        return True

class TechnicalChangeProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='technical_change_problem'):
        default_params = {'A1':1, 'A2':2, 'a1':1/2, 'a2':1/2}
        xn = 13
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        A1, A2, a1, a2 = params['A1'], params['A2'], params['a1'], params['a2']
        if A2>A1:
            changetype = 'increase in total factor productivity'
        elif A2<A1:
            changetype = 'decrease in total factor productivity'
        elif a2>a1:
            changetype = 'technical change favoring labor'
        elif a2<a1:
            changetype = 'technical change favoring capital'
        else:
            changetype = 'no change'
        self.sol['changetype'] = changetype
        firm1 = CobbDouglasFirm(A=A1, a=a1, label='T1')
        firm2 = CobbDouglasFirm(A=A2, a=a2, color='red', linestyle='dashed', label='T2')
        if equals(A1,A2):
            xunit = (1/A1)/6
            yunit = (1/A1)/6
        else:
            yunit = (1/A1 + 1/A2)/12
            xunit = (1/A1 + 1/A2)/12
        setup_axis = Axis(xn=xn,yn=xn,xunit=xunit,yunit=yunit,noticklabels=True,xlab=r'$L$',ylab=r'$K$')
        setup_axis.add(firm1)
        setup_axis.add(firm2)
        self.setup_axis = setup_axis
        setup_list = []
        setup = fr"""
The diagram below illustrates a technological change in a firm's production function. The black solid line shows the firm's unit isoquant prior to the technical change, and the red dashed line shows the firm's unit isoquant subsequent to the technical change.
\begin{{center}}
\includegraphics[width=3in]{{{name}_setup.png}}
\end{{center}}
"""
        online_setup = fr"""
The diagram below illustrates a technological change in a firm's production function. The black solid line shows the firm's unit isoquant prior to the technical change, and the red dashed line shows the firm's unit isoquant subsequent to the technical change.
<p>
<img src="/CSUN-Econ-310/assets/images/graphs/{name}_setup.png">
</p>
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"What type of technical change does this illustrate?"
        online_question = question
        answer = changetype
        online_answer = answer
        answers = [
            'increase in total factor productivity',
            'decrease in total factor productivity',
            'technical change favoring labor',
            'technical change favoring capital'
        ]
        sol = answers.index(answer)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,sol,horz=False,shuffle=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        params = self.params
        A1, A2, a1, a2 = params['A1'], params['A2'], params['a1'], params['a2']
        if (A1!=A2) and (a1!=a2): return False
        if equals(A1,A2) and equals(a1,a2): return False
        return True
        
class NormalFormProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='normal_form_problem'):
        default_params = {
            'players': ['Player 1', 'Player 2'],
            'strategies': [['A','B'],['A','B']],
            'payoffs': [[[4,4],[10,0]],
                        [[0,10],[6,6]]],
            'gametype': "Prisoner's Dilemma"
        }
        xn = 13
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        players, strategies, payoffs, gametype = params['players'], params['strategies'], params['payoffs'], params['gametype']
        normalform = NormalForm(players=players, strategies=strategies, payoffs=payoffs, gametype=gametype)
        ne = normalform.ne
        ne_distractors = normalform.ne_distractors
        if len(ne)==0:
            ne_sol = fr"No Nash Equilibria"
            _distractors_ = rng.choice(ne_distractors, 2, replace=False)
            ne_d1 = fr"1 Nash Equilibria: {_distractors_[0]}"
            ne_d2 = fr"1 Nash Equilibria: {_distractors_[1]}"
            ne_d3 = fr"2 Nash Equilibria: {', '.join(rng.choice(ne_distractors,2,replace=False))}"
        elif len(ne)==1:
            ne_sol = fr"{len(ne)} Nash Equilibria: {ne[0]}"
            ne_d1 = fr"No Nash Equilibria"
            ne_d2 = fr"1 Nash Equilibria: {rng.choice(ne_distractors)}"
            ne_d3 = fr"2 Nash Equilibria: {', '.join(rng.choice(ne_distractors,2,replace=False))}"
        else:
            ne_sol = fr"{len(ne)} Nash Equilibria: {', '.join(ne)}"
            ne_d1 = fr"No Nash Equilibria"
            ne_d2 = fr"1 Nash Equilibria: {rng.choice(ne_distractors)}"
            ne_d3 = fr"2 Nash Equilibria: {', '.join(rng.choice(ne_distractors,2,replace=False))}"
        self.normalform = normalform
        setup_list = []
        setup = fr"""
Consider the 2-player game described by the normal form below:
{normalform.table_as_latex()}
"""
        online_setup = fr"""
<p>Consider the 2-player game described by the normal form below:</p>
{normalform.table_as_html()}
"""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = "Find all the Nash equilibria."
        online_question = question
        answer = ne_sol
        online_answer = answer
        answers = [ne_sol, ne_d1, ne_d2, ne_d3]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=False,shuffle=True,rng=rng)
        })
        question = "Do the strategic dynamics of this game most resemble Prisoner's Dilemma, Stag Hunt, Chicken, or Rock Paper Scissors?"
        online_question = question
        answer = gametype
        online_answer = answer
        answers = ["Prisoner's Dilemma", "Stag Hunt", "Chicken", "Rock Paper Scissors"]
        sol = answers.index(answer)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,sol,horz=True,shuffle=False,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list

class MonopolyProblem(GenericProblem):
    # p = alpha - beta*q
    # c(q) = f + a*q + b*q^2
    def __init__(self, params=None, rng=rng, name='quadratic_optimization_problem'):
        default_params = {'alpha':12,'beta':1,'f':0,'a':0,'b':0.5}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        alpha, beta, f, a, b = params['alpha'], params['beta'], params['f'], params['a'], params['b']
        consumer = LinearConsumer(alpha, beta)
        monopoly = Monopoly(consumer.demand, f, a, b)
        self.consumer = consumer
        self.monopoly = monopoly
        self.sol = monopoly.sol.copy()
        setup_list = []
        setup = fr"""
Price-taking consumers in the market for a commodity have a demand curve given by:
$$ q = {consumer.demand.print()} $$
{monopoly.setup()}
"""
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        setup = fr"""
{consumer.setup()}
{monopoly.setup()}
"""
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = "Calculate the profit maximizing price."
        answer = monopoly.sol['p']
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": fr"\(p = {answer:g}\)",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "Calculate the profit maximizing quantity."
        answer = monopoly.sol['q']
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": fr"\(q = {answer:g}\)",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "Calculate the monopolist's profit."
        answer = monopoly.sol['profit']
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": fr"\(\Pi = {answer:g}\)",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "Calculate the consumer surplus."
        answer = monopoly.sol['CS']
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": fr"\(CS = {answer:g}\)",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "What is the efficient quantity that would maximize total surplus?"
        answer = monopoly.sol['q_eff']
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": fr"\(q_e = {answer:g}\)",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "What is the efficient price level?"
        answer = monopoly.sol['p_eff']
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": fr"\(p_e = {answer:g}\)",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "Calculate the monopolist's profit at the efficient outcome."
        answer = monopoly.sol['profit_eff']
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": fr"\(\Pi_e = {answer:g}\)",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "Calculate the consumer surplus at the efficient outcome."
        answer = monopoly.sol['CS_eff']
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": fr"\(CS_e = {answer:g}\)",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "Calculate the deadweight loss caused by monopolistic behavior."
        answer = monopoly.sol['DWL']
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": fr"\(DWL = {answer:g}\)",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if not is_divisible(self.sol['q'],1): return False
        if not is_divisible(self.sol['p'],1): return False
        if not is_divisible(self.sol['q_eff'],1): return False
        if not is_divisible(self.sol['p_eff'],1): return False
        if self.sol['q']<=0: return False
        if self.sol['p']<=0: return False
        if self.sol['q_eff']<=0: return False
        if self.sol['p_eff']<=0: return False
        if self.sol['profit']<=0: return False
        return True
        
class Cournot2Problem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='cournot2_problem'):
        default_params = {'alpha':12,'beta':1,'a1':0,'b1':1,'a2':0,'b2':1}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        alpha, beta, a1, b1, a2, b2 = params['alpha'], params['beta'], params['a1'], params['b1'], params['a2'], params['b2']
        firm1 = QuadraticCostFirm(a=a1, b=b1)
        firm2 = QuadraticCostFirm(a=a2, b=b2)
        demand = LinearDemand(a=alpha, b=beta)
        cournot2 = Cournot2(firm1, firm2, demand)
        self.sol = cournot2.sol.copy()
        self.cournot2 = cournot2
        setup_list = []
        setup = cournot2.setup()
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = "What quantity does firm 1 produce in the Nash equilibrium?"
        online_question = question
        answer = cournot2.sol['q1']
        online_answer = fr"\(q_1 = {answer:g}\)"
        answers = generate_distractors(answer, rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "What quantity does firm 2 produce in the Nash equilibrium?"
        online_question = question
        answer = cournot2.sol['q2']
        online_answer = fr"\(q_2 = {answer:g}\)"
        answers = generate_distractors(answer, rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "What is the Nash equilibrium price in this market?"
        online_question = question
        answer = cournot2.sol['p']
        online_answer = fr"\(p = {answer:g}\)"
        answers = generate_distractors(answer, rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "What is the Nash equilibrium profit of firm 1?"
        online_question = question
        answer = cournot2.sol['profit1']
        online_answer = fr"\(\Pi_1 = {answer:g}\)"
        answers = generate_distractors(answer, rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "What is the Nash equilibrium profit of firm 2?"
        online_question = question
        answer = cournot2.sol['profit2']
        online_answer = fr"\(\Pi_2 = {answer:g}\)"
        answers = generate_distractors(answer, rng=rng)
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
        if not is_divisible(self.sol['p'],1): return False
        if not is_divisible(self.sol['q1'],1): return False
        if not is_divisible(self.sol['q2'],1): return False
        if self.sol['p']<=0: return False
        if self.sol['q1']<=0: return False
        if self.sol['q2']<=0: return False
        return True
        
class CournotNProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='cournotN_problem'):
        default_params = {'alpha':12,'beta':1,'mc':3,'N':2}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        alpha, beta, mc, N = params['alpha'], params['beta'], params['mc'], params['N']
        demand = LinearDemand(a=alpha, b=beta)
        cournotN = CournotN(mc, N, demand)
        self.sol = cournotN.sol.copy()
        self.cournotN = cournotN
        setup_list = []
        setup = cournotN.setup()
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = "What quantity does each firm produce in the Nash equilibrium?"
        online_question = question
        answer = cournotN.sol['q']
        online_answer = fr"\(q_i = {answer:g}\)"
        answers = generate_distractors(answer, rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "What is the total quantity produced in the Nash equilibrium?"
        online_question = question
        answer = cournotN.sol['Q']
        online_answer = fr"\(Q = {answer:g}\)"
        answers = generate_distractors(answer, rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "What is the Nash equilibrium price in this market?"
        online_question = question
        answer = cournotN.sol['p']
        online_answer = fr"\(p = {answer:g}\)"
        answers = generate_distractors(answer, rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "What is the Nash equilibrium profit of each firm?"
        online_question = question
        answer = cournotN.sol['profit']
        online_answer = fr"\(\Pi_i = {answer:g}\)"
        answers = generate_distractors(answer, rng=rng)
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
        return True

class ExpectedValueProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='expected_value_problem'):
        default_params = {'x':[1,2,3,4],'p':[0.25,0.25,0.25,0.25]}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        x, p = params['x'], params['p']
        x = np.array(x)
        p = np.array(p)
        EX = np.sum(x*p)
        self.sol['EX'] = EX
        list_x = ', '.join([fr"\(x_{i+1}={x[i]:g}\)" for i in range(len(x))])
        list_p = ', '.join([fr"\(p_{i+1}={p[i]:g}\)" for i in range(len(p))])
        setup_list = []
        setup = fr"""
A random variable \(X\) can take on the following values: {list_x}, with probabilities {list_p}.
"""
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"Calculate the expected value of \(X\)."
        answer = EX
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": fr"\(E[X] = {answer:g}\)",
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if not equals(np.sum(self.params['p']), 1): return False
        return True

class InsuranceProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='insurance_problem'):
        default_params = {'W0':1000, 'D':200, 'p':0.2, 'fun':'ln'}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        W0, D, p, fun = params['W0'], params['D'], params['p'], params['fun']
        insurance = Insurance(W0=W0, D=D, p=p, fun=fun)
        self.sol = insurance.sol
        setup_list = []
        setup = insurance.setup()
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"Calculate the expected value of \(X\)."
        answer = insurance.sol['EX']
        online_answer = fr"\(E[X] = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"Calculate the expected utility."
        answer = insurance.sol['EU']
        online_answer = fr"\(E[u(X)] = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"Calculate the certainty equivalent of \(X\)."
        answer = insurance.sol['CE']
        online_answer = fr"\(CE = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"How much is the person willing to pay to avoid the risk of the accident?"
        answer = insurance.sol['WTP']
        online_answer = fr"\(WTP = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = fr"How much would it cost a risk-neutral insurance company to insure the individual against this risk?"
        answer = insurance.sol['FairCost']
        online_answer = fr"\(C = {answer:g}\)"
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

class PresentValueProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='present_value_problem'):
        default_params = {'beta':0.95,'x':100,'T':20}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        beta, x, T = params['beta'], params['x'], params['T']
        if T==0:
            x = np.array(x)
            xlist = ', '.join([fr"\(x_{i+1} = {x[i]:,g}\)" for i in range(len(x))])
            question = fr"Calculate the present value of a promise to receive payments {xlist} in periods \(t=1,\ldots,{len(x):g}\), when the time discount factor is \(\beta = {beta:g}\)."
            PV = np.sum(beta**np.arange(1,len(x)+1) * x)
        elif T==np.inf:
            question = fr"Calculate the present value of a promise to receive a constant payment of {x:,g} every period from \(t=1\) to eternity, when the time discount factor is \(\beta = {beta:g}\)"
            PV = beta/(1-beta)*x
        else:
            question = fr"Calculate the present value of a promise to receive a constant payment of {x:,g} every period for \({T:g}\) periods, when the time discount factor is \(\beta = {beta:g}\)" 
            PV = ((1-beta**(T+1))/(1-beta)-1)*x
        self.sol['PV'] = PV
        setup_list = []
        setup = ""
        online_setup = ""
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = question
        online_question = question
        answer = PV
        online_answer = fr"\(PV = {answer:,g}\)"
        answers = generate_distractors(answer, rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list

class SavingsProblem(GenericProblem):
    def __init__(self, params=None, rng=rng, name='savings_problem'):
        default_params = {'beta':0.95, 'p':0.95, 'Y':50000}
        GenericProblem.__init__(self, params=params, default_params=default_params, rng=rng, name=name)
        params = self.params
        beta, p, Y = params['beta'], params['p'], params['Y']
        savings = Savings(Y=Y, beta=beta, p=p)
        self.sol = savings.sol.copy()
        setup_list = []
        setup = savings.setup()
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = "How many bonds will the person buy in period 1?"
        answer = savings.sol['c2']
        online_answer = fr"\(b = {answer:,g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "How much will the person consume in period 1?"
        answer = savings.sol['c1']
        online_answer = fr"\(c_1 = {answer:,g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "How much will the person consume in period 2?"
        answer = savings.sol['c2']
        online_answer = fr"\(c_2 = {answer:,g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=False,sort=True,numerical=True,rng=rng)
        })
        question = "What is the interest rate on bonds?"
        answer = savings.sol['r']
        online_answer = fr"\(r = {answer*100:,g}\%\)"
        answers = generate_distractors(answer,rng=rng)
        answers = [fr"\({ans*100:g}\%\)" for ans in answers]
        question_list.append({
            "question": question,
            "online_question": question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,horz=True,shuffle=True,rng=rng)
        })
        self.setup_list = setup_list
        self.question_list = question_list
    def check_solution(self):
        if self.sol['c1']<=0: return False
        if self.sol['c2']<=0: return False
        if self.params['p']>=1: return False
        if self.params['beta']>=1: return False
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
    'CobbDouglasConsumerProblem': CobbDouglasConsumerProblem,
    'PerfectSubstitutesProblem': PerfectSubstitutesProblem,
    'PerfectComplementsProblem': PerfectComplementsProblem,
    'PriceChangeProblem': PriceChangeProblem,
    'PublicSchoolProblem': PublicSchoolProblem,
    'CobbDouglasWorkerProblem': CobbDouglasWorkerProblem,
    'WageChangeProblem': WageChangeProblem,
    'IncomeSupportProblem': IncomeSupportProblem,
    'ReturnsToScaleProblem': ReturnsToScaleProblem,
    'CobbDouglasFirmProblem': CobbDouglasFirmProblem,
    'CobbDouglasFirmGraphicalProblem': CobbDouglasFirmGraphicalProblem,
    'TechnicalChangeProblem': TechnicalChangeProblem,
    'NormalFormProblem': NormalFormProblem,
    'MonopolyProblem': MonopolyProblem,
    'Cournot2Problem': Cournot2Problem,
    'CournotNProblem': CournotNProblem,
    'ExpectedValueProblem': ExpectedValueProblem,
    'InsuranceProblem': InsuranceProblem,
    'PresentValueProblem': PresentValueProblem,
    'SavingsProblem': SavingsProblem
}
def load_problem(problem_str, params=None, name='generic_problem', rng=rng):
    return PROBLEM_TYPES[problem_str](params=params, name=name, rng=rng)
    
def show_menu(problem_str, params=None, name='generic_problem', rng=rng):
    prob = load_problem(problem_str, params, name, rng=rng)
    setup_list = prob.setup_list
    question_list = prob.question_list
    print(prob.params)
    for i in range(len(setup_list)):
        print(f"{i}: {setup_list[i]['setup']}".replace('\n',' '))
        print("")
    for i in range(len(question_list)):
        print(f"{i}: {question_list[i]['question']}".replace('\n',' '))
        print("")
    
        
        
        