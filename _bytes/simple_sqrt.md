---
layout: post
title: "Simple square root implementation"
date: 2017-08-24
description: "For interview prep, why else?"
image: https://user-images.githubusercontent.com/13140065/169116098-56d65621-69f3-4507-82e4-aaefe55986c9.png
---

```java
/**
    * An Integer can take on values from -2^31 to + 2^31. The argument x can 
    * take on values from 0 to 2^31. This means that all outputs of sqrt(x) 
    * can only fall in the range of 1 to sqrt(2^31) because 2^31 is the
    * largest possible Integer input. Thus, we can limit our binary search
    * range to [1, min(x, sqrt(2^31))]
    */

// We compute this value once by means of the standard library or a 
// hand-computed number
static int MAX_SQUARE_ROOT_BOUND = (int) Math.sqrt(Integer.MAX_VALUE);

public static int sqrt(int x) {
    // Check value of x
    if (x < 0) {
        return -1;
    }

    if (x == 0) {
        return 0;
    }

    int start = 1;
    int end = Math.min(x, MAX_SQUARE_ROOT_BOUND);
    int flooredSqrt = -1;

    while (start <= end) {
        int middle = (start + end) / 2;

        // Faster than using Math.pow(middle, 2)
        int middleSquared = middle * middle;

        if (middleSquared > x) {
            // Our middleSquared estimate was too high so we adjust the 
            // end marker down
            end = middle - 1;
        } else if (middleSquared < x) {
            // Our middleSquared estimate was too low so we adjust the 
            // start marker up
            start = middle + 1;
            // If we adjusting the search range upwards, then we should 
            // save the existing estimate for the square-root. By saving 
            // this value here, we are essentially performing the flooring.
            flooredSqrt = middle;
        } else {  // squared == n
            // We found the square root exactly
            return middle;
        }
    }

    return flooredSqrt;
}
```