import numpy as np

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
                t+=f'{np.abs(c)} '
            else:
                if np.abs(c)!=1:
                    t+=f'{np.abs(c)}'
                if p==1:
                    t+=f'{var} '
                else:
                    t+=f'{var}^{p}'
    if remove_first_plus_minus:
        return t[2:]
    else:
        return t

class SREQ:
    def __init__(self,N=3000,M=200,Y=100,alpha=10,beta=2,gamma=0,delta=0,eta=0.2):
        Q = (alpha - delta)/(beta/N + eta/M)
        p = (N*eta*alpha + M*beta*delta)/(N*eta + M*beta)
        
        self.N=N
        self.M=M
        self.Y=Y
        self.alpha=alpha
        self.beta=beta
        self.gamma=gamma
        self.delta=delta
        self.eta=eta
        self.Q = Q
        self.p = p
        self.qd = Q/N
        self.qs = Q/M
        self.c = Y - p*self.qd
        self.revenue = p*self.qs 
        self.cost = gamma + delta*self.qs + 0.5*self.eta*self.qs**2
        self.profit = self.revenue - self.cost
        self.totalprofit = M*self.profit
        self.util = self.c + alpha*self.qd - 0.5*beta*self.qd**2
        self.totalutil = N*self.util
        self.total_surplus = self.totalprofit + self.totalutil
        
    def check_solution(self):
        return (
            (self.c>0) and
            (self.qd>0) and
            (self.qs>0) and
            (self.p>0) and
            (np.abs(self.p%1)<0.001) and
            (np.abs(self.qd%1)<0.001) and
            (np.abs(self.qs%1)<0.001)
        )

    def general_setup(self):
        return r"""
A commodity $q$ is traded at price $p$ in a competitive market with $N$ identical consumers and $M$ identical firms.\\

Each consumer has income $Y$ and maximizes:

\begin{align*}
\max_{c,q} ~ c + \alpha q - \tfrac{1}{2} \beta q^2 ~ \text{ s.t. } c + pq = Y
\end{align*}

Each firm's cost function is:

\begin{align*}
c(q) = \gamma + \delta q + \tfrac{1}{2} \eta q^2
\end{align*}

The firm maximizes:

\begin{align*}
\max_{q} ~ pq - c(q)
\end{align*}

The short run equilibrium condition is:

\begin{align*}
Nq_d = Mq_s = Q
\end{align*}

The general solutions are:

\begin{align*}
Q = \frac{\alpha - \delta}{\beta/N + \eta/M} 
\end{align*}

\begin{align*}
p = \frac{N \eta \alpha + M \beta \delta}{N \eta + M \beta}
\end{align*}
"""

    def setup(self):
        return r"""
A commodity $q$ is traded at price $p$ in a competitive market with price-taking consumers and firms. \\
        
There are ${:,.0f}$ identical consumers each with income $Y={:,.0f}$. Each consumer has a utility function over numeraire consumption $c$ and commodity $q$ given by:

$$u(c,q) = c + {}$$

There are ${:,.0f}$ identical firms each with cost function given by:

$$c(q) = {}$$
""".format(
    self.N, 
    self.Y,
    polyeq('q', [0, self.alpha, -0.5*self.beta]),
    self.M,
    polyeq('q', [self.gamma, self.delta, 0.5*self.eta])
)

    def solution(self):
        return r"""
The solutions are: $p={}$, $q_d={}$, $q_s={}$.
""".format(self.p, self.qd, self.qs)

        
class AdValoremSR:
    def __init__(self,N=3000,M=200,Y=100,alpha=10,beta=2,gamma=0,delta=0,eta=0.2,tc=0.1,tp=0):
        Q = ((1-tp)*alpha - (1+tc)*delta)/((1+tc)*eta/M + (1-tp)*beta/N)
        p = (N*eta*alpha + M*beta*delta)/(N*eta*(1+tc) + M*beta*(1-tp))
        
        self.N=N
        self.M=M
        self.Y=Y
        self.alpha=alpha
        self.beta=beta
        self.gamma=gamma
        self.delta=delta
        self.eta=eta
        self.tc=tc
        self.tp=tp
        self.Q = Q
        self.p = p
        self.qd = Q/N
        self.qs = Q/M
        self.c = Y - p*self.qd
        self.revenue = p*self.qs 
        self.cost = gamma + delta*self.qs + 0.5*self.eta*self.qs**2
        self.profit = self.revenue - self.cost
        self.totalprofit = M*self.profit
        self.util = self.c + alpha*self.qd - 0.5*beta*self.qd**2
        self.totalutil = N*self.util
        self.tax_revenue = (tc+tp)*Q
        self.total_surplus = self.totalutil + self.totalprofit + self.tax_revenue
        self.eq_notax = SREQ(N=N,M=M,Y=Y,alpha=alpha,beta=beta,gamma=gamma,delta=delta,eta=eta)
        self.DWL = self.eq_notax.total_surplus - self.total_surplus

    def check_solution(self):
        return (
            (self.c>0) and
            (self.p>0) and
            (self.qd>0) and
            (self.qs>0) and
            (np.abs(self.p%1)<0.0001) and
            (np.abs(self.qd%1)<0.0001) and
            (np.abs(self.qs%1)<0.0001) and
            (self.eq_notax.check_solution())
        )

    def general_setup(self):
        return r"""
A commodity $q$ is traded at price $p$ in a competitive market with $N$ identical consumers and $M$ identical firms.\\

An ad-valorem tax rate of $t_c$ is placed on consumers, and an ad-valorem tax rate of $t_p$ is placed on producers.

Each consumer has income $Y$ and maximizes:

\begin{align*}
\max_{c,q} ~ c + \alpha q - \tfrac{1}{2} \beta q^2 ~ \text{ s.t. } c + (1+t_c)pq = Y
\end{align*}

Each firm's cost function is:

\begin{align*}
c(q) = \gamma + \delta q + \tfrac{1}{2} \eta q^2
\end{align*}

The firm maximizes:

\begin{align*}
\max_{q} ~ (1-t_p)pq - c(q)
\end{align*}

The short run equilibrium condition is:

\begin{align*}
Nq_d = Mq_s = Q
\end{align*}

The general solutions are:

\begin{align*}
Q = \frac{(1-t_p)\alpha - (1+t_c)\delta}{(1-t_p)\beta/N + (1+t_c)\eta/M} 
\end{align*}

\begin{align*}
p = \frac{N \eta \alpha + M \beta \delta}{(1+t_c) N \eta + (1-t_p) M \beta}
\end{align*}
"""

    def setup(self):
        t = r"""
A commodity $q$ is traded at price $p$ in a competitive market with price-taking consumers and firms. \\
        
There are ${:,.0f}$ identical consumers each with income $Y={:,.0f}$. Each consumer has a utility function over numeraire consumption $c$ and commodity $q$ given by:

$$u(c,q) = c + {}$$

There are ${:,.0f}$ identical firms each with cost function given by:

$$c(q) = {}$$

""".format(
    self.N, 
    self.Y,
    polyeq('q', [0, self.alpha, -0.5*self.beta]),
    self.M,
    polyeq('q', [self.gamma, self.delta, 0.5*self.eta])
)
        if self.tc>0:
            t+= r"An ad-valorem tax rate of ${:.0f}\%$ is placed on consumers.\\".format(self.tc*100)
        if self.tp>0:
            t+= r"An ad-valorem tax rate of ${:.0f}\%$ is placed on producers.\\".format(self.tp*100)
        return t

    def solution(self):
        return r"""
Solutions: \\

Pre-tax: $p={}$, $q_d={}$, $q_s={}$ \\

Post-tax: $p={}$, $q_d={}$, $q_s={}$
""".format(self.eq_notax.p, self.eq_notax.qd, self.eq_notax.qs, self.p, self.qd, self.qs)


