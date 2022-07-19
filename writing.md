---
title: Some of my writing
layout: base
---

{% include _get_all_tags.html category='writing' %}

<div class="row">
    <div class="col-12">
        <hr/>

        <h1>Writing</h1>

        <hr/>

        {% for tag in tags %}
        <a href="/tags/#{{ tag | slugify }}" class="badge badge-light"> {{ tag | replace: '-', ' ' | upcase }} </a>
        {% endfor %}

        <hr/>

        <div class="row">
            <div class="col-12">
                {% for post in site.posts %}

                {% if post.categories contains 'writing' %}

                {% include _post_list_item.html post=post %}

                {% endif %}

                {% endfor %}
            </div>
        </div>
    </div>
</div>
