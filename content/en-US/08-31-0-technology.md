---
id: 08-31-0-technology
locale: en-US
month: 8
day: 31
sequence_index: 0
category: technology
title: Timsort is younger than Python
teaser: Python existed for more than a decade before Tim Peters designed Timsort for it in 2002.
published: true
version: 1
---
Timsort became famous as the default sorting algorithm in Python and later in Java, but it is surprisingly recent. Tim Peters created it in **2002** by blending ideas from merge sort and insertion sort.

Its clever trick is to exploit runs that are already ordered in real-world data. Instead of treating every list as random chaos, Timsort looks for existing structure and turns that into faster practical performance.

[Timsort (Wikipedia)](https://en.wikipedia.org/wiki/Timsort)
