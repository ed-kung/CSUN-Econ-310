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
> A representative, price-taking worker decides how many units, $$L$$, of labor to supply (e.g. how many hours to work), at a unit wage $$w$$. The worker's utility function over working $$L$$ labor-units at wage $$w$$ is:
>
> $$ u(L) = wL - \frac{4}{3} L^{3/2} $$
>
> 1. Write down the worker's inverse labor supply curve. ($$w$$ in terms of $$L$$)
>
> *Answer.*
>
> Step 1. Write down the worker's optimization problem.
>
> $$ \max_{L} ~ wL - \frac{4}{3}L^{3/2} $$
>
> Step 2. Write down the worker's first order condition and rearrange it to get $$w$$ in terms of $$L$$.
>
> $$\begin{aligned}
w - \left(\tfrac{3}{2}\right)\left(\tfrac{4}{3}\right) L^{1/2} &= 0  \\
w - 2L^{1/2} &= 0 \\
w &= 2L^{1/2} 
\end{aligned}$$


## Firms

### Setup

A representative, price-taking firm uses labor to produce and sell a commodity at unit price $$p$$. The firm hires labor at a constant wage rate $$w$$. If the firm employs $$L_d$$ units of labor, it can produce $$f(L_d)$$ units of commodity output.

We call $$f(L)$$ the firm's **production function**. It shows how many units of output can be produced from $$L$$ units of labor input.

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
> A representative, price-taking firm uses labor to produce and sell a commodity at unit price $$p=3$$. The firm hires labor at a constant wage rate $$w$$. If the firm employs $$L$$ units of labor, it can produce $$f(L)$$ units of commodity output, where:
>
> $$ f(L) = 16L^{1/2} $$
>
> 1. Write down the firm's inverse labor demand curve. 
>
> *Answer.*
>
> Step 1. Write down the firm's profit function.
>
> $$\begin{aligned}
\Pi(q) &= \text{Revenue} - \text{Cost} \\
&= 3\times16L^{1/2} - wL \\
&= 48 L^{1/2} - wL 
\end{aligned}$$
>
> Step 2. Write down the firm's optimization problem.
>
> $$ \max_{L} ~ 48L^{1/2} - wL $$
>
> Step 3. Write down the firm's first order condition and rearrange it to write $$w$$ in terms of $$L$$.
>
> $$\begin{aligned}
24L^{-1/2} - w &= 0 \\
w &= 24L^{-1/2}
\end{aligned}$$


### Cost minimization

What is the relationship between a firm's production function, $$f(L)$$, and its cost function, $$c(q)$$?  Deriving the cost function from the production function is known as the **cost minimization problem**:

$$ c(q) = \min_{L} ~ wL ~ \text{ where } ~ q = f(L) $$

In other words, $$c(q)$$ is the minimum labor cost ($$wL$$) necessary to produce $$q$$ units of output.

Since there's a 1:1 mapping between $$q$$ and $$L$$, the cost function is equal to:

$$c(q) = w f^{-1}(q) $$

{: .yellow-callout-title }
> Example: Deriving a cost function
>
> Derive the cost function for the firm in the previous example, with a production function of:
>
> $$ f(L) = 16L^{1/2} $$
>
> *Answer.*
>
> Step 1. Use the production function to find out how much labor would be needed to produce $$q$$ units of output.
>
> $$\begin{aligned}
q &= 16L^{1/2}  ~ ~ ~ ~ & \text{(Write down the relationship between L and q)} \\
\frac{q}{16} &= L^{1/2} ~ ~ ~ ~ & \text{(Divide both sides by 16)}\\
L &= \left(\frac{q}{16}\right)^2 ~ ~ ~ ~ & \text{(Square both sides)}
\end{aligned}$$
>
> Step 2. The total cost is simply $$wL$$, so the firm's cost function is:
>
> $$c(q) = w\left(\frac{q}{16}\right)^2 $$

## Market equilibrium 

In equilibrium, $$L_d = L_s = L$$. By combining equations (1) and (2) and the equilibrium condition, we get:

$$ p f^\prime(L_d) = w = d^\prime(L_s) $$

or:

$$ p f^\prime(L) = d^\prime(L) $$

This equation shows us that in the equilibrium of a labor market, the firm's marginal revenue product of labor equals the worker's marginal disutility of labor.

The equation also lets us solve for the equilibrium mathematically.  $$pf^\prime(L) = d^\prime(L)$$ gives us a single equation with a single unknown variable, which we can solve for $$L$$. To then solve for $$w$$, we simply plug that value of $$L$$ into either the worker's labor supply curve or the firm's labor demand curve.

{: .blue-callout-title }
> Example: Labor market equilibrium
>
> A representative, price-taking worker decides how many units, $$L$$, of labor to supply (e.g. how many hours to work), at a unit wage $$w$$. The worker's utility function over working $$L$$ labor-units at wage $$w$$ is:
>
> $$ u(L) = wL - \frac{4}{3} L^{3/2} $$
>
> A representative, price-taking firm uses labor to produce and sell a commodity at unit price $$p=3$$. The firm hires labor at a constant wage rate $$w$$. If the firm employs $$L$$ units of labor, it can produce $$f(L)$$ units of commodity output, where:
>
> $$ f(L) = 16L^{1/2} $$
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
w &= 2L^{1/2} ~ ~ ~ ~ & \text{(Labor supply)} \\
w &= 24L^{-1/2} ~ ~ ~ ~ & \text{(Labor demand)}
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



