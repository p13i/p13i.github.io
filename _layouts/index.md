---
layout: base
---

<div class="row index">
  <div class="col-12">
    <hr />
    <h1 class="hey">Hi, I'm Pramod.</h1>
    <hr />
  </div>
  <div class="col-12 col-md-4 col-lg-3">
    <div class="row">
      <div class="col-12 col-sm-4 col-md-12">
        <img
          src="{{ site.data.images.headshot.src }}"
          alt="Portrait of Pramod Kotipalli"
          width="100%"
        />
      </div>
      <div class="col-12 col-sm-8 col-md-12">
        <div class="d-sm-none d-none d-md-inline"><hr /></div>
        {{ content }}
        <hr />
        {% include _my_links.html %}
      </div>
    </div>
  </div>
  <div class="col-12 col-md-8 col-lg-9">
    <h2>Research and engineering</h2>
    {% for post in site.posts %}
        {% if post.featured %}
          {% if post.categories contains "research" or post.categories contains "engineering" %}
            {% include _post_card.html post=post %}
          {% endif %}
        {% endif %}
    {% endfor %}
  </div>
</div>
