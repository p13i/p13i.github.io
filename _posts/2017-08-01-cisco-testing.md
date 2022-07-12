---
title: Cisco Testing-as-a-Service
date: "2017-08-01"
categories:
- engineering
tags:
- software-engineering
- python
- django
- load-testing
- rest-api
- angularjs
- javascript
- typescript
- docker
- containerization
- orchestration
- elasticsearch
- logstash
- kibana
- postgresql
- jmeter
- java
- celery
- task-queue
- message-queue
- rabbitmq
- jenkins
- vagrant
- scripting
- shell
- linux
- networking
layout: post
author: Pramod Kotipalli
description: Easy-to-use high-scale testing orchestration software
image: "https://user-images.githubusercontent.com/13140065/178388342-22edb567-e4f0-43d0-9c28-96f7e2c70e9a.png"
default_image_fullwidth: true
subcategories:
- engineering
---

![]({{ page.image }})

During my internship at Cisco, I led two full-time employees
where we created a highly-scalable distributed HTTP load
testing framework. We built a simple-to-use RESTful API that
would manage and orchestrate thousands of Docker containers.
An easy-to-use front-end, written with AngularJS, would
allow QA Engineers to select a JMeter configuration file to
run across hundreds of worker Docker containers running
JMeter. Log files were collected and analyzed on an
Elasticsearch-Logstash-Kibana (ELK) stack.

This project required 3.5k lines of clean well-documented
Python, a complete AngularJS front-end involving 1.1k lines
of TypeScript, and 0.5k lines of HTML.

Our solution was deployed to customers like AT&T and Comcast
to the scale of 100k+ users.
