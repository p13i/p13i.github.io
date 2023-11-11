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
    <meta property="og:title" content="{% if page.title %}{{ page.title }}&nbsp;|&nbsp;{% endif %}Pramod Kotipalli" />
    <meta property="og:image" content="{% if page.image.src %}{{ page.image.src }}{% else %}{{ page.image.src }}{% endif %}" />
    <title>
      {% if page.title %}{{ page.title }}&nbsp;|&nbsp;{% endif %}Pramod Kotipalli
    </title>
  </head>

  <body data-spy="scroll">
      {{ content }}
  </body>
</html>
