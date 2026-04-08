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

where $$c(q)$$ is the firm's cost function and $$f(p)$$ is the market demand curve. The optimization problem says the monopolist chooses $$p$$ and $$q$$ to maximize profit, subject to the constraint that $$q$$ and $$p$$ are related by the consumer demand curve.  In other words, the monopolist is constrained by consumer behavior.

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

The previous setup assumes that we know the demand curve already. A more foundational model would derive the demand curve from the consumer's optimization problem. We will use the following general setup to analyze monopolies. 

### Setup

A representative, price-taking consumer decides how many units $$q$$ of a commodity to purchase at unit price $$p$$. The utility they receive for purchasing $$q$$ units at price $$p$$ is:

$$ u(q) = v(q) - pq$$

The market is supplied by a single monopolist, who can produce $$q$$ units of the commodity at a total cost of $$c(q)$$.

### Consumer's Problem

The consumer solves:

$$ \max_{q} ~ v(q) - pq $$

The first order condition for the consumer is:

$$ p = v^\prime(q) ~ ~ ~ ~ (1) $$

This equation defines the inverse demand curve, and it describes the behavior of consumers in the model.

### Monopolist's Problem

The monopolist solves:

$$ \max_{p,q} ~ pq - c(q) ~ \text{s.t.} ~ p = v^\prime(q) $$

This says that the monopolist chooses $$p$$ and $$q$$ subject to the constraint that $$p$$ and $$q$$ are related by consumer demand. 

If we plug $$p = v^\prime(q)$$ into the optimization problem, it simplifes to:

$$ \max_{q} ~ v^\prime(q) q - c(q) $$

And the first order condition for the monopolist is:

$$ v^{\prime \prime} (q) q + v^\prime(q) - c^\prime(q) = 0  ~ ~ ~ ~ (2) $$

This follows from the **product rule**. Reminder: if $$f(x) = g(x)h(x)$$ then $$f^\prime(x) = g^\prime(x) h(x) + g(x) h^\prime(x) $$.

The monopolist's first order condition gives us one equation in one unknown, which we can use to solve for $$q$$.  The consumer's first order condition (i.e. the demand curve) will then tell us the price that allows the monopolist to sell $$q$$ units.

### Proof of deadweight loss

From the two first order conditions, we can derive an important fact about monopoly behavior, which is that they will always set a price which is higher than the marginal cost, and that this results in deadweight loss.

We can re-arrange the monopolist's first order condition (equation 2) as follows:

$$ v^\prime(q) = c^\prime(q) - v^{\prime \prime} (q) q $$

Now, we make note of the fact that $$v^{\prime \prime} (q)$$ is negative.  It's negative because $$v(q)$$ is a *concave* function. A concave function is one that has diminishing returns: as the consumer consumes more of $$q$$, the marginal benefit they get from consuming an additional unit declines. 

Since $$v^{\prime \prime}(q)$$ is negative, we have:

$$\begin{align}
v^\prime(q) &= c^\prime(q) - \text{negative number} \\
\Rightarrow v^\prime(q) &= c^\prime(q) + \text{positive number} \\
\Rightarrow v^\prime(q) &> c^\prime(q)
\end{align}$$

Further more, note that $$v^\prime(q)$$ is the consumer's marginal benefit function ($$MB$$) and that $$c^\prime(q)$$ is the firm's marginal cost function $$MC$$.  Also note that $$p = v^\prime(q)$$.  Taken together, these facts imply that under a monopoly: $$p > MC$$ and $$MB > MC$$. That is, the monopolist will choose a **price higher than marginal cost**, and that this leads $$MB > MC$$, which is an inefficient outcome because total surplus is maximized when $$MB = MC$$.

{: .purple-callout-title }
> Economic Insight
>
> Monopoly profit maximization leads to socially inefficient outcomes. In particular, the quantity traded will be less than the efficient amount, and the price will be higher than marginal cost. The monopoly is not willing to lower price because this would lower its profits.



