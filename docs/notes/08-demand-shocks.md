---
layout: default
title: "8. Application: Demand Shocks"
parent: Lecture Notes
---

# Application: Demand Shocks
{: .no_toc }

- TOC
{:toc}

In this lecture, we'll calculate a competitive market's short and long-run response to a negative demand shock.

## Setup

Oil is traded in a competitive market at price $$p$$. Consumers and producers are price takers.

**Consumers.** There are $$N=3,200$$ consumers. Consumers' utility over the numeraire good $$c$$ and oil consumption $$q$$ is:

$$ u(c,q) = c + \alpha q - 0.5q^2 $$

**Firms.** There are $$M$$ identical firms. Because of free entry and free exit, $$M$$ is can change over the long run. To produce $$q$$ units of oil, it costs a firm:

$$ c(q) = 64 + 0.25q^2 $$

1. In the year 2019, $$\alpha=10$$ and the market is in long run equilibrium. Calculate the price of oil, the total quantity traded, and the number of firms.

2. In the year 2020, COVID lockdowns reduce the demand for oil.  $$\alpha$$ falls to $$9$$. Calculate the short-run change in oil price and total quantity caused by this negative demand shock. Calculate what firm profits are in the new short-run equilibrium. (Note: In the short-run, the number of firms does not change.)

3. If $$\alpha$$ stays at $$9$$, how do you expect the market to evolve over the long-run?  Calculate the new long-run equilibrium price and quantity of oil when $$\alpha=9$$, and the number of firms in the new long-run equilibrium.

## Before the demand shock

{: .blue-callout-title }
> Answer to part 1
>
> Let's solve for the long-run equilibrium when $$\alpha=10$$.
>
> Step 1. Write down the consumer's optimization problem.
>
> $$ \max_{q} ~ Y - pq + 10q - 0.5q^2 $$
>
> Step 2. Solve the consumer's first order condition.
>
> $$\begin{align}
-p + 10 - q_d &= 0 \\
q_d &= 10 - p
\end{align}$$
>
> Step 3. Write down the firm's optimization problem.
>
> $$\begin{align}
\max_{q} ~ pq - 64 - 0.25q^2
\end{align}$$
>
> Step 4. Solve the firm's optimization problem (writing $$p$$ in terms of $$q_s$$)
>
> $$\begin{align}
p - 0.5q_s &= 0 \\
p &= 0.5q_s 
\end{align}$$
>
> Step 5. Solve the zero profit condition to find $$q_s$$
>
> $$\begin{align}
p_s q_s - 64 - 0.25q_s^2 &= 0 \\
(0.5q_s) q_s - 0.25q_s^2 &= 64 \\
0.5q_s^2 - 0.25q_s^2 &= 64 \\
0.25q_s^2 &= 64 \\
q_s^2 &= 256 \\
q_s &= 16
\end{align}$$
>
> Step 6. Plug $$q_s$$ into firm's first order condition to find $$p$$.
>
> $$\begin{align}
p &= 0.5q_s \\
&= 0.5(16) \\
&= 8
\end{align}$$
>
> Step 7. Plug $$p$$ into consumer's first order condition to find $$q_d$$.
>
> $$\begin{align}
q_d &= 10 - p \\
&= 10 - 8 \\
&= 2
\end{align}$$
>
> Step 8. Use $$Q = Nq_d$$ to get the total quantity.
>
> $$\begin{align}
Q &= N q_d \\
&= 3,200 (2) \\
&= 6,400
\end{align}$$
>
> Step 9. Use $$Q = Mq_s$$ to get the total number of firms.
>
> $$\begin{align}
Q &= M q_s \\
M &= \frac{Q}{q_s} \\
&= 6,400 / 16 \\
&= 400
\end{align}$$
>

So, prior to the demand shock, the long-run equilibrium price was $$p=8$$, total quantity was $$Q=6,400$$ and the number of firms was $$400$$.

## Short run after the demand shock

{: .green-callout-title }
> Answer to part 2
>
> $$\alpha$$ becomes $$9$$, but the number of firms stays the same. Solve the short-run equilibrium with $$\alpha=9$$ and $$M=400$$.
>
> Step 1. Write down the consumer's optimization problem.
>
> $$\begin{align}
\max_{q} ~ Y - pq + 9q - 0.5q^2
\end{align}$$
>
> Step 2. Solve the consumer's first order condition.
>
> $$\begin{align}
-p + 9 - q_d &= 0 \\
q_d &= 9 - p
\end{align}$$
>
> Step 3. Write down the firm's optimization problem.
>
> $$\begin{align}
\max_{q} ~ pq - 64 - 0.25q^2 
\end{align}$$
>
> Step 4. Solve the firm's first order condition.
>
> $$\begin{align}
p - 0.5q_s &= 0 \\
q_s &= 2p
\end{align}$$
>
> Step 5. Use the equilibrium condition to solve for $$p$$.
>
> $$\begin{align}
Nq_d &= Mq_s \\
3,200 (9 - p) &= 400(2p) \\
3,200 (9 - p) &= 800p \\
4(9 - p) &= p \\
36 - 4p &= p \\
5p &= 36 \\
p &= 7.2 
\end{align}$$
>
> Step 6. Use the firm's first order condition to solve for $$q_s$$.
>
> $$\begin{align}
q_s &= 2p \\
&= 2(7.2) \\
&= 14.4 
\end{align}$$
>
> Step 7. Use $$Q = Mq_s$$ to find the total quantity.
>
> $$\begin{align}
Q &= Mq_s \\
&= 400 (14.4) \\
&= 5,760
\end{align}$$
>
> Step 8. Plug $$q_s$$ and $$p$$ into the profit function to calculate firm profits.
>
> $$\begin{align}
\Pi &= pq_s - 64 - 0.25q_s^2 \\
&= (7.2)(14.4) - 64 - 0.25(7.2)^2 \\
&= -12.16
\end{align}$$

So, in the short run after the demand shock, price drops to $$p=7.2$$, total quantity falls to $$Q=5,760$$, and firms start to lose money, with losses equaling $$\Pi=-12.16$$ per firm.

## Long run after the demand shock

{: .yellow-callout-title }
> Answer to part 3
>
> In the long run, the number of firms can change. Solve the long run equilibrium when $$\alpha=9$$.
>
> If you follow the same steps as in part 1, you will arrive at the following answers:
>
> $$p=8$$, $$Q=3,200$$, $$M=200$$
>

So, in the long run after the demand shock, price goes back up to $$p=8$$, total quantity continues to fall until it hits $$Q=3,200$$, and the number of firms falls to $$M=200$$.

## Summary

Our findings are summarized in the table below:

|                                       | Price   | Total Quantity | Number of Firms | Firm Profit |
| Before negative demand shock          | $$8$$   | $$6,400$$      | $$400$$         | $$0$$       |
| Short run after negative demand shock | $$7.2$$ | $$5,760$$      | $$400$$         | $$-12.16$$  |
| Long run after negative demand shock  | $$8$$   | $$3,200$$      | $$200$$         | $$0$$       |

The example illustrates a concept we learned in Econ 160: that the long run equilibrium price of a competitive market is determined more by the production technology than by demand. This is because firms will enter or exit the market in response to a demand change, thus negating the price effect of the demand change.

{: .purple-callout-title }
> Economic Insight
>
> The long run equilibrium price of a competitive market is determined by its production technology, not by demand. This is because firms enter or exit the market in response to demand shocks, neutralizing the effect of demand on price.
