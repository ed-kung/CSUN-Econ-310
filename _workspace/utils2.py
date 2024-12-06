import numpy as np
import pandas as pd
import sympy
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

###################################################################
# MATH UTILITIES
###################################################################
def sign(x):
    if x>0: return '+'
    else: return '-'

def is_divisible(p,q):
    d = nsimplify(p/q).q
    return (d==1)

def equals(x,y,tol=1e-4):
    return np.abs(x-y)<tol

def is_rational(x, maxdenom=5):
    try:
        d = nsimplify(x).q
        return (d<=maxdenom)
    except:
        return False

def asfrac(x, inline=False, maxdenom=5, rmplus=True, rmneg=False):
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

class CobbDouglas:
    def __init__(self, A=1, x='x', a=1/2, y='y', b=1/2):
        self.A, self.x, self.a, self.y, self.b = A, x, a, y, b
    def print(self, maxdenom=10, rmplus=True, rmneg=False):
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
    def print(self, x='p', maxdenom=5):
        return PolyEq(c=[self.a/self.b, -1/self.b], x=x, p=[0,1]).print(maxdenom=maxdenom, rmplus=True)
    def print_inverse(self, x='q', maxdenom=5):
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
    def print(self, x='p', maxdenom=5):
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
        if params['k']<0:
            myExponentialFunc = ExponentialDemand
        elif params['k']>0:
            myExponentialFunc = ExponentialSupply
        equation = myExponentialFunc(a=params['a'], k=params['k'])
        setup_list = []
        setup = fr"""
$$ y = {equation.print_inverse(x='x')} $$
"""
        online_setup = setup
        setup_list.append({
            "setup": setup,
            "online_setup": online_setup
        })
        question_list = []
        question = fr"Write \(x\) as a function of \(y\)."
        online_question = question
        answer = fr"\(x = {equation.print(x='y')}\)"
        online_answer = answer
        answers = [
            answer,
            fr"\(x = {myExponentialFunc(a=equation.a, k=1/equation.k).print(x='y')}\)",
            fr"\(x = {myExponentialFunc(a=1/equation.a, k=equation.k).print(x='y')}\)",
            fr"\(x = {equation.print_inverse(x='y')}\)"
        ]
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
        })
        question = fr"Calculate \(x\) when \(y={params['y']:g}\)."
        online_question = question
        answer = equation.eval_at_p(params['y'])
        online_answer = fr"\(x = {answer:g}\)"
        answers = generate_distractors(answer,rng=rng)
        question_list.append({
            "question": question,
            "online_question": online_question,
            "answer": answer,
            "online_answer": online_answer,
            "MCQ": MCQ(question,answers,0,shuffle=False,horz=True,sort=True,numerical=True,rng=rng)
        })
        self.equation = equation
        self.setup_list = setup_list
        self.question_list = question_list
        self.sol = {'x': equation.eval_at_p(params['y'])}

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
        distractor3 = fr"\(\frac{{{nsimplify(A/B).p}}}{{{nsimplify(A/B).q}}}xy\)"
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
            "MCQ": MCQ(question,answers,0,shuffle=True,rng=rng)
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
        
    

PROBLEM_TYPES = {
    'LinearMarketProblem': LinearMarketProblem,
    'ExponentialMarketProblem': ExponentialMarketProblem,
    'ExponentialRewriteProblem': ExponentialRewriteProblem,
    'CobbDouglasSimplifyProblem': CobbDouglasSimplifyProblem,
    'LogDifferencesProblem': LogDifferencesProblem
}
def load_problem(problem_str, params=None, name='generic_problem', rng=rng):
    return PROBLEM_TYPES[problem_str](params=params, name=name, rng=rng)
    

        
        
        