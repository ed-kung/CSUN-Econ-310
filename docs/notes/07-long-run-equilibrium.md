---
layout: default
title: "7. Long Run Competitive Equilibrium"
parent: Lecture Notes
nav_order: 7
---

# Long Run Competitive Equilibrium
{: .no_toc }

- TOC
{:toc}

## General Setup

There are $$N$$ identical consumers and $$M$$ identical firms.  The number of consumers is fixed, but $$M$$ can change over time, as firms can freely enter and exit the market.

A commodity is traded in the market at price $$p$$. Consumers and firms are both price takers.

The consumers each have income $$Y$$. Their utility function over the numeraire good $$c$$ and commodity $$q$$ is:

$$u(c,q) = c + v(q)$$

The cost for a firm to produce $$q$$ units of the commodity is $$c(q)$$. Firms maximize their profit:

$$\Pi(q) = pq - c(q) $$

The market is said to be in long run equilibrium if the total quantity consumed by consumers equals the total quantity produced by firms, **AND** the profit of each firm is $$0$$, so that there is no more entry and exit by firms.

{: .purple-callout-title }
> Economic Insight
>
> Firms make zero economic profit (profit in excess of opportunity cost) in the long run equilibrium of a competitive market with free entry and free exit.

We want to find:

1. The long-run equilibrium price of the commodity $$p$$
2. The quantity consumed by each consumer in the long-run equilibrium, $$q_d$$
3. The quantity produced by each firm in the long-run equilibrium, $$q_s$$
4. The number of firms in the long-run equilibrium, $$M$$

## Equilibrium conditions

In the long run equilibrium of the market, three equations have to hold:

1. The consumer's first order condition
2. The firm's first order condition
3. The market equilibrium condition (quantity demanded = quantity supplied)
4. The zero profit condition (firms don't want to enter or exit)

### The consumer's first order condition

The consumer solves:

$$ \max_{q} ~ Y - pq + v(q) $$

The first order condition is:

$$ \text{(Eq.1)} ~ ~ ~ ~ p = v^\prime(q_d) $$

### The firm's first order condition

The producer solves:

$$ \max_{q} ~ pq - c(q) $$

The first order condition is:

$$ \text{(Eq.2)} ~ ~ ~ ~ p = c^\prime(q_s) $$

### The equilibrium condition

Total quantity demanded has to equal total quantity supplied:

$$ \text{(Eq.3)} ~ ~ ~ ~ Nq_d = Mq_s $$

### The zero profit condition

Firm profit has to be zero, so that no more firms want to enter or exit:

$$ \text{(Eq.4)} ~ ~ ~ ~ pq_s - c(q_s) = 0 $$

### Solving the system of equations

The above conditions contain 4 equations: (Eq.1, Eq.2, Eq.3, and Eq.4), and 4 unknowns: ($$p$$, $$q_d$$, $$q_s$$, and $$M$$).  The long run equilibrium is the solution to this system of equations.

{: .blue-callout-title }
> Example
>
> A commodity is traded in a competitive market at price $$p$$. Consumers and firms are price takers.
> 
> **Consumers.** There are 3,000 identical consumers each with income $$Y=100$$. Each consumer has a utility function over numeraire consumption $$c$$ and commodity $$q$$ that is equal to:
>
> $$u(c,q) = c + 10q - 0.5q^2$$
>
> **Firms.** There are $$M$$ identical firms each with cost function equal to:
>
> $$c(q) = 32 + 0.5q^2$$
>
> Firms can freely enter and exit the market, so the number of firms is flexible in the long-run.
>
> 1. Find the price and total quantity in the long-run equilibrium of the market.
> 2. How much does each consumer consume and how much does each firm produce?
> 3. How many firms are there in the long-run equilibrium?
>
> *Answer.*
>
> Step 1: Write down the consumer's optimization problem:
>
> $$\begin{align}
\max_{q} ~ 100 - pq + 10q - 0.5q^2
\end{align}$$
>
> Step 2: Solve the consumer's first order condition:
>
> $$\begin{align}
-p + 10 - q_d &= 0 \\
q_d &= 10 - p
\end{align}$$
>
> Step 3: Write down the firm's optimization problem:
>
> $$\begin{align}
\max_{q} ~ pq - 32 - 0.5q^2
\end{align}$$
>
> Step 4: Solve the firm's first order condition:
>
> $$\begin{align}
p - q_s &= 0 \\
q_s &= p
\end{align}$$
>
> Step 5: Solve the zero profit condition for $$q_s$$:
>
> $$\begin{aligned}
pq_s - 32 - 0.5q_s^2 &= 0 & \\
(q_s) q_s - 32 - 0.5q_s^2 &= 0 & \text{(plug in } p=q_s \text{ from firm FOC)} \\
q_s^2 - 32 - 0.5q_s^2 &= 0 & \\
0.5q_s^2 &= 32 & \\
q_s^2 &= 64 & \\
q_s &= 8 & 
\end{aligned}$$
>
> Step 6: Use the firm's first order condition to solve for $$p$$:
>
> $$\begin{align}
p &= q_s \\
&= 8
\end{align}$$
>
> Step 7: Use the consumer's first order condition to solve for $$q_d$$:
>
> $$\begin{align}
q_d &= 10 - p \\
&= 10 - 8 \\
&= 2
\end{align}$$
>
> Step 8: Use $$Q = Nq_d$$ to solve for the total quantity:
>
> $$\begin{align}
Q &= N q_d \\
&= 3,000 \times 2 \\
&= 6,000
\end{align}$$
>
> Step 9: Use $$Q = Mq_s$$ to solve for $$M$$:
>
> $$\begin{align}
Q &= M q_s \\
q_s &= \frac{Q}{q_s} \\
&= \frac{6,000}{8} \\
&= 750
\end{align}$$

## Summary

To find the long run equilibrium of a competitive market with free entry and free exit, follow these steps:

1. Write down the consumer's optimization problem and solve the first order conditions to get $$q_d$$ as a function of $$p$$.
2. Write down the firm's optimization problem and solve the first order conditions to get $$q_s$$ as a function of $$p$$. At this point, it would also be helpful to write $$p$$ as a function of $$q_s$$.
3. Write down the zero profit condition, plug in $$p$$ as a function of $$q_s$$, and solve for $$q_s$$.
4. Plug $$q_s$$ into the firm's first order condition to get $$p$$.
5. Plug $$p$$ into the consumer's first order condition to get $$q_d$$.
6. Use $$Q = Nq_d$$ to get the total quantity.
7. Use $$Q = Mq_s$$ to get $$M$$.
8. Use the above to calculate any other relevant variable, like consumer utility or firm profit.

