---
id: 09-02-1-technology
locale: en-US
month: 9
day: 2
sequence_index: 1
category: technology
title: Quicksort wins by liking the cache
teaser: Quicksort's big practical advantage is often memory behavior: it works in place and touches nearby data efficiently.
published: true
version: 1
---
Quicksort's average-case complexity is **O(n log n)**, but its real-world speed often comes from the hardware underneath. Because it partitions arrays in place, it tends to use memory caches well and avoids the extra copying some other sorts need.

That is a reminder that algorithm performance is not just about asymptotic notation. On modern machines, the pattern of memory access can matter almost as much as the formal count of comparisons.

[Quicksort (Wikipedia)](https://en.wikipedia.org/wiki/Quicksort)