{: .green-callout-title }
> Example 2
>
> A representative, price-taking consumer decides how many units $$q$$ of a commodity to purchase at unit price $$p$$. The utility they receive for purchasing $q$$ units at price $$p$$ is:
> 
> $$ u(q) = 18q - \frac{1}{2}q^2 - pq$$
> 
> The market is supplied by a single monopolist, who can produce $$q$$ units of the commodity at a total cost of $$c(q) = \frac{1}{2} q^2$$.
> 
> Find the profit maximizing price and quantity chosen by the monopolist. Calculate the total profit and total consumer utility. Also calculate total surplus, which we define as firm profit plus consumer utility.
>
> *Answer.*
>
> **Step 1. Solve the consumer's optimization problem to get the inverse demand curve.**
>
> $$\max_{q} ~ 18q - \frac{1}{2}q^2 - pq$$
>
> $$\begin{align}
\text{FOC: } & 18 - q - p = 0 \\
& p = 18 - q
\end{align}$$
>
> **Step 2. Write down the firm's optimization problem and simplify it.**
>
> $$\max_{p,q} ~ pq - \frac{1}{2}q^2 ~ \text{ s.t. } ~ p = 18 - q$$
>
> Which simplifies to:
>
> $$\begin{align}
& \max_{q} ~ (18-q)q - \frac{1}{2}q^2 \\
= & \max_{q} ~ 18q - q^2 - \frac{1}{2}q^2 \\
= & \max_{q} ~ 18q - \frac{3}{2} q^2 
\end{align}$$
>
> **Step 3. Solve the firm's optimization problem to get $$q$$.**
>
> $$\begin{align}
\text{FOC}[q]: ~ & 18 - 3q = 0 \\
& q = 6
\end{align}$$
>
> **Step 4. Plug $$q$$ into the inverse demand curve to get $$p$$.**
>
> $$\begin{align}
p &= 18 - q \\
p &= 12
\end{align}$$
>
> **Step 5. Plug $$p$$ and $$q$$ into the profit and consumer utility functions to get profit and utility.**
>
> $$\begin{align}
\Pi &= pq - \frac{1}{2}q^2 \\
    &= 12(6) - \frac{1}{2}(6)^2 \\
	&= 54 \\
U &= 18q - \frac{1}{2}q^2 - pq \\
  &= 18(6) - \frac{1}{2}(6)^2 - 12(6) \\
  &= 18 \\
TS &= \Pi + U \\
   &= 54 + 18 \\
   &= 72
\end{align}$$


## Benevolent Social Planner

Now let's ask what a **benevolent social planner** would do. The "benevolent social planner" is a hypothetical entity that can tell the firm how to behave, and seeks to maximize total surplus (that is, total firm profit plus total consumer utility).

{: .red-callout-title}
> Warning
>
> A benevolent social planner is **not** the same thing as the government. Government officials cannot be assumed to be fully benevolent or seeking to maximize total surplus. Rather, government officials are individuals who have their own personal incentives and who seek to maximize their own personal utility. A smart political system will try to align government officials' incentives with total surplus, but no political system can perfectly do this.
>
> Instead, you should think of the benevolent social planner is an analytical tool to help us think through what the optimal social outcome would be, without necessarily having a way to realistically achieve it.

The benevolent social planner seeks to maximize total firm profit plus total consumer utility:

$$ \max_{p, q} ~ \Pi + U $$

Which, in our setup, is equivalent to:

$$ \max_{p, q} ~ ( pq - c(q) ) + ( v(q) - pq) $$

Notice that the $$pq$$'s cancel out, resulting in a simplified maximization problem:

$$ \max_{q} ~ v(q) - c(q) $$

The first order condition of this maximization problem is:

$$ v^\prime(q) - c^\prime(q) = 0$$

Or, rearranging:

$$ v^\prime(q) = c^\prime(q) $$

In other words, the benevolent social planner chooses the outcome where marginal benefit equals marginal cost!  Which, based on optimization theory, is exactly what we'd expect for someone seeking to maximize total surplus.

{: .purple-callout-title }
> Economic Insight
>
> A benevolent social planner who seeks to maximize total surplus (total firm profit plus total consumer utility) would choose the quantity of output where the consumer's marginal benefit equals the firm's marginal cost. This is essentially what would have happened under a competitive market; but it's not what happens under a monopoly.

An interesting observation is that the $$pq$$'s cancel out of the social planner's optimization problem.  $$pq$$ is the firm's revenue and the consumer's cost. It represents a transfer of surplus from the consumer to the firm.  Since the social planner only cares about the total surplus, and not necessarily how it's distributed between consumer and firm, the actual value of $$pq$$ doesn't matter for the social planner's objective function.


