---
layout: default
title: 4. Labor Market
parent: Lecture Notes
nav_order: 4
---

# A Model of Labor Markets
{: .no_toc }

- TOC
{:toc}

In this lecture, we'll build a simple model of a labor market with a representative worker (labor supplier) and a representative firm (labor demander).

The worker takes the wage rate (i.e. market price of labor) as given, and decides how many units of labor to supply.

The firm employs labor in order to produce and sell a commodity. The firm takes the wage rate and the commodity price as given, and decides how many units of labor to employ, which in turn determines how many units of the commodity it produces.

In equilibrium, the quantity of labor supplied by workers must equal the quantity of labor demanded by firms.

## Workers

### Setup

A representative, price-taking worker decides how many units, $$L_s$$, of labor to supply (e.g. how many hours to work), at a unit wage $$w$$. The worker's utility function over working $$L_s$$ labor-units at wage $$w$$ is:

$$ u(L_s) = wL_s - d(L_s) $$

$$ wL_s $$ is the total amount of income that the worker earns (the total benefit from working), and $$d(L_s)$$ is the disutility from labor.

### First order condition

The worker's optimization problem is the following:

$$ \max_{L_s} ~ wL_s - d(L_s) $$

Taking the derivative with respect to $$q$$ gives us the first order condition:

$$ w - d^\prime(L_s) = 0 $$

or:

$$ w = d^\prime(L_s) ~ ~ ~ ~ (\text{Eq.1})$$

Equation (1) is the first order condition of the worker. It therefore shows the relationship between wage rate and quantity of labor supplied, because this is the equation the worker uses to determine how many labor units to supply.

In other words, equation (1) defines the worker's **labor supply curve**!  Technically, it's the *inverse labor supply curve* because it shows $$w$$ in terms of $$L_s$$. If we re-arrange the equation to write $$L_s$$ as a function of $$w$$, we'd get the labor supply curve.

Equation (1) shows that at the worker's optimal choice, the wage rate equals the marginal disutility of labor.  In other words, workers will work up to the point where the amount of wage they earn is just equal to the how much they dislike working the incremental hour.

{: .purple-callout-title }
> Economic Insight
> 
> In a labor market, the equilibrium wage rate will equal the worker's marginal disutility of labor.

{: .blue-callout-title }
> Example: Deriving a labor supply function
>
> A representative, price-taking worker decides how many units, $$L_s$$, of labor to supply (e.g. how many hours to work), at a unit wage $$w$$. The worker's utility function over working $$L_s$$ labor-units at wage $$w$$ is:
>
> $$ u(L_s) = wL_s - \frac{4}{3} L_s^{3/2} $$
>
> 1. Write down the worker's inverse labor supply curve. ($$w$$ in terms of $$L_s$$)
>
> *Answer.*
>
> Step 1. Write down the worker's optimization problem.
>
> $$ \max_{L_s} ~ wL_s - \frac{4}{3}L_s^{3/2} $$
>
> Step 2. Write down the worker's first order condition and rearrange it to get $$w$$ in terms of $$L_s$$.
>
> $$\begin{aligned}
w - \left(\tfrac{3}{2}\right)\left(\tfrac{4}{3}\right) L_s^{1/2} &= 0  \\
w - 2L_s^{1/2} &= 0 \\
w &= 2L_s^{1/2} 
\end{aligned}$$


## Firms

### Setup

A representative, price-taking firm uses labor to produce and sell a commodity at unit price $$p$$. The firm hires labor at a constant wage rate $$w$$. If the firm employs $$L_d$$ units of labor, it can produce $$f(L_d)$$ units of commodity output.

We call $$f(L_d)$$ the firm's **production function**. It shows how many units of output can be produced from $$L_d$$ units of labor input.

### First order condition

The firm's profit function is revenue minus cost, which can be written as follows:

$$\Pi(L_d) = p f(L_d) - wL_d $$

The firm's optimization problem is therefore:

$$ \max_{L_d} ~ p f(L_d) - wL_d $$

Taking the derivative with respect to $$L_d$$ gives us the first order condition:

$$ p f^\prime(L_d) - w = 0 $$

or:

$$ p f^\prime(L_d) = w ~ ~ ~ ~ (\text{Eq.2}) $$

Equation (2) is the first order condition of the firm. It therefore shows the relationship between commodity price, wage rate, and quantity of labor demanded.

