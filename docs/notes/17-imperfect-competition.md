---
layout: default
title: "17. Imperfect Competition"
parent: Lecture Notes
nav_order: 17
---

# Imperfect Competition
{: .no_toc }

- TOC
{:toc}

## Background Review

In models of perfect competition, we assumed that none of the firms had any influence over the market price. In models of monopoly, we assumed that a single firm has full control over the market price. The reality is usually somewhere in between. In most real world markets, firms have some influence over prices, but not complete control. We call models that sit in between perfect competition and monopoly models of **imperfect competition**.

Imperfect competition often results from markets that are **oligopolies**. An oligopoly describes a market that is dominated by a small number of firms. Because there is more than one firm, no single firm has complete control over market prices. But because the firms are large players in the market, each firm exerts some degree of influence over market pricing.

In an oligopoly, firms make decisions that are dependent on the actions taken by other firms. Game theory is therefore necessary to study the behavior of oligopolistic markets.

## Bertrand Model

### Setup

The **Bertrand Model** is a model of price competition between two oligopolistic firms.

The model has a simple setup. There are two identical firms that sell identical products. The firms both have a cost function:

$$c(q) = cq$$

So average cost and marginal cost are both constant and equal to $$c$$.

The two firms compete by setting price. If the two firms have the same price, they split the market demand evenly. If one firm has a lower price, the lower-priced firm gets all the demand and the higher-priced firm gets no demand.

Let $$Q_d(p)$$ describe the market demand curve.

If $$p_1 = p_2 = p$$ then:

$$\begin{align}
\Pi_1 &= \frac{1}{2} (p - c) Q_d(p) \\
\Pi_2 &= \frac{1}{2} (p - c) Q_d(p)
\end{align}$$

If $$p_1 < p_2$$ then:

$$\begin{align}
\Pi_1 &= (p_1 - c)Q_d(p_1) \\
\Pi_2 &= 0
\end{align}$$

Vice versa for $$p_2 < p_1$$.

This can be set up as a game where the players are firm 1 and firm 2, their choices are $$p_1$$ and $$p_2$$, and their payoff functions are the profit functions shown above.

### Nash equilibrium

We can prove that the only Nash equilibrium is where $$p_1 = p_2 = c$$. That is, the only Nash equilibrium is for both firms to price at marginal cost (and thus earn zero profit.)

We can prove this by showing that *no* Nash equilibrium can exist with a price above marginal cost.

Suppose $$p_{-i} > c$$. What is firm $$i$$'s best response?

To answer that, let's consider different possible of choices of $$p_i$$ as a response to $$p_{-i}$$:

- If $$p_i > p_{-i}$$, firm $$i$$ has no demand and makes zero profit.
- If $$p_i = p_{-i}$$, the firms split the demand and firm $$i$$ makes $$\Pi_i = \frac{1}{2} (p_{-i} - c) Q_d(p_{-i})$$.
- If $$p_i = p_{-i} - \epsilon$$, where $$\epsilon$$ is a small number (e.g. 1 cent), then firm $$i$$ gets the entire market and earns $$\Pi_i = (p_{-i} - \epsilon - c) Q_d(p_{-i} - \epsilon) \approx (p_{-i} - c)Q_d(p_{-i})$$.
 
From the above analysis, it's clear that the best response to firm $$-i$$ choosing price $$p_{-i}$$ is to simply undercut $$p_{-i}$$ by a little bit, like one cent.

If you undercut by just a little bit, you essentially double your profit because you end up capturing the entire market without having a meaningful change in the price you receive.

In other words, both firms have an incentive to keep undercutting each other until price is driven down to marginal cost.

This is akin to a Prisoner's Dilemma, where the firms could achieve higher profits if they cooperated on a high price, but each firm always has an incentive to undercut the other one.

{: .purple-callout-title }
> Economic Insight
>
> The Bertrand Model predicts that when firms compete on price, the competition will be so cutthroat that prices are driven down to marginal cost even if there are only two firms. 
>
> We do not observe this pattern in reality. So why isn't price competition as cutthroat in real life? A few reasons include:
>
> - Consumer search costs. It is costly for consumers to find the lowest priced option, so firms can maintain a price differential without losing all market share.
> - Capacity constraints. The lowest priced firm may not have the capacity to service the entire market, allowing for higher priced firms to retain market share.
> - Differentiated products. The Bertrand Model assumes that the firms are totally identical, *including* how long it takes consumers to buy from them. In reality, firms sell different products. Even if they sell the same product (e.g. gasoline), they are still differentiated on their geographic locations.

