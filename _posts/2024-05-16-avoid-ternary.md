---
title: "Avoid ternary statements, seriously."
categories:
  - writing
  - engineering
layout: post
redirect_from: "avoid-ternary"
---

This is a personal preference informed by my experience.
Using expanded statements can make code more readable and
less prone to future coding errors. Some things to consider:

- C++ in scripting contexts is okay.
- Ternary statements in Python are acceptable.
- When can it be used in C++? At the very minimum for more
  "scripting" uses of C++.
- Simple statements like
  `int value = true ? 1 : 0;  // value = 1`.