In other words, equation (2) defines the firm's **labor demand curve**.  Technically, it's the *inverse labor demand curve* because it shows $$w$$ in terms of $$L_d$$. But if we re-arrange the equation to write $$L_d$$ in terms of $$w$$, we'd get the labor demand curve.

Equation (2) also shows that at the firm's optimal choice, the wage rate equals the **marginal revenue product of labor**. That is, the firm will continue to employ labor until the marginal revenue it gets from the incremental worker is exactly equal to the wage rate it pays for the incremental worker.

{: .purple-callout-title }
> Economic Insight
> 
> In a labor market, the equilibrium wage rate will equal the firm's marginal revenue product of labor.

{: .green-callout-title }
> Example: Deriving a labor demand function
>
> A representative, price-taking firm uses labor to produce and sell a commodity at unit price $$p=3$$. The firm hires labor at a constant wage rate $$w$$. If the firm employs $$L_d$$ units of labor, it can produce $$f(L_d)$$ units of commodity output, where:
>
> $$ f(L_d) = 16L_d^{1/2} $$
>
> 1. Write down the firm's inverse labor demand curve. 
>
> *Answer.*
>
> Step 1. Write down the firm's profit function.
>
> $$\begin{aligned}
\Pi(L_d) &= \text{Revenue} - \text{Cost} \\
&= 3\times16L_d^{1/2} - wL_d \\
&= 48 L_d^{1/2} - wL_d 
\end{aligned}$$
>
> Step 2. Write down the firm's optimization problem.
>
> $$ \max_{L_d} ~ 48L_d^{1/2} - wL_d $$
>
> Step 3. Write down the firm's first order condition and rearrange it to write $$w$$ in terms of $$L_d$$.
>
> $$\begin{aligned}
24L_d^{-1/2} - w &= 0 \\
w &= 24L_d^{-1/2}
\end{aligned}$$


### Cost minimization

What is the relationship between a firm's production function, $$f(L_d)$$, and its cost function, $$c(q_s)$$?  Deriving the cost function from the production function is known as the **cost minimization problem**:

$$ c(q_s) = \min_{L_d} ~ wL_d ~ \text{ where } ~ q_s = f(L_d) $$

In other words, $$c(q_s)$$ is the minimum labor cost ($$wL_d$$) necessary to produce $$q_s$$ units of output.

Since there's a 1:1 mapping between $$q_s$$ and $$L_d$$, the cost function is equal to:

$$c(q_s) = w f^{-1}(q_s) $$

{: .yellow-callout-title }
> Example: Deriving a cost function
>
> Derive the cost function for the firm in the previous example, with a production function of:
>
> $$ f(L_d) = 16L_d^{1/2} $$
>
> *Answer.*
>
> Step 1. Use the production function to find out how much labor would be needed to produce $$q_s$$ units of output.
>
> $$\begin{aligned}
q_s &= 16L_d^{1/2}  ~ ~ ~ ~ & \text{(Write down the relationship between L_d and q_s)} \\
\frac{q_s}{16} &= L_d^{1/2} ~ ~ ~ ~ & \text{(Divide both sides by 16)}\\
L_d &= \left(\frac{q_s}{16}\right)^2 ~ ~ ~ ~ & \text{(Square both sides)}
\end{aligned}$$
>
> Step 2. The total cost is simply $$wL_d$$, so the firm's cost function is:
>
> $$c(q_s) = w\left(\frac{q_s}{16}\right)^2 $$

## Market equilibrium 

In equilibrium, the quantity of labor supplied must equal the quantity of labor demanded. That is, $$L_s = L_d$$. This equation is called the "labor market clearing condition".

We now have the following three equations:

