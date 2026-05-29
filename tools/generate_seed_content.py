#!/usr/bin/env python3
"""Generate seed Markdown facts for pl-PL and en-US."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"

FACTS = [
    ("science", "Sharks are older than trees", "Did you know sharks existed before trees?", "Sharks have roamed the oceans for more than **400 million years**. Trees appeared roughly **350 million years** ago.\n\nThat means sharks survived multiple mass extinctions long before forests covered the land."),
    ("psychology", "The spacing effect", "Reviewing over time beats cramming.", "Memory research shows that **spaced repetition** strengthens recall far better than one long session.\n\nSpreading study across days helps your brain consolidate information into long-term memory."),
    ("language", "Salary comes from salt", "The word salary has a salty origin.", "The English word **salary** comes from the Latin *salarium*, linked to payments that Roman soldiers sometimes received to buy **salt**.\n\nSalt was so valuable that it became a symbol of steady income."),
    ("history", "The Library of Alexandria", "A legendary center of ancient knowledge.", "The Library of Alexandria was one of the ancient world's greatest attempts to **collect human knowledge** in one place.\n\nIts exact fate is debated, but its legacy still symbolizes curiosity and learning."),
    ("mythology", "Atlas holds the sky", "Why we call map collections atlases.", "In Greek myth, **Atlas** was condemned to hold up the heavens. Renaissance mapmakers put his image on book covers.\n\nThat is why a book of maps became known as an **atlas**."),
    ("finance", "Compound interest", "Small gains can snowball over time.", "**Compound interest** means you earn returns not only on your original amount, but also on previously earned interest.\n\nOver long periods, steady contributions can grow surprisingly fast."),
    ("society", "The bystander effect", "More witnesses can mean less help.", "Social psychologists found that people are sometimes **less likely to help** in emergencies when others are present.\n\nShared responsibility can quietly reduce individual action."),
    ("philosophy", "Occam's razor", "Prefer simpler explanations when possible.", "**Occam's razor** suggests that when two explanations fit the facts, the simpler one is often preferable.\n\nIt is a tool for clarity, not proof."),
    ("myth-busting", "Goldfish memory", "Goldfish remember more than three seconds.", "Experiments show goldfish can remember feeding locations and cues for **weeks or months**.\n\nThe famous three-second myth is far too short."),
    ("general", "Honey never spoils", "Archaeologists found edible ancient honey.", "Honey's low moisture and natural acidity make it hostile to bacteria.\n\nSealed honey pots in tombs thousands of years old have still been found **safe to eat**."),
    ("science", "Bananas are berries", "Botany classifies fruit differently than kitchens do.", "In botanical terms, a berry develops from one flower with one ovary. By that definition, **bananas qualify**.\n\nStrawberries, meanwhile, are not true berries."),
    ("psychology", "The Zeigarnik effect", "Unfinished tasks stick in your mind.", "Bluma Zeigarnik noticed that people remember **interrupted tasks** better than completed ones.\n\nThat is one reason open loops feel mentally sticky."),
    ("language", "Alphabet order is arbitrary", "A-B-C order is not universal.", "The Latin alphabet order we use today is a **historical convention**, not a natural law.\n\nOther writing systems use completely different arrangements."),
    ("history", "The printing press", "Books changed faster than kings expected.", "Johannes Gutenberg's movable-type press made books **cheaper and faster** to produce.\n\nKnowledge spread widely, reshaping religion, science, and politics."),
    ("science", "Octopus hearts", "An octopus pumps blood with three hearts.", "Two hearts move blood through the gills, while a third pumps it to the rest of the body.\n\nWhen an octopus swims, the main heart often **rests**, which is one reason they prefer crawling."),
    ("culture", "Tea changed trade routes", "Tea shaped empires and daily rituals.", "Tea became one of the world's most traded commodities, influencing diplomacy, colonization, and everyday social life.\n\nA simple cup can carry centuries of history."),
    ("math", "Zero is younger than you think", "Zero as a number took centuries to spread.", "Ancient societies had symbols for absence, but using **zero as a full number** developed gradually.\n\nIt later became essential for modern mathematics."),
    ("biology", "Trees communicate", "Forests share resources underground.", "Trees can transfer nutrients through fungal networks often called the **wood wide web**.\n\nA forest behaves less like isolated plants and more like a cooperative system."),
    ("law", "Ignorantia juris non excusat", "Not knowing the law rarely excuses breaking it.", "Many legal systems hold that citizens are expected to follow laws even if they never read them.\n\nIt is a reason public legal education matters."),
    ("technology", "The first computer bug", "A real moth once caused a malfunction.", "In 1947, operators found a moth trapped in a relay of the Harvard Mark II computer.\n\nThe incident popularized the term **debugging**."),
    ("reflection", "Questions beat answers", "Curiosity keeps the mind flexible.", "A good question opens more paths than a rushed answer.\n\nThat is why daily facts work best when they invite you to wonder, not just memorize."),
]

PL_TITLES = [
    ("Rekin jest starszy niż drzewa", "Czy wiesz, że rekiny istniały przed drzewami?", "Rekiny pływają po oceanach od ponad **400 milionów lat**. Drzewa pojawiły się dopiero około **350 milionów lat** temu.\n\nRekiny przetrwały wiele masowych wymierań, zanim lasy w ogóle powstały."),
    ("Efekt spacingu", "Powtarzanie w odstępach działa lepiej niż wkuwanie.", "Badania pamięci pokazują, że **powtórki rozłożone w czasie** dają lepsze efekty niż jedna długa sesja.\n\nKrótkie powroty do materiału pomagają mózgowi utrwalać wiedzę."),
    ("Pensja ma słony początek", "Słowo pensja wiąże się z solą.", "Polskie słowo **pensja** ma korzenie w łacińskim *salarium*, czyli wypłacie związanej z zakupem **soli**.\n\nSól była tak cenna, że stała się symbolem regularnego dochodu."),
    ("Biblioteka Aleksandryjska", "Legendarny skarb wiedzy starożytności.", "Biblioteka Aleksandryjska była jedną z największych prób zebrania **ludzkiej wiedzy** w jednym miejscu.\n\nJeśli los dokładnie o niej wiemy, jej symbolika wciąż oznacza ciekawość świata."),
    ("Atlas i mapy", "Stąd nazwa atlas na zbiorze map.", "W mitologii greckiej **Atlas** miał dźwigać niebiosa. Renesansowi kartografowie umieszczali jego wizerunek na okładkach.\n\nTak powstała nazwa **atlas**."),
    ("Procent składany", "Małe zyski mogą rosnąć przez lata.", "**Procent składany** oznacza, że zysk liczysz nie tylko od kapitału, ale też od wcześniejszych odsetek.\n\nPrzy długim horyzoncie czasu regularne odkładanie robi ogromną różnicę."),
    ("Efekt świadka", "Więcej osób nie zawsze znaczy więcej pomocy.", "Psychologowie społeczni zauważyli, że ludzie czasem **rzadziej reagują**, gdy wokół są inni.\n\nRozproszona odpowiedzialność potrafi wyciszyć działanie."),
    ("Brzytwa Ockhama", "Prostsze wyjaśnienie bywa lepsze.", "**Brzytwa Ockhama** mówi, że gdy dwa wyjaśnienia pasują do faktów, często lepsze jest prostsze.\n\nTo narzędzie jasności, a nie dowód ostateczny."),
    ("Pamięć złotej rybki", "Złote rybki pamiętają dłużej niż kilka sekund.", "Badania pokazują, że rybki potrafią zapamiętać miejsca karmienia nawet na **tygodnie lub miesiące**.\n\nMit o trzech sekundach jest mocno przesadzony."),
    ("Miód się nie psuje", "Archeolodzy znajdowali jadalny stary miód.", "Niska wilgotność i naturalna kwasowość miodu utrudniają rozwój bakterii.\n\nZamknięte naczynia sprzed tysięcy lat potrafiły nadal zawierać **jadalny miód**."),
    ("Banan to jagoda", "Botanika nie zgadza się z kuchnią.", "W ujęciu botanicznym jagoda rozwija się z jednego owarium jednego kwiatu. Według tej definicji **banan jest jagodą**.\n\nTruskawka nią nie jest."),
    ("Efekt Zeigarnik", "Niedokończone zadania zostają w głowie.", "Bluma Zeigarnik zauważyła, że łatwiej pamiętamy **przerwane zadania** niż te ukończone.\n\nDlatego otwarte sprawy tak ciągną uwagę."),
    ("Kolejność alfabetu", "A-B-C to konwencja, nie prawo natury.", "Porządek liter alfabetu łacińskiego to **historyczna umowa**, a nie coś oczywistego.\n\nInne systemy pisma mają zupełnie inne układy."),
    ("Prasa drukarska", "Książki zmieniły świat szybciej, niż sądzono.", "Ruchome czcionki Gutenberga sprawiły, że książki stały się **tańsze i szybsze** w produkcji.\n\nWiedza zaczęła krążyć szerzej niż kiedykolwiek wcześniej."),
    ("Serce ośmiornicy", "Ośmiornica ma trzy serca.", "Dwa serca pompują krew przez skrzela, a trzecie do reszty ciała.\n\nGdy ośmiornica pływa, główne serce często **odpoczywa**, dlatego woli pełzać."),
    ("Herbata i handel", "Herbata kształtowała imperia.", "Herbata stała się jednym z najważniejszych towarów świata i wpływała na dyplomację, kolonializm i codzienne rytuały.\n\nZwykła filiżanka może mieć długą historię."),
    ("Zero jako liczba", "Zero nie zawsze było oczywiste.", "Wiele kultur miało symbol braku, ale pełne użycie **zera jako liczby** rozwijało się stopniowo.\n\nPóźniej stało się fundamentem nowoczesnej matematyki."),
    ("Drzewa rozmawiają", "Las dzieli zasoby pod ziemią.", "Drzewa przenoszą składniki przez sieci grzybów, często nazywane **leśnym internetem**.\n\nLas działa bardziej jak współpraca niż zbiór samotnych roślin."),
    ("Niewiedza o prawie", "Nieznanie prawa zwykle nie zwalnia z odpowiedzialności.", "W wielu systemach prawnych obowiązuje zasada, że obywatel ma stosować prawo nawet bez jego czytania.\n\nTo argument za prostszą edukacją prawną."),
    ("Pierwszy bug", "Prawdziwa ćma zatrzymała komputer.", "W 1947 roku w Harvard Mark II znaleziono ćmę w przekaźniku.\n\nTo wydarzenie utrwaliło słowo **debugging**."),
    ("Pytania są ważniejsze", "Ciekawość utrzymuje umysł w ruchu.", "Dobre pytanie otwiera więcej dróg niż pośpieszna odpowiedź.\n\nDlatego codzienny fakt działa najlepiej, gdy zostawia po sobie zadziwienie."),
]


def release_ms(day: datetime) -> int:
    release = day.replace(hour=7, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
    return int(release.timestamp() * 1000)


def write_fact(locale: str, day: datetime, category: str, title: str, teaser: str, body: str, index: int) -> None:
    fact_id = f"{day.strftime('%Y-%m-%d')}-{category}-{index:02d}"
    folder = CONTENT_DIR / locale
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{fact_id}.md"
    path.write_text(
        "\n".join(
            [
                "---",
                f"id: {fact_id}",
                f"locale: {locale}",
                f"category: {category}",
                f"title: {title}",
                f"teaser: {teaser}",
                f"release_epoch_ms: {release_ms(day)}",
                "published: true",
                "version: 1",
                "---",
                body,
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    start = datetime(2026, 5, 19, tzinfo=timezone.utc)
    for index in range(21):
        day = start + timedelta(days=index)
        category, title_en, teaser_en, body_en = FACTS[index]
        title_pl, teaser_pl, body_pl = PL_TITLES[index]
        write_fact("en-US", day, category, title_en, teaser_en, body_en, index)
        write_fact("pl-PL", day, category, title_pl, teaser_pl, body_pl, index)
    print("Generated 42 seed facts in content/")


if __name__ == "__main__":
    main()
