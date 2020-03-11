---
layout: posts/post
author: Pramod Kotipalli
title:  Twitter Sentiment Analysis
subtitle: Understanding user sentiment to aid mental health diagnosis
tags:
    - twitter-api
    - machine-learning
    - artifical-intelligence
    - ibm-watson-api
thumbnail_url: /static/images/2016-08-01-twitter-sentiment-analysis/twitter-sentiment-analysis-thumbnail.png
redirect_from: "/portfolio/twitter/"
default_image_fullwidth: True
subcategories:
    - engineering
---

![]({{ page.thumbnail_url }})

# Motivation
- The United States, in particular, features extremely high costs for healthcare
- Public awareness and support mental health care is increasing

# Solution created
- Pipeline to gather tweets on two polar topics to understand users’ sentiment towards them
- Demonstration that identifies those users who use depression-indicative language
- Useful to mental health professionals to identify long-term trends in user’s mental health

# Pipeline overview
1. Data collection: Collected nearly 4,000 tweets from the Twitter Developer API and labelled them based on hashtags present. For example, tweets containing "depressed" (or related hashtags) will be labelled as belonging to the "depressive-indicative" class; tweets containing "happy" (or related hashtags) will be labelled as part of the "non-depressive-indicative" class.
2. Understand the user's position in the Twitter community: Call the Twitter API to gain information about the user's followers, followees, average retweet counts, and more.
3. Data analysis: Send each of the 4,000 tweets through IBM Watson's Tone Analyzer API to gain more dimensions of sentiment information about each tweet.
4. Classification model: Use the labelled data to discriminate between tweets that are "depressive-indicative" or not in terms of their language characteristics. Trained classification model with scikit-learn’s k-Nearest Neighbors implementation.
5. Classify an unknown user: Given an unknown user, generate visualizations and an overall classification of their Twitter tweet language.

# Technologies used
- Python + Django web framework
- scikit-learn & IBM Watson intelligence APIs
- chart.js & Material Bootstrap

![](/static/images/2016-08-01-twitter-sentiment-analysis/twitter-sentiment-analysis-a.png)

![](/static/images/2016-08-01-twitter-sentiment-analysis/twitter-sentiment-analysis-b.png)

![](/static/images/2016-08-01-twitter-sentiment-analysis/twitter-sentiment-analysis-c.png)
