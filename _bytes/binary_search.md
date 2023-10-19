---
layout: post
title: Binary search
date: 2021-04-12
programming_language: "csharp"
description: "For interview prep, why else?"
image: https://user-images.githubusercontent.com/13140065/169116098-56d65621-69f3-4507-82e4-aaefe55986c9.png
---

```csharp
int BinarySearch(
    int[] array,
    int value,
    int start,
    int end)
{
    if (start > end)
    {
        return -1;
    }

    int middle = (start + end) / 2;

    if (array[middle] == value)
    {
        return middle;
    }

    if (value < array[middle])
    {
        return BinarySearch(array, value, start, middle - 1);
    }
    else
    {
        return BinarySearch(array, value, middle + 1, end);
    }
}
```
