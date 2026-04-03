---
layout: default
title: "15. Price Discrimination"
parent: Lecture Notes
nav_order: 15
---

# Price Discrimination
{: .no_toc }

- TOC
{:toc}

## What is price discrimination?

Price discrimination happens when a firm charges different prices to different customers, usually based on some verifiable characteristic.

A common example of price discrimination is student and veteran discounts. If a consumer can prove that they are a student or a veteran, the firm is willing to charge them a lower price.

Another example of price discrimination is through the use of coupons. The differentiating characteristic is whether the consumer is willing to spend the time to look for coupons. More price sensitive consumers (who firms would naturally want to charge a lower price to) are more likely to spend the time to clip coupons.

Usually, the discounts are targeted at consumer groups with more *elastic* demand. In other words, the discounts are targeted at more price-sensitive groups, while the less price-sensitive groups pay full price.

{: .red-callout-title }
> Warning
>
> It's only price discrimination if the product being sold at different prices is the same. Thus, charging more money for a business class seat is *not* price discrimination, because the business class seat and the economy class seat are not the same product. Similarly, charging a higher auto insurance premium to a risky driver is *not* price discrimination because it costs the insurance company more to insure risky drivers than safe drivers.

## Third degree price discrimination

Third degree price discrimination happens when a firm can identify (and verify) at least two groups of consumers. It then charges a different price to each group. This usually results in higher profit than if it charged a single price to all consumers.

{: .blue-callout-title }
> Example 1
>
> There are two types of consumers in the market, type A and type B. The demand curve for type A consumers is given by:
>
> $$ q_A = 12 - p $$
>
> The demand curve for type B consumers is given by:
>
> $$ q_B = 10 - p $$
>
> The market is supplied by a single monopolist, who can practice third degree price discrimination. The monopoly can produce $$q$$ units of the commodity at a total cost of:
>
> $$c(q) = 2q$$
>
> 1. Calculate the profit maximizing price for type A consumers under third degree price discrimination.
> 2. Calculate the profit maximizing price for type B consumers under third degree price discrimination.
> 3. Calculate the monopolist's total profit under third degree price discrimination.
> 4. Calculate the price that the monopolist would charge if it were not able to price discriminate.
> 5. Calculate the monopolist's profit if it were not able to price discriminate.
>
> *Answer.*
>
> **Step 1: Write the inverse demand curves for each consumer type.**
> 
> To solve this problem, the first thing to realize is that choosing price for each type of consumer is the same as choosing quantity for each type of consumer. This is because price and quantity are related by a 1-for-1 relationship via the demand curves.
>
> Thus, we can write:
>
> $$ q_A = 12 - p_A  $$
> 
> and
>
> $$ q_B = 10 - p_B $$
>
> It will also help us to re-arrange the above two equations into inverse demand curves:
> 
> $$ p_A = 12 - q_A $$
> 
> and
> 
> $$ p_B = 10 - q_B $$
>
> **Step 2: Write the total profit in terms of $$q_A$$ and $$q_B$$.**
>
> The total profit is:
>
> $$\begin{align}
\Pi & = p_A q_A + p_B q_B - 2(q_A + q_B) \\
    & = (12 - q_A) q_A + (10 - q_B) q_B - 2q_A - 2q_B \\
    & = 12 q_A - q_A^2 + 10q_B - q_B^2 -2q_A - 2q_B \\
    & = 10 q_A - q_A^2 + 8q_B - q_B^2
\end{align}$$
>
> **Step 3: Write the firm's optimization problem.**
>
> The firm's optimization problem is:
>
> $$ \max_{q_A, q_B} ~ 10q_A - q_A^2 + 8q_B - q_B^2 $$ 
>
> **Step 4: Write down the first order conditions.**
>
> This is a unconstrained multivariate optimization problem. The condiitons for a maximum are that the partial derivatives with respect to $$q_A$$ and $$q_B$$ are both zero.
>
> $$ \text{FOC}[q_A]: ~ 10 - 2q_A = 0 $$
>
> $$ \text{FOC}[q_B]: ~ 8 - 2q_B = 0 $$
>
> **Step 5: Solve the first order conditions.**
>
> These two first order conditions are easily solved, giving $$q_A = 5$$ and $$q_B = 4$$.
>
> **Step 6: Plug $$q_A$$ and $$q_B$$ back into the inverse demand curves.**
>
> Plugging them back in, we get $$p_A = 7$$ and $$p_B = 6$$.
>
> **Step 7: Calculate the total profit at these prices and quantities.**
>
> $$\begin{align}
\Pi & = 10q_A - q_A^2 + 8q_B - q_B^2 \\
    & = 10(5) - (5)^2 + 8(4) - (4)^2 \\
    & = 50 - 25 + 32 - 16 \\
    & = 41
\end{align}$$
>
> So we now have our answers for parts 1-3 of the problem.
>
> **Step 7: Find the total demand curve (and the inverse total demand curve)**
>
> If the firm can't price discriminate, it has to treat the consumers as a single demand curve. Add up the demand curves of both consumers:
>
> $$\begin{align}
q &= q_A + q_B \\
  &= (12 - p) + (10 - p) \\
  &= 22 - 2p
