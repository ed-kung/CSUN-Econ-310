---
layout: default
title: 4. Commodity Market
parent: Lecture Notes
nav_order: 4
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

A representative, price-taking consumer decides how many units, \(q_d\), of a commodity to purchase at unit price \(p\). The utility they receive for purchasing \(q_d\) units at price \(p\) is:

$$ u(q_d) = v(q_d) - pq_d $$

$$v(q_d)$$ is the total benefit that the consumer derives when he consumes $$q_d$$ units of the commodity.  $$pq_d$$ is the total cost paid by the consumer.

### First order condition

The consumer's optimization problem is the following:

$$ \max_{q_d} ~ v(q_d) - pq_d $$

Taking the derivative with respect to $$q$$ gives us the first order condition:

$$ v^\prime(q_d) - p = 0 $$

or:

$$ v^\prime(q_d) = p ~ ~ ~ ~ (\text{Eq.1})$$

Equation (1) is the first order condition of the consumer. It therefore shows the relationship between price and quantity demanded, because this is the equation the consumer uses to determine how many units to consume.

In other words, equation (1) defines the consumer's **demand curve**!  Technically, it's the *inverse demand curve* because it shows $$p$$ in terms of $$q_d$$. If we re-arrange the equation to write $$q_d$$ as a function of $$p$$, we'd get the demand curve.

Equation (1) shows that at the consumer's optimal choice, price equals marginal benefit, because $$v^\prime(q_d)$$ is additional benefit from an incremental unit of consumption, when the current consumption is already $$q_d$$.

{: .blue-callout-title }
> Example: Deriving a demand curve
> 

## Firms

### Setup

A representative, price-taking firm decides how many units, \(q_s\), of a commodity to produce and sell at unit price \(p\). The firm's total cost function for producing \(q_s\) units is $$c(q_s)$$.

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

{: .blue-callout-title }
> Example: Another commodity market equilibrium
>


