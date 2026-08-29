---
layout: compress
---

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1, shrink-to-fit=no"
    />
    <meta http-equiv="x-ua-compatible" content="ie=edge" />
    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
    <link rel="icon" href="/favicon.ico" type="image/x-icon" />

    {% include _stylesheets.html %}

    {% seo %}

  </head>

  <body
    data-spy="scroll"
    data-target="#toc"
    {% if page.math == false %}data-katex="false"{% endif %}
  >
    <div
      class="container-fluid"
      style="
        height: 1em;
        background: url('{{ site.data.images.header.src }}')
          no-repeat center top;"></div>
    {% include _navbar.html %}
    <div class="container content">
      {{ content }}
    </div>
    {% include _javascripts.html %}
  </body>
</html>
