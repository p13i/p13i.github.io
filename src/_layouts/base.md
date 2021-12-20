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

<div class="container-fluid" style="
height: 1em;
background: url('https://user-images.githubusercontent.com/13140065/146843822-cd8dd013-15b5-461c-a45d-db01aa000451.jpg') no-repeat center top"></div>

{% include _navbar.html %}

<div class="container content">
    {{ content }}
</div>

<script type="text/javascript" src="/js/main.js"></script>
 
</body>
</html>
