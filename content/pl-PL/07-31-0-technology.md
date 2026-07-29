---
id: 07-31-0-technology
locale: pl-PL
month: 7
day: 31
sequence_index: 0
category: technology
title: "Gdy przeglądarki zakazały certyfikatów SHA-1"
teaser: W 2017 roku wszystkie główne przeglądarki przestały ufać certyfikatom SSL opartym na SHA-1 po udowodnieniu możliwości kolizji.
published: true
version: 1
---
Eksperci od lat ostrzegali, że **SHA-1** jest zbyt słaby dla certyfikatów SSL/TLS, ale migracja szła powoli. Punkt zwrotny nastąpił w lutym 2017 roku, gdy Google i CWI Amsterdam opublikowali atak **SHAttered** — pierwszą praktyczną kolizję SHA-1, generującą dwa różne pliki PDF o tym samym hashu.

W ciągu tygodni Chrome, Firefox, Edge i Safari domyślnie **odrzuciły certyfikaty SHA-1**. Urzędy certyfikacji już wcześniej wydawały zamienniki SHA-256, ale SHAttered zamienił teoretyczne ryzyko w udowodniony exploit, zmuszając ostatnich opornych do natychmiastowej aktualizacji.

[SHA-1 (Wikipedia)](https://pl.wikipedia.org/wiki/SHA-1)
