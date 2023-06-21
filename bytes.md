---
title: code4all
layout: base
---

<div class="row">
    <div class="col-12">
        <hr/>
        <h1>{{ page.title }}</h1>
        <hr/>
        <div class="row">
            {% for byte in site.bytes %}
                <div class="col-lg-3 col-6 col-xs-12">
                    {% include _byte.html byte=byte %}
                </div>
            {% endfor %}
        </div>
</div>
