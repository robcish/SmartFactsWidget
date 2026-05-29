#!/usr/bin/env python3
"""Publish facts for 22–28 May so Detail swipe-back has history before 29 May."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

FACTS: list[dict] = [
    {
        "id": "05-22-0-myth-busting",
        "month": 5,
        "day": 22,
        "sequence_index": 0,
        "category": "myth-busting",
        "en": {
            "title": "Goldfish do not have a 3-second memory",
            "teaser": "They can remember things for months.",
            "body": (
                "Experiments show goldfish can **remember feeding cues and routes** for weeks "
                "or longer — the famous “three-second memory” is a myth.\n\n"
                "[Goldfish (Wikipedia)](https://en.wikipedia.org/wiki/Goldfish)"
            ),
        },
        "pl": {
            "title": "Złote rybki nie mają pamięci na 3 sekundy",
            "teaser": "Potrafią pamiętać rzeczy przez wiele miesięcy.",
            "body": (
                "Badania pokazują, że złote rybki **pamiętają sygnały karmienia i trasy** "
                "przez tygodnie lub dłużej — legenda o „pamięci trzy sekundy” to mit.\n\n"
                "[Złota rybka (Wikipedia)](https://pl.wikipedia.org/wiki/Z%C5%82ota_rybka)"
            ),
        },
    },
    {
        "id": "05-22-1-reflection",
        "month": 5,
        "day": 22,
        "sequence_index": 1,
        "category": "reflection",
        "en": {
            "title": "You are a different reader than yesterday",
            "teaser": "Every fact you read leaves a small trace.",
            "body": (
                "Learning is not only about storing facts — it is about **noticing what surprises you**. "
                "That surprise is often where real understanding begins.\n\n"
                "What was the last fact that made you stop and think?"
            ),
        },
        "pl": {
            "title": "Czytasz inaczej niż wczoraj",
            "teaser": "Każdy przeczytany fakt zostawia po sobie ślad.",
            "body": (
                "Uczenie się to nie tylko zapamiętywanie — to też **zauważanie, co cię zaskakuje**. "
                "Właśnie tam często zaczyna się prawdziwe zrozumienie.\n\n"
                "Jaki był ostatni fakt, przy którym się zatrzymałeś?"
            ),
        },
    },
    {
        "id": "05-23-0-general",
        "month": 5,
        "day": 23,
        "sequence_index": 0,
        "category": "general",
        "en": {
            "title": "Honey can last for millennia",
            "teaser": "Archaeologists have opened pots of still-edible honey.",
            "body": (
                "Low moisture and natural acids make honey **hostile to bacteria**, "
                "so sealed honey can remain edible for thousands of years.\n\n"
                "[Honey (Wikipedia)](https://en.wikipedia.org/wiki/Honey)"
            ),
        },
        "pl": {
            "title": "Miód może przetrwać tysiąclecia",
            "teaser": "Archeolodzy otwierali dżbany z nadal jadalnym miodem.",
            "body": (
                "Niska wilgotność i naturalne kwasy sprawiają, że miód jest **niegościnny dla bakterii**, "
                "więc szczelnie zamknięty może być jadalny przez tysiące lat.\n\n"
                "[Miód (Wikipedia)](https://pl.wikipedia.org/wiki/Mi%C3%B3d)"
            ),
        },
    },
    {
        "id": "05-23-1-science",
        "month": 5,
        "day": 23,
        "sequence_index": 1,
        "category": "science",
        "en": {
            "title": "Bananas are slightly radioactive",
            "teaser": "They contain potassium-40 — a natural isotope.",
            "body": (
                "Bananas contain **potassium-40**, a radioactive isotope. The dose is tiny and harmless, "
                "but scientists jokingly use the “banana equivalent dose” as a fun scale.\n\n"
                "[Banana equivalent dose (Wikipedia)](https://en.wikipedia.org/wiki/Banana_equivalent_dose)"
            ),
        },
        "pl": {
            "title": "Banany są lekko radioaktywne",
            "teaser": "Zawierają potas-40 — naturalny izotop.",
            "body": (
                "W bananach jest **potas-40**, radioaktywny izotop. Dawka jest mikroskopijna i nieszkodliwa, "
                "ale naukowcy żartobliwie używają „bananowej dawki równoważnej” jako skali.\n\n"
                "[Banan (Wikipedia)](https://pl.wikipedia.org/wiki/Banan)"
            ),
        },
    },
    {
        "id": "05-24-0-history",
        "month": 5,
        "day": 24,
        "sequence_index": 0,
        "category": "history",
        "en": {
            "title": "The shortest war lasted about 38 minutes",
            "teaser": "Britain vs. Zanzibar, 1896.",
            "body": (
                "The **Anglo-Zanzibar War** of 27 August 1896 is often cited as the shortest recorded war, "
                "ending after roughly 38–45 minutes.\n\n"
                "[Anglo-Zanzibar War (Wikipedia)](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War)"
            ),
        },
        "pl": {
            "title": "Najkrótsza wojna trwała około 38 minut",
            "teaser": "Wielka Brytania kontra Zanzibar, 1896.",
            "body": (
                "**Wojna brytyjsko-zanzibarska** z 27 sierpnia 1896 r. bywa uznawana za najkrótszą "
                "udokumentowaną w historii — zakończyła się po około 38–45 minutach.\n\n"
                "[Wojna brytyjsko-zanzibarska (Wikipedia)](https://pl.wikipedia.org/wiki/Wojna_brytyjsko-zanzibarska)"
            ),
        },
    },
    {
        "id": "05-24-1-geography",
        "month": 5,
        "day": 24,
        "sequence_index": 1,
        "category": "geography",
        "en": {
            "title": "Vatican City is the world's smallest state",
            "teaser": "Under half a square kilometre.",
            "body": (
                "**Vatican City** covers about 0.49 km² and is an independent city-state surrounded by Rome.\n\n"
                "[Vatican City (Wikipedia)](https://en.wikipedia.org/wiki/Vatican_City)"
            ),
        },
        "pl": {
            "title": "Watykan to najmniejsze państwo świata",
            "teaser": "Poniżej pół kilometra kwadratowego.",
            "body": (
                "**Watykan** ma około 0,49 km² i jest niezależnym państwem-miastem otoczonym przez Rzym.\n\n"
                "[Watykan (Wikipedia)](https://pl.wikipedia.org/wiki/Watykan)"
            ),
        },
    },
    {
        "id": "05-25-0-biology",
        "month": 5,
        "day": 25,
        "sequence_index": 0,
        "category": "biology",
        "en": {
            "title": "You have more bacterial cells than human cells",
            "teaser": "Your microbiome is a ecosystem of its own.",
            "body": (
                "Estimates suggest the **microbes in and on your body** can outnumber your own human cells, "
                "though the exact ratio is debated and changes with counting methods.\n\n"
                "[Human microbiome (Wikipedia)](https://en.wikipedia.org/wiki/Human_microbiome)"
            ),
        },
        "pl": {
            "title": "Masz więcej komórek bakterii niż ludzkich",
            "teaser": "Twój mikrobiom to osobny ekosystem.",
            "body": (
                "Szacunki mówią, że **mikroby w i na twoim ciele** mogą przewyższać liczbę komórek ludzkich, "
                "choć dokładny stosunek bywa kwestionowany.\n\n"
                "[Mikrobiom (Wikipedia)](https://pl.wikipedia.org/wiki/Mikrobiom)"
            ),
        },
    },
    {
        "id": "05-25-1-animals",
        "month": 5,
        "day": 25,
        "sequence_index": 1,
        "category": "animals",
        "en": {
            "title": "An octopus has three hearts",
            "teaser": "Two pump blood to the gills, one to the body.",
            "body": (
                "Octopuses have **two branchial hearts** for the gills and one systemic heart for the rest of the body. "
                "The systemic heart even stops when they swim.\n\n"
                "[Octopus (Wikipedia)](https://en.wikipedia.org/wiki/Octopus)"
            ),
        },
        "pl": {
            "title": "Ośmiornica ma trzy serca",
            "teaser": "Dwa tłoczą krew do skrzeli, jedno do ciała.",
            "body": (
                "Ośmiornice mają **dwa serca skrzelowe** i jedno serce systemowe. "
                "To systemowe nawet przestaje bić, gdy zwierzę pływa.\n\n"
                "[Ośmiornica (Wikipedia)](https://pl.wikipedia.org/wiki/O%C5%9Bmiornica)"
            ),
        },
    },
    {
        "id": "05-26-0-technology",
        "month": 5,
        "day": 26,
        "sequence_index": 0,
        "category": "technology",
        "en": {
            "title": "The first computer bug was a moth",
            "teaser": "Found in a Harvard Mark II relay in 1947.",
            "body": (
                "Operators taped a **moth** found in a relay of the Harvard Mark II into the logbook — "
                "popularizing the term “debugging.”\n\n"
                "[Software bug (Wikipedia)](https://en.wikipedia.org/wiki/Software_bug)"
            ),
        },
        "pl": {
            "title": "Pierwszy „computer bug” to ćma",
            "teaser": "Znaleziona w przekaźniku Harvard Mark II w 1947.",
            "body": (
                "Operatorzy przykleili do dziennika **ćmę** znalezioną w przekaźniku Harvard Mark II — "
                "utrwalając termin „debugging”.\n\n"
                "[Błąd oprogramowania (Wikipedia)](https://pl.wikipedia.org/wiki/B%C5%82%C4%85d_oprogramowania)"
            ),
        },
    },
    {
        "id": "05-26-1-culture",
        "month": 5,
        "day": 26,
        "sequence_index": 1,
        "category": "culture",
        "en": {
            "title": "The Nobel Prizes are funded by dynamite",
            "teaser": "Alfred Nobel's will redirected his fortune.",
            "body": (
                "Alfred Nobel, inventor of dynamite, left his wealth to fund the **Nobel Prizes** "
                "after a premature obituary called him a “merchant of death.”\n\n"
                "[Alfred Nobel (Wikipedia)](https://en.wikipedia.org/wiki/Alfred_Nobel)"
            ),
        },
        "pl": {
            "title": "Nagrody Nobla finansuje dynamit",
            "teaser": "Testament Alfreda Nobla przekierował jego fortunę.",
            "body": (
                "Alfred Nobel, wynalazca dynamitu, przeznaczył majątek na **nagrody Nobla** "
                "po przedwczesnym nekrologu, który nazwał go „kupcem śmierci”.\n\n"
                "[Alfred Nobel (Wikipedia)](https://pl.wikipedia.org/wiki/Alfred_Nobel)"
            ),
        },
    },
    {
        "id": "05-27-0-food",
        "month": 5,
        "day": 27,
        "sequence_index": 0,
        "category": "food",
        "en": {
            "title": "Carrots do not give you night vision",
            "teaser": "That story was wartime propaganda.",
            "body": (
                "The UK promoted **carrots for night vision** during World War II to hide radar advances. "
                "Carrots are healthy, but they will not turn you into a cat.\n\n"
                "[Carrot (Wikipedia)](https://en.wikipedia.org/wiki/Carrot)"
            ),
        },
        "pl": {
            "title": "Marchewka nie daje noktowizji",
            "teaser": "To opowieść z czasów propagandy wojennej.",
            "body": (
                "W czasie II wojny światowej UK promowało **marchewkę dla lepszego widzenia w nocy**, "
                "by ukryć radar. Marchewka jest zdrowa, ale nie zamieni cię w kota.\n\n"
                "[Marchew (Wikipedia)](https://pl.wikipedia.org/wiki/Marchew_zwyczajna)"
            ),
        },
    },
    {
        "id": "05-27-1-sport",
        "month": 5,
        "day": 27,
        "sequence_index": 1,
        "category": "sport",
        "en": {
            "title": "Olympic gold medals are mostly silver",
            "teaser": "They need only a thin layer of gold.",
            "body": (
                "Modern Olympic **gold medals** are required to be at least 92.5% silver, "
                "with a minimum of 6 grams of gold plating.\n\n"
                "[Olympic medal (Wikipedia)](https://en.wikipedia.org/wiki/Olympic_medal)"
            ),
        },
        "pl": {
            "title": "Złote medale olimpijskie to głównie srebro",
            "teaser": "Wystarczy cienka warstwa złota.",
            "body": (
                "Współczesne **złote medale olimpijskie** muszą mieć co najmniej 92,5% srebra "
                "i minimum 6 gramów złocenia.\n\n"
                "[Medal olimpijski (Wikipedia)](https://pl.wikipedia.org/wiki/Medal_olimpijski)"
            ),
        },
    },
    {
        "id": "05-28-0-psychology",
        "month": 5,
        "day": 28,
        "sequence_index": 0,
        "category": "psychology",
        "en": {
            "title": "The placebo effect is real medicine",
            "teaser": "Expectation can change how you feel.",
            "body": (
                "Even inactive treatments can trigger **measurable changes** when people believe they help — "
                "which is why clinical trials use blinded controls.\n\n"
                "[Placebo (Wikipedia)](https://en.wikipedia.org/wiki/Placebo)"
            ),
        },
        "pl": {
            "title": "Efekt placebo to prawdziwa medycyna",
            "teaser": "Oczekiwanie potrafi zmienić samopoczucie.",
            "body": (
                "Nawet nieaktywne substancje mogą wywołać **mierzalne zmiany**, gdy wierzysz, że pomagają — "
                "dlatego badania kliniczne stosują ślepe kontrole.\n\n"
                "[Placebo (Wikipedia)](https://pl.wikipedia.org/wiki/Placebo)"
            ),
        },
    },
    {
        "id": "05-28-1-language",
        "month": 5,
        "day": 28,
        "sequence_index": 1,
        "category": "language",
        "en": {
            "title": "Papua New Guinea has hundreds of languages",
            "teaser": "Linguistic diversity at its extreme.",
            "body": (
                "With over **800 living languages**, Papua New Guinea is one of the most linguistically diverse "
                "places on Earth.\n\n"
                "[Languages of Papua New Guinea (Wikipedia)](https://en.wikipedia.org/wiki/Languages_of_Papua_New_Guinea)"
            ),
        },
        "pl": {
            "title": "Papua-Nowa Gwinea ma setki języków",
            "teaser": "Ekstremalna różnorodność językowa.",
            "body": (
                "Ponad **800 żywych języków** czyni Papuę-Nową Gwineę jednym z najbardziej zróżnicowanych "
                "językowo miejsc na Ziemi.\n\n"
                "[Języki Papui-Nowej Gwinei (Wikipedia)](https://pl.wikipedia.org/wiki/J%C4%99zyki_Papui-Nowej_Gwinei)"
            ),
        },
    },
]


def write_md(locale: str, fact: dict, block: dict) -> None:
    path = CONTENT / locale / f"{fact['id']}.md"
    frontmatter = f"""---
id: {fact['id']}
locale: {locale}
month: {fact['month']}
day: {fact['day']}
sequence_index: {fact['sequence_index']}
category: {fact['category']}
title: {block['title']}
teaser: {block['teaser']}
published: true
version: 1
---
{block['body']}
"""
    path.write_text(frontmatter, encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


def main() -> None:
    for fact in FACTS:
        write_md("en-US", fact, fact["en"])
        write_md("pl-PL", fact, fact["pl"])
    print(f"\nPublished {len(FACTS)} days × 2 slots × 2 locales.")


if __name__ == "__main__":
    main()