$$\begin{align}
w = d^\prime(L_s) ~ ~ ~ ~ ~ ~ & \text{Worker's First Order Condition} \\
w = pf^\prime(L_d) ~ ~ ~ ~ ~ ~ & \text{Firm's First Order Condition} \\
L_d = L_s ~ ~ ~ ~ ~ ~& \text{Labor Market Clearing Condition} 
\end{align}$$

The first equation is the labor supply equation and it comes from the worker's optimizing behavior. The second equation is the labor demand equation and it comes from the firm's optimizing behavior. The third equation is the market clearing condition.

Together, these equations give us three equations in three unknowns ($$w$$, $$L_d$$, $$L_s$$). We can solve the system of equations to find the equilibrium wage rate and quantity of labor.

{: .blue-callout-title }
> Example: Labor market equilibrium
>
> A representative, price-taking worker decides how many units, $$L_s$$, of labor to supply (e.g. how many hours to work), at a unit wage $$w$$. The worker's utility function over working $$L_s$$ labor-units at wage $$w$$ is:
>
> $$ u(L_s) = wL_s - \frac{4}{3} L_s^{3/2} $$
>
> A representative, price-taking firm uses labor to produce and sell a commodity at unit price $$p=3$$. The firm hires labor at a constant wage rate $$w$$. If the firm employs $$L_d$$ units of labor, it can produce $$f(L_d)$$ units of commodity output, where:
>
> $$ f(L_d) = 16L_d^{1/2} $$
>
> 1. Write down the inverse labor supply curve.
> 2. Write down the inverse labor demand curve.
> 3. Calculate the equilibrium wage rate $$w$$ and quantity of labor demanded/supplied, $$L$$.
> 4. Calculate the equilibrium utility of the worker.
> 5. Calculate the equilibrium profit of the firm.
>
> *Answer.*
>
> **Write down the inverse labor supply and demand curves.**
>
> Since this problem's setup is the same as the above two examples, we already did this part.
>
> $$\begin{aligned}
w &= 2L_s^{1/2} ~ ~ ~ ~ & \text{(Labor supply)} \\
w &= 24L_d^{-1/2} ~ ~ ~ ~ & \text{(Labor demand)}
\end{aligned}$$
>
> **Calculate the equilibrium wage and quantity of labor.**
>
> To do this, set the inverse demand function equal to the inverse supply function and solve for the equilibrium quantity of labor, $$L$$.
>
> $$\begin{aligned}
2L^{1/2} &= 24L^{-1/2} & \\
2L^{1/2} L^{1/2} &= 24 ~ ~ ~ ~ & \text{(Multiply both sides by }L^{1/2}\text{)} \\
2L &= 24 & \\
L &= 12 &
\end{aligned}$$
>
> To get the equilibrium wage rate, plug $$L$$ into either the inverse demand equation or the inverse supply equation.
>
> $$\begin{aligned}
w &= 2L^{1/2} ~ ~ ~ ~ & \text{(inverse supply equation)} \\
&= 2(12)^{1/2} &
&= 6.9282
\end{aligned}$$
>
> **Calculate the equilibrium utility of the worker and profit of the firm.**
>
> Simply plug into the worker's utility function and firm's profit function.
>
> $$\begin{aligned}
U &= wL - \tfrac{4}{3}L^{3/2} \\
&= 6.9282(12) - \tfrac{4}{3}(12)^{3/2} \\
&= 27.7128
\end{aligned}$$
>
> $$\begin{aligned}
\Pi &= 48L^{1/2} - wL \\
&= 48 (12)^{1/2} - 6.9282(12) \\
&= 83.1384
\end{aligned}$$

## Big Picture Review

- We model a labor market with two main groups of actors: workers and firms. (Workers are the labor suppliers and firms are the labor demanders.)
- Workers take the market wage as given, and choose how many units of labor to supply (i.e. how many hours to work, how hard to work, etc) in order to maximize their utility.
    - Worker utility is modeled as earnings minus the "disutility of work", i.e. workers get some negative utility from working.
- Firms take the market wage as given, and choose how many units of labor to consume (i.e. how many workers to hire, for how long, etc) in order to maximize their profit.
    - A firm's profit is equal to its revenue minus its cost.
    - Their revenue is equal to price times quantity produced, and quantity produced is determined by how much labor they use. The relationship between labor used and output is known as the "production function". 
    - There is a direct relationship between a firm's production function and its cost function (it's two ways of looking at the same thing).
    - In this simple model, the only input that the firm uses is labor. We ignore the role of capital, energy, and other inputs.
- The key drivers of a worker's decision making is their disutility of work and the wage.
- The key drivers of a firm's decision making is their production function and the wage.
- The labor supply curve arises out of the first order condition of the worker's optimization problem.
- The labor demand curve arises out of the first order condition of the firm's optimization problem.
- In equilibrium, the wage adjusts such that the quantity of labor supplied matches the quantity of labor demanded.