{: .yellow-callout-title }
> Example 3
>
> Return to the setup from Example 2. Solve the benevolent social planner's problem and compare it to the outcomes under monopoly.
>
> *Answer*.
>
> **Step 1. Write down the social planner's problem.**
>
> $$ \max_{p,q} ~ (pq - \frac{1}{2}q^2) + (18q - \frac{1}{2}q^2 - pq) $$ 
>
> which simplifies to:
>
> $$ \max_{q} 18q - q^2 $$
>
> **Step 2. Solve the social planner's problem to get $$q$$.**
>
> $$\begin{align}
\text{FOC}[q]: ~ & 18 - 2q = 0 \\
& q = 9
\end{align}$$
>
> **Step 3. Plug $$q$$ into the consumer's inverse demand curve to get $$p$$.**
>
> Note that we already derived, in Example 2, that the inverse demand curve is $$p = 18-q$$.  Thus, $$p = 9$$.
>
> **Step 4. Plug $$p$$ and $$q$$ into the profit function and utility functions to get firm profit and consumer utility.**
>
> $$\begin{align}
\Pi &= pq - \frac{1}{2}q^2 \\
    &= 9(9) - \frac{1}{2}(9)^2 \\
	&= 40.5 \\
U &= 18q - \frac{1}{2}q^2 - pq \\
  &= 18(9) - \frac{1}{2}(9)^2 - 9(9) \\
  &= 40.5 \\
TS &= \Pi + U \\
   &= 40.5 + 40.5 \\
   &= 81
\end{align}$$
>
> **Step 5. Make a table comparing the outcomes under monopoly to the outcomes under the social planner.
>
> |   | Monopoly | Social Planner | 
> | - | -------- | -------------- |
> | $$p$$ | 12 | 9 |
> | $$q$$ | 6 | 9 |
> | $$\Pi$$ | 54 | 40.5 |
> | $$U$$ | 18 | 40.5 |
> | $$TS$$ | 72 | 81 |
>
> Thus, the total surplus under monopoly is $$9$$ less than the total surplus under the social planner. We say that the monopolist creates a **deadweight loss** of 9. 


## Regulating monopolies

Monopolies result in deadweight loss due to above-marginal-cost pricing and a purposeful withholding of supply from the market.

This suggests that governments can step in to regulate monopolists and **potentially** improve outcomes.

One idea would be to simply force monopolists to price at marginal cost. Unfortunately, this idea is not practical for a few reasons:

1. This can actually result in the firm losing money, especially if the monopoly is due to high fixed costs. Forcing a high fixed-cost monopolist to charge a very low marginal cost can make it so that they can't recuperate their fixed cost. The government can try to force a firm to set low prices, but they can't force a firm to stay in business. So if the government tries to artificially restrict prices too much, the firm may simply stop operating.

2. Even if the firm could make a profit while pricing at marginal cost, regulating firms in this way would require the government to actually know the cost structure of the firm. This is a difficult and potentially costly task.

3. If the government were to force a firm to price at marginal cost, then the firm would have very little incentive to invest in lowering its costs, since that would also force it to lower its prices. This kind of regulation could therefore stifle innovation. 

4. The firm could also choose to lie about its marginal costs.

{: .purple-callout-title }
> Economic Insight
>
> The four criticisms above apply not just to monopolists, but any firm that has some degree of pricing power (which in reality, is most firms.) Thus, it applies to price gouging rules that were recently touted by Kamala Harris's campaign. The four points above explain why economists generally do not favor price controls or price gouging legislation.

If price controls are not effective, then how are monopolists actually regulated? In reality, monopolies are regulated in a number of different ways:

- **Rate of return regulation.** Instead of forcing the monopolist to price at marginal cost, the government can restrict the monopolist's profit to its opportunity cost of capital. This would force its profits to be in line with how a competitive firm would behave. The downside to this kind of regulation is that it still stifles innovation and investment, because the monopolist has little incentive to invest in more efficient production.

- **Antitrust laws.** These refer to laws that prevent monopolies from forming in the first place, or that allow the government to break up existing monopolies. The goal of these laws is to ensure that markets remain competitive by preventing a single supplier from dominating. The downside of antitrust regulation is that it can prevent efficiency-enhancing mergers. (Recall that in the case of economies of scale, the larger firm is actually more efficient and can produce at lower cost.)

- **Public ownership/control.** This refers to a situation in which a monopoly is directly owned or controlled by a public entity. LADWP is one such example. Although it is a private entity, its board of directors is appointed by the Mayor, and thus the city exerts some direct control over it. The downside of public ownership/control is that there is no guarantee that a non-profit public entity would behave more efficiently than a for-profit private one.

Sometimes, a monopoly may not need to be regulated. Before determining whether or not a monopoly should be regulated by force of law, one should consider whether the regulations themselves give rise to corruption or other incentive problems within the government.  Moreover, one should understand that regulations can themselves be barriers to entry because they increase the fixed cost of compliance. 

Finally, it should be noted that monopolies can sometimes behave like competitive firms simply due to the *threat* of competition. For example, even though Amazon enjoys a dominant market position in e-commerce, the threat of competition from other players like Walmart, Target, and Costco may keep its behavior in check.




