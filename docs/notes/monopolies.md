---
layout: default
title: "14. Monopolies"
parent: Lecture Notes
nav_order: 14
---

# Monopolies
{: .no_toc }

- TOC
{:toc}

## Background Review

A monopoly is a firm that is the only supplier in a market. We call the firm a monopolist or a monopoly, and we say that the market is "monopolized". 

Monopolies arise due to **barriers to entry**. A barrier to entry is anything that makes it difficult or impossible for a new entrant to compete profitably with the incumbent monopolist.

Examples of barriers to entry icnlude:

- **Extreme economies of scale.** This happens when there are very large fixed costs but low marginal costs. Thus, average total cost is declining with firm size. When there are extreme economies of scale, the largest firm can supply the product at a lower average cost than any new entrant. This makes it difficult for new entrants to compete profitably. Water, power, cable, and software are all examples of industries with large fixed costs and low marginal costs, and thus prone to monopolization because of extreme economies of scale.

- **Extreme network effects.** This happens when the product becomes more valuable when the user base gets larger. Examples include two-sided online marketplaces, like YouTube and Uber, and social networks like Facebook. When there are extreme network effects, the largest firm has a more valuable product than any new entrant. This makes it difficult for new entrants to compete profitably.

- **Ownership of unique resources.** This happens when the monopolist is the only firm with access to the required input resources. An example would be a manufacturer of diamond rings who happens to control all the diamond mines, or a company with a secret technology that no one else has access to. 

- **Legal barriers to entry.** This happens when new entrants are legally prohibited from competing. Examples include firms with patents and copyrights. Patents and copyrights are legal tools designed to incentivize innovation by allowing inventors and creators to profit from intellectual or creative work that would otherwise be easy to copy and steal.

{: .purple-callout-title }
> Economic Insight
>
> If a market has extreme economies of scale or extreme network effects, economists will sometimes call that market a **natural monopoly**. They are called natural monopolies because these markets will gravitate towards a single supplier, even with unrestricted competition. 


## Monopoly Profit Maximization

The key difference between a monopolist and a competitive firm is that the monopolist is not a price-taker.  Instead, the monopolist can choose to produce any level of output $$q$$ at any price $$p$$, so long as the price and quantity obey the demand curve.

Thus, the monopolist's optimization problem is:

$$ \max_{p,q} ~ pq - c(q) ~ \text{ s.t. } ~ q = f(p) $$

where $$c(q)$$ is the firm's cost function and $$f(p)$$ is the market demand curve.

{: .blue-callout-title }
> Example 1
>
> A commodity $$q$$ is supplied by a monopolist with cost function:
>
> $$c(q) = \frac{1}{2} q^2 $$
>
> The monopolist faces a market demand curve given by:
>
> $$ Q_d = 12 - p $$
>
> Find the profit maximizing price and quantity. What is the maximum profit?
>
> *Answer.*
>
> Step 1. Write down the optimization problem:
>
> $$ \max_{p,q} ~ pq - \frac{1}{2}q^2 \text{ s.t. } q = 12 - p $$
>
> Step 2. Plug $$p = 12 - q$$ into $$p$$ in the objective function:
>
> $$\begin{align}
& \max_{q} ~ (12 - q)q - \frac{1}{2}q^2  \\
= & \max_{q} ~ 12q - q^2 - \frac{1}{2} q^2 \\
= & \max_{q} ~ 12q - \frac{3}{2} q^2 
\end{align}$$
>
> Step 3. Write down the first order condition and find the profit maximizing quantity.
>
> $$\begin{align}
12 - 3q &= 0 \\
3q &= 12 \\
q &= 4
\end{align}$$
>
> Step 4. Plug the profit maximizing quantity into the demand curve to find the profit maximizing price.
>
> $$\begin{align}
p &= 12 - q \\
&= 12 - 4 \\
&= 8
\end{align}$$
>
> Step 5. Plug $$p$$ and $$q$$ into the profit function to calculate profit.
>
> $$\begin{align}
\Pi &= pq - \frac{1}{2}q^2 \\
&= (8)(4) - \frac{1}{2} (4)^2 \\
&= 24
\end{align}$$

## General Setup

