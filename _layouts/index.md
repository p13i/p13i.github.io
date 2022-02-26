---
layout: base
---

<div class="row index">
  <div class="col-12">
    <hr />
    <h3 class="hey">hey there! 😁</h3>
    <hr />
  </div>
  <div class="col-12 col-md-6 col-lg-4">
    <div class="row">
      <div class="col-12">
        <img src="{{ site.data.images.headshot.src }}" width="100%" />
      </div>
      <div class="col-12">
        <hr />
        {{ content }}
      </div>
      <div class="col-12">
        <hr />
        {% include _my_links.html %}
      </div>
    </div>
  </div>
  <div class="col-12 col-md-6 col-lg-8">
    {% for post in site.posts %}
        {% if post.categories contains "research" %}
            {% include _post_card.html post=post %}
        {% endif %}
    {% endfor %}
  </div>
</div>