## Cournot Model

### General Setup

The **Cournot Model** is a model of quantity competition between two or more oligopolistic firms.  It can be used to model firms that compete on price but must first decide on capacity, since capacity choice is like choosing how much quantity you're willing and able to supply.

The general setup is like this:

Consumers in a market for commodity $$q$$ have a demand curve given by: 

$$Q_d = f(p)$$

where $$Q_d$$ is the total quantity demanded. This leads to an inverse demand curve:

$$ p = g(Q_d) $$

The market is supplied by $$N$$ firms. Each firm $$i$$ has a cost function given by $$c_i(q_i)$$, where $$q_i$$ is the total quantity produced by firm $$i$$.

Note that with these definitions, we can write total quantity:

$$Q_d = \sum_{i=1}^N q_i $$

and thus:

$$p = g(Q_d) = g\left( \sum_{i=1}^N q_i \right) $$

Although this looks complicated, it's nothing deep. It just says that the equilibrium price is determined by the total quantity chosen by all firms.

Each firm's profit function is therefore:

$$ \begin{align}
\Pi_i (q_i, q_{-i}) &= pq_i - c_i(q_i) \\
&= g\left( \sum_{j=1}^N q_j \right) q_i - c_i(q_i)
\end{align}$$

The firms simultaneously choose their own production quantity, $$q_i$$, taking each other firm's quantities, $$q_{-i}$$, as given.

### Nash equilibrium

In the Nash equilibrium, each firm chooses $$q_i$$ to maximize $$\Pi_i(q_i, q_{-i})$$, taking the $$q_{-i}$$ as given (i.e. they find their best response function.)

They find their optimal choice of $$q_i$$ by solving the first order condition:

$$ g^\prime\left( \sum_{j=1}^N q_j \right) q_i + g\left(\sum_{j=1}^N q_j\right) - c_i^\prime(q_i) = 0 $$

(This follows from the product rule and the chain rule.)

The equation above shows the first order condition for a firm $$i$$. Since there are $$N$$ firms we have $$N$$ first order conditions with $$N$$ unknowns. The unknowns are the quantities, $$q_1$$ through $$q_N$$. We can solve the system of equations to find the Nash equilibrium.

{: .blue-callout-title }
> Example
>
> Consumers in a market for commodity $$q$$ have a demand curve given by:
>
> $$Q_d = 18 - p$$
>
> The market is supplied by two firms. The cost function of firm 1 is:
>
> $$ c_1(q_1) = 3q_1 $$
>
> The cost function of firm 2 is:
>
> $$ c_2(q_2) = 3q_2 $$
>
> The firms engage in Cournot competition. 
>
> 1. Find the quantities chosen by each firm in the Nash equilibrium.
> 2. Find the price in the Nash equilibrium.
> 3. Calculate the profit of each firm in the Nash equilibrium.
>
> *Answer.*
>
> Step 1. Write down the inverse demand curve. (Solve for $$p$$ as a function of $$Q_d$$.)
>
> $$\begin{align}
Q_d &= 18 - p \\
p &= 18 - Q_d
\end{align}$$
>
> Step 2. Write down the profit of each firm, as a function of $$q_1$$ and $$q_2$$.
>
> $$\begin{align}
\Pi_1(q_1, q_2) &= pq_1 - 3q_1 \\
                &= (18 - Q_d) q_1 - 3q_1 \\
				&= (18 - q_1 - q_2) q_1 - 3q_1 \\
				&= 18q_1 - q_1^2 - q_2 q_1 - 3q_1 \\
				&= 15q_1 - q_1^2 - q_2 q_1
\end{align}$$
>
> Repeating the procedure for firm 2 we get:
>
> $$\begin{align}
\Pi_2(q_1,q_2) = 15q_2 - q_2^2 - q_1 q_2 
\end{align}$$
> 
> Step 3. Write down the first order conditions for each firm.
>
> $$\begin{align}
FOC[q_1]: 15 - 2q_1 - q_2 &= 0 \\
FOC[q_2]: 15 - q_1 - 2q_2 &= 0
\end{align}$$
>
> For mathematical convenience, it will be useful to put $$q_1$$ and $$q_2$$ on the other side of the equation so that they're positive:
>
> $$\begin{align}
2q_1 + q_2 &= 15 \\
q_1 + 2q_2 &= 15
\end{align}$$
>
> Step 4. Solve the system of equations using any technique. I prefer the [elimination method](https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:systems-of-equations/x2f8bb11595b61c86:solving-systems-elimination/a/elimination-method-review){:target="_blank"}.
>
> $$\begin{align}
  2( 2q_1 + q_2 ) &= 2(15) \\
