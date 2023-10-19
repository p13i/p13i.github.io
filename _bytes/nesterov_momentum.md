---
layout: post
title: Nesterov gradient descent
programming_language: Python
date: 2021-04-12
description: For Stanford AA222
---

```py
import numpy as np


class CountWillExceedWarning(RuntimeError):
    pass


def step_nesterov_momentum(f_fn, g_fn, x, v, alpha, beta):
    """ Source: Course textbook, Algorithm 5.4 (p. 76) """
    g = g_fn(x + beta * v)
    # normalization step
    g = g / np.linalg.norm(g)
    v[:] = beta * v - alpha * g
    return x + v, v


def impl_nesterov_momentum(f_fn, g_fn, x0, alpha, beta):
    x, v = x0, np.zeros(x0.size)
    x_history = [x]
    while True:
        try:
            x, v = step_nesterov_momentum(f_fn, g_fn, x, v, alpha, beta)
            x_history.append(x)
        except CountWillExceedWarning:
            break
    return x_history


def optimize(f, g, x0, n, count, prob, return_history=False):
    """
    Args:
        f (function): Function to be optimized
        g (function): Gradient function for `f`
        x0 (np.array): Initial position to start from
        n (int): Number of evaluations allowed. Remember `g` costs twice of `f`
        count (function): takes no arguments are returns current count
        prob (str): Name of the problem. So you can use a different strategy
                 for each problem. `prob` can be `simple1`,`simple2`,`simple3`,
                 `secret1` or `secret2`
        return_history (bool)
    Returns:
        x_best (np.array): best selection of variables found
    """

    def f_fn(x):
        if count() + 1 >= n:
            raise CountWillExceedWarning()
        return f(x)

    def g_fn(x):
        if count() + 2 >= n:
            raise CountWillExceedWarning()
        return g(x)

    x_history = impl_nesterov_momentum(f_fn, g_fn, x0, alpha=0.1, beta=0.5)

    if return_history:
        return x_history

    return x_history[-1]
```
