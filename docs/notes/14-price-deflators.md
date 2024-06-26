---
layout: default
title: "14. Application: Issues with the CPI"
parent: Lecture Notes
nav_order: 14
---

# Application: Issues with the CPI
{: .no_toc }

- TOC
{:toc}

## What is the CPI?

CPI stands for the **Consumer Price Index**.  The CPI is a measure of *aggregate* price levels. That is, when the prices of many goods are changing all at the same time, and in different ways, the CPI gives us a sense of how much these prices changed *on average*.

CPI is measured between two periods: a base period and a comparison period. It is calculated by first selecting a fixed basket of goods, then calculating the total cost to buy that basket in the comparison period compared to the base period:

$$ \text{CPI} = \frac{\text{Cost of basket in comparison period}}{\text{Cost of basket in base period}} \times 100 $$

{: .blue-callout-title }
> CPI Example
>
> There are two goods, $$x$$ and $$y$$.  In 2020 (the base period), the prices of the goods were $$p_x = 10$$ and $$p_y=5$$. In 2024 (the comparison period), the prices of the goods were $$p_x=12$$ and $$p_y=7$$. Calculate the CPI between 2020 and 2024 using a basket with $$x=5$$ and $$y=5$$.
>
> *Answer.*
>
> $$\begin{align}
\text{CPI} &= \frac{\text{Cost of basket in comparison period}}{\text{Cost of basket in base period}} \times 100 \\
&= \frac{12 \cdot 5 + 7 \cdot 5}{10 \cdot 5 + 5 \cdot 5} \times 100 \\
&= 126.7
\end{align}$$
>
> In other words, the cost of the basket increased by 26.7%.


CPI is most commonly used as a cost of living adjustment. It attempts to measure how much your income has to increase in order to keep up with inflation.  

{: .green-callout-title }
> Example
>
> If CPI in 2024 is 140 and 2020 is the base period, then CPI says that your income has to go up by 40% between 2020 and 2024 in order to maintain the same standard of living in 2024 as you had in 2020.


## Problems with the CPI

One problem with the CPI is that it doesn't take into account *substitution effects*. That is, when prices change, people also change the bundle of goods they purchase.  That is, consumers *substitute* between goods when prices change.

Because of substitution effects, CPI can give a misleading impression of how much quality of life has actually changed.

The issue is most starkly demonstrated with the following example:

{: .yellow-callout-title }
> Example
>
> Suppose in the year 2020, the average consumers buys 100 gallons of Exxon gas and 100 gallons of Shell gas. The price of both is $5/gallon.  In 2021, a major fire at Shell's main refinery raises the price of Shell gas to $7/gallon, while the price of Exxon gas stays at $5/gallon.
>
> 1. Show that the CPI in 2021 (using 2020 as the base period) is 120.
>
> 2. Do you think income really needs to go up by 20% to maintain the same standard of living?
>
> *Answer.*
>
> $$\begin{align}
\text{CPI} &= \frac{5\times100 + 7\times100}{5\times100 + 5\times100} \times 100 \\
& = 120
\end{align}$$
>
> However, income doesn't need to increase by 20% to maintain the same standard of living. Instead of buying Shell gas, which is now more expensive, consumers can choose to buy Exxon gas instead. Since the price of the lowest cost gas hasn't changed, most consumers are not affected by the price increase. Only consumers who cannot conveniently access Exxon gas are worse off.

## Income required to maintain constant utility

Instead of calculating the income required to buy the same bundle of goods, an alternative approach is to calculate the income required to maintain the same level of utility.  The example below demonstrates.

