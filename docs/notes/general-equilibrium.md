---
layout: default
title: 5. General Equilibrium
parent: Lecture Notes
nav_order: 5
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

$$ q_s = f(L_d) ~ ~ ~ ~ (\text{Eq.6}) $$

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
> A representative, price-taking consumer decides how many units, $$q_d$$, of a commodity to purchase at unit price $$p$$. The utility they receive for purchasing $$q_d$$ units at price $$p$$ is:
>
> $$ u(q_d) = 16 \ln q_d - pq_d $$
>
> A representative, price-taking worker decides how many units, $$L_s$$, of labor to supply at unit wage $$w$$. The worker's utility function over working $$L_s$$ labor-units at wage $$w$$ is:
>
> $$ u(L_s) = wL_s - \frac{1}{2} L_s^2 $$
>
> A representative, price-taking firm uses labor to produce and sell a commodity at unit price $$p$$. The firm hires labor at a constant wage rate $$w$$. If the firm employs $$L_d$$ units of labor, it can produce $$f(L_d)$$ units of commodity output, where:
>
> $$ f(L_d) = 6L_d^{1/2} $$
>
> 1. Calculate the equilibrium quantity of labor, $$L$$.
> 2. Calculate the equilibrium quantity of commodity, $$q$$.
> 3. Calculate the equilibrium wage rate $$w$$.
> 4. Calculate the equilibrium commodity price $$p$$.
> 5. Calculate the equilibrium utility of the consumer.
> 6. Calculate the equilibrium utility of the worker.
> 7. Calculate the equilibrium profit of the firm.
>
> *Answer.*
>
> Step 1. Find the consumer's inverse commodity demand curve and label it Eq.1.
>
> The consumer's optimization problem is:
>
> $$ \max_{q_d} ~ 16 \ln q_d - pq_d $$
>
> And their first order condition is:
>
> $$ \frac{16}{q_d} - p = 0 $$
>
> Which gives an inverse demand curve:
>
> $$ p = \frac{16}{q_d} ~ ~ ~ ~ \text{(Eq.1)}$$
>
> Step 2. Find the worker's inverse labor supply curve and label it Eq.2.
>
> The worker's optimization problem is:
>
> $$ \max_{L_s} ~ wL_s - \frac{1}{2}L_s^2 $$
>
> And the first order condition is:
>
> $$ w - L_s = 0$$
>
> Which gives an inverse labor supply curve:
>
> $$ w = L_s ~ ~ ~ ~ \text{(Eq.2)}$$
>
> Step 3. Find the firm's inverse labor demand curve and label it Eq.3.
>
> The firm's optimization problem is:
>
> $$ \max_{L_d} ~ 6pL_d^{1/2} - wL_d $$
>
> And the first order condition is:
>
> $$ 3pL_d^{-1/2} - w = 0 $$
>
> Which gives an inverse labor demand curve:
>
> $$ w = 3pL_d^{-1/2} ~ ~ ~ ~ \text{(Eq.3)} $$
>
> Step 4. Write down the commodity market clearing condition, labor market clearing condition, and feasibility condition.
>
> $$\begin{align}
L_d = L_s = L ~ ~ ~ ~ & \text{(Eq.4)}  \\
q_d = q_s = q ~ ~ ~ ~ & \text{(Eq.5)}  \\
q_s = 6L_d^{1/2} ~ ~ ~ ~ & \text{(Eq.6)} 
\end{align}$$
>
> Step 5. Replace $$q_d$$ and $$q_s$$ with simply $$q$$, and $$L_d$$, $$L_s$$ with $$L$$ in equations 1, 2, 3, and 6:
>
> $$\begin{align}
p = \frac{16}{q} ~ ~ ~ ~ & \text{(Eq.1)} \\
w = L ~ ~ ~ ~ & \text{(Eq.2)} \\
w = 3pL^{-1/2} ~ ~ ~ ~ & \text{(Eq.3)} \\
q = 6L^{1/2} ~ ~ ~ ~ & \text{(Eq.6)} 
\end{align}$$
> 
> Step 6. Combine equations 2 and 3:
>
> $$ L = 3pL^{-1/2} $$
>
> Step 7. Use equation 1 to substitute for $$p$$:
>
> $$\begin{align}
L &= 3 \left( \frac{16}{q} \right) L^{-1/2} \\
L  &= \left(\frac{48}{q} \right) L^{-1/2}
\end{align}$$
>
> Step 8. Use equation 6 to sbustitute for $$q$$ and solve for $$L$$:
>
> $$\begin{align}
L &= \left( \frac{48}{6L^{1/2}} \right) L^{-1/2} \\
L &= \left( \frac{8}{L^{1/2}} \right) L^{-1/2} \\
L &= \frac{8}{L^{1/2} L^{1/2}} \\
L &= \frac{8}{L} \\
L^2 &= 8 \\
L &= \sqrt{8} \\
L &= 2.8284
\end{align}$$
>
> Step 9. Plug $$L$$ into equation 6 to get $$q$$.
>
> $$ q = 6L^{1/2} = 10.0908 $$
>
> Step 10. Plug $$L$$ into equation 2 to get $$w$$.
>
> $$ w = L = 2.8284 $$
>
> Step 11. Plug $$q$$ into equation 1 to get $$p$$.
>
> $$ p = \frac{16}{q} = 1.58561$$
>
> Step 12. Plug $$L, q, w, p$$ into the consumer utility, worker utility, and firm profit functiosn to calculate the utilities and profits.
>
> $$\begin{aligned}
U_c &= 20.9859 \\
U_w &= 4 \\
\Pi &= 8
\end{aligned}$$

## Big Picture Review

- "General equilibrium" refers to models in which the equilibrium of multiple interrelated markets are simultaneously determined.
- We studied a general equilibrium model of interrelated commodity and labor markets.
- The firm sits between the two markets. It is the producer in the commodity market, but the demander in the labor market.
- We made a simplification by disconnecting the workers from the consumers. In a more complex model, we could model them as the same people.
- The key "exogenous" factors driving this model are:
    - The consumers' utility function over the commodity
    - The firms' production function
    - The workers' disutility over work
- In general equilibrium, the commodity price and the wage are determined such that both the commodity market and the labor market are simultaneously in equilibrium.
