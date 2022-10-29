---
layout: compress
---

<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1, shrink-to-fit=no"
    />
    <meta http-equiv="x-ua-compatible" content="ie=edge" />
    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
    <link rel="icon" href="/favicon.ico" type="image/x-icon" />

    <title>Pramod Kotipalli</title>

    {% include _stylesheets.html %}

    {% seo %}
  </head>

  <body data-spy="scroll" data-target="#toc">
    <div
      class="container-fluid"
      style="
        height: 1em;
        background: url('{{ site.data.images.header.src }}')
          no-repeat center top;
      "
    ></div>

    {% include _navbar.html %}

    <div class="container content">
      {{ content }}
    </div>

    {% include _javascripts.html %}

  </body>
</html>
