---
layout: default
title: "15. Theory of Production"
parent: Lecture Notes
nav_order: 15
---

# Theory of Production
{: .no_toc }

- TOC
{:toc}


## General Setup

A firm uses labor and capital as inputs to produce an output. If $$L$$ is the amount of labor input and $$K$$ is the amount of capital input, then the amount of output $$Y$$ is given by:

$$ Y = f(K,L) $$

We call $$f(K,L)$$ the *production function* because it maps the choice of inputs to the amount of output.

Firms can hire one unit of labor at a wage rate $$w$$ and it can rent one unit of capital at a rental rate $$r$$.  For simplicity, we assume that the price of the firm's output is $$1$$. (We can simply assume that labor and capital prices are priced in terms of the output unit.)

The firm chooses $$L$$ and $$K$$ to maximize profits. The firm's optimization problem is:

$$ \max_{K,L} ~ f(K,L) - wL - rK $$



### Alternative setup: cost functions

An alternative way to formulate the problem is to first derive a cost function. We define the cost function $$c(q)$$ as the minimum total cost to produce $$q$$ units of output:

$$ c(q) = \min_{K,L} ~ wL + rK ~ ~ \text{ s.t. } f(K,L)=q $$

Once we have the cost function, the firm's optimization problem becomes:

$$ \max_{q} ~ q - c(q) $$

The cost function approach and the direct approach are equivalent.



## Cobb Douglas Production Function

In this class we will work only with a 

### Returns to scale in Cobb Douglas production functions

- If $$a+b=1$$, then the production function exhibits *constant returns to scale*. That is, if you increase both $$L$$ and $$K$$ by a factor of $$m$$, output also increases by a factor of $$m$$.

{: .blue-callout-title }
> Proof
>
> $$\begin{align}
f(mL, mK) &= A (mL)^a (mK)^b \\
&= A m^a L^a m^b K^b \\
&= m^{a+b} A L^a K^b \\
&= m^{a+b} f(L,K) \\
&= m f(L,K)
\end{align}$$

- If $$a+b<1$$, then the production function exhibits *decreasing returns to scale*. That is, if you increase both $$L$$ and $$K$$ by a factor of $$m$$, output increases by a factor *less* than $$m$$.

{: .green-callout-title }
> Proof
>
> $$\begin{align}
f(mL, mK) &= m^{a+b} f(L,K) < m f(L,K)
\end{align}$$

- If $$a+b>1$$, then the production function exhibits *increasing returns to scale*. That is, if you increase both $$L$$ and $$K$$ by a factor of $$m$$, output increases by a factor *more* than $$m$$.

{: .yellow-callout-title }
> Proof
>
> $$\begin{align}
f(mL, mK) &= m^{a+b} f(L,K) > m f(L,K)
\end{align}$$