We will use the following general setup with quasilinear utility to analyze monopolies. 

{: .purple-callout-title }
> Note
>
> For simplicity, instead of modeling $$N$$ consumers like we did before, we will let the market demand be modeled by a single representative consumer.

### Setup

A commodity $$q$$ is supplied by a monopolist with cost function $$c(q)$$.

A representative consumer with income $$Y$$ has utility function over numeraire consumption $$c$$ and the commodity $$q$$ given by:

$$ u(c,q) = c + v(q) $$

$$v(q)$$ is such that $$v^\prime(q)>0$$ and $$v^{\prime\prime}(q)<0$$. 


### Consumer's Problem

The consumer solves:

$$ \max_{c,q} ~ c + v(q) ~ \text{s.t.} ~ c = Y - pq $$

The first order condition for the consumer is:

$$ p = v^\prime(q) $$

This equation defines the supply curve and must hold in any equilibrium of the model.

### Monopolist's Problem

The monopolist solves:

$$ \max_{p,q} ~ pq - c(q) ~ \text{s.t.} ~ p = v^\prime(q) $$

The objective function is simply profit. The constraint says that the relationship between price and quantity must obey the demand curve which was derived from the consumer's optimization problem.

The monopolist's optimization problem becomes:

$$ \max_{q} ~ v^\prime(q) q - c(q) $$

And the first order condition for the monopolist is:

$$ v^{\prime \prime} (q) q + v^\prime(q) - c^\prime(q) = 0 $$

This follows from the **chain rule**. Reminder: if $$f(x) = g(x)h(x)$$ then $$f^\prime(x) = g^\prime(x) h(x) + g(x) h^\prime(x) $$.

The monopolist's first order condition gives us one equation in one unknown, which we can use to solve for $$q$$.  The consumer's first order condition (i.e. the demand curve) will then tell us the price that allows the monopolist to sell $$q$$ units.

