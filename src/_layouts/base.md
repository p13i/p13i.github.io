---
layout: compress
regenerate: true
---

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta http-equiv="x-ua-compatible" content="ie=edge">

    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
    <link rel="icon" href="/favicon.ico" type="image/x-icon">

    <title>Pramod Kotipalli</title>

    <style>
        {% capture inline_css %}
        {% include inline.scss %}
        {% endcapture %}
        {{ inline_css | scssify }}
    </style>
    
    {% seo %}

</head>
<body>

    {% if jekyll.environment == "stanford" %}
    
<div class="container-fluid" style="height: 1.5em;background: url('/static/images/header-stanford.jpg') no-repeat top;background-size: cover;width: 100%;"></div>

    {% else %}
    
<div class="container-fluid" style="
height: 1em;
background: url('/static/images/header.jpg') no-repeat center top"></div>

    {% endif %}

{% include _navbar.html %}

<div class="container content">
    {{ content }}
</div>

<script type="text/javascript" src="/js/main.js"></script>
 
</body>
</html>
