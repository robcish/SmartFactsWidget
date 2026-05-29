#!/usr/bin/env python3
"""Generate slot-based fact database (4 facts/day at 0, 6, 12, 18 Europe/Warsaw)."""

from __future__ import annotations

import shutil
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
TZ = ZoneInfo("Europe/Warsaw")
SLOT_HOURS = (0, 6, 12, 18)
# First slot: today 00:00 Warsaw (override via SMARTFACTS_START_DATE=YYYY-MM-DD)
START = datetime(2026, 5, 29, 0, 0, tzinfo=TZ)
CATEGORY_COOLDOWN_DAYS = 2

# (category, pl_title, pl_teaser, pl_body, en_title, en_teaser, en_body)
FACTS: list[tuple[str, str, str, str, str, str, str]] = [
    (
        "animals",
        "Krowy mają przyjaciół",
        "Krowy tęsknią za swoimi ulubionymi kompanami.",
        "Badania pokazują, że krowy **bardzo przywiązują się** do wybranych osób z stada i odczuwają silny stres po rozłączeniu.\n\nTo przypomina, że emocje u zwierząt bywają bardziej złożone, niż sądzimy.\n\n[Więcej o zachowaniu bydła (Wikipedia)](https://pl.wikipedia.org/wiki/Krowa_domowa)",
        "Cows have best friends",
        "Cows miss their favorite herd companions.",
        "Research shows cows **form strong bonds** with specific herd mates and experience significant stress when separated.\n\n[More on cattle behavior (Wikipedia)](https://en.wikipedia.org/wiki/Cattle)",
    ),
    (
        "biology",
        "Mrówki ważą więcej niż ludzie",
        "Łączna masa mrówek może przewyższać masę ludzi.",
        "Szacuje się, że **łączna masa wszystkich mrówek** na Ziemi jest porównywalna lub większa niż łączna masa wszystkich ludzi.\n\nMrówki to jedni z najbardziej udanych organizmów społecznych planety.\n\n[Mrówki (Wikipedia)](https://pl.wikipedia.org/wiki/Mr%C3%B3wki)",
        "Ants outweigh humanity",
        "All ants combined may weigh more than all humans.",
        "Estimates suggest the **total mass of all ants** on Earth is comparable to or greater than the total mass of all humans.\n\n[Ant (Wikipedia)](https://en.wikipedia.org/wiki/Ant)",
    ),
    (
        "animals",
        "Koń nie jest jak kot",
        "Konie praktycznie nie wymiotują.",
        "Ze względu na budowę układu pokarmowego konie **nie potrafią wymiotować** jak wiele innych ssaków.\n\nCofanie treści żołądkowej u nich jest ekstremalnie rzadkie i niebezpieczne.\n\n[Koń (Wikipedia)](https://pl.wikipedia.org/wiki/Ko%C5%84)",
        "Horses can't vomit",
        "A horse's stomach works very differently from yours.",
        "Because of their digestive anatomy, horses **cannot vomit** the way many mammals can.\n\n[Horse (Wikipedia)](https://en.wikipedia.org/wiki/Horse)",
    ),
    (
        "history",
        "Wojna przez psa",
        "Pograniczny incydent w 1925 roku wymknął na serio.",
        "W 1925 roku Bułgaria i Grecja weszły w krótki konflikt znaný jako **incydent w Petriczu** — po tym, jak grecki żołnierz przekroczył granicę, goniąc uciekającego psa.\n\n[Crisis of 1925 (Wikipedia)](https://en.wikipedia.org/wiki/Crisis_of_1925)",
        "A war over a dog",
        "A border chase escalated in 1925.",
        "In 1925 Bulgaria and Greece clashed in the brief **Petric incident** after a Greek soldier crossed the border chasing his runaway dog.\n\n[Crisis of 1925 (Wikipedia)](https://en.wikipedia.org/wiki/Crisis_of_1925)",
    ),
    (
        "history",
        "Debata o biuście syrenki",
        "Rada miejska Ustki szukała idealnego rozmiaru.",
        "W latach 2004–2007 rada Ustki przez długi czas **debatowała nad herbem** i rozmiarem piersi syrenki — sprawa stała się ogólnopolską ciekawostką.\n\n[Ustka (Wikipedia)](https://pl.wikipedia.org/wiki/Ustka)",
        "The siren bust debate",
        "One Polish town argued over its coat of arms.",
        "From 2004 to 2007 the town council of Ustka **debated the mermaid on its coat of arms** and the size of her bust — becoming a nationwide talking point.\n\n[Ustka (Wikipedia)](https://en.wikipedia.org/wiki/Ustka)",
    ),
    (
        "geography",
        "USA bez języka urzędowego",
        "Angielski dominuje, ale prawnie nie jest urzędowy.",
        "Stany Zjednoczone **nie mają języka urzędowego** na poziomie federalnym. Angielski jest dominujący, ale to kwestia praktyki, nie konstytucyjnego przepisu.\n\n[Języki w Stanach Zjednoczonych (Wikipedia)](https://pl.wikipedia.org/wiki/J%C4%99zyki_w_Stanach_Zjednoczonych)",
        "The US has no official language",
        "English dominates — but not by federal law.",
        "The United States has **no official language** at the federal level. English is dominant in practice, not by constitutional decree.\n\n[Languages of the United States (Wikipedia)](https://en.wikipedia.org/wiki/Languages_of_the_United_States)",
    ),
    (
        "geography",
        "Gdzie nie ma Coca-Coli",
        "Tylko dwa kraje bez legalnej sprzedaży.",
        "Ze względów polityczno-ekonomicznych **Kuba i Korea Północna** to jedyne kraje, w których Coca-Cola nie jest legalnie dostępna.\n\n[Coca-Cola (Wikipedia)](https://pl.wikipedia.org/wiki/Coca-Cola)",
        "Where Coca-Cola isn't sold",
        "Only two countries ban it legally.",
        "For political and economic reasons, **Cuba and North Korea** are the only countries where Coca-Cola is not legally sold.\n\n[Coca-Cola (Wikipedia)](https://en.wikipedia.org/wiki/Coca-Cola)",
    ),
    (
        "food",
        "Kokos zamiast krwi?",
        "Woda kokosowa bywa używana w nagłych wypadkach.",
        "W sytuacjach kryzysowych woda z młodego kokosa może służyć jako **zamiennik płynu infuzyjnego** — jest sterylna i ma odpowiedni skład elektrolitów.\n\n[Woda kokosowa (Wikipedia)](https://pl.wikipedia.org/wiki/Woda_kokosowa)",
        "Coconut water as plasma?",
        "Young coconut water has been used in emergencies.",
        "In crisis situations, water from young coconuts has been used as an **intravenous fluid substitute** because it is sterile and electrolyte-rich.\n\n[Coconut water (Wikipedia)](https://en.wikipedia.org/wiki/Coconut_water)",
    ),
    (
        "food",
        "Ananas to krzak, nie drzewo",
        "Rośnie nisko, blisko ziemi.",
        "Ananasy **nie rosną na drzewach** — wyrastają z niskiego krzaka. Jeden owoc to w rzeczywistości zrośnięty owocostan wielu kwiatów.\n\n[Ananas (Wikipedia)](https://pl.wikipedia.org/wiki/Ananas_jadalny)",
        "Pineapples grow on bushes",
        "Not on tall trees — close to the ground.",
        "Pineapples **do not grow on trees**. They rise from low plants, and one pineapple is actually a fused cluster of many flowers.\n\n[Pineapple (Wikipedia)](https://en.wikipedia.org/wiki/Pineapple)",
    ),
    (
        "myth-busting",
        "Biała czekolada to nie czekolada?",
        "Prawnie brakuje jej kakao.",
        "Biała czekolada nie zawiera miazgi kakaowej, więc w wielu przepisach **technicznie nie jest czekoladą** — składa się głównie z tłuszczu kakaowego, cukru i mleka.\n\n[Czekolada (Wikipedia)](https://pl.wikipedia.org/wiki/Czekolada)",
        "White chocolate isn't chocolate?",
        "Legally, it often misses cocoa mass.",
        "White chocolate contains no cocoa solids, so in many standards it **technically isn't chocolate** — mostly cocoa butter, sugar, and milk.\n\n[Chocolate (Wikipedia)](https://en.wikipedia.org/wiki/Chocolate)",
    ),
    (
        "science",
        "Miód nie psuje się",
        "Archeolodzy znajdowali jadalny miód sprzed tysięcy lat.",
        "Niska wilgotność i kwasowość miodu czynią go **niegościnym dla bakterii**. Zamknięty słoik może przetrwać tysiąclecia.\n\n[Miód (Wikipedia)](https://pl.wikipedia.org/wiki/Mi%C3%B3d)",
        "Honey doesn't spoil",
        "Sealed honey can last for millennia.",
        "Honey's low moisture and acidity make it **hostile to bacteria**. Properly sealed jars have survived thousands of years.\n\n[Honey (Wikipedia)](https://en.wikipedia.org/wiki/Honey)",
    ),
    (
        "astronomy",
        "Jeden dzień na Wenus trwa dłużej niż rok",
        "Planeta kręci się bardzo wolno.",
        "Na Wenus **jeden obrót wokół osi** trwa dłużej niż jeden obieg wokół Słońca — dzień planetarny jest dłuższy niż rok.\n\n[Wenus (Wikipedia)](https://pl.wikipedia.org/wiki/Wenus)",
        "A Venus day beats its year",
        "The planet spins extremely slowly.",
        "On Venus, **one rotation** takes longer than one orbit around the Sun — a day lasts longer than a year.\n\n[Venus (Wikipedia)](https://en.wikipedia.org/wiki/Venus)",
    ),
    (
        "math",
        "Zero kiedyś nie istniało",
        "Jako liczba pojawiło się stosunkowo późno.",
        "Wiele cywilizacji radziło sobie bez **zera jako pełnej liczby**. Dopiero później stało się fundamentem matematyki.\n\n[Zero (Wikipedia)](https://pl.wikipedia.org/wiki/Zero)",
        "Zero arrived late",
        "It wasn't always a number.",
        "Many civilizations managed without **zero as a full number**. It became essential to modern math much later.\n\n[0 (Wikipedia)](https://en.wikipedia.org/wiki/0)",
    ),
    (
        "technology",
        "Pierwszy „bug” był ćmą",
        "Literally — owad w komputerze.",
        "W 1947 roku w Harvard Mark II znaleziono **prawdziwą ćmę** w przekaźniku. Stąd popularne określenie *debugging*.\n\n[Software bug (Wikipedia)](https://en.wikipedia.org/wiki/Software_bug",
        "The first computer bug was a moth",
        "A real insect in the machine.",
        "In 1947 operators found an actual **moth** stuck in a Harvard Mark II relay — helping popularize the term *debugging*.\n\n[Software bug (Wikipedia)](https://en.wikipedia.org/wiki/Software_bug)",
    ),
    (
        "psychology",
        "Efekt Zeigarnik",
        "Niedokończone zadania zostają w głowie.",
        "Bluma Zeigarnik zauważyła, że łatwiej pamiętamy **przerwane zadania** niż te ukończone — stąd uczucie „wiszących spraw”.\n\n[Efekt Zeigarnik (Wikipedia)](https://pl.wikipedia.org/wiki/Efekt_Zeigarnik)",
        "The Zeigarnik effect",
        "Unfinished tasks stick in memory.",
        "Bluma Zeigarnik found we remember **interrupted tasks** better than completed ones — hello, mental open loops.\n\n[Zeigarnik effect (Wikipedia)](https://en.wikipedia.org/wiki/Zeigarnik_effect)",
    ),
    (
        "language",
        "Pensja ma słony początek",
        "Słowo łączy się z solą.",
        "Łacińskie *salarium* wiązało wypłaty rzymskich żołnierzy z **solą** — towarem niegdyś niezwykle cennym.\n\n[Sól (Wikipedia)](https://pl.wikipedia.org/wiki/S%C3%B3l",
        "Salary comes from salt",
        "The word has a salty origin.",
        "Latin *salarium* linked Roman soldiers' pay to **salt** — once extraordinarily valuable.\n\n[Salt (Wikipedia)](https://en.wikipedia.org/wiki/Salt)",
    ),
    (
        "philosophy",
        "Brzytwa Ockhama",
        "Prostsze wyjaśnienie bywa lepsze.",
        "**Brzytwa Ockhama** mówi: gdy dwa wyjaśnienia pasują do faktów, często lepsze jest prostsze. To narzędzie jasności, nie dowód.\n\n[Brzytwa Ockhama (Wikipedia)](https://pl.wikipedia.org/wiki/Brzytwa_Ockhama)",
        "Occam's razor",
        "Simpler explanations often win.",
        "**Occam's razor** suggests that when two explanations fit, the simpler one is often preferable — a clarity tool, not proof.\n\n[Occam's razor (Wikipedia)](https://en.wikipedia.org/wiki/Occam%27s_razor)",
    ),
    (
        "society",
        "Efekt świadka",
        "Więcej osób ≠ więcej pomocy.",
        "Psychologowie społeczni zauważyli, że przy wielu świadkach ludzie **rzadziej reagują** w nagłych sytuacjach.\n\n[Efekt świadka (Wikipedia)](https://pl.wikipedia.org/wiki/Efekt_%C5%9Bwiadka)",
        "The bystander effect",
        "More witnesses can mean less help.",
        "Social psychologists found that with many witnesses, people are **less likely to intervene** in emergencies.\n\n[Bystander effect (Wikipedia)](https://en.wikipedia.org/wiki/Bystander_effect)",
    ),
    (
        "law",
        "Nie znasz prawa? I tak obowiązuje",
        "Ignorancja rzadko zwalnia.",
        "W wielu systemach prawnych obowiązuje zasada: **nieznajomość prawa nie zwalnia** z jego przestrzegania.\n\n[Ignorantia iuris nocet (Wikipedia)](https://pl.wikipedia.org/wiki/Ignorantia_iuris_nocet)",
        "Ignorance of the law",
        "Not knowing rarely excuses you.",
        "Many legal systems hold that **ignorance of the law** does not excuse breaking it.\n\n[Ignorantia juris non excusat (Wikipedia)](https://en.wikipedia.org/wiki/Ignorantia_juris_non_excusat)",
    ),
    (
        "finance",
        "Procent składany robi robotę",
        "Małe kwoty rosną z czasem.",
        "**Procent składany** oznacza, że zysk liczysz też od wcześniejszych zysków — przy długim horyzoncie robi ogromną różnicę.\n\n[Procent składany (Wikipedia)](https://pl.wikipedia.org/wiki/Procent_sk%C5%82adany)",
        "Compound interest adds up",
        "Small gains snowball over time.",
        "**Compound interest** means you earn returns on previous returns too — over long horizons the difference is huge.\n\n[Compound interest (Wikipedia)](https://en.wikipedia.org/wiki/Compound_interest)",
    ),
    (
        "culture",
        "Herbata zmieniła świat",
        "Kubek może mieć długą historię.",
        "Herbata stała się jednym z najważniejszych towarów handlu globalnego i wpływała na **dyplomację, kolonializm i codzienne rytuały**.\n\n[Herbata (Wikipedia)](https://pl.wikipedia.org/wiki/Herbata)",
        "Tea reshaped history",
        "A cup can carry centuries.",
        "Tea became a major global commodity, shaping **diplomacy, colonialism, and daily rituals**.\n\n[Tea (Wikipedia)](https://en.wikipedia.org/wiki/Tea",
    ),
    (
        "mythology",
        "Atlas i mapy",
        "Stąd nazwa atlas.",
        "W mitologii greckiej **Atlas** dźwigał niebiosa. Renesansowi kartografowie umieszczali jego wizerunek na okładkach zbiorów map.\n\n[Atlas (mitologia) (Wikipedia)](https://pl.wikipedia.org/wiki/Atlas_(mitologia))",
        "Why maps are called atlases",
        "Blame a Greek titan.",
        "In Greek myth **Atlas** held up the heavens. Renaissance mapmakers put him on book covers — hence *atlas*.\n\n[Atlas (mythology) (Wikipedia)](https://en.wikipedia.org/wiki/Atlas_(mythology))",
    ),
    (
        "sport",
        "Piłka nożna to globalny język",
        "Mecz łączy ludzi szybciej niż słowa.",
        "Futbal jest najpopularniejszym sportem świata — **miliardy ludzi** oglądają i grają, niezależnie od języka czy kultury.\n\n[Piłka nożna (Wikipedia)](https://pl.wikipedia.org/wiki/Pi%C5%82ka_no%C5%BCna)",
        "Football is a global language",
        "A match connects faster than words.",
        "Soccer is the world's most popular sport — **billions** watch and play across languages and cultures.\n\n[Association football (Wikipedia)](https://en.wikipedia.org/wiki/Association_football)",
    ),
    (
        "environment",
        "Las to sieć pod ziemią",
        "Drzewa dzielą zasoby.",
        "Drzewa przenoszą składniki przez grzybie grzybnię — często mówi się o **„leśnym internecie”**.\n\n[Mikoryza (Wikipedia)](https://pl.wikipedia.org/wiki/Mikoryza)",
        "Forests share underground",
        "Trees trade nutrients.",
        "Trees move nutrients through fungal networks — often called the **wood wide web**.\n\n[Mycorrhizal network (Wikipedia)](https://en.wikipedia.org/wiki/Mycorrhizal_network",
    ),
    (
        "general",
        "Banany to jagody (botanycznie)",
        "Kuchnia i botanika się nie zgadzają.",
        "W ujęciu botanicznym **banan jest jagodą**. Truskawka — nie.\n\n[Banan (Wikipedia)](https://pl.wikipedia.org/wiki/Banan",
        "Bananas are berries (botanically)",
        "Kitchen labels ≠ plant science.",
        "Botanically, a **banana is a berry**. A strawberry is not.\n\n[Banana (Wikipedia)](https://en.wikipedia.org/wiki/Banana",
    ),
    (
        "reflection",
        "Pytanie > odpowiedź",
        "Ciekawość utrzymuje umysł w ruchu.",
        "Dobre pytanie otwiera więcej dróg niż pośpieszna odpowiedź. **Ciekawość** to paliwo nauki.\n\n[Ciekawość (Wikipedia)](https://pl.wikipedia.org/wiki/Ciekawo%C5%9B%C4%87",
        "Questions beat rushed answers",
        "Curiosity keeps you moving.",
        "A good question opens more paths than a hasty answer. **Curiosity** fuels learning.\n\n[Curiosity (Wikipedia)](https://en.wikipedia.org/wiki/Curiosity",
    ),
    (
        "biology",
        "Ośmiornica ma trzy serca",
        "I niebieską krew.",
        "Dwa serca pompują krew przez skrzela, trzecie do reszty ciała. Hemocyjanina sprawia, że krew bywa **niebieska**.\n\n[Ośmiornica (Wikipedia)](https://pl.wikipedia.org/wiki/O%C5%9Bmiornica",
        "An octopus has three hearts",
        "And blue blood.",
        "Two hearts pump blood through gills, one to the body. Hemocyanin can make its blood **blue**.\n\n[Octopus (Wikipedia)](https://en.wikipedia.org/wiki/Octopus",
    ),
    (
        "science",
        "Rekin starszy niż drzewo",
        "Rekinom jesteśmy winni pokorę.",
        "Rekiny pływają po oceanach od ponad **400 mln lat** — długo przed większością drzew lądowych.\n\n[Rekin (Wikipedia)](https://pl.wikipedia.org/wiki/Rekin",
        "Sharks predate trees",
        "They've been around a long time.",
        "Sharks have swum the oceans for over **400 million years** — long before most land trees.\n\n[Shark (Wikipedia)](https://en.wikipedia.org/wiki/Shark",
    ),
    (
        "geography",
        "Rosja ma 11 stref czasowych",
        "Jeden kraj, wiele zegarów.",
        "Rozciągnięta na dwa kontynenty Rosja obejmuje **11 stref czasowych** — rekord wśród państw.\n\n[Strefy czasowe w Rosji (Wikipedia)](https://pl.wikipedia.org/wiki/Strefy_czasowe_w_Rosji",
        "Russia spans 11 time zones",
        "One country, many clocks.",
        "Stretching across two continents, Russia covers **11 time zones** — a world record among nations.\n\n[Time in Russia (Wikipedia)](https://en.wikipedia.org/wiki/Time_in_Russia",
    ),
    (
        "history",
        "Prasa Gutenberga",
        "Książki poszły w świat.",
        "Ruchome czcionki sprawiły, że książki stały się **tańsze i szybsze** w produkcji — wiedza zaczęła krążyć szerzej niż kiedykolwiek.\n\n[Prasa drukarska (Wikipedia)](https://pl.wikipedia.org/wiki/Prasa_drukarska",
        "Gutenberg's press",
        "Books went mainstream.",
        "Movable type made books **cheaper and faster** to produce — knowledge spread like never before.\n\n[Printing press (Wikipedia)](https://en.wikipedia.org/wiki/Printing_press",
    ),
    (
        "myth-busting",
        "Złota rybka pamięta",
        "Mit o 3 sekundach to przesada.",
        "Badania pokazują, że ryby akwariowe potrafią pamiętać sygnały i miejsca karmienia przez **tygodnie lub miesiące**.\n\n[Złota rybka (Wikipedia)](https://pl.wikipedia.org/wiki/Z%C5%82ota_rybka",
        "Goldfish remember",
        "The three-second myth is wrong.",
        "Studies show goldfish can remember feeding cues for **weeks or months**.\n\n[Goldfish (Wikipedia)](https://en.wikipedia.org/wiki/Goldfish",
    ),
    (
        "technology",
        "Pierwsze hasło komputerowe",
        "Było… wydrukowane.",
        "Jedno z pierwszych haseł systemowych w MIT było tak proste, że dziś brzmi jak **absurd** — ale kiedyś chroniło dostęp do całej maszyny.\n\n[Hasło (informatyka) (Wikipedia)](https://pl.wikipedia.org/wiki/Has%C5%82o_(informatyka)",
        "Early computer passwords",
        "Security looked very different.",
        "One of the earliest system passwords was so simple it sounds absurd today — yet it guarded an entire machine.\n\n[Password (Wikipedia)](https://en.wikipedia.org/wiki/Password",
    ),
    (
        "psychology",
        "Efekt spacingu",
        "Rozłożone powtórki wygrywają.",
        "**Spaced repetition** działa lepiej niż wkuwanie w jednej nocy — mózg potrzebuje przerw, żeby utrwalić wiedzę.\n\n[Powtarzanie rozłożone (Wikipedia)](https://pl.wikipedia.org/wiki/Powtarzanie_roz%C5%82o%C5%BCone",
        "The spacing effect",
        "Cramming loses to spaced review.",
        "**Spaced repetition** beats one long cram session — your brain needs gaps to consolidate memory.\n\n[Spacing effect (Wikipedia)](https://en.wikipedia.org/wiki/Spacing_effect",
    ),
    (
        "astronomy",
        "Księżyc oddala się od Ziemi",
        "Około 3,8 cm rocznie.",
        "Księżyc **powoli oddala się** od nas — kosmiczny oddział, który zmienia też długość dnia na Ziemi (bardzo, bardzo powoli).\n\n[Księżyc (Wikipedia)](https://pl.wikipedia.org/wiki/Ksi%C4%99%C5%BCyc",
        "The Moon is drifting away",
        "About 3.8 cm per year.",
        "The Moon is **slowly moving away** from Earth — a cosmic tug that also changes our day length over eons.\n\n[Moon (Wikipedia)](https://en.wikipedia.org/wiki/Moon",
    ),
    (
        "math",
        "Pizza i geometria",
        "Kąt w pizzy to często 45°.",
        "Dzieląc okrąg na 8 kawałków, każdy kawałek ma **45 stopni** w wierzchołku — prosta geometria w kuchni.\n\n[Kąt (geometryczny) (Wikipedia)](https://pl.wikipedia.org/wiki/K%C4%85t_(geometryczny)",
        "Pizza angles",
        "Eight slices, 45 degrees each.",
        "Cut a circle into eight slices and each slice has a **45°** tip — geometry at dinner.\n\n[Angle (Wikipedia)](https://en.wikipedia.org/wiki/Angle",
    ),
    (
        "food",
        "Wasabi często to rzodkiew",
        "Prawdziwe bywa drogie.",
        "W wielu restauracjach **zielony pasty** do sushi to mieszanka z rzodkwi i musztardy — prawdziwe wasabi jest rzadsze i delikatniejsze.\n\n[Wasabi (Wikipedia)](https://pl.wikipedia.org/wiki/Wasabi",
        "Your wasabi may be horseradish",
        "Real wasabi is rare.",
        "In many restaurants the green paste is **horseradish-based** — true wasabi is rarer and milder.\n\n[Wasabi (Wikipedia)](https://en.wikipedia.org/wiki/Wasabi",
    ),
    (
        "sport",
        "Maraton ma starożytne korzenie",
        "Legenda o goncu z Maratonu.",
        "Nazwa maratonu nawiązuje do **bitwy pod Maratonem** w 490 r. p.n.e. — stąd dystans ok. 42 km.\n\n[Maraton (sport) (Wikipedia)](https://pl.wikipedia.org/wiki/Maraton_(sport)",
        "Marathon's ancient roots",
        "Named after a Greek battle.",
        "The marathon distance nods to the **Battle of Marathon** in 490 BCE — hence ~42 km.\n\n[Marathon (Wikipedia)](https://en.wikipedia.org/wiki/Marathon",
    ),
    (
        "environment",
        "Amazonia produkuje tlen… częściowo sama zużywa",
        "Las deszczowy to skomplikowany system.",
        "Amazoński las deszczowy **recyrkuluje** ogromne ilości wody i tlenu — jego rola w klimacie jest kluczowa, ale uproszczone memy bywają mylące.\n\n[Amazonia (Wikipedia)](https://pl.wikipedia.org/wiki/Amazonia",
        "The Amazon is a closed loop",
        "Rainforests recycle their own oxygen.",
        "The Amazon **recycles** huge amounts of water and oxygen — vital for climate, though simplified memes can mislead.\n\n[Amazon rainforest (Wikipedia)](https://en.wikipedia.org/wiki/Amazon_rainforest",
    ),
    (
        "culture",
        "Origami to nie tylko papier",
        "Sztuka składania ma setki lat.",
        "Tradycyjne **origami** zakłada składanie bez cięcia — dziś łączy sztukę, matematykę i inżynierię.\n\n[Origami (Wikipedia)](https://pl.wikipedia.org/wiki/Origami",
        "Origami is math in disguise",
        "Fold without cutting.",
        "Classic **origami** avoids cuts — today it blends art, math, and engineering.\n\n[Origami (Wikipedia)](https://en.wikipedia.org/wiki/Origami",
    ),
    (
        "philosophy",
        "Paradoks łodzi Tezeusza",
        "Czy to wciąż ta sama łódź?",
        "Jeśli wymieniasz element po elemencie, **kiedy przestaje być tą samą łodzią?** — pytanie o tożsamość, nie o drewno.\n\n[Łódź Tezeusza (Wikipedia)](https://pl.wikipedia.org/wiki/%C5%81%C3%B3d%C5%BA_Tezeusza",
        "The Ship of Theseus",
        "When does it stop being the same ship?",
        "Replace every plank — **when is it no longer the same ship?** A question of identity, not wood.\n\n[Ship of Theseus (Wikipedia)](https://en.wikipedia.org/wiki/Ship_of_Theseus",
    ),
    (
        "general",
        "Litery Q i U w polskim",
        "Q prawie zawsze idzie z U.",
        "W polszczyźnie **q** prawie wyłącznie występuje w zapisie *qu* — stąd rzadkość tej litery w krzyżówkach.\n\n[Alfabet polski (Wikipedia)](https://pl.wikipedia.org/wiki/Alfabet_polski",
        "Q rarely flies solo in Polish",
        "It almost always pairs with U.",
        "In Polish, **q** almost always appears in *qu* — making it a crossword rarity.\n\n[Polish alphabet (Wikipedia)](https://en.wikipedia.org/wiki/Polish_alphabet",
    ),
    (
        "law",
        "W Szwajcarii zakaz… jednego gatunku królika?",
        "Prawo bywa bardzo szczegółowe.",
        "Niektóre przepisy lokalne brzmią dziwnie, dopóki nie poznasz kontekstu — **prawo odzwierciedla historię miejsca**.\n\n[Prawo szwajcarskie (Wikipedia)](https://pl.wikipedia.org/wiki/Prawo_szwajcarskie",
        "Swiss law gets very specific",
        "Context makes odd rules make sense.",
        "Some local laws sound bizarre until you know the history — **law mirrors place and time**.\n\n[Swiss law (Wikipedia)](https://en.wikipedia.org/wiki/Swiss_law",
    ),
    (
        "finance",
        "Inflacja zjada drobne",
        "100 zł dziś ≠ 100 zł za 20 lat.",
        "**Inflacja** obniża siłę nabywczą pieniądza w czasie — stąd znaczenie oszczędzania i inwestowania mądrze.\n\n[Inflacja (Wikipedia)](https://pl.wikipedia.org/wiki/Inflacja",
        "Inflation eats purchasing power",
        "$100 today ≠ $100 in 20 years.",
        "**Inflation** erodes what money buys over time — why saving and investing matter.\n\n[Inflation (Wikipedia)](https://en.wikipedia.org/wiki/Inflation",
    ),
    (
        "mythology",
        "Prometeusz i ogień",
        "Kradzież ognia dla ludzi.",
        "W mitologii greckiej **Prometeusz** dał ludziom ogień — i zapłacił za to bolesną karą.\n\n[Prometeusz (Wikipedia)](https://pl.wikipedia.org/wiki/Prometeusz",
        "Prometheus stole fire",
        "Mythic gift, mythic punishment.",
        "In Greek myth **Prometheus** gave humans fire — and paid a painful price.\n\n[Prometheus (Wikipedia)](https://en.wikipedia.org/wiki/Prometheus",
    ),
    (
        "society",
        "Dunbar i liczba 150",
        "Ile relacji utrzymujesz naprawdę?",
        "Antropolog Robin Dunbar szacuje, że **~150 osób** to orientacyjny limit stabilnej sieci społecznej.\n\n[Liczba Dunbara (Wikipedia)](https://pl.wikipedia.org/wiki/Liczba_Dunbara",
        "Dunbar's number",
        "How many people can you really know?",
        "Anthropologist Robin Dunbar estimates **~150** as a rough limit for stable social ties.\n\n[Dunbar's number (Wikipedia)](https://en.wikipedia.org/wiki/Dunbar%27s_number",
    ),
    (
        "language",
        "Emoji to nowy dialekt",
        "😊 może znaczyć co innego niż myślisz.",
        "Emoji mają **kontekst kulturowy** — ten sam symbol bywa odbierany różnie na świecie.\n\n[Emoji (Wikipedia)](https://pl.wikipedia.org/wiki/Emoji",
        "Emoji mean different things",
        "Context is everything.",
        "Emojis carry **cultural context** — the same symbol reads differently worldwide.\n\n[Emoji (Wikipedia)](https://en.wikipedia.org/wiki/Emoji",
    ),
]


