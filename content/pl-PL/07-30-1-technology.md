---
id: 07-30-1-technology
locale: pl-PL
month: 7
day: 30
sequence_index: 1
category: technology
title: "Dlaczego Git używa skrótów SHA-1"
teaser: Git hashuje każdy commit algorytmem SHA-1 — nie dla bezpieczeństwa, lecz by zagwarantować, że kod nigdy po cichu się nie zmieni.
published: true
version: 1
---
Gdy Linus Torvalds projektował Gita w 2005 roku, wybrał **SHA-1** do odciskania palca każdego obiektu — blobów, drzew, commitów i tagów. Celem była **integralność danych**, a nie bezpieczeństwo kryptograficzne: jeśli choćby jeden bit zmieni się podczas przechowywania lub przesyłu, hash się nie zgodzi i Git to wykryje.

Sam Torvalds ujął to prosto: *„Możesz mieć pewność, że pięć lat później odzyskasz dokładnie te same dane, które włożyłeś."* Po ataku kolizyjnym SHAttered w 2017 roku Git rozpoczął migrację do **SHA-256**, ale pierwotna filozofia pozostaje — hashe to adresy treści, nie kotwice zaufania.

[Git (Wikipedia)](https://pl.wikipedia.org/wiki/Git_(oprogramowanie))
