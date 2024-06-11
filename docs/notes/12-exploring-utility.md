---
layout: default
title: "12. Exploring Utility Functions"
parent: Lecture Notes
nav_order: 12
---

# Exploring Utility Functions
{: .no_toc }

- TOC
{:toc}

In this lecture we explore the properties of various types of utility functions over two goods, $$u(x,y)$$.

## Cobb Douglas

A Cobb Douglas utility function has the following form:

$$ u(x,y) = x^a y^b $$

where $$a>0$$ and $$b>0$$.

A Cobb Douglas utility function has indifference curves that look like:

![cobb-douglas](/CSUN-Econ-310/assets/images/12-exploring-utility-cobb-douglas.png)

The MRS between $$x$$ and $$y$$ in a Cobb Douglas utility function is:

$$MRS_{xy} (x,y) = \frac{u_x(x,y)}{u_y(x,y)} = \frac{ay}{bx}$$

As can be seen from the MRS, Cobb Douglas has the realistic property of "taste for variety". That is, the desirability of $$x$$ relative to $$y$$ goes down when the consumer consumes more of $$x$$, and goes up when the consumer consumes more of $$y$$.

Cobb Douglas also has the interesting property that the proportion of income a consumer spends on a good depends only on $$a$$ and $$b$$, and does not depend on the relative prices. (I leave it as an exercise for you to show this.)

Because of its flexibility and mathematical convenience, Cobb Douglas is a common choice for modeling consumer utility.


---

{: .blue-callout-title }
> Cobb Douglas Example
>
> 

---

## Perfect Substitutes

If two goods $$x$$ and $$y$$ are perfect substitutes, then the utility function of the consumer must look like:

$$ u(x,y) = ax + by $$

where $$a>0$$ and $$b>0$$.

The indifference curves will be straight lines:

![cobb-douglas](/CSUN-Econ-310/assets/images/12-exploring-utility-perfect-subs.png)

The MRS between $$x$$ and $$y$$ is:

$$MRS_{xy} (x,y) = \frac{u_x(x,y)}{u_y(x,y)} = \frac{a}{b}$$

The MRS is constant, which means that the consumer is always willing to trade between $$x$$ and $$y$$ at a rate of $$a/b$$. (The consumer is always willing to give up $$a/b$$ units of $$y$$ to get $$1$$ unit of $$x$$.)

### Corner solutions

Perfect substitutes are interesting because the optimal choice is usually either a *corner solution*, or there are *infinitely many* optimal choices. 

For example, consider your decision to choose between Exxon gasoline and Shell gasoline, which are perfect substitutes. If Exxon is cheaper, you would only purchase gas from Exxon and zero from Shell. On the other hand, if Shell is cheaper, you would only purchase from Shell and zero from Exxon. If they are the same price, then any combination of Shell and Exxon gasoline would be optimal.

---

{: .green-callout-title }
> Perfect Substitutes Example
>
> 

---

## Leontieff (Perfect Complements)

If two goods are perfect complements, we say that the consumer has a "Leontieff" utility function. A Leontieff utility function is defined by:

$$u(x,y) = \min (x,y) $$

A Leontieff utility function has the following indifference curves:

![cobb-douglas](/CSUN-Econ-310/assets/images/12-exploring-utility-leontieff.png)

The MRS of a Leontieff utility function is tricky to define mathematically. It is either zero or infinity depending on the location.

Leontieff utility functions are used to model goods that require one another in order to be useful. For example, if $$x$$ are left shoes and $$y$$ are right shoes, then the utility over $$x$$ and $$y$$ is appropriately modeled by Leontieff utility.

The important thing to remember about Leontieff utility is that $$x$$ and $$y$$ must always be purchased in equal quantities.

---

{: .yellow-callout-title }
> Leontieff Example
>
> 

---

## Quasilinear Utility

A utility function is said to be quasilinear in $$x$$ if it has the following form:

$$u(x,y) = x + v(y)$$

You've already seen examples of quasilinear utility functions, which we worked with in lectures 4-8.  In those examples, the utility function was quasilinear in the consumption of the "numeraire good" which we called $$c$$ at the time.

Quasilinear utility functions have indifference curves are all parallel shifts along the $$x$$ axis:

![cobb-douglas](/CSUN-Econ-310/assets/images/12-exploring-utility-quasilinear.png)

The MRS between $$y$$ and $$x$$ (that is, the amount of $$x$$ the consumer is willing to give up for 1 unit of $$y$$) is:

$$ MRS_{yx} (x,y) = \frac{u_y(x,y)}{u_x(x,y)} = v^\prime(y) $$

If $$x$$ is defined as numeraire consumption (e.g. money left over), then $$v^\prime(y)$$ has an easy interpretation as the consumer's marginal willingness-to-pay for good $$y$$, as measured in dollar units.

Quasilinear utility functions are often used to model consumer choice between a single commodity and a generic measure of "money left over for other goods".

---

{: .blue-callout-title }
> Quasilinear Example
>
>

---










