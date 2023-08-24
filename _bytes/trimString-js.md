---
layout: post
title: "Trim whitspace from either end"
programming_language: JavaScript
date: 2023-08-24
---

# `trimString.js`

Gets rid of whitespace on either side of a string and returns a new string. For example, `trimString(" abc ")` will result in `"abc"`.

```js
// https://stackoverflow.com/a/3084733/5071723
function trimString(str) {
  return str.replace(/^\s+|\s+$/g, "");
}
```