\end{align}$$
>
> As usual, it's also helpful to write down the inverse total demand curve:
>
> $$\begin{align}
 q &= 22 - 2p \\
2p &= 22 - q \\
 p &= 11 - \frac{1}{2} q
\end{align}$$
>
> **Step 8: Write down the profit (without price discrimination) in terms of total quantity $$q$$**
>
> $$\begin{align}
\Pi &= p q - 2q \\
    &= (11 - \frac{1}{2}q)q - 2q \\
    &= 11q - \frac{1}{2} q^2 - 2q \\
    &= 9q - \frac{1}{2}q^2
\end{align}$$
>
> **Step 9: Write down the firm's maximization problem (without price discrimination)**
>
> The key difference is that the firm now chooses a total quantity for the whole market, instead of different quantities for each type of consumer:
>
> $$ \max_{q} ~ 9q - \frac{1}{2} q^2 $$
>
> **Step 10: Write the first order condition and solve**
>
> $$\text{FOC}[q]: ~ 9 - q = 0 $$
>
> From which we get $$q = 9$$. Plugging this back into the inverse total demand curve, we get $$p = 6.5$$.
>
> **Step 11: Use $$q$$ and $$p$$ to calculate total profit without price discrimination**
>
> $$\begin{align}
\Pi &= 9q - \frac{1}{2} q^2 \\
    &= 9(9) - \frac{1}{2} (9)^2 \\
    &= 81 - \frac{1}{2} 81 \\
    &= 40.5
\end{align}$$

The example shows that the firm indeed increases its profit by engaging in price discrimination. It also shows that when firms price discriminate, some consumers get charged *more* and some get charged *less*. The consumers who get charged more are worse off, but the consumers who get charged less are better off.

This is a well known feature of price discrimination. Although price discrimination might *sound* like a greedy unethical practice, some consumers actually stand to benefit. If the consumers who benefit are those whom we'd otherwise want to prioritize (like low income students or veterans), then price discrimination isn't *necessarily* something that needs to be actively discouraged. In practice, since firms tend to charge less to price sensitive consumers and more to price insensitive consumers, price discrimination often leads to lower prices for lower income people.

{: .purple-callout-title}
> Economic Insight
>
> Price discrimination increases the profit of firms, but it isn't welfare-reducing for all consumers. Price discrimination tends to makes price sensitive consumers better off but price insensitive consumers worse off.

### Examples of third degree price discrimination

Student discounts, veterans discounts, senior citizen discounts are all examples of third degree price discrimination. Any time different prices are offered to different groups of people who can verify their group status, that's an example of third degree price discrimination.



## First degree (or perfect) price discrimination

First degree price discrimination (also called perfect price discrimination) happens when the firm know exactly how much each person is willing to pay to buy their product, *and* the firm is able to verify the identity of each consumer and charge a different price to every person.

If a firm is able to do this, then it will be able to charge each consumer *exactly* how much they're willing to pay, and no less. By doing this, the firm actually extracts *all* the available surplus in the market.

The diagram below illustrates the distribution of surplus in a market with perfect price discrimination. The market is **efficient** because all of the available surplus is extracted, but it is highly inequitable as the firm accumulates *all* of the surplus available in the market.

![perfect-price-discrimination](/CSUN-Econ-310/assets/images/price-discrimination-1st-degree.png)

*(The red shaded region shows producer surplus and the blue shaded region shows consumer surplus.)*

### Examples of first degree price discrimination

True first degree price discrimination isn't possible in practice. It's not possible for firms to know so much detail about every individual's underlying utility for a product. 

However, college financial aid is often cited as an example approximating first degree price discrimination. Colleges charge a very high price of tuition. Then, their financial aid office offers individualized discounts to families based on their needs. Thus, they try to charge exactly the price to each student to get them to actually attend the college.

As mentioned in the above insight, this insight frames price discrimination as a benefit to more price-sensitive customers, which highlights how price discrimination can be beneficial to some but not others. Note that offers of individualized financial aid are probably what lets colleges set very high tuitions to begin with.  If they were not allowed to offer individualized aid packages, they might have to lower the price for everyone to keep enrollment numbers the same.

## Second degree price discrimination

Second degree price discrimination happens when the firm can't perfectly identify all individuals, but it does know their demand curves.

What the firm can do is charge a fixed entry fee that extracts all of the surplus of at least one of the consumer groups. It then charges a price on top of the fixed entry fee. This is sometimes known as *club pricing* or *two-part tariffs*, because the price comes in two parts: an entry fee and a low unit price. The low unit price is attractive to price-sensitive customers, but the entry fee is used to extract the surplus that consumers get from being offered the low unit price.

Can you think of any well known companies that use this pricing model?

We won't solve second degree price discrimination problems in this class. But you can reference the *Nicholson and Snyder* textbook if you want to learn more.





