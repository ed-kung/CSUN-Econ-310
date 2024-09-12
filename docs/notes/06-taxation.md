---
layout: default
title: "6. Application: Ad Valorem Taxes"
parent: Lecture Notes
nav_order: 6
---

# Application: Ad Valorem Taxes
{: .no_toc }

- TOC
{:toc}

## What is an ad valorem tax?

An ad valorem tax is a tax based on a percentage of the transacted value. Most taxes that we pay in real life are ad valorem taxes. For example, the 10% sales tax that we're accustomed to paying in Los Angeles is an ad valorem tax because the amount of tax is not based on how many items you purchased but based on the value of the sale.

Mathematically, if a consumer has to pay an ad valorem tax rate of $$t_c$$, and they buy $$q$$ units at price $$p$$, the total tax they pay is $$t_c p  q$$.

Similarly, if a producer has to pay an ad valorem tax rate of $$t_p$$, and they sell $$q$$ units at price $$p$$, the total tax they pay is $$t_p  p  q$$.


## General setup 

A commodity is traded at price $$p$$ in a competitive market with price-taking consumers and firms.

There are $$N$$ identical consumers each with income $$Y$$. The consumer has a utility function over numeraire consumption $$c$$ and commodity $$q$$ given by:

$$ u(c,q) = c + v(q) $$

There are $$M$$ identical firms each with cost function $$c(q)$$. 

An ad valorem tax rate of $$t_c$$ is levied on the consumers and an ad valorem  tax rate of $$t_p$$ is levied on the producers. 

We want to find:

1. The equilibrium price of the commodity $$p$$.
2. The quantity consumed per consumer, $$q_d$$, and the quantity produced per firm, $$q_s$$.
3. The total tax revenue raised.
4. The deadweight loss due to the tax. (Loss in total consumer utility plus producer profits plus tax revenue due to the tax.)


## Equilibrium conditions

In the equilibrium, three equations must hold:

1. The consumer's first order condition
2. The firm's first order condition
3. The market equilibrium condition

### The consumer's first order condition

The consumer solves:

$$ \max_{c,q} ~ c + v(q) ~ \text{ s.t. } ~ c + (1+t_c)pq = Y $$

Which becomes:

$$ \max_{q} ~ Y - (1+t_c) pq + v(q) $$

The first order condition is:

$$ \text{(Eq.1)} ~ ~ ~ (1+t_c) p = v^\prime(q_d) $$

### The producer's first order condition

The firm solves:

$$ \max_{q} ~ (1 - t_p) pq - c(q) $$

which leads to the first order condition:

$$ \text{(Eq.2)} ~ ~ ~ (1 - t_p) p = c^\prime(q_s) $$

### Market equilibrium condition

The market equilibrium condition simply says that the total quantity consumed equals the total quantity produced:

$$ \text{(Eq.3)} ~ ~ ~  N q_d = M q_d $$

To find the equilibrium, we simply solve the above three equations for $$p$$, $$q_d$$, and $$q_s$$.  

