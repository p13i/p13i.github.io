---
title: Idempotent
date: "2024-04-27"
categories:
  - writing
tags:
  - poetry
layout: post
author: Pramod Kotipalli
---

Something I notes since joining control plane team is when I
am writing an algorithm. Most of my SWE tasks are defining
inputs and outputs and the logic in between. When I am
implementing that logic in the code editor, I have to make
sure I make _idempotent_ changes when touching these
prod-critical high-level code paths (like the Processing in
ListRoles).

For me, I realized that that is an approach to rollouts, but
also in small CLs, and even down to how I make manipulations
of the code.

---

I had to Google it for myself to make sure it was the right
word: idempotent- denoting an element of a set which is
unchanged in value when multiplied or otherwise operated on
by itself.
