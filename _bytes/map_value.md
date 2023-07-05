---
layout: post
title: "Map numbers from one range to another"
programming_language: TypeScript
date: 2021-02-23
---

# `mapValue.ts`

For example, `mapValue(1, 0, 2, 0, 10)` will result in `5`.

```ts
function mapValue(
  value: number,
  valueRangeStart: number,
  valueRangeEnd: number,
  newRangeStart: number,
  newRangeEnd: number
) {
  return (
    newRangeStart +
    ((newRangeEnd - newRangeStart) /
      (valueRangeEnd - valueRangeStart)) *
      (value - valueRangeStart)
  );
}
```
