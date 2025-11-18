---
layout: default
title: "12. Consumption and Savings"
parent: Lecture Notes
nav_order: 12
---

# Consumption and Savings
{: .no_toc }

- TOC
{:toc}

## The Time Value of Money

Before we can talk about savings, we need to understand the time value of money.

The time value of money arises from a simple insight: the promise of $1 at a future date is worth less than $1 in the pocket now.  There are at least a few reasons for this:

- You could die before the future date, thus rendering the future promise worthless.
- You can invest the $1 now and earn a rate of return, thus ending up with more than $1 at the future date.
- The promisor may not make good on the promise, either intentionally or due to circumstances outside their control.
- A life circumstance may arise for you which requires you to have money now, and you can't wait to receive money at a future date.
- Psychologically, humans have demonstrated that they often value present utility greater than future utility. This is why many of you have trouble committing to study or exercise.

For all these reasons, $1 promised at a future date is worth less than $1 today.

## The Discount Factor and Present Value

Economists often model time preference using what's known as the **time discount factor**, and we often denote it with $$\beta$$, where $$\beta<1$$.

A discount factor of $$\beta$$ says that 1 unit of value (either dollars or utility) promised 1 time-period from now, is worth only $$\beta$$ value units today.  As a corollary, if 1 unit of value is promised $$t$$ periods from now, then that promise is worth only $$\beta^t$$ value units today.

We call the worth of a promise, valued in terms of today, the **present value** of the promise.

{: .blue-callout-title }
> Example
>
> An individual has a discount factor of $$\beta=0.95$$ per year. What is the present value of $100 to be received in one year's time?
>
> *Answer.* $$\beta \times 100 = 95$$

{: .green-callout-title }
> Example
>
> An individual has a discount factor of $$\beta=0.95$$ per year. What is the present value of $100 to be received in ten years' time?
>
> *Answer.* $$\beta^{10} \times 100 = (0.95)^{10} \times 100 = 59.87$$

### Relationship between discount factor and interest rates

If financial returns are all that matters, then there is a 1:1 relationship between the discount factor and interest rates.

Suppose an individual can invest money at an annual rate of return $$r$$. We call $$r$$ the **interest rate**. That is, if they invest $1 today, they will receive $$\$(1+r)$$ in one year's time.

To derive the relationship between the discount factor and the interest rate, we simply have to ask: What is a promise of $1 in one year's time worth today?

If financial returns are all that matter, then a promise of $1 in one year's time is worth exactly $$\$ \left( \frac{1}{1+r} \right)$$ today.

That's because if $$\$ \left( \frac{1}{1+r} \right)$$ were invested today, it would be worth:

$$ \$ \left( \frac{1}{1+r} \right) \times (1+r) = \$ 1 $$

in one year's time.

The relationship between the discount factor and the interest rate is therefore:

$$ \beta = \frac{1}{1+r} $$

### Some useful present value formulas

Here are some useful formulas for calculating the present value of a stream of payments.

**General stream of payments**

In general, if a promise is made where you will receive value units of $$x_1, x_2, \ldots, x_T$$ in periods $$t=1, 2, \ldots, T$$, then the present value (at $$t=0$$) is:

$$ PV = \sum_{t=1}^T \beta^t x_t $$

**Constant stream of payments**

If the stream of payments is *constant*, i.e. $$x_t = x$$ for all $$t$$, then the present value is:

$$ PV = \left( \frac{1-\beta^{T+1}}{1-\beta} - 1 \right) x$$


{: .yellow-callout-title }
> Example
>
> A person's discount factor is $$\beta = 0.9$$ per annum. Calculate the present value of receiving $100 each year for 20 years.
>
> *Answer.*
>
> $$\begin{align}
PV &= \left( \frac{1-(0.9)^{21}}{0.1} - 1 \right) 100 \\
&= 790.581
\end{align}$$


