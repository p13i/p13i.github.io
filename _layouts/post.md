---
layout: base
---

<hr/>

<div class="row post">
    <div class="col-12">
        <h1 class="title">{{ page.title }}</h1>
        <hr/>
    </div>
    <div class="col-12 col-lg-4">
        {% if page.image %}
            <img src="{{ page.image }}"/>
        {% endif %}
        <hr/>
        <p class="description">{{ page.description }}</p>
        <hr/>
        <p class="date">{{ page.date | date_to_long_string: "ordinal", "US" }}</p>
        <hr/>
        {% include _post_tags.html post=page %}
        {% if page.downloads %}
            <hr/>
            <div class="list-group">
            {% for download in page.downloads %}
                {% include _download_btn.html url=download.url name=download.name %}
            {% endfor %}
            </div>
            <hr/>
        {% endif %}
        <hr/>
        <nav id="toc" data-toggle="toc" class="sticky-top"></nav>
    </div>
    <div class="col-12 col-lg-8 order-lg-last">
        <div class="post">
            <div class="{% if page.default_image_fullwidth %}default-image-fullwidth{% endif %}">
                {{ content }}
            </div>
            {% include _copyright.html %}
        </div>
    </div>
</div>
