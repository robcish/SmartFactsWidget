---
id: 07-30-1-technology
locale: en-US
month: 7
day: 30
sequence_index: 1
category: technology
title: "Why Git Uses SHA-1 Hashes"
teaser: Git hashes every commit with SHA-1 — not for security, but to guarantee your code never silently changes.
published: true
version: 1
---
When Linus Torvalds designed Git in 2005, he chose **SHA-1** to fingerprint every object — blobs, trees, commits, and tags. The goal was **data integrity**, not cryptographic security: if even one bit flips in storage or transit, the hash won't match and Git will notice.

Torvalds himself put it simply: *"You can trust that five years later, you get the exact same data you put in."* After the 2017 SHAttered collision attack, Git began transitioning to **SHA-256**, but the original design philosophy remains — hashes are content addresses, not trust anchors.

[Git (Wikipedia)](https://en.wikipedia.org/wiki/Git)