{: .green-callout-title }
> Example 2
>
> A commodity $$q$$ is supplied by a monopolist with cost function:
>
> $$ c(q) = 48 + \frac{1}{2} q^2 $$
>
> A representative consumer with income $$Y = 100$$ has utility function over numeraire consumption $$c$$ and the commodity $$q$$ given by:
>
> $$ u(c,q) = c + 18q - \frac{1}{2} q^2 $$
>
> Find the profit maximizing price and quantity. Calculate total profit and total consumer utility at that point.
>
> *Answer.*
>
> Step 1. Solve the consumer's problem to find the demand curve.  
> (*Hint: When solving monopoly problems, it's easier to write the demand curve in terms of $$p$$ as a function of $$q$$.*)
>
> Set up the consumer's problem:
> 
> $$\begin{align}
& \max_{c,q} ~ c + 18q - \frac{1}{2}q^2 ~ \text{ s.t. } ~ c = 100 - pq \\
= & \max_{q} ~ 100 - pq + 18q - \frac{1}{2}q^2 
\end{align}$$
> 
> Solve the first order condition to get the demand curve:
>
> $$\begin{align}
 -p + 18 - q &= 0 \\
p &= 18 - q ~ 
\end{align}$$
>
> Step 2. Write down the firm's problem and plug $$p = 18 - q$$ in for $$p$$.
>
> $$\begin{align}
& \max_{c,q} ~ pq - 48 - \frac{1}{2}q^2 ~ \text{ s.t. } ~ p = 18 - q \\
= & \max_{q} ~ (18 - q)q - 48 - \frac{1}{2}q^2 \\
= & \max_{q} ~ 18q - q^2 - 48 - \frac{1}{2}q^2 \\
= & \max_{q} ~ 18q - \frac{3}{2} q^2 - 48
\end{align}$$
>
> Step 3. Solve the first order condition for $$q$$.
>
> $$\begin{align}
18 - 3q &= 0 \\
3q &= 18 \\
q &= 6
\end{align}$$
>
> Step 4. Plug $$q$$ into the demand curve to get $$p$$.
>
> $$ p = 18 - q = 18 - 6 = 12 $$
>
> Step 5. Plug $$p$$ and $$q$$ into the profit function and utility function to get profit and total utility. 
>
> $$\begin{align}
\Pi &= pq - 48 - \frac{1}{2} q^2 \\
&= (12)(6) - 48 - \frac{1}{2} (6)^2 \\
&= 6 \\
U &= 100 - pq + 18q - \frac{1}{2}q^2 \\
&= 100 - (12)(6) + 18(6) - \frac{1}{2}(6)^2 \\
&= 118
\end{align}$$

## Monopolies and deadweight loss

If we rearrange the monopolist's first order condition, we get:

$$ v^\prime(q) = c^\prime(q) - v^{\prime \prime}(q) q $$

Now, we make use of three facts:

1. $$v^\prime(q)$$ is the marginal benefit of the consumer from consuming commodity $$q$$.

2. $$c^\prime(q)$$ is the marginal cost of the firm in producing commodity $$q$$.

3. $$v^{\prime \prime} (q)$$ is always negative.

This implies that:

$$ \text{Marginal benefit of consumers} = \text{Marginal cost of producers} - \text{Negative number} $$

Or:

$$ \text{Marginal benefit of consumers} = \text{Marginal cost of producers} + \text{Positive number} $$

And thus:

$$ \text{Marginal benefit of consumers} > \text{Marginal cost of producers}$$

In other words, consumer marginal benefit exceeds firm marginal cost at the profit-maximizing choice of the monopolist.

This means that the producer could produce 1 more unit, and this unit would benefit the next consumer more than it would cost the firm to produce. This is an **inefficiency**. Total surplus is **not** maximized.

But why wouldn't the firm be willing to produce the next unit if the next consumer is willing to pay more than the cost for it?

- *Answer*: Because the firm cannot charge different prices to different consumers. If it lowers the price for this one consumer it would have to lower price for all consumers. That would lower the firm's profit.

{: .purple-callout-title }
> Economic Insight
>
> Monopoly profit maximization leads to socially inefficient outcomes. In particular, the quantity traded will be less than the efficient amount, and the price will be higher than marginal cost. The monopoly is not willing to lower price because this would lower its profits.

{: .yellow-callout-title }
> Example 3
>
> Return to the setup from example 2. Calculate the monopolist's marginal cost at the profit maximizing quantity and calculate the consumer's marginal benefit, $$v^\prime(q)$$. Show that the marginal benefit is greater than the marginal cost.
>
> *Answer*.
>
> Firm's marginal cost:
>
> $$\begin{align}
c(q) &= 48 + \frac{1}{2} q^2 \\
c^\prime(q) &= q
\end{align}$$
>
> $$q=6$$, so $$c^\prime(6) = 6$$. The marginal cost of the firm at $$q=6$$ is $$6$$.
>
> Consumer's marginal benefit:
>
> $$\begin{align}
v(q) &= 18q - \frac{1}{2} q^2 \\
v^\prime(q) &= 18 - q 
\end{align}$$
>
> $$q=6$$, so $$v^\prime(q) = 12$$. The consumer's marginal benefit at $$q=6$$ is $$12$$, which is greater than the firm's marginal cost.



{: .blue-callout-title }
> Example 4
> 
> Using the setup from example 2, find the efficient quantity. Calculate price, total profit, and total utility at the efficient quantity. Then calculate deadweight loss, which is defined as the loss in total combined profit and utility due to monopolistic behavior.
>
> *Answer.*
>
> Step 1. Solve the consumer's problem to find the demand curve.
>
> We already did this in the example 2, and found that $$p = 18 - q$$.
>
> Step 2. Write down the optimization problem for maximizing combined profit and utility.
>
> $$\begin{align}
& \max_{q} ~ U + \Pi \\
= & \max_{q} ~ (100 - pq + 18q - \frac{1}{2}q^2) + (pq - 48 - \frac{1}{2}q^2) \\
= & \max_{q} ~ 52 + 18q - q^2
\end{align}$$
>
> *(Notice how the resulting objective function doesn't depend on price. Price only causes a transfer of surplus from consumer to producer, but doesn't influence total surplus.)*
>
> Step 3. Write down the first order condition and solve for the efficient quantity.
>
> $$\begin{align}
18 - 2q &= 0 \\
2q &= 18 \\
q &= 9
\end{align}$$
>
> Step 4. Use the demand curve to find the price at the efficient quantity.
>
> $$ p = 18 - q = 9 $$
>
> Step 5. Plug price and quantity into the profit and utility functions to get profit and utility at the efficient quantity. We get:
>
> $$\begin{align}
\Pi &= -7.5 \\
U &= 140.5
\end{align}$$
>
> Step 6. Compare the surpluses under the profit-maximizing quantity versus the efficient quantity.
>
> |         | Profit-Maximizing | Efficient |
> | $$q$$   | $$6$$             | $$9$$     |
> | $$p$$   | $$12$$            | $$9$$     |
> | $$\Pi$$ | $$6$$             | $$-7.5$$  |
> | $$U$$   | $$118$$           | $$140.5$$ |
> | $$TS$$  | $$124$$           | $$133$$   |
> | $$DWL$$ | $$9$$             |           |


The example above shows that the efficient outcome may actually result in negative profits for the monopolist. This is especially true when the monopolist has very high fixed costs but very low marginal costs, which would be the case in monopolies with extreme economies of scale. That's because the efficient outcome involves charging $$\text{Price} = \text{Marginal cost}$$, which results in a price that's too low for the firm to recover its fixed costs.

{: .purple-callout-title }
> Economic Insight
>
> Forcing a firm to price at marginal cost, especially when fixed costs are high and marginal costs are low, can result in the firm losing money.


## Regulating monopolies

Monopolies result in deadweight loss due to above-marginal-cost pricing and a purposeful withholding of supply from the market.

This suggests that governments can step in to regulate monopolists and **potentially** improve outcomes.

One idea would be to simply force monopolists to price at marginal cost. Unfortunately, this idea is not practical for a few reasons:

1. As we saw above, this could result in the firm losing money. Governments cannot force firms to lose money indefinitely, because eventually they will simply choose to stop operating.

2. Even if the firm could make a profit while pricing at marginal cost, regulating firms in this way would require the government to actually know the cost structure of the firm. This is a difficult and potentially costly task.

3. If the government were to force a firm to price at marginal cost, then the firm would have very little incentive to invest in lowering its costs, since that would also force it to lower its prices. This kind of regulation could therefore stifle innovation. 

4. The firm could also choose to lie about its marginal costs.

{: .purple-callout-title }
> Economic Insight
>
> The four criticisms above apply not just to monopolists, but any firm that has some degree of pricing power (which in reality, is most firms.) Thus, it applies to price gouging rules that were recently touted by Kamala Harris's campaign. The four points above explain why economists generally do not favor price controls or price gouging legislation.

If price controls are not effective, then how are monopolists actually regulated? In reality, monopolies are regulated in a number of different ways:

- **Rate of return regulation.** Instead of forcing the monopolist to price at marginal cost, the government can restrict the monopolist's profit to its opportunity cost of capital. This would force its profits to be in line with how a competitive firm would behave. The downside to rate of return regulation is that it could stifle innovation and investment.

- **Antitrust laws.** These refer to laws that prevent monopolies from forming or can be used to break up existing monopolies. The goal of these laws is to ensure that markets remain competitive by preventing a single supplier from dominating. The downside of antitrust regulation is that it can prevent efficiency-enhancing mergers. (Recall that in the case of economies of scale, the larger firm is actually more efficient and can produce at lower cost.)

- **Public ownership/control.** This refers to a situation in which a monopoly is directly owned or controlled by a public entity. LADWP is one such example. It is owned by the City of Los Angeles and its board of directors is appointed by the Mayor. The downside of public ownership is that there is no guarantee that a non-profit public entity would behave more efficiently than a for-profit private one.

Sometimes, a monopoly may not need to be regulated. Before determining whether or not a monopoly should be regulated by force of law, one should consider whether the regulations themselves give rise to corruption or other incentive problems within the government.  Moreover, one should understand that regulations can themselves be barriers to entry because they increase the fixed cost of compliance. 

Finally, it should be noted that monopolies can sometimes behave like competitive firms simply due to the *threat* of competition. For example, even though Amazon enjoys a dominant market position in e-commerce, the threat of competition from smaller online players like Walmart, Target, and Costco may keep its behavior in check.




