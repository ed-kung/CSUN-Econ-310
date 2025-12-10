---
layout: default
title: 3. Commodity Market
parent: Lecture Notes
nav_order: 3
---

# A Model of Commodity Markets
{: .no_toc }

- TOC
{:toc}

In this lecture, we'll build a simple model of a commodity market with a representative consumer and a representative producer (firm).

The consumer takes the market price as given, and decides how many units of the commodity to purchase.

The firm takes the market price as given, and decides how many units of the commodity to produce and sell.

In equilibrium, the quantity demanded by consumers must equal the quantity supplied by firms.

## Consumers

### Setup

A representative, price-taking consumer decides how many units, $$q_d$$, of a commodity to purchase at unit price $$p$$. The utility they receive for purchasing $$q_d$$ units at price $$p$$ is:

$$ u(q_d) = v(q_d) - pq_d $$

$$v(q_d)$$ is the total benefit that the consumer derives when he consumes $$q_d$$ units of the commodity.  $$pq_d$$ is the total cost paid by the consumer.

### First order condition

The consumer's optimization problem is the following:

$$ \max_{q_d} ~ v(q_d) - pq_d $$

The maximum utility is achieved when the derivative of the consumer's uitlity function is equal to zero. Taking the derivative and setting it equal to zero yields the first order condition:


$$ v^\prime(q_d) - p = 0 $$

or:

$$ v^\prime(q_d) = p ~ ~ ~ ~ (\text{Eq.1})$$

Equation (1) is the first order condition of the consumer. It therefore shows the relationship between price and quantity demanded, because this is the equation the consumer uses to determine how many units to consume.

In other words, equation (1) defines the consumer's **demand curve**!  Technically, it's the *inverse demand curve* because it shows $$p$$ in terms of $$q_d$$. If we re-arrange the equation to write $$q_d$$ as a function of $$p$$, we'd get the demand curve.

Equation (1) shows that at the consumer's optimal choice, price equals marginal benefit, because $$v^\prime(q_d)$$ is additional benefit from an incremental unit of consumption, when the current consumption is already $$q_d$$.

{: .blue-callout-title }
> Example: Deriving a demand curve
> 
> A representative, price-taking consumer decides how many units, $$q$$, of a commodity to purchase at unit price $$p$$. The utility they receive for purchasing $$q$$ units at price $$p$$ is:
>
> $$ u(q) = 9q - \frac{3}{2} q^2 - pq $$
>
> 1. Write down the consumer's demand curve.
>
> *Answer.*
>
> Step 1. Write down the consumer's optimization problem.
>
> $$ \max_{q} ~ 9q - \frac{3}{2}q^2 - pq $$
>
> Step 2. Write down the consumer's first order condition.
>
> $$ 9 - 3q - p = 0 $$
>
> Step 3. Rearrange the first order condition so that we write the quantity demanded in terms of $$p$$.
>
> $$\begin{aligned}
9 - 3q - p &= 0 & \\
3q &= 9 - p ~ ~ ~ ~ & \text{(Add 3q to both sides)} \\
q &= 3 - \frac{1}{3}p ~ ~ ~ ~ & \text{(Divide both sides by 3)}
\end{aligned}$$
>
> So $$q_d = 3 - \frac{1}{3}p$$ is the consumer's demand curve.

## Firms

### Setup

A representative, price-taking firm decides how many units, $$q_s$$, of a commodity to produce and sell at unit price $$p$$. The firm's total cost function for producing $$q_s$$ units is $$c(q_s)$$.

### First order condition

The firm's profit function is revenue minus cost, which can be written as follows:

$$\Pi(q_s) = pq_s - c(q_s)$$

The firm's optimization problem is therefore:

$$ \max_{q_s} ~ pq_s - c(q_s) $$

Taking the derivative with respect to $$q$$ gives u the first order condition:

$$ p - c^\prime(q_s) = 0 $$

or:

$$ p = c^\prime(q_s) ~ ~ ~ ~ (\text{Eq.2}) $$

Equation (2) is the first order condition of the firm. It therefore shows the relationship between price and quantity supplied, because this is the equation the firm uses to determine how many units to produce.

In other words, equation (2) defines the producer's **supply curve**!  Technically, it's the *inverse supply curve* because it shows $$p$$ in terms of $$q_s$$. But if we re-arrange the equation to write $$q_s$$ in terms of $$p$$, we'd get the supply curve.

Equation (2) also shows that at the producer's optimal choice, price equals marginal cost, because $$c^\prime(q_s)$$ is the additional cost to produce an incremental unit of output, when the current output is $$q_s$$.

