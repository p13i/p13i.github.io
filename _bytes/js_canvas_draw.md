---
layout: post
title: simple javascript canvas draw frame function
programming_language: javascript
date: 2024-12-08
---

```js
var i = 0;
var oneSecondStartMs = 0;
var oneSecondEndMs = 0;
var drawMs = 0;
const canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
function drawImage() {
  const startMs = Date.now();
  if (i % FPS == 0) {
    oneSecondStartMs = startMs;
  }
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (var y = canvas.height - 1; y >= 0; y--) {
    for (var x = 0; x < canvas.width; x++) {
      var [r, g, b, a] = IMAGES[i][x][y];
      a = 1;
      ctx.fillStyle = `rgba( ${r} , ${g} , ${b}, ${a} )`;
      ctx.fillRect(x, y, 1, 1);
    }
  }
  const endMs = Date.now();
  if (i % FPS == FPS - 1) {
    oneSecondEndMs = endMs;
    const oneSceneSecondInMs =
      oneSecondEndMs - oneSecondStartMs;
    const fps = (FPS * 1000) / oneSceneSecondInMs;
    const message = `Drawing at ${fps.toFixed(2)} fps.`;
    document.getElementById("fps").innerHTML = message;
  }
  i = (i + 1) % IMAGES.length;
  drawMs = endMs - startMs;
  queueDrawImage();
}
```
