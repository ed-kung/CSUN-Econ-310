---
layout: default
title: 6. General Equilibrium
parent: Lecture Notes
nav_order: 6
---

# A General Equilibrium Model of the Economy
{: .no_toc }

- TOC
{:toc}

In this lecture, we will combine the commodity market model with the labor market model, to get a complete model of the economy.

This model is called a **general equilibrium model** because it fully explains all prices (the commodity price and the wage rate) as a function of the model's parameters.

## Setup

### Consumers

A representative, price-taking consumer decides how many units, \(q_d\), of a commodity to purchase at unit price \(p\). The utility they receive for purchasing \(q_d\) units at price \(p\) is:

$$ u(q_d) = v(q_d) - pq_d $$

The consumer's optimization problem is:

$$ \max_{q_d} ~ v(q_d) - pq_d $$

And their first order condition is:

$$ v^\prime(q_d) = p ~ ~ ~ ~ (\text{Eq.1})$$

### Workers

A representative, price-taking worker decides how many units, \(L_s\), of labor to supply (e.g. how many hours to work), at a unit wage \(w\). The worker's utility function over working \(L_s\) labor-units at wage \(w\) is:

$$ u(L_s) = wL_s - d(L_s) $$

The worker's optimization problem is:

$$ \max_{L_s} ~ wL_s - d(L_s) $$

And their first order condition is:

$$ w = d^\prime(L_s) ~ ~ ~ ~ (\text{Eq.2})$$

### Firms

A representative, price-taking firm uses labor to produce and sell a commodity at unit price \(p\). The firm hires labor at a constant wage rate \(w\). If the firm employs \(L_d\) units of labor, it can produce \(f(L_d)\) units of commodity output.

The firm's optimization problem is:

$$ \max_{L_d} ~ p f(L_d) - wL_d $$

And their first order condition is:

$$ p f^\prime(L_d) = w ~ ~ ~ ~ (\text{Eq.3}) $$

{: .red-callout-title }
> Note
>
> We've set up the firm problem as if they are choosing the amount of labor, resulting in a quantity of output $$q = f(L)$$.
>
> We could have set up the problem as the firm choosing the amount of output to produce, and hiring the amount of labor necessary to produce it: $$L = f^{-1}(q)$$. 
>
> The firm's optimization problem would have been:
>
> $$ \max_{q_s} ~ pq_s - wf^{-1}(q_s) $$
>
> Both ways of setting up the problem would have been equivalent.


## Equilibrium Conditions

Equations 1-3 describe the behavior of the consumer, the worker, and the firm. We call them the **optimality conditions**. All three equations must hold in any equilibrium of the model.

In addition to the optimality conditions, we have three additional equations that must be satisfied in any equilibrium of the model:

$$ q_d = q_s = q ~ ~ ~ ~ (\text{Eq.4}) $$

$$ L_d = L_s = L ~ ~ ~ ~ (\text{Eq.5}) $$

$$ q = f(L) ~ ~ ~ ~ (\text{Eq.6}) $$

- Equation (4) is what we call the **commodity market clearing condition**. It says that the quantity of commodity demanded must equal the quantity of commodity supplied.

- Equation (5) is what we call the **labor market clearing condition**. It says that the quantity of labor demanded must equal the quantity of labor supplied.

- Equation (6) is what we call the **feasibility condition**. It says that the amount of commodity traded in the commodity market must be produceable by the amount of labor employed in the labor market.

Equations 1-6 therefore define a system of 6 questions in 6 unknowns. The unknowns are: 

- The commodity price $$p$$
- The wage rate $$w$$
- The quantity of commodity demanded, $$q_d$$
- The quantity of commodity supplied, $$q_s$$
- The quantity of labor demanded, $$L_d$$ 
- The quantity of labor supplied, $$L_s$$

Since there are 6 equations in 6 unknowns, the system can be solved to find the equilibrium prices and quantities in both the commodity market and the labor market.

{: .blue-callout-title }
> Example: General equilibrium 
>



