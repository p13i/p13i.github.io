---
layout: base
---

<div class="row index">
  <div class="col-12">
    <hr />
    <h3 class="hey">hey there! 😁</h3>
    <hr />
  </div>
  <div class="col-12 col-md-4 col-lg-3">
    <div class="row">
      <div class="col-md-12 col-sm-4 col-4">
        <img src="{{ site.data.images.headshot.src }}" width="100%" />
      </div>
      <div class="col-md-12 col-sm-8 col-8">
        <div class="d-sm-none d-none d-md-inline"><hr /></div>
        {{ content }}
      </div>
      <div class="col-12">
        <hr />
        {% include _my_links.html %}
      </div>
    </div>
  </div>
  <div class="col-12 col-md-8 col-lg-9">
    {% for post in site.posts %}
        {% if post.featured %}
            {% include _post_card.html post=post %}
        {% endif %}
    {% endfor %}
  </div>
</div>
