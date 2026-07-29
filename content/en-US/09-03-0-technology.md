---
id: 09-03-0-technology
locale: en-US
month: 9
day: 3
sequence_index: 0
category: technology
title: Radix sort can beat n log n
teaser: Radix sort avoids comparison limits by grouping values digit by digit instead of asking which pair is larger.
published: true
version: 1
---
Comparison sorts are bounded by the famous **O(n log n)** lower limit, but radix sort plays a different game. It processes keys digit by digit, so for fixed-width data like integers, it can run in effectively linear time.

That does not make it universally better. Radix sort works best when the data format is friendly, yet it remains a beautiful example of how changing the model of computation can sidestep an apparent barrier.

[Radix sort (Wikipedia)](https://en.wikipedia.org/wiki/Radix_sort)