{: .purple-callout-title }
> Note
>
> You may have seen the formula:
>
> $$ NPV = PMT \times \left( \frac{1 - (1+r)^{-T}}{r} \right) $$
>
> Which calcualtes the net present value of a regular payment amount $$PMT$$ from periods $$t=1$$ through $$t=T$$. 
>
> Using $$\beta = \frac{1}{1+r}$$, it's possible to show that the previous two formulas for present value are equivalent. (I leave this as an exercise.)




**Infinite stream of constant payments**

If the stream of payments is both constant and *infinite*, meaning you receive payments of $$x$$ for every period from $$t=1$$ to $$t=\infty$$, then the present value is:

$$ PV = \frac{\beta}{1-\beta} x $$

*Proof.*  This one is somewhat fun to prove:

$$\begin{align}
PV &= \beta x + \beta^2 x + \beta^3 x + \ldots \\
&= \beta x + \beta \left( \beta x + \beta^2 x + \beta^3 x + \ldots \right) \\
&= \beta x + \beta PV \\
(1-\beta) PV &= \beta x  \\
PV &= \frac{\beta}{1-\beta} x
\end{align}$$

{: .blue-callout-title }
> Example
>
> A person's discount factor is $$\beta = 0.95$$ per annum. Calculate the present value of receiving $100 starting from 1 year from now and every year thereafter, forever.
>
> *Answer.*
>
> $$\begin{align}
PV &= \frac{\beta}{1-\beta} x \\
&= \frac{0.95}{0.05} 100 \\
&= 1900
\end{align}$$


## The Consumption Savings Problem

Now that we've established that money and utility both have a time value, we are ready to study the consumption-savings decision. This refers to a person's decision of how much to save vs. how much to consume each period.

### Basic setup

We'll work with the simplest possible setup to study consumption and savings.

Suppose an individual lives for two periods, $$t=1$$ and $$t=2$$. In period 1, he earns an income of $$Y$$. In period 2, he earns no income.

The individual gets utility from consuming in each period. If he consumes a dollar amount $$c_t$$ in period $$t$$, the utility he gets is $$u(c_t)$$.

The consumer's objective is to maximize his present value of time-discounted utility:

$$u(c_1) + \beta u(c_2)$$

where $$\beta$$ is the person's discount factor.

In order to consume in period 2, the person must save in period 1. He can save by buying **bonds**. A bond is a promise to pay $$\$1$$ per bond in period 2, and the price of the bond in period 1 is $$p$$.

The individual's maximization problem is therefore:

$$ \max_{c_1, c_2} ~ u(c_1) + \beta u(c_2) ~ \text{s.t.} ~ c_1 + pb_1 = Y ~ \text{and} ~ c_2 = b_1 $$

where $$b_1$$ is the number of bond purchases made in period 1.

The problem can be rewritten:

$$ \max_{c_1, c_2} ~ u(c_1) + \beta u(c_2) ~ \text{s.t.} ~ c_1 + pc_2 = Y $$

which looks very much like the consumer choice problems we've solved in the past!

{: .purple-callout-title }
> Relationship between price of a bond and interest rate
>
> Note that we defined $$p$$ as the price of a bond that pays out $1 after one period. The total return is therefore $$1$$, with an initial investment of $$p$$. The *rate of return* (i.e. the percentage gain) is therefore $$r = \frac{1-p}{p}$$. Rearranging that gives $$p = \frac{1}{1+r} $$.

### First order conditions and the Euler equation

The first order conditions are:

$$\begin{align}
u^\prime(c_1) &= \lambda \\
\beta u^\prime(c_2) &= \lambda p
\end{align}$$

And if you divide the two first order conditions you get:

$$\begin{align}
\beta \frac{u^\prime(c_2)}{u^\prime(c_1)} = p 
\end{align}$$

This equation, which relates the marginal utilities in the two periods to the discount factor and the rate of return, is called the **Euler equation**. It is named after the great mathematician Leonhard Euler, who derived similar equations while studying dynamical systems.