def slot_datetimes(max_slots: int) -> list[datetime]:
    """Yield consecutive slots (one fact each) from START."""
    slots: list[datetime] = []
    day = START
    while len(slots) < max_slots:
        for hour in SLOT_HOURS:
            slots.append(day.replace(hour=hour, minute=0, second=0, microsecond=0))
            if len(slots) >= max_slots:
                break
        day += timedelta(days=1)
    return slots


def category_allowed(category: str, slot_day: date, last_used: dict[str, date]) -> bool:
    previous = last_used.get(category)
    if previous is None:
        return True
    return (slot_day - previous).days >= CATEGORY_COOLDOWN_DAYS


def schedule_facts(
    facts: list[tuple[str, str, str, str, str, str, str]],
) -> list[tuple[datetime, tuple[str, str, str, str, str, str, str]]]:
    """Assign one fact per slot; enforce 2-day category cooldown."""
    from collections import defaultdict, deque

    by_category: dict[str, deque] = defaultdict(deque)
    for fact in facts:
        by_category[fact[0]].append(fact)

    remaining = sum(len(q) for q in by_category.values())
    slots = slot_datetimes(remaining)
    last_used: dict[str, date] = {}
    scheduled: list[tuple[datetime, tuple]] = []

    for slot in slots:
        slot_day = slot.date()
        eligible = [
            cat
            for cat, queue in by_category.items()
            if queue and category_allowed(cat, slot_day, last_used)
        ]
        if not eligible:
            raise RuntimeError(
                f"No eligible category for slot {slot.isoformat()}. "
                f"Add more facts/categories or relax cooldown."
            )
        # Prefer category unused longest ago (variety)
        eligible.sort(key=lambda c: last_used.get(c, date(1970, 1, 1)))
        category = eligible[0]
        fact = by_category[category].popleft()
        last_used[category] = slot_day
        scheduled.append((slot, fact))

    return scheduled


