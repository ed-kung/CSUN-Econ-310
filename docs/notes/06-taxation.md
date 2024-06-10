---
layout: default
title: "6. Application: Taxation"
parent: Lecture Notes
nav_order: 6
---

# Application: Taxation
{: .no_toc }

- TOC
{:toc}

## Unit taxes

### What is a unit tax?

A unit tax is a tax that charges a fixed amount of tax per unit purchased or sold. Unit taxes aren't very common in real life, but they're easy to analyze so economics classes start with them. Ad valorem taxes are more common, and we discuss them below.

### Unit tax on consumers

A unit tax of $$t$$ per unit on consumers says that consumers have to pay the government $$t$$ dollars per unit of commodity that they purchase.

In the quasilinear framework, the consumer's optimization problem becomes:

$$ \max_{c,q} ~ c + v(q) ~ ~ \text{ s.t. } c = Y - (p+t)q $$

The consumer's first order condition becomes:

$$ p = v^\prime(q_d) - t $$

{: .purple-callout-title }
> Economic Insight
>
> When consumers are taxed at a rate of $$t$$ per unit, then instead of price equals marginal willingness-to-pay, we get that price equals marginal willingness-to-pay minus tax.

{: .blue-callout-title }
> Example 1
>
> **Consumers.** There are $$500$$ identical consumers each with income $$Y=100$$. Each consumer has a utility function over numeraire consumption $$c$$ and commodity $$q$$ that is equal to:
>
> $$u(c,q) = c + 10q - 0.5q^2$$
>
> **Firms.** There are $$100$$ identical firms each with cost function equal to:
>
> $$c(q) = 0.1q^2$$
>
> Suppose the government charges consumers a unit tax of $$t$$ per unit of commodity purchased. 
>
> 1. Write down the equilibrium price $$p$$ and total quantity $$Q$$, expressed in terms of the tax rate $$t$$.
> 2. Write down each consumer's utility in terms of $$t$$.
> 3. Write down each firm's profit in terms of $$t$$.
> 4. Write down the total tax revenue in terms of $$t$$.
>
> *Answer.*
>
> Step 1: Write down the consumer's optimization problem:
>
> $$\begin{align}
\max_{q} ~ 100 - (p+t)q + 10q - 0.5q^2
\end{align}$$
>
> Step 2: Solve the consumer's first order condition:
>
> $$\begin{align}
-(p+t) + 10 - q_d &= 0 \\
q_d &= 10 - p - t
\end{align}$$
>
> Step 3: Write down the firm's optimization problem:
>
> $$\begin{align}
\max_{q} pq - 10 - 0.1q^2
\end{align}$$
>
> Step 4: Solve the firm's first order condition:
>
> $$\begin{align}
p - 0.2q_s &= 0 \\
q_s &= 5p 
\end{align}$$
>
> Step 5: Solve the equilibrium condition:
>
> $$\begin{align}
500 q_d &= 100 q_s \\
5 q_d &= q_s \\
5 (10 - p - t) &= 5p \\
10 - p - t &= p \\
10 - t &= 2p \\
p &= 5 - 0.5t 
\end{align}$$
>
> Step 6: Calculate all the other equilibrium variables, expressed in terms of $$t$$.
>
> Quantity consumed by each consumer:
>
> $$\begin{align}
q_d &= 10 - p - t \\
&= 10 - (5 - 0.5t) - t \\
&= 10 - 5 + 0.5t - t \\
&= 5 - 0.5t 
\end{align}$$
>
> Utility of each consumer:
>
> $$\begin{align}
u &= 100 - (p+t)q_d + 10q_d - 0.5q_d^2 \\
&= 100 - (5 - 0.5t + t)(5 - 0.5t) + 10(5-0.5t) - 0.5(5-0.5t)^2 \\
&= 100 - (5 + 0.5t)(5 - 0.5t) + 10(5-0.5t) - 0.5(5-0.5t)^2 
\end{align}$$
>
> Quantity produced by each firm:
>
> $$\begin{align}
q_s &= 5p \\
&= 5(5 - 0.5t) \\
&= 25 - 2.5t 
\end{align}$$
>
> Profit of each firm:
> 
> $$\begin{align}
\Pi &= pq_s - 0.1q_s^2 \\
&= (5 - 0.5t)(25 - 2.5t) - 0.1(25 - 2.5t)^2 
\end{align}$$
>
> Total quantity traded:
>
> $$\begin{align}
Q &= 100q_s \\
&= 100 (25 - 2.5t) \\
&= 2,500 - 250t 
\end{align}$$
>
> Tax revenue:
>
> $$\begin{align}
R &= tQ \\
&= t(2,500 - 250t) \\
&= 2,500t - 250t^2 
\end{align}$$
>
> If we were to plot the tax revenue as a function of $$t$$, we would get:
>
> ![laffer-curve](/CSUN-Econ-310/assets/images/06-taxation-laffer-curve.png)
>
> This inverse-U shape relationship between tax revenue and tax rate is known as the Laffer Curve.

{: .purple-callout-title }
> Economic Insight
>
> Tax revenues cannot be raised indefinitely by increasing tax rates. At some point, taxes become so high that increasing the tax rate will actually shrink the market by so much that tax revenue goes down.  The inverse-U shaped relationship between tax rates and tax revenue is known as the **Laffer Curve**.

### Unit tax on producers

