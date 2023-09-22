---
layout: post
title: Rich Captions
date: "2016-09-01"
categories:
  - engineering
tags:
  - youtube-api
  - latex
author: Pramod Kotipalli
description: LaTeX-enchanced captioning for academic videos
image: https://user-images.githubusercontent.com/13140065/178387663-3e9ba24a-e4d9-4c67-bc58-f17af2dc43a0.png
---

# Problem identified

- Online education is rapidly gaining momentum
- Video captioning systems are limited to displaying simple
  plain-text
- Math/science students learn better by reading
  semantically-useful symbols

# Solution created

- Create web application where content creators can easily
  caption their videos in LaTeX
- Allows anyone on the internet to watch these captioned
  videos without cost

{% include _post_image.html src="https://user-images.githubusercontent.com/13140065/178387697-33c7ce7f-de4f-410c-bbea-0aaab1e4b608.png" %}

# Design paradigms & technologies used

- REST API design and docs with Django REST framework
- Material Design front-end with AngularJS +
  Javascript/jQuery
- YouTube iframe API
- LaTeX, KaTeX
