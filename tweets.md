---
title: My "Tweets"
layout: base
---

<div class="row">
    <div class="col-lg-2 col-md-0"></div>
    <div class="col-lg-8 col-md-12">
        <hr/>
        <h1>{{ page.title }}</h1>
        <hr/>
        <div class="row">
            <div class="col-12">
                {% for tweet in site.data.tweets %}
                    {% include _tweet.html tweet=tweet %}
                {% endfor %}
            </div>
        </div>
    </div>
</div>
