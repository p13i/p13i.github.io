---
title: code4all
layout: base
---

<div class="row">
    <div class="col-12">
        <h1>{{ page.title }}</h1>
        <div class="row">
            {% for byte in site.bytes %}
                <div class="col-3">
                    {% include _byte.html byte=byte %}
                </div>
            {% endfor %}
        </div>
</div>