-     (q_1 + 2q_2) &= -15
\end{align}$$
>
> $$\begin{align}
  (  4q_1 + 2q_2 ) &= 30 \\
-     (q_1 + 2q_2) &= -15
\end{align}$$
>
> $$\begin{align}
3q_1 &= 15 \\
q_1 &= 5
\end{align}$$
>
> To get $$q_2$$, we can plug $$q_1=5$$ into any of the first order conditions. We get $$q_2 = 5$$.
> 
> The total quantity is therefore $$Q_d = 10$$, and price is $$p = 18 - Q_d = 8$$.
>
> The profit of either firm is:
>
> $$\begin{align}
\Pi_i &= pq_i - 3q_i \\
      &= (8)(5) - 3(5) \\
      &= 25
\end{align}$$

{: .green-callout-title }
> Example
>
> Consumers in a market for commodity $$q$$ have a demand curve given by:
>
> $$Q_d = A - p$$
>
> The market is supplied by $$N$$ *identical* firms. The cost function of each firm is:
>
> $$c_i(q_i) = cq_i$$
>
> where $$c$$ is a constant number. (The firms thus have constant average and marginal costs.)
>
> The firms engage in Cournot competition.
>
> 1. Derive a formula for the Nash equilibrium quantity of a single firm $$q_i$$.
> 2. Derive a formula for the Nash equilibrium price in the market.
> 3. Show that as $$N$$ gets very large, the Nash equilibrium price approaches the marginal cost $$c$$.
>
> *Answer.*
>
> Step 1. Write down the inverse demand curve.
>
> $$\begin{align}
p &= A - Q_d \\
&= A - \sum_{i=1}^N q_i
\end{align}$$
>
> Step 2. Write down the profit function of each firm.
>
> $$\begin{align}
\Pi_i (q_i, q_{-i}) &= p q_i - cq_i \\
&= (p - c) q_i \\
&= \left(A - \sum_{j=1}^N q_j - c\right) q_i \\
&= \left(A -c - q_i - \sum_{j \neq i} q_j \right) q_i \\
&= (A - c)q_i - q_i^2 - \left(\sum_{j \neq i } q_j \right) q_i 
\end{align}$$
>
> Step 3. Write down the first order condition for firm $$i$$.
>
> $$\begin{align}
FOC[q_i]: (A-c) - 2q_i - \left(\sum_{j \neq i} q_j \right) &= 0
\end{align}$$
>
> Step 4. Take advantage of the fact that the firms are identical. The Nash equilibrium must be symmetric. Thus, let $$q_i = q^\ast$$ for all $$i$$. Plugging that into the first order condition gives us:
>
> $$\begin{align}
(A-c) - 2q^\ast - \left(\sum_{j \neq i} q^\ast \right) &= 0 \\
(A-c) - 2q^\ast - (N-1)q^\ast &= 0 \\
(A-c) &= 2q^\ast + (N-1)q^\ast \\
(A-c) &= (N+1) q^\ast \\
q^\ast &= \frac{A-c}{N+1} 
\end{align}$$
>
> This answers part 1 of the question.
>
> Step 5. Calculate the total quantity.
>
> $$Q_d = Nq^\ast = \frac{N}{N+1} (A - c) $$
>
> Step 6. Use the inverse demand curve to find the equilibrium price.
>
> $$\begin{align}
p &= A - Q_d \\
&= A - \frac{N}{N+1}(A - c) \\
&= \left(1 - \frac{N}{N+1}\right)A + \frac{N}{N+1} c \\
&= \frac{1}{N+1} A + \frac{N}{N+1} c 
\end{align}$$
>
> As $$N$$ gets very large, $$\frac{1}{N+1}$$ approaches zero and $$\frac{N}{N+1}$$ approaches $$1$$. So the equilibrium price approaches $$c$$, the marginal cost of production.

{: .purple-callout-title}
> Economic Insight
>
> The Cournot Model encapsulates both monopoly and perfect competition. If $$N=1$$, the Nash equilibrium of the Cournot Model is the same as the market outcome for a profit-maximizing monopolist. Moreover, as $$N \rightarrow \infty$$, the Nash equilibrium price approaches marginal cost, which is what would result from perfect competition.