{: .blue-callout-title }
> Example
>
> A consumer has utility function over two goods, $$x$$ and $$y$$, given by:
>
> $$ u(x,y) = x^{\tfrac{1}{2}} y^{\tfrac{1}{2}} $$
>
> In period 1, the consumer has income $$I = 100$$, the price of $$x$$ is $$p_x=1$$ and the price of $$y$$ is $$p_y=1$$.
>
> In period 2, the price of $$y$$ changes to $$p_y^\prime=2$$ but the price of $$x$$ stays the same.
>
> 1. Calculate the CPI in period 2 with period 1 as the base period.
>
> 2. Suppose that income increases in period 2 by the CPI factor. Show that the consumer's utility in period 2 would actually be higher than in period 1.
>
> 3. What income does the consumer need in period 2 to maintain the same utility as in period 1?
>
> *Answer to part 1.*
>
> First, we need to find the optimal consumption bundle in period 1.
>
> The consumer's optimization problem is:
>
> $$\begin{align}
\max_{x,y} ~ x^{\tfrac{1}{2}} y^{\tfrac{1}{2}} ~ \text{ s.t. } x + y = 100
\end{align}$$
>
> The first order conditions are:
>
> $$\begin{align}
\tfrac{1}{2} x^{-\tfrac{1}{2}} y^{\tfrac{1}{2}} &= \lambda \\
\tfrac{1}{2} x^{\tfrac{1}{2}} y^{-\tfrac{1}{2}} &= \lambda 
\end{align}$$
>
> Dividing the two first order conditions gives us:
>
> $$\begin{align}
\frac{y}{x} &= 1 \\
y &= x
\end{align}$$
>
> So the optimal choice of $$x$$ and $$y$$ in period 1 is $$x=50$$ and $$y=50$$. Utility is $$50^{\tfrac{1}{2}} 50^{\tfrac{1}{2}} = 50$$.
>
> To calculate CPI, simply apply the definition:
>
> $$\begin{align}
\text{CPI} &= \frac{\text{Cost in period 2}}{\text{Cost in period 1}} \times 100\\
&= \frac{50 + 2\times50}{50 + 50} \times 100 \\
&= 150
\end{align}$$
>
> *Answer to part 2.*
>
> Suppose income increased by 50%, as the CPI suggests that it needs to in order to maintain the standard of living.
>
> The consumer's optimization problem in period 2, with an income of $$I^\prime=150$$ is:
>
> $$\begin{align}
\max_{x,y} ~ x^{\tfrac{1}{2}} y^{\tfrac{1}{2}} ~ \text{ s.t. } x + 2y = 150 
\end{align}$$
>
> The first order conditions are:
>
> $$\begin{align}
\tfrac{1}{2} x^{-\tfrac{1}{2}} y^{\tfrac{1}{2}} &= \lambda \\
\tfrac{1}{2} x^{\tfrac{1}{2}} y^{-\tfrac{1}{2}} &= 2\lambda 
\end{align}$$
>
> Dividing the two first order conditions gives us:
>
> $$\begin{align}
\frac{y}{x} &= \tfrac{1}{2} \\
y &= \tfrac{1}{2} x 
\end{align}$$
>
> Plug this into the budget constraint:
>
> $$\begin{align}
x + 2y &= 150 \\
x + 2\left(\tfrac{1}{2}x\right) &= 150 \\
2x &= 150 \\
x &= 75
\end{align}$$
>
> Plug $$x=75$$ into $$y=\tfrac{1}{2}x$$ to get $$y=37.5$$. Utility is $$75^{\tfrac{1}{2}} (37.5)^{\tfrac{1}{2}} = 53.03$$. Thus, increasing income by the CPI actually increased the consumer's total utility in period 2.
>
> *Answer to part 3.*
>
> We need to find the income $$I^\prime$$ such that:
>
> $$\begin{align}
\max_{x,y} ~ x^{\tfrac{1}{2}} y^{\tfrac{1}{2}} ~ \text{ s.t. } ~ x + 2y = I^\prime
\end{align}$$
>
> results in a utility of $$50$$. We therefore need to find the optimal choice of $$x$$ and $$y$$ as functions of $$I^\prime$$ and find the $$I^\prime$$ that results in a utility of $$50$$.
>
> The first order conditions are:
>
> $$\begin{align}
\tfrac{1}{2} x^{-\tfrac{1}{2}} y^{\tfrac{1}{2}} &= \lambda \\
\tfrac{1}{2} x^{\tfrac{1}{2}} y^{-\tfrac{1}{2}} &= 2\lambda 
\end{align}$$
>
> Dividing the two first order conditions gives us:
>
> $$\begin{align}
\frac{y}{x} &= \tfrac{1}{2} \\
y &= \tfrac{1}{2} x 
\end{align}$$
>
> Plug this into the budget constraint:
>
> $$\begin{align}
x + 2y &= I^\prime \\
x + 2\left(\tfrac{1}{2}x\right) &= 150 \\
2x &= I^\prime \\
x &= \tfrac{1}{2} I^\prime
\end{align}$$
>
> And since $$y = \tfrac{1}{2}x$$, we get $$y = \tfrac{1}{4} I^\prime $$. Utility is:
>
> $$\begin{align}
u(x,y) &= x^{\tfrac{1}{2}} y^{\tfrac{1}{2}} \\
&= \left( \tfrac{1}{2} I^\prime \right)^{\tfrac{1}{2}} \left( \tfrac{1}{4} I^\prime \right)^{\tfrac{1}{2}} \\
&= \left( \tfrac{1}{8} I^{\prime 2} \right)^{\tfrac{1}{2}} \\
&= \left( \tfrac{1}{8} \right)^{\tfrac{1}{2}} I^\prime 
\end{align}$$
>
> And so we need to find $$I^\prime$$ where utility is $$50$$:
>
> $$\begin{align}
\left( \tfrac{1}{8} \right)^{\tfrac{1}{2}} I^\prime  &= 50\\
I^{\prime} &= \left( \tfrac{1}{8} \right)^{-\tfrac{1}{2}} 50 \\
&= 141.42
\end{align}$$
>
> Income only needed to increase by 41% in order to maintain the same standard of living, as opposed to the 50% increase suggested by the CPI.

{: .purple-callout-title }
> Economic Insight
>
> The CPI does not always accurately measure the amount of income needed to maintain the same standard of living.  This problem is known as *substitution bias* in the CPI.  Substitution bias is stronger when the prices of substitutable goods are changing relative to each other.


## Why do we still use CPI?

Given that there are issues with the CPI, why is it still the most popular way to make cost of living adjustments?

The most important reason is that utility functions are difficult, if not impossible, to accurately measure. Utility-based cost of living adjustments depend on unreliable assumptions about the shape of the utility function.  Such an approach to making cost of living adjustments may be considered opaque, difficult to understand, and illegitimate by the public.

Despite its weaknesses, the CPI only relies on observable data, such as prices and household consumption patterns. It is therefore more transparent, relies on fewer assumptions, and thus more defensible to the public than model-based adjustments.

Still, it is important for economists to understand the inherent weaknesses of CPI and to be identify situations in which the CPI's substitution bias will be more or less severe.
 


