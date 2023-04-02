---
title: Some of my writing
layout: base
---

{% include _get_all_tags.html category='writing' %}

<div class="row">
    <div class="col-lg-2 col-md-0"></div>
    <div class="col-lg-8 col-md-12">
        <hr/>
        <h1>Writing</h1>
        {% include _all_tags.html %}
        <hr/>
        <div class="row">
            <div class="col-12">
                {% for post in site.posts %}
                {% if post.categories contains 'writing' %}
                {% include _post_card.html post=post %}
                {% endif %}
                {% endfor %}
            </div>
        </div>
    </div>
</div>
