---
layout: base
---

<hr/>

<div class="row post">
    <div class="col-12">
        <div class="row">
            <div class="col-12 col-lg-4"></div> 
            <div class="col-12 col-lg-8">
                <h1 class="title" data-toc-skip>{{ page.title | markdownify }}</h1>
            </div>
        </div>
    </div>
    <div class="col-12">
        <hr/>
    </div>
    <div class="col-12">
        <div class="row">
            <div class="col-12 col-lg-4">
                {% if page.image %}
                    <img src="{{ page.image }}"/>
                    <hr/>
                {% endif %}
                {% if page.redirect_from %}
                    <a href="https://p13i.io/{{ page.redirect_from }}">https://p13i.io/{{ page.redirect_from }}</a>
                    <hr/>
                {% endif %}
                {% if page.description %}
                    <p class="description">{{ page.description | markdownify }}</p>
                    <hr/>
                {% endif %}
                <p class="date">{{ page.date | date_to_long_string: "ordinal", "US" }}</p>
                <hr/>
                {% include _post_tags.html post=page %}
                <hr/>
                {% if page.downloads %}
                    <div class="list-group">
                    {% for download in page.downloads %}
                        {% include _download_btn.html url=download.url name=download.name %}
                    {% endfor %}
                    </div>
                    <hr/>
                {% endif %}
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
    </div>
</div>