{: .purple-callout-title }
> Economic Insight
>
> Note that if $$\beta = p$$, which would be the case if $$\beta=\frac{1}{1+r}$$, then $$u^\prime(c_1) = u^\prime(c_2)$$ at the optimal consumption-savings decision. Moreover, this implies that $$c_1 = c_2$$!  In other words, the person will consume the same amount in period 1 as in period 2.
>
> This is an example of **consumption smoothing**. That is, people generally desire to smooth out their consumption over time. That's why people will borrow when they're young, save money in their prime earning years, and then draw down their savings when they're old.
>
> If the rate of return on bonds is equivalent to a person's discount factor, then they will smooth their consumption perfectly. If the bond offers a higher rate of return that the person's subjective time preference, they may choose to save more. If the bond offers a lower rate of return than the person's subjective time preference, they may choose to save less.

{: .blue-callout-title }
> Example
>
> An individual lives for two periods. In period 1, he earns an income of $$Y=1,000$$. In period 2, he earns no income. In order to consume in period 2, the person must buy bonds in period 1. A bond promises to pay $$\$1$$ per bond in period 2, and the price of a bond in period 1 is $$p=0.95$$.
>
> The individual gets utility from consuming in each period. If he consumes a dollar amount $$c_t$$ in period $$t$$, the utility he gets is $$u(c_t) = \ln c_t$$.
>
> The individual's objective is to maximize his present value of time-discounted utility:
>
> $$\ln c_1 + \beta \ln c_2 $$
>
> where $$\beta = 0.95$$.
>
> 1. Write down the individual's optimization problem.
> 2. How much will the person consume in each period. How many bond purchases will he make?
> 3. Calculate the interest rate on bonds.
>
> *Answer.*
>
> Step 1. Write down the optimization problem is:
>
> $$\max_{c_1, c_2} ~ \ln c_1 + \beta \ln c_2 ~ \text{s.t.} ~ c_1 + pc_2 = Y$$
>
> Step 2. Write down the order conditions:
>
> $$\begin{align}
\frac{1}{c_1} &= \lambda \\
\frac{\beta}{c_2} &= \lambda p
\end{align}$$
>
> Step 3. Divide the first order conditions:
>
> $$\begin{align}
\frac{ \beta / c_2 }{ 1/c_1} &= p \\
\beta \frac{c_1}{c_2} &= p \\
\frac{c_1}{c_2} &= \frac{p}{\beta} \\
&= \frac{0.95}{0.95} \\
&= 1
\end{align}$$
>
> So, at the optimum, $$c_1 = c_2$$.
> 
> Step 4. Plug $$c_1 = c_2$$ into the budget constraint:
>
> $$\begin{align}
c_1 + p c_2 &= Y \\
c_2 + p c_2 &= Y \\
(1+p)c_2 &= Y \\
c_2 &= \frac{Y}{1+p} \\
&= \frac{1,000}{1.95} \\
&= 512.82
\end{align}$$
>
> This implies that $$c_1 = c_2 = 518.82$$, and also that the individual purchases $$518.82$$ worth of bonds.
>
> Finally, let's calculate the interest rate:
>
> $$\begin{align}
r = \frac{1-p}{p} = \frac{0.05}{0.95} = 0.0526
\end{align}$$

### Interest rates and the supply of credit

In the above example, we derived an equation that must hold in equilibrium:

$$ c_2 = \frac{Y}{1+p} $$

The equation shows that the amount of second period consumption depends on the price of bonds. And in particular, that second period consumption decreases when the price of bonds increases.

Now, recall that second period consumption is equivalent to bond purchases. The equation we derived is therefore a **demand curve for bonds**, or more generally, a demand curve for savings. And it shows that when the price of bonds goes up (i.e. the interest rate goes down), the demand for savings goes down. Conversely, it also shows that when the price of bonds goes down (interest rates go up), then demand for savings go up.

The iteresting thing to note is that the demand for savings is also the **supply of credit**, because loans are made based on the deposits that consumers give to banks or the bonds that consumers buy from other institutions, like the government or from companies. Our model therefore shows how the supply of credit depends on the interest rates.

{: .purple-callout-title }
> Economic Insight
>
> The demand for savings and the supply of credit are closely interrelated, and both are affected by the interest rates available in the market.
>
> Because the Federal Reserve can control interest rates, this makes them one of the most powerful institutions in the country and the world.




