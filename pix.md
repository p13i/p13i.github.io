---
title: Photography
layout: base
---

<hr/>

All my cute photos I'd like to share with the world.

{% assign all_photo_tags = "" | split: "" %}
{% for photo in site.data.pix %}
{% if photo.tags %}
{% for tag in photo.tags %}
{% unless all_photo_tags contains tag %}
{% assign all_photo_tags = all_photo_tags | push: tag %}
{% endunless %}
{% endfor %}
{% endif %}
{% endfor %}
{% assign all_photo_tags = all_photo_tags | sort %}
{% if all_photo_tags != empty %}
<div class="gallery-tag-summary">
  <hr />
  <div class="gallery-tag-summary-title">Albums</div>
  <div class="gallery-tag-summary-list">
    {% for tag in all_photo_tags %}
    {% assign album_href = tag | slugify | prepend: "/pix/" %}
    {% include _tag.html tag=tag href=album_href %}
    {% endfor %}
  </div>
</div>
{% endif %}

<hr/>

{% include _gallery.html %}
