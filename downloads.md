---
title: Downloads for you!
layout: base
---

<div class="row">
    <div class="col-12">
        <hr/>

        <h1>Downloads</h1>

        <hr/>

        <p>3D assets, images, and easy-to-build source for most of my work.</p>
        
        <p>I am a <strong>strong</strong> believer in open-sourcing whatever I can so that others may learn from my work, as I have learned from countless others.</p>

        <hr/>

        <div class="row">
            <div class="card-columns">

            {% for post in site.posts %}

            {% if post.downloads %}
            
            <div class="card">
                <img src="{{ site.data.images.loading.src }}"
                    data-src="{{ post.image }}"
                    class="card-img-top lazyload">
                <div class="card-body">
                  <h5 class="card-title">{{ post.title }}</h5>
                  <p class="card-text">{{ post.description }}</p>
                </div>
                <ul class="list-group list-group-flush">
                    {% for download in post.downloads %}

                    <a class="list-group-item list-group-item-action" href="{{ download.url }}" target="_blank">{{ download.name }}&nbsp;&#187;</a>
                    
                    {% endfor %}
                </ul>
                <div class="card-body">
                  <a href="{{ post.url }}" class="card-link">Go to post »</a>
                </div>
              </div>

              {% endif %}

            {% endfor %}
            
            </div>

        </div>

        {% include _copyright.html %}
    </div>
</div>