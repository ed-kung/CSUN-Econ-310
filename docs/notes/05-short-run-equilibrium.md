---
layout: default
title: 5. Short Run Competitive Equilibrium
parent: Lecture Notes
---

# Short Run Competitive Equilibrium
{: .no_toc }

- TOC
{:toc}

## General setup

There are $$N$$ identical consumers and $$M$$ identical firms. A commodity is traded in the market at price $$p$$, which the conusmers and firms both take as given.

The consumers each have income $$Y$$. Their utility function over the numeraire good $$c$$ and the commodity $$q$$ is:

$$u(c,q) = c + v(q)$$

The cost for a firm to produce $$q$$ units of the commodity is $$c(q)$$. Firms maximize their profit: 

$$\Pi(q) = pq - c(q)$$

The market is said to be in equilibrium if the total quantity consumed by consumers equals the total quantity produced by the firms.  

We want to find:

1. The equilibrium price of the commodity, $$p$$.
2. The quantity consumed by each consumer in the equilibrium, $$q_d$$.
3. The quantity produced by each firm in the equilibrium $$q_s$$.

## Equilibrium conditions

In the equilibrium of the market, three equations have to hold:

1. The consumer's first order condition
2. The firm's first order condition
3. The market equilibrium condition

### The consumer's first order condition

The consumer solves:

$$ \max_{q} ~ Y - pq + v(q) $$

which leads to the consumer's first order condition, which we call equation 1:

$$\begin{align} \text{(Eq.1)} & ~ ~ ~ ~ p = v^\prime(q_d) \end{align}$$

### The firm's first order condition

The firm solves:

$$ \max_{q} ~ pq - c(q) $$

which leads to the firm's first order condition, which we call equation 2:

$$\begin{align} \text{(Eq.2)} & ~ ~ ~ ~ p = c^\prime(q_s) \end{align}$$

### The equilibrium condition

In equilibrium, the total quantity consumed by consumers is equal to the total quantity produced by firms.  Since every consumer and every firm is identical, we can write:

$$\begin{align} \text{(Eq.3)} & ~ ~ ~ ~ Nq_d = Mq_s \end{align}$$

This is the equilibrium condition, which we call equation 3.

### Solving the system of equations

The consumer's first order condition (Eq.1), the firm's first order condition (Eq.2), and the equilibrium condition (Eq.3) all have to hold in equilibrium. We therefore have three equations (Eq.1, Eq.2, Eq.3) and three unknowns ($$p$$, $$q_d$$, $$q_s$$). We can find the equilibrium by solving this system of equations.

{: .blue-callout-title }
> Example
>
> **Consumers.** There are 3,000 identical consumers each with income $$Y=100$$. Each consumer has a utility function over numeraire consumption $$c$$ and commodity $$q$$ that is equal to:
>
> $$u(c,q) = c + 10q - q^2$$
>
> **Firms.** There are 200 identical firms each with cost function equal to:
>
> $$c(q) = 10 + 0.1q^2$$
>
> 1. Calculate the equilibrium price $$p$$ and total quantity $$Q$$ traded in the market.
> 2. Calculate the total consumer utility in the market equilibrium.
> 3. Calculate the total producer profit in the market equilibirum.
>
> *Answer.*
>
> Step 1: Write down the consumers' optimization problem:
>
> $$\begin{align} 
& \max_{c,q} ~ c + 10q - q^2 ~ ~ \text{ s.t. } c = 100 - pq \\
= & \max_{q} ~ 100 - pq + 10q - q^2
\end{align}$$
>
> Step 2: Solve the consumer's first order condition (write down $$q_d$$ instead of $$q$$ to emphasize it's the consumer's choice):
>
> $$\begin{align}
-p + 10 - 2q_d &= 0 \\
q_d &= \frac{10 - p}{2} 
\end{align}$$
>
> Step 3: Write down the firm's optimization problem:
>
> $$\begin{align}
\max_{q} ~ pq - 10 - 0.1q^2
\end{align}$$
>
> Step 4: Solve the firm's first order condition (write down $$q_s$$ instead of $$q$$ to emphasize it's the firm's choice):
>
> $$\begin{align}
p - 0.2q_s &= 0 \\
q_s &= 5p
\end{align}$$
>
> Step 5: Solve the equilibrium condition:
>
> $$\begin{align}
3000q_d &= 200q_s \\
15q_d &= q_s \\
15 \left(\frac{10-p}{2}\right) &= 5p \\
7.5(10-p) &= 5p \\
75 - 7.5p &= 5p \\
75 &= 12.5p \\
6 &= p
\end{align}$$
>
> Step 6: Wrap up by calculating all the other equilibrium variables.
>
> To get $$q_d$$, plug $$p=6$$ into the consumer's first order condition. We get $$q_d=2$$.
>
> To get $$q_s$$, plug $$p=6$$ into the producer's first order condition. We get $$q_s=30$$.
>
> To get total quantity, multiple $$q_d$$ by $$3,000$$ or $$q_s$$ by $$200$$. Either way, we get $$Q=6,000$$.
>
> To get each consumer's utility, first calculate $$c = Y - p q_d = 100 - (6)(2) = 88$$. 
>
> Then, plug $$c=88$$ and $$q_d=2$$ into $$u(c,q)$$:
>
> $$\begin{align}
u(c,q_d) &= c + 10q_d - (q_d)^2 \\
&= 88 + 10(2) - (2)^2 \\
&= 104
\end{align}$$
>
> The total consumer utility is simply $$3,000 \times 104 = 312,000$$.
>
> To get each firm's profit, plug $$p=6$$ and $$q_s=30$$ into $$\Pi(q)$$:
>
> $$\begin{align}
\Pi(q_s) &= pq_s - 10 - 0.1(q_s)^2 \\
&= (6)(30) - 10 - 0.1(30)^2 \\
&= 80
\end{align}$$
>
> To get total firm profit, multiply $$80$$ by $$200$$ to get a total firm profit of $$16,000$$.

