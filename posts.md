---
title: Posts
layout: base
---

{% include _get_all_tags.html %}

<div class="row">
    <div class="col-lg-2 col-md-0"></div>
    <div class="col-lg-8 col-md-12">
        <hr/>
        <h1>Posts</h1>
        {% include _all_tags.html %}
        <hr/>
        <div class="row">
            <div class="col-12">
                {% for post in site.posts %}
                {% include _post_card.html post=post %}
                {% endfor %}
            </div>
        </div>
    </div>
</div>
