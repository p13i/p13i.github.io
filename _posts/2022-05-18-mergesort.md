---
title: Mergesort in C
date: "2022-05-18"
categories:
  - engineering
layout: post
description: "A cute implementation of mergesort in C"
image: "https://user-images.githubusercontent.com/13140065/169116098-56d65621-69f3-4507-82e4-aaefe55986c9.png"
downloads:
  - name: "💻 GitHub source"
    url: https://github.com/p13i/mergesort-c/blob/main/main.c#L27
---

In preparation for technical interviews, I implemented
mergesort in C. The [source on Github](https://github.com/p13i/mergesort-c/blob/main/main.c#L27)
has an extensive set of tests. I like how 'cute' the code
looks.

---

```c
int *MergeSort(int *array, int length)
{
    if (NULL == array || length < 1) {
        return NULL;
    }
    return MergeSortRecursive(array, length, 0, length);
}

// right is exclusive, array of [left, right)
int *MergeSortRecursive(int *array, int length, int left, int right)
{
    if ((right - left) == 1)
    {
        int *result = MakeArray(1);
        result[0] = array[left];
        return result;
    }

    int middle = (left + right) / 2;

    int leftLength = middle - left;
    int rightLength = right - middle;

    int *leftSide = MergeSortRecursive(array, length, left, middle);
    int *rightSide = MergeSortRecursive(array, length, middle, right);

    // Now merge the two halfs, k is index into mergedArray
    int i = 0, j = 0, k = 0;
    int *mergedArray = MakeArray(right - left);

    while (i < leftLength && j < rightLength)
    {
        if (leftSide[i] < rightSide[j])
        {
            mergedArray[k++] = leftSide[i++];
        }
        else
        {
            mergedArray[k++] = rightSide[j++];
        }
    }

    while (i < leftLength)
    {
        mergedArray[k++] = leftSide[i++];
    }

    while (j < rightLength)
    {
        mergedArray[k++] = rightSide[j++];
    }

    free(leftSide);
    free(rightSide);

    return mergedArray;
}

int *MakeArray(int length)
{
    int *array = malloc(sizeof(int) * length);
    // NULL check here?
    return array;
}
```
