---
id: 09-02-1-technology
locale: pl-PL
month: 9
day: 2
sequence_index: 1
category: technology
title: Quicksort wygrywa, bo lubi cache
teaser: Praktyczna przewaga quicksorta czesto wynika z pracy pamieci: sortuje w miejscu i sprawnie dotyka sasiednich danych.
published: true
version: 1
---
Srednia zlozonosc quicksorta to **O(n log n)**, ale jego szybkosc w praktyce czesto bierze sie ze sprzyjajacego zachowania pamieci. Poniewaz dzieli tablice w miejscu, dobrze wykorzystuje cache procesora i unika dodatkowego kopiowania potrzebnego w niektorych innych metodach.

To przypomina, ze wydajnosc algorytmu nie zalezy tylko od notacji asymptotycznej. We wspolczesnych komputerach wzorzec dostepu do pamieci bywa niemal tak samo wazny jak formalna liczba porownan.

[Quicksort (Wikipedia)](https://pl.wikipedia.org/wiki/Quicksort)
