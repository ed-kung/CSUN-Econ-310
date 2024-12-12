---
layout: default
title: 5. Labor Market
parent: Lecture Notes
nav_order: 5
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

A representative, price-taking worker decides how many units, \(L_s\), of labor to supply (e.g. how many hours to work), at a unit wage \(w\). The worker's utility function over working \(L_s\) labor-units at wage \(w\) is:

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
> 

## Firms

### Setup

A representative, price-taking firm uses labor to produce and sell a commodity at unit price \(p\). The firm hires labor at a constant wage rate \(w\). If the firm employs \(L_d\) units of labor, it can produce \(f(L_d)\) units of commodity output.

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
> 

### Cost minimization

What is the relationship between a firm's production function, $$f(L)$$, and its cost function, $$c(q)$$?  Deriving the cost function from the production function is known as the **cost minimization problem**:

$$ c(q) = \min_{L} ~ wL ~ \text{ where } ~ q = f(L) $$

In other words, $$c(q)$$ is the minimum labor cost ($$wL$$) necessary to produce $$q$$ units of output.

Since there's a 1:1 mapping between $$q$$ and $$L$$, the cost function is equal to:

$$c(q) = w f^{-1}(q) $$

{: .yellow-callout-title }
> Example: Deriving a cost function
>
>

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
> 