{: .blue-callout-title }
> Example 1
>
> A commodity $$q$$ is traded at price $$p$$ in a competitive market with price-taking consumers and firms. 
>
> There are $$100$$ identical consumers each with income $$Y=100$$. Each consumer has utility over numeraire consumption $$c$$ and commodity $$q$$ given by:
>
> $$ u(c,q) = c + 12q - \tfrac{1}{2} q^2 $$
>
> There are $$50$$ identical firms each with cost function given by:
>
> $$ c(q) = \tfrac{1}{2} q^2 $$
>
> An ad-valorem tax rate of $$50\%$$ is placed on the consumers.
>
> 1. Find the equilibrium *without* the tax. Calculate total consumer utility and total firm profit.
> 2. Find the equilibrium *with* the tax. Calculate total utility, total profit, and tax revenue.
> 3. Calculate the deadweight loss due to the tax.
>
> *Without tax.*
>
> Without tax, the consumer solves:
>
> $$ \max_{q} ~ 100 - pq + 12q - \tfrac{1}{2} q^2 $$
>
> The first order condition is:
>
> $$\begin{align}
-p + 12 - q_d &= 0 \\
q_d &= 12 - p
\end{align}$$
>
> Without tax, the producer solves:
>
> $$ \max_{q} ~ pq - \tfrac{1}{2} q^2 $$
>
> The first order condition is:
> 
> $$\begin{align}
p - q_s &= 0 \\
q_s &= p
\end{align}$$
>
> The market equilibrium condition is:
>
> $$\begin{align}
Nq_d &= Mq_s \\
100 (12 - p) &= 50p \\
2(12-p) &= p \\
24 - 2p &= p \\
24 &= 3p \\
p &= 8
\end{align}$$
>
> Plug $$p=8$$ into the above equations to get $$q_d=4$$, $$q_s=8$$. The per-consumer utility is $$108$$ and the per-firm profit is $$32$$.
>
> *With tax.*
>
> With tax, the consumer solves:
>
> $$\max_{q} ~ 100 - 1.5pq + 12q - \tfrac{1}{2} q^2 $$
>
> The first order condition is:
>
> $$\begin{align}
-1.5p + 12 - q_d &= 0 \\
q_d &= 12 - 1.5p 
\end{align}$$
>
> With tax, the producer solves:
>
> $$ \max_{q} ~ pq - \tfrac{1}{2} q^2 $$
>
> The first order condition is:
> 
> $$\begin{align}
p - q_s &= 0 \\
q_s &= p
\end{align}$$
>
> The market equilibrium condition is:
>
> $$\begin{align}
Nq_d &= Mq_s \\
100 (12 - 1.5p) &= 50p \\
2(12-1.5p) &= p \\
24 - 3p &= p \\
24 &= 4p \\
p &= 6
\end{align}$$
>
> Plug $$p=6$$ into the above equations to get $$q_d=3$$ and $$q_s=6$$. The per-consumer utility is $$104.5$$. The per-firm profit is $$18$$. Tax revenue is $$0.5 p Q = 900$$.
>
> *Deadweight loss.*
>
> If we put the above results into a table, we get this:
>
> |                                | Without tax          | With tax            |
> | ------------------------------ | -------------------- | ------------------- |
> | $$p$$                          | $$8$$                | $$6$$               |
> | $$q_d$$                        | $$4$$                | $$3$$               |
> | $$q_s$$                        | $$8$$                | $$6$$               |
> | $$Q$$                          | $$400$$              | $$300$$             |
> | Per-consumer utility           | $$108$$              | $$104.5$$           |
> | Total consumer utility         | $$10,800$$           | $$10,450$$          |
> | Per-firm profit                | $$32$$               | $$18$$              |
> | Total firm profit              | $$1,600$$            | $$900$$             |
> | Tax revenue                    | $$0$$                | $$900$$             |
> | Total surplus                  | $$12,400$$           | $$12,250$$          |
>
> The deadweight loss is the loss in total surplus due to the tax. The deadweight loss is therefore equal to $$150$$.

## Lump sum taxes

A lump sum tax is a tax that a person has to pay regardless of how much of a commodity they buy or sell.  It is sometimes called a "poll tax", or a "head tax", because it is paid "per head".

