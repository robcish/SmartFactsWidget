---
id: 07-29-0-technology
locale: en-US
month: 7
day: 29
sequence_index: 0
category: technology
title: "Why Linked Lists Still Matter"
teaser: Arrays win at random access, but linked lists dominate when you need fast inserts and deletes.
published: true
version: 1
---
In a **linked list**, each element points to the next, so inserting or removing a node takes **O(1)** time — you just rewire a couple of pointers. The tradeoff is that finding the *n*-th element requires walking the chain from the start, making random access **O(n)**.

This is the mirror image of arrays, where reading any index is instant but inserting in the middle means shifting every subsequent element. Modern CPUs favour arrays because of cache locality, yet linked lists remain essential inside **operating system schedulers**, memory allocators, and undo-history stacks where constant-time splicing matters more than sequential reads.

[Linked list (Wikipedia)](https://en.wikipedia.org/wiki/Linked_list)
