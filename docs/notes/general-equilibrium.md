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
> A representative, price-taking consumer decides how many units, $$q$$, of a commodity to purchase at unit price $$p$$. The utility they receive for purchasing $$q$$ units at price $$p$$ is:
>
> $$ u(q) = 16 \ln q - pq $$
>
> A representative, price-taking worker decides how many units, $$L$$, of labor to supply at unit wage $$w$$. The worker's utility function over working $$L$$ labor-units at wage $$w$$ is:
>
> $$ u(L) = wL - \frac{1}{2} L^2 $$
>
> A representative, price-taking firm uses labor to produce and sell a commodity at unit price $$p$$. The firm hires labor at a constant wage rate $$w$$. If the firm employs $$L$$ units of labor, it can produce $$f(L)$$ units of commodity output, where:
>
> $$ f(L) = 6L^{1/2} $$
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
> $$ \max_{q} ~ 16 \ln q - pq $$
>
> And their first order condition is:
>
> $$ \frac{16}{q} - p = 0 $$
>
> Which gives an inverse demand curve:
>
> $$ p = \frac{16}{q} ~ ~ ~ ~ \text{(Eq.1)}$$
>
> Step 2. Find the worker's inverse labor supply curve and label it Eq.2.
>
> The worker's optimization problem is:
>
> $$ \max_{L} ~ wL - \frac{1}{2}L^2 $$
>
> And the first order condition is:
>
> $$ w - L = 0$$
>
> Which gives an inverse labor supply curve:
>
> $$ w = L ~ ~ ~ ~ \text{(Eq.2)}$$
>
> Step 3. Find the firm's inverse labor demand curve and label it Eq.3.
>
> The firm's optimization problem is:
>
> $$ \max_{L} ~ 6pL^{1/2} - wL $$
>
> And the first order condition is:
>
> $$ 3pL^{-1/2} - w = 0 $$
>
> Which gives an inverse labor demand curve:
>
> $$ w = 3pL^{-1/2} ~ ~ ~ ~ \text{(Eq.3)} $$
>
> Step 4. Use Eq.1 and Eq.2 to plug in for $$w$$ and $$p$$ in Eq.3. You'll get an equation in terms of $$L$$ and $$q$$.
>
> $$\begin{aligned}
w &= 3pL^{-1/2} & \\
L &= 3\left(\frac{16}{q}\right)L^{-1/2} & \\
L &= \frac{48}{q} L^{-1/2} & \\
L^{3/2} &= \frac{48}{q} ~ ~ ~ ~ & \text{(Multiply both sides by }L^{1/2}\text{)} \\
qL^{3/2} &= 48 ~ ~ ~ ~ & \text{(Multiply both sides by q)}
\end{aligned}$$
>
> Step 5. Use $$q = f(L) = 6L^{1/2}$$ to plug in for $$q$$ in the above equation. Then solve for $$L$$.
>
> $$\begin{aligned}
qL^{3/2} &= 48 & \\
6L^{1/2} L^{3/2} &= 48 & \\
L^{2} &= 8 & \\
L &= \sqrt{8}  & \\
&= 2.8284 &
\end{aligned}$$
>
> Step 6. Plug $$L$$ into the $$f(L)$$ to get $$q$$.
>
> $$ q = f(L) = 6L^{1/2} = 10.0908 $$
>
> Step 7. Plug $$L$$ into the inverse labor supply curve to get $$w$$.
>
> $$ w = L = 2.8284 $$
>
> Step 8. Plug $$q$$ into the inverse commodity demand curve to get $$p$$.
>
> $$ p = \frac{16}{q} = 1.58561$$
>
> Step 9. Plug $$L, q, w, p$$ into the consumer utility, worker utility, and firm profit functiosn to calculate the utilities and profits.
>
> $$\begin{aligned}
U_c &= 20.9859 \\
U_w &= 4 \\
\Pi &= 8
\end{aligned}$$