{: .green-callout-title }
> Example 2
>
> We'll consider the same setup as example 1, but instead of an ad valorem tax on consumers, the same tax revenue is raised via a lump sum tax on consumers.
>
> A commodity $$q$$ is traded at price $$p$$ in a competitive market with price-taking consumers and firms. 
>
> There are $$100$$ identical consumers each with income $$Y=100$$. Each consumer has utility over numeraire consumption $$c$$ and commodity $$q$$ given by:
>
> $$ u(c,q) = c + 12q - \tfrac{1}{2} q^2 $$
>
> There are $$50$$ identical firms each with cost function given by:
>
> $$ c(q) = \tfrac{1}{2} q^2 $$
>
> 1. Suppose the government wants to raise $$900$$ in tax revenues via a lump sum tax on consumers. How much tax must they charge to each consumer?
>
> 2. Find the equilibrium with the lump sum tax. What is the deadweight loss?
>
> *Answer.*
>
> Since there are $$100$$ consumers and the government wants to raise $$900$$, it must charge a lump sum tax of $$9$$ to each consumer.
>
> The consumer's budget constraint becomes: $$c = 91 - pq$$.
>
> The consumer solves:
>
> $$ \max_{q} ~ 91 - pq + 12q - \tfrac{1}{2} q^2 $$
>
> The first order condition is:
>
> The first order condition is:
>
> $$\begin{align}
-p + 12 - q_d &= 0 \\
q_d &= 12 - p
\end{align}$$
>
> Without tax, the producer solves:
>
> $$ \max_{q} ~ pq - \tfrac{1}{2} q^2 $$
>
> The first order condition is:
> 
> $$\begin{align}
p - q_s &= 0 \\
q_s &= p
\end{align}$$
>
> The market equilibrium condition is:
>
> $$\begin{align}
Nq_d &= Mq_s \\
100 (12 - p) &= 50p \\
2(12-p) &= p \\
24 - 2p &= p \\
24 &= 3p \\
p &= 8
\end{align}$$
>
> Plug $$p=8$$ into the above equations to get $$q_d=4$$, $$q_s=8$$. The per-consumer utility is $$91$$ and the per-firm profit is $$32$$. The tax revenue is $$900$$.
>
> If we augment our previous table with these results we get:
>
> |                        | Without tax  | Ad valorem tax | Lump sum tax   | 
> | ---------------------- | ------------ | -------------- | -------------- |
> | $$p$$                  | $$8$$        | $$6$$          | $$8$$          |
> | $$q_d$$                | $$4$$        | $$3$$          | $$4$$          |
> | $$q_s$$                | $$8$$        | $$6$$          | $$8$$          |
> | $$Q$$                  | $$400$$      | $$300$$        | $$400$$        |
> | Per-consumer utility   | $$108$$      | $$104.5$$      | $$99$$         |
> | Total consumer utility | $$10,800$$   | $$10,450$$     | $$9,900$$      |
> | Per-firm profit        | $$32$$       | $$18$$         | $$32$$         |
> | Total firm profit      | $$1,600$$    | $$900$$        | $$1,600$$      |
> | Tax revenue            | $$0$$        | $$900$$        | $$900$$        |
> | Total surplus          | $$12,400$$   | $$12,250$$     | $$12,400$$     |
>
> This example shows that the lump sum tax raises the same tax revenue but without deadweight loss. 

### The "Lump-sum Principle"

In the above example, a lump sum tax was able to raise the same amount of revenue but without the deadweight loss of an ad valorem tax.  This is a more general principle: that a lump sum tax can raise the same amount of tax revenue with less welfare cost than a tax on a specific commodity.

{: .purple-callout-title }
> Economic Insight
>
> A lump sum tax can raise the same amount of revenue as a commodity tax, but with less deadweight loss.

Lump sum taxes result in less deadweight loss because they are *non-distortionary*. That is, they do not distort the incentives of any of the market participants, since a lump sum tax has to be paid regardless of behavior.

{: .purple-callout-title }
> Note
>
> The personal income tax is not a lump sum tax since it is only paid by those who work, and it scales with the amount of work.  The personal income tax is a commodity tax on the commodity of work.

If lump sum taxes have a lower welfare cost than commodity taxes, why aren't they more commonly used in real life?  

One answer is that lump sum taxes are *regressive*. Under a lump sum tax, rich people would pay a much smaller percentage of their income in taxes than poor people. Many people would consider this unfair.

Another answer is that lump sum taxes are *impractical*. Consider the United States. In 2023, the U.S. Federal Government raised about $4.4 trillion in tax revenue from a population of 340 million. If this tax revenue was spread as a lump sum tax amongst the 340 million people, each person would have a tax bill of $13,000.  A family of 4 would have a combined tax bill of $52,000 which is too much for most families to practically afford and would in any case be politically infeasible.

What if the lump sum tax was only charged to people above a certain income? Then it wouldn't be a lump sum tax anymore because the tax now depends on behavior.  It would change people's incentives and lead to deadweight loss by causing some people to inefficiently work less (to get under the income threshold), or perhaps even to hide their income by various means.

