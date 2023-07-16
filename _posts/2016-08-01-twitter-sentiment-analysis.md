---
title: Twitter Sentiment Analysis
date: 2016-08-01
categories:
  - engineering
tags:
  - machine-learning
  - artificial-intelligence
layout: post
author: Pramod Kotipalli
description: Understanding user sentiment to aid mental health diagnosis
image: https://user-images.githubusercontent.com/13140065/178387533-dd7c868a-b32d-4995-a9c4-99503e06d02c.png
---

# Motivation

- The United States, in particular, features extremely high
  costs for healthcare
- Public awareness and support mental health care is
  increasing

# Solution created

- Pipeline to gather tweets on two polar topics to
  understand users’ sentiment towards them
- Demonstration that identifies those users who use
  depression-indicative language
- Useful to mental health professionals to identify
  long-term trends in user’s mental health

# Pipeline overview

1. Data collection: Collected nearly 4,000 tweets from the
   Twitter Developer API and labelled them based on hashtags
   present. For example, tweets containing "depressed" (or
   related hashtags) will be labelled as belonging to the
   "depressive-indicative" class; tweets containing "happy"
   (or related hashtags) will be labelled as part of the
   "non-depressive-indicative" class.
2. Understand the user's position in the Twitter community:
   Call the Twitter API to gain information about the user's
   followers, followees, average retweet counts, and more.
3. Data analysis: Send each of the 4,000 tweets through IBM
   Watson's Tone Analyzer API to gain more dimensions of
   sentiment information about each tweet.
4. Classification model: Use the labelled data to
   discriminate between tweets that are
   "depressive-indicative" or not in terms of their language
   characteristics. Trained classification model with
   scikit-learn’s k-Nearest Neighbors implementation.
5. Classify an unknown user: Given an unknown user, generate
   visualizations and an overall classification of their
   Twitter tweet language.

# Technologies used

- Python + Django web framework
- scikit-learn & IBM Watson intelligence APIs
- chart.js & Material Bootstrap

{% include _post_image.html src="https://user-images.githubusercontent.com/13140065/178387561-66615bea-d78d-4430-a965-78020ee4259c.png" %}

{% include _post_image.html src="https://user-images.githubusercontent.com/13140065/178387590-9f140371-4925-44b5-aa57-57cdb600e1c6.png" %}

{% include _post_image.html src="https://user-images.githubusercontent.com/13140065/178387621-18441b40-cfb1-42ac-bc36-282095ac2e56.png" %}
