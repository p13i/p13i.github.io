---
title: Photography
layout: base
theme: dark
---

<style>
  .my-card-columns {
    -webkit-column-count: 3;
    -moz-column-count: 3;
    column-count: 3;
    -webkit-column-gap: 1.25rem;
    -moz-column-gap: 1.25rem;
    column-gap: 1.25rem;
    orphans: 1;
    widows: 1;
  }

  .card-columns .card {
    display: inline-block;
    width: 100%;
  }

  .my-card {
    padding: 1em;
    background-color: black;
  }
  body {
    background-color: black;
  }
</style>

<script type="text/javascript">
  document.addEventListener(
    "DOMContentLoaded",
    function () {
      const slider = document.getElementById("slider");
      const numColumnsSpan =
        document.getElementById("num-columns");
      const cardsDiv = document.getElementById(
        "my-card-columns",
      );
      function setColumnsCount() {
        cardsDiv.style.columnCount = slider.value;
        numColumnsSpan.textContent = slider.value;
      }
      slider.addEventListener("input", () =>
        setColumnsCount(slider.value),
      );
      setColumnsCount(3);
    },
  );
</script>

<br />
<div
  style="
    position: absolute;
    left: 0;
    right: 0;
    width: 100%;
    background-color: black;
    color: white;
  "
>
  <div class="container-fluid">
    <div class="row">
      <p>i'm a vsco girl.. in a vosco world...</p>
      <hr />
      <div class="float-right">
        <label for="slider"
          >Set number of columns in grid (between 1 and 8),
          currently
          <strong><span id="num-columns"></span></strong
          >:</label
        >
        <br />
        <input
          type="range"
          id="slider"
          name="slider"
          min="1"
          max="8"
          value="3"
        />
      </div>
    </div>
    <hr />
    <div class="row">
      <div
        class="card-columns my-card-columns"
        id="my-card-columns"
      >
        {% for post in site.posts %} {% if post.downloads %}
        <div class="card my-card" style="border-width: 0">
          <img
            src="{{ site.data.images.loading.src }}"
            data-src="{{ post.image }}"
            class="card-img-top lazyload"
          />
        </div>
        {% endif %} {% endfor %}
      </div>
    </div>
  </div>
</div>
