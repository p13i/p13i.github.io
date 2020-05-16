---
layout: posts/post
author: Pramod Kotipalli
title:  Rich Captions
description: LaTeX-enchanced captioning for academic videos
tags:
    - youtube-api
    - latex
image: /static/images/2016-09-01-rich-captions/rich-captions-thumbnail.png
redirect_from: "/portfolio/rich-captions/"
default_image_fullwidth: True
subcategories:
    - engineering
---

![]({{ page.image }})

# Problem identified
- Online education is rapidly gaining momentum
- Video captioning systems are limited to displaying simple plain-text
- Math/science students learn better by reading semantically-useful symbols

# Solution created
- Create web application where content creators can easily caption their videos in LaTeX
- Allows anyone on the internet to watch these captioned videos without cost

![](/static/images/2016-09-01-rich-captions/rich-captions-screenshot.png)

# Design paradigms & technologies used
- REST API design and docs with Django REST framework
- Material Design front-end with AngularJS + Javascript/jQuery
- YouTube iframe API
- LaTeX, KaTeX
