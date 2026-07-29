---
id: 07-29-0-technology
locale: pl-PL
month: 7
day: 29
sequence_index: 0
category: technology
title: "Dlaczego listy wiązane wciąż mają znaczenie"
teaser: Tablice wygrywają w dostępie swobodnym, ale listy wiązane górują przy szybkim wstawianiu i usuwaniu.
published: true
version: 1
---
W **liście wiązanej** każdy element wskazuje na kolejny, więc wstawienie lub usunięcie węzła zajmuje **O(1)** — wystarczy przepiąć kilka wskaźników. Ceną jest to, że dotarcie do *n*-tego elementu wymaga przejścia łańcucha od początku, co daje dostęp losowy w **O(n)**.

To dokładne przeciwieństwo tablicy, gdzie odczyt dowolnego indeksu jest natychmiastowy, ale wstawienie w środku wymaga przesunięcia wszystkich kolejnych elementów. Współczesne procesory preferują tablice ze względu na lokalność pamięci podręcznej, ale listy wiązane pozostają kluczowe w **planistach systemów operacyjnych**, alokatorach pamięci i stosach cofania, gdzie stałoczasowe łączenie ma większe znaczenie niż sekwencyjny odczyt.

[Lista wiązana (Wikipedia)](https://pl.wikipedia.org/wiki/Lista_(informatyka))
