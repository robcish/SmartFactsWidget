---
id: 08-14-0-technology
locale: pl-PL
month: 8
day: 14
sequence_index: 0
category: technology
title: Go zaprojektowano, by programowanie znów było nudne
teaser: Ken Thompson i Rob Pike stworzyli Go w Google, by walczyć ze złożonością — celowo pomijając dziedziczenie i generyki, aby język pozostał prosty.
published: true
version: 1
---
Go powstał w **2009** roku z frustracji wolnymi czasami kompilacji C++ w Google. Jego twórcy — **Ken Thompson** (współtwórca Uniksa, UTF-8 i języka B) oraz **Rob Pike** (Plan 9, UTF-8) — celowo zaprojektowali go jako nudny: bez klas, bez dziedziczenia, bez wyjątków, minimalna składnia.

Kluczową cechą języka jest wbudowana **współbieżność** przez goroutines — lekkie wątki zajmujące zaledwie kilka kilobajtów pamięci każdy. Pojedynczy program w Go z łatwością obsługuje miliony jednoczesnych goroutines. To uczyniło Go domyślnym językiem infrastruktury chmurowej: Docker, Kubernetes i Terraform są napisane w Go.

[Go (język programowania) (Wikipedia)](https://pl.wikipedia.org/wiki/Go_(j%C4%99zyk_programowania))
