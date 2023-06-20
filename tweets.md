---
title: Twit-a-Verse
layout: base
---

<br/>

<div class="row">
    <div class="col-lg-2 col-md-0"></div>
    <div class="col-lg-8 col-md-12" style="background-color: aliceblue; border-radius: 1em; padding: 2em; box-shadow: inset 0px 0px 8px 0px #1d9bf0;">
        <h1 style="color: #1d9bf0; font-weight: 900;">{{ page.title }}</h1>
        <hr/>
        <div class="row">
            <div class="col-12">
                {% assign sorted = site.tweets | sort: 'num' | reverse  %}
                {% for tweet in sorted %}
                    {% include _tweet.html tweet=tweet %}
                {% endfor %}
            </div>
        </div>
    </div>
</div>
