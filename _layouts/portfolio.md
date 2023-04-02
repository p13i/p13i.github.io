---
layout: base
---

{% include _get_all_tags.html category=page.data.include_category %}

<div class="row portfolio">
    <div class="col-12">
        <hr/>
        <h1>{{ page.title }}</h1>
        {% include _all_tags.html %}
        {% include _tiled_portfolio.html category=page.data.include_category %}
    </div>
</div>