def write_fact(
    slot: datetime,
    category: str,
    locale: str,
    title: str,
    teaser: str,
    body: str,
) -> None:
    fact_id = f"{slot.strftime('%Y-%m-%d')}-{slot.hour:02d}-{category}"
    release_ms = int(slot.timestamp() * 1000)
    folder = CONTENT / locale
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
                f"release_epoch_ms: {release_ms}",
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
    import os

    global START
    start_override = os.environ.get("SMARTFACTS_START_DATE")
    if start_override:
        START = datetime.strptime(start_override, "%Y-%m-%d").replace(tzinfo=TZ)

    if CONTENT.exists():
        shutil.rmtree(CONTENT)
    rules_path = ROOT / "content" / "FACT_GENERATION_RULES.md"
    rules_content = rules_path.read_text(encoding="utf-8") if rules_path.exists() else None

    if CONTENT.exists():
        shutil.rmtree(CONTENT)

    scheduled = schedule_facts(FACTS)
    for slot, fact in scheduled:
        category, pl_t, pl_te, pl_b, en_t, en_te, en_b = fact
        write_fact(slot, category, "pl-PL", pl_t, pl_te, pl_b)
        write_fact(slot, category, "en-US", en_t, en_te, en_b)

    if rules_content:
        rules_path.parent.mkdir(parents=True, exist_ok=True)
        rules_path.write_text(rules_content, encoding="utf-8")

    print(f"Generated {len(scheduled)} slots × 2 locales = {len(scheduled) * 2} files")
    print(f"Start: {scheduled[0][0].isoformat()} → {scheduled[-1][0].isoformat()}")
    print(f"Category cooldown: {CATEGORY_COOLDOWN_DAYS} calendar days")


if __name__ == "__main__":
    main()
