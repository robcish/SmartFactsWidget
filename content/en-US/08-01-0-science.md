---
id: 08-01-0-science
locale: en-US
month: 8
day: 1
sequence_index: 0
category: science
title: "PlayStation 3s That Broke HTTPS"
teaser: In 2008 researchers used a cluster of PlayStation 3 consoles to forge a trusted web certificate by exploiting MD5 weaknesses.
published: true
version: 1
---
At the 25th Chaos Communication Congress in 2008, a team of researchers revealed they had used **200 PlayStation 3 consoles** to generate an MD5 collision. The result was a **rogue Certificate Authority certificate** that browsers trusted completely.

With that forged CA, the team could mint valid HTTPS certificates for *any* website — enabling undetectable man-in-the-middle attacks. They chose PS3s because the Cell processor's SPUs were exceptionally fast at the parallel math needed for collision-finding. The demo prompted certificate authorities worldwide to **abandon MD5** and switch to SHA-based signatures.

[MD5 (Wikipedia)](https://en.wikipedia.org/wiki/MD5)