## Application: The price of gasoline and Uber

Why is it useful to be able to solve for a market equilibrium, starting from the consumers' and firms' optimization problems?  

Because the optimization problems are more "fundamental" than a supply curve or a demand curve.  By modeling the problem starting from fundamentals, we can more precisely model the effects of changes to the incentive structure. 

The following example demonstrates.

{: .green-callout-title }
> Example
>
> There are $$10,000$$ identical Uber drivers (producers) and $$10,000$$ identical Uber riders (consumers). The price per mile of an Uber ride is $$p$$.  Riders and drivers are both price takers.
>
> **Riders.** When Uber riders take an Uber, they benefit in two ways: 1) convenience and 2) saving on the cost of gasoline. 
>
> The utility they get from convenience is $$10q - 0.5q^2$$, where $$q$$ is the number of miles they ride.  
>
> The utility they get from gasoline cost savings is $$p_g q$$, where $$p_g$$ is the price-per-mile of gasoline.  
>
> An Uber rider's utility function over numeraire consumption $$c$$ and miles ridden $$q$$ is therefore:
>
> $$u(c,q) = c + 10q - 0.5q^2 + p_g q$$
>
> **Drivers.** When Uber drivers drive for Uber, they have two costs: 1) the opportunity cost of time and 2) the cost of gasoline. 
>
> The cost of gasoline is simply $$p_g q$$ where $$q$$ is the number of miles driven.  
>
> The opportunity cost of time is $$0.5q^2$$.
>
> An Uber driver's profit function is therefore:
>
> $$\Pi(q) = pq - p_gq - 0.5q^2 $$
>
> Find the equilibrium price and quantity of Uber rides, expressed in terms of the price of gasoline $$p_g$$.
>
> *Answer.*
>
> Step 1: Write down the consumer's optimization problem:
>
> $$\begin{align}
\max_{q} ~ Y - pq + 10q - 0.5q^2 + p_g q
\end{align}$$
>
> Step 2: Solve the consumer's first order condition: 
>
> $$\begin{align}
-p + 10 - q_d + p_g &= 0 \\
q_d &= 10 + p_g - p
\end{align}$$
>
> Step 3: Write down the producer's optimization problem:
>
> $$\begin{align}
\max_{q} ~ pq - p_g q - 0.5q^2
\end{align}$$
>
> Step 4: Solve the producer's first order condition:
>
> $$\begin{align}
p - p_g - q_s &= 0 \\
q_s &= p - p_g
\end{align}$$
>
> Step 5: Solve the equilibrium condition:
>
> $$\begin{align}
10,000q_d &= 10,000q_s \\
q_d &= q_s \\
10 + p_g - p &= p - p_g \\
10 + 2p_g &= 2p \\
5 + p_g &= p 
\end{align}$$
>
> So the equilibrium price of an Uber mile is $$p = 5 + p_g$$. It increases 1:1 with the price of gasoline!
>
> To calculate the equilibrium quantity, plug $$p = 5 + p_g$$ back into either the consumer or the producer first order condition:
>
> $$\begin{align}
q_s &= p - p_g \\
&= (5 + p_g) - p_g \\
&=5
\end{align}$$
>
> The total quantity is therefore: $$10,000 \times 5 = 50,000$$.
> 
> Our work shows that in the equilibrium, the price of an Uber mile is $$p = 5 + p_g$$, and the total quantity of miles driven/ridden is $$Q=50,000$$. 
>
> Notice that the price of an Uber mile increases 1:1 with the price of a mile of gasoline, but the equilibrium quantity of Ubers is unaffected by the price of gasoline.
>
> This result makes sense when you consider that the price of gasoline both increases both the marginal benefit of an Uber ride but also the marginal cost. Moreover, the increase in marginal benefit is exactly the same as the increase in the marginal cost, because they're both due to the increase in gas cost. Because of this, consumers are willing to offset the cost of the gasoline by paying a higher price for Uber. In equilibrium, the price goes up but the quantity does not change.

{: .purple-callout-title }
> Economic Insight
>
> When the marginal willingness-to-pay and the marginal cost of a commodity both increase/decrease by the same amount, we expect the price of the commodity to increase/decrease by that amount, but the equilibrium quantity to remain unchanged.


## Summary

To find the short run equilibrium of a competitive market, follow these steps:

1. Write down the optimization problem of the consumers, then solve their first order condition to get $$q_d$$ as a function of $$p$$.
2. Write down the optimization problem of the firms, then solve their first order condition to get $$q_s$$ as a function of $$p$$.
3. Use $$Nq_d = Mq_s$$ to find the equilibrium $$p$$.
4. Plug $$p$$ into the first order conditions to find $$q_s$$ and $$q_d$$.
5. Use the above to calculate any other relevant variable, such as consumer utility or firm profit.

