---
id: 08-01-0-science
locale: pl-PL
month: 8
day: 1
sequence_index: 0
category: science
title: "PlayStation 3, które złamały HTTPS"
teaser: W 2008 roku badacze użyli klastra konsol PlayStation 3 do sfałszowania zaufanego certyfikatu internetowego, wykorzystując słabości MD5.
published: true
version: 1
---
Na 25. Chaos Communication Congress w 2008 roku zespół badaczy ujawnił, że wykorzystał **200 konsol PlayStation 3** do wygenerowania kolizji MD5. Efektem był **fałszywy certyfikat urzędu certyfikacji**, któremu przeglądarki w pełni ufały.

Dzięki takiemu sfałszowanemu CA zespół mógł wystawiać ważne certyfikaty HTTPS dla *dowolnej* strony — umożliwiając niewykrywalne ataki typu man-in-the-middle. Wybrano PS3, ponieważ jednostki SPU procesora Cell były wyjątkowo szybkie w równoległych obliczeniach potrzebnych do znajdowania kolizji. Demonstracja skłoniła urzędy certyfikacji na całym świecie do **porzucenia MD5** i przejścia na podpisy oparte na SHA.

[MD5 (Wikipedia)](https://pl.wikipedia.org/wiki/MD5)
