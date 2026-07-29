---
id: 08-12-0-technology
locale: pl-PL
month: 8
day: 12
sequence_index: 0
category: technology
title: Rust gwarantuje bezpieczeństwo pamięci bez garbage collectora
teaser: Rust zaprojektowano, aby wyeliminować błędy uszkodzenia pamięci nękające C i C++ — osiągając bezpieczeństwo przez system własności zamiast garbage collectora.
published: true
version: 1
---
Graydon Hoare rozpoczął pracę nad Rustem jako osobisty projekt w Mozilli w **2006** roku, sfrustrowany błędami pamięci w kodzie C++ Firefoksa. Kluczową innowacją języka jest **system własności**: każda wartość ma dokładnie jednego właściciela, a kompilator wymusza reguły pożyczania w czasie kompilacji, wyłapując use-after-free, wyścigi danych i błędy pustych wskaźników, zanim kod w ogóle się uruchomi.

To podejście „abstrakcji bez kosztu" oznacza, że programy w Ruście działają tak szybko jak C/C++ bez poświęcania bezpieczeństwa. W 2023 roku kod w Ruście zaczął być przyjmowany do jądra Linuksa — kamień milowy, na który żaden język poza C czekał 30 lat.

[Rust (język programowania) (Wikipedia)](https://pl.wikipedia.org/wiki/Rust_(j%C4%99zyk_programowania))
