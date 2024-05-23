---
layout: default
title: "10. Constrained Multivariate Optimization"
parent: Lecture Notes
nav_order: 10
---

# Constrained Multivariate Optimization
{: .no_toc }

- TOC
{:toc}

## Setup

### General problem

The general $$n$$-dimensional problem is:

$$ \max_{x_1, \ldots, x_n} ~ f(x_1, \ldots, x_n) ~ \text{ s.t. } ~ g(x_1, \ldots, x_n) = 0 $$

That is, we want to find the values of $$x_1, \ldots, x_n$$ that maximize $$f(x_1, \ldots, x_n)$$, subject to the condition that $$g(x_1, \ldots, x_n) = 0$$.

### 2-dimensional problem

For most of this class, we'll only work with the two dimensional problem:

$$ \max_{x,y} ~ f(x,y) ~ \text{ s.t. } ~ g(x,y) = 0$$

That is, we want to find the values of $$x$$ and $$y$$ that maximize $$f(x,y)$$, subject to the condition that $$g(x,y) = 0$$.

## Constrained optimization with contour maps

The image below shows the contour map a mountain that spans the border of two countries.  The border is marked by a red line. To the west of the border is Green Country, and to the east is Blue Country.  What's the highest point of the mountain that lies directly on the border?

<img src="/CSUN-Econ-310/assets/images/contour-map-2.png" alt="contour-with-border" width="480">

This is an example of constrained optimization, because we're looking for the highest point subject to the constraint that the point must lie on the border.

As it turns out, the maximum point lies on the contour which *just touches* the border, or constraint.

{: .purple-callout-title }
> Mathematical Insight
>
> In two dimensional constrained optimization, the maximal point is found on the contour line that *just touches*, i.e. is *tangent* to, the constraint. 

{: .blue-callout-title }
> Example
>
> An example with x^0.5 y^0.5

## Constrained optimization with equations

### General problem

### 2-dimensional problem with linear constraint

{: .green-callout-title }
> Example
>
> 