{: .green-callout-title }
> Example: Deriving a supply curve
> 
> A representative, price-taking firm decides how many units, $$q$$, of a commodity to produce and sell at unit price $$p$$. The firm's total cost function for producing $$q$$ units is:
>
> $$ c(q) = q + q^2 $$
>
> 1. Write down the firm's supply curve.
>
> *Answer.*
>
> Step 1. Write down the firm's profit function.
>
> $$\begin{aligned}
\Pi(q) &= \text{Revenue} - \text{Cost} \\
&= pq - c(q) \\
&= pq - q - q^2 
\end{aligned}$$
>
> Step 2. Write down the firm's optimization problem.
>
> $$ \max_{q} ~ pq - q - q^2 $$
>
> Step 3. Write down the firm's first order condition.
>
> $$ p - 1 - 2q = 0 $$
>
> Step 4. Rearrange the first order condition to write $$q$$ in terms of $$p$$.
>
> $$\begin{aligned}
p - 1 - 2q &= 0 \\
2q &= p - 1 \\
q &= \frac{1}{2}p - \frac{1}{2}
\end{aligned}$$
>
> So $$q_s = \frac{1}{2}p - \frac{1}{2} $$ is the producer's supply curve.

## Market equilibrium 

In equilibrium, $$q_d = q_s = q$$. By combining equations (1) and (2) and the equilibrium condition, we get:

$$ v^\prime(q_d) = p = c^\prime(q_s) $$

or:

$$ v^\prime(q) = c^\prime(q) $$

This equation shows us that in the equilibrium, marginal benefit of the consumers equals marginal cost of the firms.

The equation also lets us solve for the equilibrium mathematically.  $$v^\prime(q) = c^\prime(q)$$ gives us a single equation with a single unknown variable, which we can solve for $$q$$. To then solve for $$p$$, we simply plug that value of $$q$$ into either the consumer's demand curve or the firm's supply curve.