A unit tax of $$t$$ per unit on producers says that producers have to pay the government $$t$$ dollars per unit of commodity they produce.

The firm's optimization problem becomes:

$$ \max_{q} ~ (p - t)q - c(q) $$

The firm's first order condition becomes:

$$ p = c^\prime(q_s) + t $$

{: .purple-callout-title }
> Economic Insight
>
> When producers are taxed at a rate of $$t$$ per unit, then instead of price equals marginal cost, we get that price equals marginal cost plus tax. 

{: .green-callout-title }
> Example 2 
>
> **Consumers.** There are $$500$$ identical consumers each with income $$Y=100$$. Each consumer has a utility function over numeraire consumption $$c$$ and commodity $$q$$ that is equal to:
>
> $$u(c,q) = c + 10q - 0.5q^2$$
>
> **Firms.** There are $$100$$ identical firms each with cost function equal to:
>
> $$c(q) = 0.1q^2$$
>
> Suppose the government charges *producers* a unit tax of $$t$$ per unit of commodity produced. 
>
> 1. Write down the equilibrium price $$p$$ and total quantity $$Q$$, expressed in terms of the tax rate $$t$$.
> 2. Write down each consumer's utility in terms of $$t$$.
> 3. Write down each firm's profit in terms of $$t$$.
> 4. Write down the total tax revenue in terms of $$t$$.
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
\max_{q} ~ (p-t)q - 10 - 0.1q^2
\end{align}$$
>
> Step 4: Solve the firm's first order condition:
>
> $$\begin{align}
p - t - 0.2q_s &= 0 \\
q_s &= 5(p - t) 
\end{align}$$
>
> Step 5: Solve the equilibrium condition:
>
> $$\begin{align}
500 q_d &= 100 q_s \\
5 q_d &= q_s \\
5 (10 - p) &= 5(p - t) \\
10 - p &= p - t \\
10 + t &= 2p \\
p &= 5 + 0.5t 
\end{align}$$
>
> Step 6: Calculate all the other equilibrium variables, expressed in terms of $$t$$.
>
> Quantity consumed by each consumer:
>
> $$\begin{align}
q_d &= 10 - p \\
&= 10 - (5 + 0.5t)  \\
&= 10 - 5 - 0.5t  \\
&= 5 - 0.5t 
\end{align}$$
>
> Utility of each consumer:
>
> $$\begin{align}
u &= 100 - pq_d + 10q_d - 0.5q_d^2 \\
&= 100 - (5 + 0.5t)(5 - 0.5t) + 10(5-0.5t) - 0.5(5-0.5t)^2 
\end{align}$$
>
> Quantity produced by each firm:
>
> $$\begin{align}
q_s &= 5(p - t) \\
&= 5(5 + 0.5t - t) \\\
&= 5(5 - 0.5t) \\
&= 25 - 2.5t 
\end{align}$$
>
> Profit of each firm:
> 
> $$\begin{align}
\Pi &= (p - t)q_s - 0.1q_s^2 \\
&= (5 + 0.5t - t)(25 - 2.5t) - 0.1(25 - 2.5t)^2  \\
&= (5 - 0.5t)(25 - 2.5t) - 0.1(25 - 2.5t)^2  \\
\end{align}$$
>
> Total quantity traded:
>
> $$\begin{align}
Q &= 100q_s \\
&= 100 (25 - 2.5t) \\
&= 2,500 - 250t 
\end{align}$$
>
> Tax revenue:
>
> $$\begin{align}
R &= tQ \\
&= t(2,500 - 250t) \\
&= 2,500t - 250t^2 
\end{align}$$
>

### Equivalency of tax incidence

In the above two examples, we saw that the equilibrium quantity, consumer utility, firm profit, and tax revenue are the same regardless of whether the unit tax is paid by the consumers or paid by the firms. Thus, the equilibrium impact of a unit tax does not depend on whether the tax is levied on consumers or firms.

This is a result you should have already learned in Econ 160. But now you're able to prove it mathematically (at least in the context of quasilinear utility functions.)

{: .purple-callout-title }
> Economic Insight
>
> In a competitive market, it doesn't matter whether a unit tax is charged to the consumers or the producers. The economic impact will be the same.


## Ad valorem taxes

### What is an ad valorem tax?

An ad valorem tax is a tax based on a percentage of the transacted value. Most taxes that we pay in real life are ad valorem taxes. For example, the 10% sales tax that we're accustomed to paying in Los Angeles is an ad valorem tax because the amount of tax is not based on how many items you purchased but based on the value of the sale.

### Ad valorem tax on consumers

An ad valorem tax on consumers makes it so that instead of paying $$pq$$ to purchase $$q$$ units, they have to pay $$(1+t)pq$$ instead, where $$t$$ is the tax rate.

The consumer's optimization problem becomes:

$$ \max_{q} ~ Y - (1+t)pq + v(q)$$

and the consumer's first order condition becomes:

$$p = \frac{v^\prime(q_d)}{1+t}$$

### Ad valorem tax on producers

An ad valorem tax on producers makes it so that instead of receiving $$pq$$ from selling $$q$$ units, producers only receive $$(1-t)pq$$ instead.

The producer's optimization problem becomes:

$$ \max_{q} ~ (1-t)pq + c(q) $$

and their first order condition becomes:

$$ p = \frac{c^\prime(q_s)}{1-t} $$

We won't solve an example with ad valorem taxes, but you should know how to set up the first order conditions.

