---
layout: default
title: "17. Monopolies"
parent: Lecture Notes
nav_order: 17
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

{: .purple-callout-title }
> Economic Insight
>
> If a market has extreme economies of scale or extreme network effects, economists will sometimes call that market a **natural monopoly**. They are called natural monopolies because these markets will gravitate towards a single supplier, even with unrestricted competition. 

- **Ownership of unique resources.** This happens when the monopolist is the only firm with access to the required input resources. An example would be a manufacturer of diamond rings who happens to control all the diamond mines, or a company with a secret technology that no one else has access to. 

- **Legal barriers to entry.** This happens when new entrants are legally prohibited from competing. Examples include firms with patents and copyrights. Patents and copyrights are legal tools designed to incentivize innovation by allowing inventors and creators to profit from intellectual or creative work that would otherwise be easy to copy and steal.


## General Setup

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

In Econ 160, you learned that monopolies cause deadweight loss because they choose prices which are above marginal cost. In the above example, we can easily see that at the profit maximizing quantity, price is equal to $$12$$ but the marginal cost is equal to $$6$$, which implies that total surplus is not maximized.

To see this more formally in the example, let us calculate the **efficient quantity** and the total profit and total utility at that quantity. The efficient quantity is defined as the quantity that would maximize the combined total profit plus utility.

{: .yellow-callout-title }
> Example 3
> 
> Using the setup from example 2, find the efficient quantity. Calculate price, total profit, and total utility at the efficient quantity. Then calculate deadweight loss, which is defined as the loss in total combined profit and utility due to monopolistic behavior.
>
> *Answer.*
>
> Step 1. Solve the consumer's problem to find the demand curve.
>
> We already did this in the previous example, and found that $$p = 18 - q$$.
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

## Regulating monopolies

Deadweight loss in monopolies comes from above marginal cost pricing. It would be socially efficient for the monopoly to lower price to marginal cost, but they don't do that because they can earn more profit by raising price above marginal cost. This gives us an idea for how to regulate monopolies: force them to charge price equal to their marginal cost. 

Unfortunately, this idea doesn't work well in practice. Remember that monopolies often arise out of situations with high fixed costs and low marginal costs. If you force such a company to price at marginal cost, they are likely to lose money due to their high fixed costs. Example 3 demonstrates one such example.

In reality, monopolies are regulated in a number of different ways:

- **Rate of return regulation.** Instead of forcing the monopolist to price at marginal cost, the government can restrict the monopolist's profit to its opportunity cost of capital. This would force its profits to be in line with how a competitive firm would behave. The downside to rate of return regulation is that it could stifle innovation and investment.

- **Antitrust laws.** These refer to laws that prevent monopolies from forming or can be used to break up existing monopolies. The goal of these laws is to ensure that markets remain competitive by preventing a single supplier from dominating. The downside of antitrust regulation is that it can prevent efficiency-enhancing mergers. (Recall that in the case of economies of scale, the larger firm is actually more efficient and can produce at lower cost.)

- **Public ownership/control.** This refers to a situation in which a monopoly is directly owned or controlled by a public entity. LADWP is one such example. It is owned by the City of Los Angeles and its board of directors is appointed by the Mayor.

Sometimes, a monopoly may not need to be regulated. Before determining whether or not a monopoly should be regulated by force of law, one should consider whether the regulations themselves give rise to corruption or other incentive problems within the government.  Moreover, one should understand that regulations can themselves be barriers to entry because they increase the fixed cost of compliance. 

Finally, it should be noted that monopolies can sometimes behave like competitive firms simply due to the *threat* of competition. For example, even though Amazon enjoys a dominant market position in e-commerce, the threat of competition from smaller online players like Walmart, Target, and Costco may keep its behavior in check.




