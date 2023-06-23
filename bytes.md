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
            <div class="card-columns">
            {% for byte in site.bytes %}
                    {% include _byte.html byte=byte %}
            {% endfor %}
            </div>
        </div>
</div>
