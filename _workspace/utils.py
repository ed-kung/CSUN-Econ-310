import numpy as np

class SREQ:
    def __init__(self,N=3000,M=200,Y=100,alpha=10,beta=2,gamma=0,delta=0,eta=0.2):
        self.N=N
        self.M=M
        self.Y=Y
        self.alpha=alpha
        self.beta=beta
        self.gamma=gamma
        self.delta=delta
        self.eta=eta
    
    def solve(self):
        self.Q = (self.alpha - self.delta) / (self.beta/self.N + self.eta/self.M)
        self.p = (self.N*self.eta*self.alpha + self.M*self.beta*self.delta)/(self.N*self.eta + self.M*self.beta)
        self.qd = self.Q / self.N
        self.qs = self.Q / self.M
        self.c = self.Y - self.p*self.qd
        self.revenue = self.p * self.qs
        self.cost = self.gamma + self.delta*self.qs + 0.5*self.eta*self.qs**2
        self.profit = self.revenue - self.cost
        self.totalprofit = self.M * self.profit
        self.util = self.c + self.alpha*self.qd - 0.5*self.beta*self.qd**2
        self.totalutil = self.N*self.util
        return {
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
    
        