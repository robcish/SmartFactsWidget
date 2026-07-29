---
id: 07-31-0-technology
locale: en-US
month: 7
day: 31
sequence_index: 0
category: technology
title: "When Browsers Banned SHA-1 Certificates"
teaser: In 2017 every major browser stopped trusting SHA-1 SSL certificates after researchers proved the hash could be forged.
published: true
version: 1
---
For years, security experts warned that **SHA-1** was too weak for SSL/TLS certificates, but migration was slow. The tipping point came in February 2017 when Google and CWI Amsterdam published the **SHAttered** attack — the first practical SHA-1 collision, producing two different PDFs with the same hash.

Within weeks, Chrome, Firefox, Edge, and Safari all **rejected SHA-1 certificates** by default. Certificate authorities had already been issuing SHA-256 replacements, but SHAttered turned a theoretical risk into a demonstrated exploit, forcing the last holdouts to upgrade overnight.

[SHA-1 (Wikipedia)](https://en.wikipedia.org/wiki/SHA-1)
