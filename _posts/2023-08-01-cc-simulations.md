---
title: "C++ simulations in the browser"
categories:
  - research
  - design
  - engineering
tags:
  - "c++"
  - computer-graphics
layout: post
description: ""
image: "https://p13i.io/assets/2023-08-01-cc-simulations-thumbnail.jpg"
featured: true
---

This is a continually-improving rendering program being built from scratch in C++, and run in your browser.

<hr/>
<div id="spinner"></div>
<div id="status">Downloading...</div>
<hr/>
<span id="controls">
    <span>
        <input type="checkbox" id="resize">Resize canvas
    </span>
    <span>
        <input type="checkbox" id="pointerLock" checked="checked">Lock/hide mouse pointer &nbsp;&nbsp;&nbsp;
    </span>
    <span>
        <input type="button" value="Fullscreen" onclick='Module.requestFullscreen(document.getElementById("pointerLock").checked,document.getElementById("resize").checked)'>
    </span>
</span>
<progress value="0" max="100" id="progress" hidden="1"></progress>
<hr/>
<canvas id="canvas" oncontextmenu="event.preventDefault()" tabindex="-1"></canvas>
<hr/>
<p>Console output:</p>
<textarea id="output" rows="5" cols="40"></textarea>
<script type="text/javascript" src="https://p13i.io/cs/wasm.js"></script>
<script type="text/javascript" src="https://p13i.io/cs/index.js"></script>