class LREQ:
    def __init__(self,N=3000,Y=100,alpha=10,beta=2,gamma=32,delta=0,eta=0.2):
        self.N=N
        self.Y=Y
        self.alpha=alpha
        self.beta=beta
        self.gamma=gamma
        self.delta=delta
        self.eta=eta
    
    def solve(self):
        self.qs = np.sqrt(2*self.gamma / self.eta)
        self.p = self.delta + self.eta*self.qs
        self.qd = (self.alpha - self.p) / self.beta
        self.Q = self.N*self.qd
        self.M = self.Q / self.qs
        self.c = self.Y - self.p*self.qd
        self.revenue = self.p * self.qs
        self.cost = self.gamma + self.delta*self.qs + 0.5*self.eta*self.qs**2
        self.profit = self.revenue - self.cost
        self.totalprofit = self.M * self.profit
        self.util = self.c + self.alpha*self.qd - 0.5*self.beta*self.qd**2
        self.totalutil = self.N*self.util
        return {
            "M": self.M,
            "Q": self.Q, 
            "p": self.p,
            "qd": self.qd,
            "qs": self.qs,
            "c": self.c,
            "profit": self.profit,
            "totalprofit": self.totalprofit,
            "util": self.util,
            "totalutil": self.totalutil
        }

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