{: .yellow-callout-title }
> Example: Commodity market equilibrium
> 
> A representative, price-taking consumer decides how many units, $$q$$, of a commodity to purchase at unit price $$p$$. The utility they receive for purchasing $$q$$ units at price $$p$$ is:
>
> $$ u(q) = 9q - \frac{3}{2} q^2 - pq $$
> 
> A representative, price-taking firm decides how many units, $$q$$, of a commodity to produce and sell at unit price $$p$$. The firm's total cost function for producing $$q$$ units is:
>
> $$ c(q) = q + q^2 $$
>
> 1. Write down the consumer's demand curve.
> 2. Write down the producer's supply curve.
> 3. Calculate the equilibrium price and quantity.
> 4. Calcualte the consumer surplus in equilibrium (i.e. the consumer's utility.)
> 5. Calculate the producer surplus in equilibrium (i.e. the producer's profit.)
>
> *Answer.*
>
> **Write down the consumer's demand curve.**
>
> We already did this in the previous example.
>
> $$q_d = 3 - \frac{1}{3}p$$
>
> **Write down the producer's supply curve.**
>
> We did this too.
>
> $$q_s = \frac{1}{2}p - \frac{1}{2}$$
>
> **Calculate the equilibrium price and quantity.**
>
> To do this, write down the equilibrium condition ($$q_s=q_d$$) and solve for $$p$$.
>
> $$\begin{aligned}
q_s &= q_d & \\
\tfrac{1}{2}p - \tfrac{1}{2} &= 3 - \tfrac{1}{3}p & \\
\tfrac{1}{2}p + \tfrac{1}{3}p &= 3 + \tfrac{1}{2} & \\
\left( \tfrac{1}{2} + \tfrac{1}{3} \right) p &= 3.5 & \\
\tfrac{5}{6}p &= 3.5 & \\
p &= \tfrac{6}{5} \times 3.5 & \\
p &= 4.2 &
\end{aligned}$$
>
> Then, plug $$p=4.2$$ into either the supply or demand curve to get $$q$$.
>
> $$\begin{aligned}
q_d &= 3 - \tfrac{1}{3}p \\
    &= 3 - \tfrac{1}{3}\times 4.2 \\
	&= 1.6
\end{aligned}$$
>
> So the equilibrium price and quantity are $$p=4.2$$, $$q=1.6$$.
>
> **Calculate the consumer surplus.**
>
> To do this, just plug $$p$$ and $$q$$ into the utility function.
>
> $$\begin{aligned}
u &= 9q - \tfrac{3}{2}q^2 - pq \\
&= 9(1.6) - \tfrac{3}{2}(1.6)^2 - (4.2)(1.6) \\
&= 3.84
\end{aligned}$$
>
> **Calculate the producer surplus.**
>
> To do this, just plug $$p$$ and $$q$$ into the profit function.
>
> $$\begin{aligned}
\Pi &= pq - q - q^2 \\
&= (4.2)(1.6) - 1.6 - (1.6)^2 \\
&= 2.56
\end{aligned}$$
>
> Note that if you had drawn the supply and demand curves and calculated the consumer and producer surpluses graphically, you'd get the same answers.

{: .blue-callout-title }
> Example: Another commodity market equilibrium
> 
> A representative, price-taking consumer decides how many units, $$q$$, of a commodity to purchase at unit price $$p$$. The utility they receive for purchasing $$q$$ units at price $$p$$ is:
>
> $$ u(q) = 9 \ln q - pq $$
> 
> A representative, price-taking firm decides how many units, $$q$$, of a commodity to produce and sell at unit price $$p$$. The firm's total cost function for producing $$q$$ units is:
>
> $$ c(q) = \frac{1}{2} q^2 $$
>
> 1. Write down the consumer's inverse demand curve. (The inverse demand curve simply writes $$p$$ in terms of $$q$$.)
> 2. Write down the producer's inverse supply curve.
> 3. Calculate the equilibrium price and quantity.
> 4. Calcualte the consumer surplus in equilibrium (i.e. the consumer's utility.)
> 5. Calculate the producer surplus in equilibrium (i.e. the producer's profit.)
>
> *Answer.*
>
> **Write down the consumer's inverse demand curve.**
>
> Step 1. Write down the consumer's optimization problem.
>
> $$ \max_{q} ~ 9 \ln q - pq $$
>
> Step 2. Write down the consumer's first order condition.
>
> $$ \frac{9}{q} - p = 0 $$
>
> Step 3. Rearrange the first order condition to write $$p$$ as a function of quantity demanded.
>
> $$\begin{aligned}
\frac{9}{q_d} - p &= 0 \\
p &= \frac{9}{q_d}
\end{aligned}$$
>
> **Write down the producer's inverse supply curve.**
>
> Step 1. Write down the firm's profit function.
>
> $$\begin{aligned}
\Pi(q) &= pq - c(q) \\
&= pq - \frac{1}{2}q^2 
\end{aligned}$$
>
> Step 2. Write down the firm's optimization problem.
>
> $$ \max_{q} ~ pq - \frac{1}{2}q^2 $$
>
> Step 3. Write down the firm's first order condition.
>
> $$ p - q = 0 $$
>
> Step 4. Rearrange the first order condition to write $$p$$ as a function of quantity supplied.
>
> $$ p = q_s $$
>
> **Calculate the equilibrium price and quantity.**
>
> In equilibrium, the inverse supply curve and the inverse demand curve should equal each other at the same quantity. So set the inverse supply and demand curves equal to each other and solve for $$q$$.
>
> $$\begin{aligned}
q &= \frac{9}{q} \\ 
q^2 &= 9 \\
q &= \sqrt{9} \\
q &= 3
\end{aligned}$$
>
> To get the equilibrium price, plug $$q=3$$ into either the inverse supply curve or the inverse demand curve.
>
> $$\begin{aligned}
p &= q_s ~ ~ ~ ~ & \text{(inverse supply curve)} \\
&= 3
\end{aligned}$$
>
> So the equilibrium price and quantity are $$p=3$$, $$q=3$$.
>
> **Calculate the producer and consumer surplus in equilibrium.**
>
> To get consumer surplus, plug $$p$$ and $$q$$ into the consumer's utility function. To get producer surplus, plug $$p$$ and $$q$$ into the producer's profit function.
>
> $$\begin{aligned}
CS &= 9\ln q - pq \\
&= 9\ln(3) - 3\times3 \\
&= 0.8875
\end{aligned}$$
>
> $$\begin{aligned}
PS &= pq - \tfrac{1}{2}q^2 \\
&= 3\times3 - \tfrac{1}{2}(3)^2 \\
&= 4.5
\end{aligned}$$

## Big Picture Review

- We model a commodity market with two main groups of actors: consumers and producers (or firms).
- Consumers take the market price as given, and choose how many units of the commodity to purchase to maximize their utility.
    - Their utility is modeled by something called the "utility function." It represents the benefits, psychological or otherwise, that the consumer derives from purchasing the good.
- Producers take the market price as given, and choose how many units of the commodity to produce to maximize their profit.
    - A firm's profit is equal to its revenue minus its cost.
    - The cost function determines how much it costs the firm to produce any given amount of output. 
- The key drivers of a consumer's decision making is their utility function and the price.
- The key drivers of a firm's decision making is their cost function and the price.
- The demand curve arises out of the first order condition of the consumer's optimization problem.
- The supply curve arises out of the first order condition of the producer's optimization problem.
- In equilibrium, the price adjusts such that the quantity produced matches the quantity consumed.
