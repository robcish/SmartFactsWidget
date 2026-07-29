---
id: 08-31-0-technology
locale: pl-PL
month: 8
day: 31
sequence_index: 0
category: technology
title: Timsort jest mlodszy od Pythona
teaser: Python istnial ponad dekade, zanim Tim Peters zaprojektowal dla niego Timsort w 2002 roku.
published: true
version: 1
---
Timsort zaslynal jako domyslny algorytm sortowania w Pythonie, a pozniej takze w Javie, ale jest zaskakujaco mlody. Tim Peters stworzyl go w **2002 roku**, laczac pomysly z merge sorta i insertion sorta.

Jego sprytny pomysl polega na wykorzystywaniu fragmentow danych, ktore sa juz czesciowo uporzadkowane. Zamiast traktowac kazda liste jak przypadkowy chaos, Timsort szuka istniejacej struktury i przekuwa ja w lepsza wydajnosc.
