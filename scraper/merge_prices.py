#!/usr/bin/env python3
"""
Forrásolt bolti árak beolvasztása a data/arak/*.json fájlokba.

Bemenet: scraper/research/prices_g1..g4.json (2026-09-24-i kutatás: kereskedők nyilvános
bruttó árai, termékoldal-URL-lel). Kimenet: data/arak/<slug>.json – alap_ar, variansok,
forrasok, megjegyzes, faq frissül; varos_szorzok és (ahol van) reszletek megmarad,
kivéve a cement / osb-lap / betonacél kézzel írt szövegeit, amelyek itt újraíródnak.

Futtatás: python scraper/merge_prices.py
"""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "..", "data")
ARAK = os.path.join(DATA, "arak")
RESEARCH = os.path.join(BASE, "research")
DATUM = "2026-09-24"

SLUG_MAP = {"belteri-festek": "beltéri-festék", "kulteri-festek": "kültéri-festék"}

# Rövid, egységes mértékegység (a kutatásban néhol magyarázat volt a zárójelben)
EGYSEG = {
    "vakolat": "Ft/zsák (25 kg)",
    "vizszigetelo": "Ft/m²",
    "padlolapragaszto": "Ft/zsák (25 kg)",
    "tetoszeloec": "Ft/fm",
    "csavar": "Ft/csomag (200 db)",
    "dubel": "Ft/csomag (100 db)",
    "hoszigetelomdubel": "Ft/db",
    "anyascsavar": "Ft/csomag (50 db)",
    "szilikon": "Ft/db (280–310 ml)",
    "akriltomito": "Ft/db (280–310 ml)",
    "szigeteloszalag": "Ft/tekercs",
    "alapozo": "Ft/liter",
    "beltéri-festék": "Ft/liter",
    "kültéri-festék": "Ft/liter",
}

# Olvasóknak szóló rövid megjegyzés az árhoz (mit takar a sáv, mire figyeljen)
MEGJEGYZES = {
    "cement": "Sok tüzép mázsaárat ad (1 q = 4 zsák). Raklap (40–64 zsák) vételénél a raklapdíj külön tétel.",
    "beton": "Betonüzemi ár, bruttó, kiszállítás nélkül. A mixeres szállítás jellemzően nettó 4 000–6 500 Ft/m³, legalább 7 m³ fuvarra számolva; a betonpumpa külön díj.",
    "soder": "Bányai ár, rakodással, szállítás nélkül. Házhoz szállítva, m³-re számolva jellemzően 10 000–13 000 Ft/m³. Átváltás: 1 m³ homokos kavics ≈ 1,8–1,9 tonna.",
    "kavics": "Mosott, osztályozott kavics bányai ára. Tüzépi telephelyen kisebb tételben 11 000 Ft/t körül. 1 m³ ≈ 1,5–1,6 tonna.",
    "homok": "Bányai ár, szállítás nélkül. 1 m³ homok ≈ 1,4–1,7 tonna.",
    "zuzott-ko": "Az útalapnak használt Z 0/22–0/32 zúzottkő 4 700–9 200 Ft/t, az osztályozott nemes zúzalék 9 000–14 000 Ft/t. 1 m³ ≈ 1,5–1,7 tonna.",
    "mesz": "Oltott mész / mészhidrát 25 kg-os zsákban.",
    "aljzatbeton": "Sok esztrich csak 40 kg-os zsákban kapható (2 600–2 850 Ft); a sáv 25 kg-ra vetített ár.",
    "betonacél": "Kiskereskedelmi szálár (6 m-es szál). Tonnás, kötegelt tételnél bruttó 300 Ft/kg körül is elérhető. Súly: Ø8 0,395 kg/fm, Ø10 0,617, Ø12 0,888, Ø16 1,58 kg/fm.",
    "zartszelveny": "Fekete (nem horganyzott) S235 acél, 6 m-es szálban; a fm-ár a szálár hatoda. Méret szerint nagy a szórás: 20×20×2 ~630 Ft/fm, 60×60×3 ~2 900 Ft/fm.",
    "szogvas": "Melegen hengerelt, egyenlő szárú L-acél, 6 m-es szálban.",
    "horganyzott-lemez": "1000×2000 mm-es tábla (2 m²); az ár a vastagsággal nagyjából arányos.",
    "trapezlemez": "T18 profil. A 2 000–2 100 Ft/m² körüli árak jellemzően II. osztályú vagy akciós lemezre vonatkoznak.",
    "tegla": "Kisméretű tömör tégla (25×12×6,5 cm). Egész téglás falhoz kb. 104 db/m², féltéglás falhoz 52 db/m² kell.",
    "poroton": "Porotherm falazóblokk, 16 db/m². Hőszigeteléssel töltött Thermo blokkok 2 900–3 400 Ft/db (a sávban nincsenek benne).",
    "zsaluko": "Kb. 8–8,7 db kell 1 m² falhoz. A raklapdíj külön tétel.",
    "ytong": "Vastagság szerint: 10 cm 600–840, 20 cm 1 550–1 650, 30 cm ~2 350, 37,5 cm 2 630–3 260 Ft/db. 8,33 db/m², így a 30 cm-es fal anyaga ~19 500 Ft/m².",
    "b30-blokk": "35 db/m², ez 14 000–15 400 Ft/m² falfelület.",
    "tetocserep": "Alapcserép darabára. Típustól függően 9,8–12 db/m² kell (hódfarkú kerámiából 30 felett), m²-re számolva 4 100–9 100 Ft.",
    "eternit": "Azbesztmentes szálcement hullámpala, táblára árulják. A m²-ár a táblafelületre vetített; az átfedések miatt a fedett m² kb. 20–30%-kal drágább.",
    "bitumenes-zsindely": "Csak a zsindely; alátétlemez, OSB és szeg nélkül.",
    "tetofolia": "Jellemzően 75 m²-es tekercsben; a m²-ár átszámolt érték.",
    "kozetgyapot": "Homlokzati, vakolható tábla: 5 cm ~3 600, 10 cm 5 200–6 600, 15 cm 8 400–9 750 Ft/m². Födémre, tetőtérbe való, nem terhelhető kőzetgyapot olcsóbb: 10 cm ~2 500, 15 cm ~3 700 Ft/m².",
    "uveggyapot": "Vastagság szerint: 5 cm 670–850, 10 cm 1 330–1 700, 15 cm 2 000–3 300, 20 cm ~4 000 Ft/m².",
    "hungarocell": "EPS 80 homlokzati lap. 10 cm tüzépen 2 260–5 100 Ft/m², barkácsáruházban (grafitos) 6 800–7 000 Ft/m².",
    "eps": "A sáv 10 cm vastag lapokra vonatkozik. Ökölszabály: EPS 80 kb. 230–510, EPS 100 340–420, EPS 150 ~460 Ft/m² centiméterenként.",
    "xps": "Vastagság szerint: 5 cm 3 200–3 600, 10 cm 6 000–7 000, 15 cm 10 400–10 600 Ft/m² (kb. 640–700 Ft/m² centiméterenként).",
    "penotekercs": "Egyszerű 2–3 mm-es PE hab 170–240 Ft/m²; XPS és hőtükrös alátétek 400–1 200 Ft/m².",
    "szigetelofolia": "Egyszerű 0,2 mm-es PE fólia 150–280 Ft/m²; alumíniumos párazáró 270–530 Ft/m².",
    "gipszkarton": "Normál 12,5 mm-es lap 2 150–2 650 Ft, impregnált (zöld) 3 590–4 110 Ft, tűzgátló ~3 550–3 600 Ft.",
    "polikarbonat": "Üregkamrás lap: 4 mm 3 200–3 900, 6 mm 4 300–5 200, 10 mm 5 900–8 800, 16 mm 8 450–9 900 Ft/m². Bronz és opál színben 5–15%-kal drágább.",
    "osb-lap": "2500×1250 mm-es tábla (3,125 m²): 12 mm 6 700–7 800, 18 mm 9 500–11 700, 22 mm 12 600–13 500 Ft.",
    "retegelt-lemez": "Nyír rétegelt lemez, 1525×1525 mm: 9 mm ~13 000, 12 mm 17 000–21 000, 18 mm 25 500–31 500 Ft. Nagytábla (1250×2500) 18 mm ~43 800 Ft. Borovi fenyő rétegelt lemez olcsóbb.",
    "fa-gerenda": "A fatelepek m³-ben áraznak (4–6 m-es hosszig 185 000–192 000 Ft/m³); a fm-ár ebből számolt. Gyalulás és impregnálás külön díj.",
    "deszka": "Gyalulatlan 2,5 cm-es fenyődeszka 470–1 050 Ft/fm szélességtől függően; gyalult 19 mm-es lucfenyő 680–1 350 Ft/fm.",
    "lec": "Tetőléc 270–330 Ft/fm, 5×5 cm-es léc (stafni) 500–600 Ft/fm.",
    "laminalt-gerenda": "BSH (ragasztott rétegelt) gerenda, 359 000–400 000 Ft/m³. KVH jellemzően 10–25%-kal olcsóbb.",
    "jarolap": "Barkácsáruházi alap gres padlólap 3 500–6 000 Ft/m², nagyformátumú rektifikált 7 000–9 000 Ft/m².",
    "csempe": "Barkácsáruházi fehér/márványos fali csempe 4 000–7 000 Ft/m², szaküzleti I. osztály 8 000–9 600 Ft/m².",
    "terko": "6 cm-es szürke alaptérkő 4 600–6 200, színes vagy mosott felületű 6 500–8 000 Ft/m². A 8 cm-es kivitel 15–25%-kal drágább. Szállítás és raklapdíj külön.",
    "parkett": "Anyagár, lerakás nélkül. Tömör tölgy csaphornyos 14 700–23 400, háromrétegű tölgy 22 000–29 000 Ft/m².",
    "laminalt-padlo": "7–8 mm AC4 alaptermék 2 700–4 000, vízálló vagy AC5 6 000–8 000 Ft/m².",
    "vinyl-padlo": "Klikkes SPC/LVT padló; jellemzően 7 500–9 000 Ft/m².",
    "sorolap": "Kültéri, fagyálló gres/kerámia lap. 8–10 mm vastag 3 300–7 000 Ft/m², a 2 cm-es teraszlap 10 000–16 000 Ft/m².",
    "vakolat": "Kézi alapvakolat 25 kg-os zsákban. Gépi vakolat 40 kg-os zsákban 3 000–4 200 Ft.",
    "ragaszto": "Nagy a különbség a típusok között: C1 alapragasztó 2 300–2 600, flexibilis S1 ragasztó 10 000–13 800 Ft / 25 kg.",
    "habarcs": "A falazóhabarcs jellemzően 30–40 kg-os zsákban kapható; a sáv 25 kg-ra vetített ár.",
    "vizszigetelo": "Kenhető (fürdőszobai) vízszigetelés, kb. 1,4 kg/m² anyagigénnyel számolva. Bitumenes lemez: lásd építési karton.",
    "fugazo": "5 kg-os kiszerelésben kg-onként 1 250–1 600, 2 kg-osban 1 650–2 000 Ft. Epoxi fugázó ennél drágább.",
    "gletteloanvag": "Porglett 20 kg-os zsákban (320–485 Ft/kg).",
    "padlolapragaszto": "Flexibilis (C2TE S1) padlólapragasztó 25 kg-os zsákban.",
    "geotextilia": "Nagy tekercsben 340–480 Ft/m².",
    "drencso": "Ø100 geotextíliás 1 630–2 090 Ft/fm, csupasz Ø100 700–1 525 Ft/fm, Ø160 2 810–4 190 Ft/fm.",
    "tetoszeloec": "Horganyzott vagy színes bádog oromszegély / ereszszegély, 2 m-es szálban.",
    "horganyozott-szeg": "Natúr (nem horganyzott) huzalszeg 810–1 290 Ft/kg.",
    "csavar": "200 db-os kiskereskedelmi csomag 800–2 900 Ft; ömlesztett 1000 db-os dobozban darabonként 2–4,5 Ft.",
    "dubel": "Egyszerű műanyag tipli 9–20 Ft/db, márkás univerzális dübel 39–53 Ft/db.",
    "hoszigetelomdubel": "250 db-os dobozban 35–60 Ft/db, darabáron 100 Ft körül. Acélszeges dübel drágább.",
    "anyascsavar": "M8×60 horganyzott hatlapfejű csavar anyával, 50 garnitúrára számolva.",
    "habragaszto": "Hőszigetelő lapok ragasztására való PU ragasztóhab.",
    "epuletkarton": "Csupaszlemez (kátránypapír) ~500 Ft/m², oxidált bitumenes lemez (GV35–GV45) 1 090–1 330 Ft/m², SBS modifikált 3 000–3 700 Ft/m².",
    "szigeteloszalag": "Két eltérő termék: kétoldalas rögzítőszalag 1 700–2 100 Ft / 25 m, egyoldalas légzáró szalag 18 000–20 700 Ft / 40 m (450–520 Ft/fm).",
    "pu-hab": "Normál pisztolyhab 2 800–3 200 Ft; flexibilis vagy tűzgátló 4 500–5 600 Ft.",
    "szilikon": "A márkás szilikonok többsége 280 ml-es kartusban kapható.",
    "akriltomito": "Festhető akril 700–1 100 Ft, gyors kötésű/esőálló 1 200–1 500 Ft.",
    "falazohalo": "Homlokzati üvegszövet háló, 50 m²-es tekercsben.",
    "alapozo": "5 l-es kiszerelésben literenként 1 000–1 900 Ft, 1 l-esben 1 500–2 850 Ft.",
    "beltéri-festék": "15 l-es fehér diszperziós festék 700–950 Ft/l, prémium mosható 1 900–2 000 Ft/l. Színkevert és kis kiszerelés drágább.",
    "kültéri-festék": "Diszperziós homlokzatfesték 1 400–1 700 Ft/l, prémium akril/szilikon 3 000–4 000 Ft/l, szilikát 4 700 Ft/l körül.",
}

# Vastagság szerint erősen szóró anyagoknál egy-két extra, jól ismert változat
EXTRA_VARIANS = {
    "ytong": [{"nev": "Ytong Classic 37,5 cm (600×200×375)", "ar": 2900}],
    "kozetgyapot": [{"nev": "Födém-/tetőtéri kőzetgyapot 10 cm (nem terhelhető)", "ar": 2490},
                    {"nev": "Födém-/tetőtéri kőzetgyapot 15 cm (nem terhelhető)", "ar": 3735}],
    "osb-lap": [{"nev": "OSB-3 10 mm 2500×1250", "ar": 6390}, {"nev": "OSB-3 15 mm 2500×1250", "ar": 8990}],
    "betonacél": [],
}

VARIANS_EGYSEG_TISZTIT = re.compile(r"\s+(bruttó.*)$")


def nevelo(szo: str) -> str:
    return "az" if szo[:1].lower() in "aáeéiíoóöőuúüű" else "a"


def huf(n) -> str:
    return f"{int(round(n)):,}".replace(",", " ")


def boltok_felsorolas(forrasok, n=4):
    seen = []
    for f in forrasok:
        b = re.sub(r"\s*\(.*?\)", "", f.get("bolt", "")).strip()
        if b and b not in seen:
            seen.append(b)
    return ", ".join(seen[:n])


def clean_forras(f):
    ell = str(f.get("ellenorizve", ""))
    kiolvasva = "keres" not in ell.lower()
    m = re.search(r"\d{4}-\d{2}-\d{2}", ell)
    return {
        "bolt": f.get("bolt", "").strip(),
        "termek": f.get("termek", "").strip(),
        "ar": f.get("ar"),
        "egyseg": f.get("egyseg", "").strip(),
        "url": f.get("url", "").strip(),
        "datum": m.group(0) if m else DATUM,
        "oldalrol_kiolvasva": kiolvasva,
        "megjegyzes": f.get("megjegyzes", "").strip(),
    }


def faq_general(nev, egyseg, alap, variansok, forrasok, megj):
    nl = nev.lower()
    a = nevelo(nl)
    olcso = min(variansok, key=lambda v: v["ar"])
    draga = max(variansok, key=lambda v: v["ar"])
    faq = [
        {
            "kerdes": f"Mennyibe kerül {a} {nl} 2026-ban?",
            "valasz": (f"{nev} ára 2026 szeptemberében {huf(alap['min'])}–{huf(alap['max'])} {egyseg}, "
                       f"a boltok átlagára {huf(alap['atlag'])} {egyseg} (bruttó, szállítás nélkül). "
                       f"A vizsgált változatok közül a legolcsóbb: {olcso['nev']} ({huf(olcso['ar'])} Ft), "
                       f"a legdrágább: {draga['nev']} ({huf(draga['ar'])} Ft)."),
        },
        {
            "kerdes": f"Honnan származnak {a} {nl} árai?",
            "valasz": (f"{len(forrasok)} magyar kereskedő nyilvános, bruttó árából ({boltok_felsorolas(forrasok)}), "
                       f"2026. szeptember 24-i állapot szerint. A források listája linkekkel az oldal alján található."),
        },
    ]
    if megj:
        faq.append({"kerdes": f"Mitől függ {a} {nl} ára?", "valasz": megj})
    faq.append({
        "kerdes": "Változnak az árak városonként?",
        "valasz": ("A kereskedők listaárai országosan hasonlóak, a különbséget főleg a szállítási díj és a helyi telepek árazása adja. "
                   "A városi oldalakon szereplő értékek az országos átlagból, a regionális árszinttel becsült helyi árak."),
    })
    faq.append({
        "kerdes": f"Mire figyelj {nl} vásárlásakor?",
        "valasz": ("Kérj írásos ajánlatot legalább 3 helyről, és kérdezz rá a szállítási díjra, a raklapdíjra és arra, hogy az ár bruttó vagy nettó. "
                   "Nagyobb tételnél a tüzépek gyakran adnak kedvezményt."),
    })
    return faq


TBL = 'class="min-w-full bg-white border border-gray-200 rounded-lg shadow-sm my-4"'
TH = 'class="px-4 py-2 text-left text-sm font-semibold text-gray-700"'
TD = 'class="px-4 py-2 text-sm text-gray-800"'


def tabla(fejlec, sorok):
    h = "".join(f"<th {TH}>{x}</th>" for x in fejlec)
    b = "".join('<tr class="border-t border-gray-100">' + "".join(f"<td {TD}>{c}</td>" for c in s) + "</tr>" for s in sorok)
    return f'<table {TBL}><thead class="bg-gray-50"><tr>{h}</tr></thead><tbody>{b}</tbody></table>'


def kezi_szovegek(slug, d):
    """A három, kézzel bővített anyagoldal (cement, OSB, betonacél) szövegei új árakkal."""
    if slug == "cement":
        d["faq"] = [
            {"kerdes": "Mennyibe kerül egy 25 kg-os zsák cement 2026-ban?",
             "valasz": "2026 szeptemberében a tüzépeken és webshopokban 2 000–2 750 Ft egy 25 kg-os zsák, az átlag 2 300 Ft. Ez kilogrammonként 80–110 Ft."},
            {"kerdes": "Mennyi 1 mázsa cement ára?",
             "valasz": "1 mázsa (100 kg) 4 zsák, 2026-ban 8 000–11 000 Ft. Sok tüzép eleve mázsaárat ír ki."},
            {"kerdes": "Mennyi egy raklap cement ára?",
             "valasz": "Raklaponként a zsákszám gyártótól függ (40–64 zsák). 54 zsákos raklappal számolva 108 000–148 000 Ft, plusz a visszaváltható raklap díja."},
            {"kerdes": "Mennyi cement kell 1 m³ betonhoz?",
             "valasz": "C16/20–C20/25 betonhoz kb. 280–320 kg, azaz 11–13 zsák. 1 m³ házilag kevert beton cementje így 25 000–30 000 Ft, sóderrel együtt 30 000–35 000 Ft körül van."},
            {"kerdes": "Honnan származnak a cementárak?",
             "valasz": "9 kereskedő (pl. Winkler Tüzép, Kézér Tüzép, Tüzép Shop, Bauplaza, Otthonker) nyilvános bruttó árából, 2026. szeptember 24-i állapot szerint."},
        ]
        d["reszletek"] = [
            {"cim": "Cement ára zsákonként, mázsánként és raklaponként",
             "szoveg": "<p>A cementet 25 kg-os zsákban árulják. 2026 szeptemberi bruttó árak:</p>" + tabla(
                 ["Kiszerelés", "Ár"],
                 [["25 kg-os zsák", "2 000–2 750 Ft"], ["Kilogrammonként", "80–110 Ft/kg"],
                  ["1 mázsa (100 kg = 4 zsák)", "8 000–11 000 Ft"], ["Raklap (54 zsák = 1350 kg)", "108 000–148 000 Ft"]])
                 + "<p>Raklapos vételnél a raklap letétje és a kiszállítás külön tétel.</p>"},
            {"cim": "Melyik cement mire való? (CEM I és CEM II)",
             "szoveg": "<ul class=\"list-disc pl-6\"><li><strong>CEM II/B-M 32,5 R</strong> – általános célú, a legolcsóbb (2 000–2 300 Ft). Falazás, vakolat, aljzat, kisebb beton.</li><li><strong>CEM II 42,5 N/R</strong> – nagyobb szilárdságú (2 200–2 400 Ft). Beton, alapozás.</li><li><strong>CEM I 42,5 R</strong> – tiszta portlandcement (2 400–2 750 Ft). Vasbeton, gyorsabb szilárdulás.</li></ul><p>Házépítésnél a CEM II a leggyakoribb; statikailag terhelt vasbetonhoz a terv írja elő a típust.</p>"},
        ]
    elif slug == "osb-lap":
        rows = [["OSB-3 10 mm", 6390], ["OSB-3 12 mm", 7300], ["OSB-3 15 mm", 8990], ["OSB-3 18 mm", 10800], ["OSB-3 22 mm", 13000]]
        d["faq"] = [
            {"kerdes": "Mennyibe kerül egy OSB lap 2026-ban?",
             "valasz": "Egy 2500×1250 mm-es OSB-3 tábla 2026 szeptemberében 6 400–13 500 Ft: a 12 mm-es 6 700–7 800 Ft, a 18 mm-es 9 500–11 700 Ft, a 22 mm-es 12 600–13 500 Ft."},
            {"kerdes": "Mennyi az OSB lap ára m²-enként?",
             "valasz": "Egy tábla 3,125 m², így a 12 mm-es lap kb. 2 340 Ft/m², a 18 mm-es kb. 3 450 Ft/m², a 22 mm-es kb. 4 160 Ft/m²."},
            {"kerdes": "Vízálló az OSB-3 lap?",
             "valasz": "Az OSB-3 nedvességálló, de tartós vízterhelést nem bír. Fokozottan párás vagy teherhordó helyre az OSB-4 való."},
            {"kerdes": "Hány m² egy OSB lap?",
             "valasz": "A ma jellemző 2500×1250 mm-es tábla 3,125 m². A régebbi 2440×1220 mm-es méret 2,98 m²."},
            {"kerdes": "Honnan származnak az OSB-árak?",
             "valasz": "Fatelepek és építőanyag-kereskedők (pl. Fadepo, Mar-Team, Kőházy, Mixvill, Káplár, Woodland) nyilvános bruttó áraiból, 2026. szeptember 24-i állapot szerint."},
        ]
        d["reszletek"] = [
            {"cim": "OSB lap ára m²-enként 2026",
             "szoveg": "<p>A ma kapható OSB táblák többsége <strong>2500×1250 mm</strong>, azaz <strong>3,125 m²</strong>. A táblaárból így jön ki a négyzetméterár:</p>" + tabla(
                 ["Vastagság", "Ár táblánként", "Ár m²-enként"],
                 [[n, f"{huf(p)} Ft", f"~{huf(p / 3.125)} Ft/m²"] for n, p in rows])
                 + "<p>A táblaárak a Fadepo Fatelep szeptemberi árlistájából és további kereskedők áraiból valók. Nútféderes (675×2500 mm) lapok táblánként olcsóbbak, de kisebbek.</p>"},
            {"cim": "Vízálló OSB lap: OSB-3 vagy OSB-4?",
             "szoveg": "<p>Az <strong>OSB-3</strong> nedvességálló, teherhordó lap: tetőtér, födém, padlóaljzat, falburkolat. Tartós vízterhelést nem visel el. Az <strong>OSB-4</strong> teherbíróbb és nedvességállóbb, ára jellemzően 25–40%-kal magasabb.</p><p>Kültéren, időjárásnak kitett felületen egyik sem használható védőréteg (zsindely, lemezfedés, vízszigetelés) nélkül.</p>"},
            {"cim": "Mennyi OSB lap kell?",
             "szoveg": "<p>Egy 2500×1250 mm-es tábla <strong>3,125 m²</strong>. A szükséges lapszám:</p><p class=\"font-semibold\">lapszám = terület (m²) ÷ 3,125 × 1,10 (10% vágási veszteség)</p><p>Példa: 40 m² födémhez 40 ÷ 3,125 = 12,8 tábla, ráhagyással <strong>14 tábla</strong>. 18 mm-es lappal ez kb. 151 000 Ft.</p>"},
        ]
    elif slug == "betonacél":
        d["faq"] = [
            {"kerdes": "Mennyi a betonacél ára kg-onként 2026-ban?",
             "valasz": "A B500B bordás betonacél kiskereskedelmi ára 2026 szeptemberében 415–455 Ft/kg (6 m-es szálban, bruttó). Tonnás, kötegelt tételnél bruttó 300 Ft/kg körül is elérhető."},
            {"kerdes": "Mennyibe kerül egy szál betonvas?",
             "valasz": "6 m-es szálban: Ø8 kb. 1 030 Ft (2,37 kg), Ø10 kb. 1 590 Ft (3,70 kg), Ø12 kb. 2 350 Ft (5,33 kg), Ø16 kb. 4 000 Ft (9,47 kg)."},
            {"kerdes": "Hány kg betonacél kell 1 m³ betonhoz?",
             "valasz": "Sáv- és lemezalaphoz kb. 60–90 kg/m³, födémhez 80–120 kg/m³, oszlophoz és gerendához 100–150 kg/m³. A pontos mennyiséget a vasalási terv adja meg."},
            {"kerdes": "Miért más a nagyker és a tüzép ára?",
             "valasz": "A nagykereskedők kötegben (2–5 tonna) adják, ott a kg-ár bruttó 300 Ft körül van. Tüzépen szálanként, kis tételben 415–455 Ft/kg."},
            {"kerdes": "Honnan származnak a betonacélárak?",
             "valasz": "Tüzépek és vaskereskedők (pl. Winkler Tüzép, Baustar 98, Újház Bodrogi, Újház Farmker, Vas Centrum) nyilvános árából, 2026. szeptember 24-i állapot szerint."},
        ]
        suly = {"Ø8": 0.395, "Ø10": 0.617, "Ø12": 0.888, "Ø16": 1.58}
        arak = {"Ø8": 436, "Ø10": 430, "Ø12": 441, "Ø16": 423}
        d["reszletek"] = [
            {"cim": "Betonacél ár átmérő szerint (2026)",
             "szoveg": "<p>B500B bordás betonacél, 6 m-es szálban, bruttó tüzépi ár:</p>" + tabla(
                 ["Átmérő", "Ft/kg", "kg/fm", "Ft/fm", "Ft/szál (6 m)"],
                 [[k, huf(arak[k]), str(suly[k]).replace(".", ","), huf(arak[k] * suly[k]), huf(arak[k] * suly[k] * 6)] for k in arak])
                 + "<p>A kg-ár átmérőtől alig függ. Tonnás tételnél és kötegben érezhetően olcsóbb.</p>"},
            {"cim": "Mennyi betonacél kell? (kg/m³ becslés)",
             "szoveg": "<ul class=\"list-disc pl-6\"><li>Sávalap, lemezalap: <strong>60–90 kg/m³</strong></li><li>Födém, koszorú: <strong>80–120 kg/m³</strong></li><li>Oszlop, gerenda: <strong>100–150 kg/m³</strong></li></ul><p>Példa: 10 m³ lemezalap 75 kg/m³-rel = 750 kg, tüzépi áron kb. 325 000 Ft. A pontos mennyiséget a statikai terv határozza meg.</p>"},
        ]


def main():
    kutatas = {}
    for g in ("g1", "g2", "g3", "g4"):
        with open(os.path.join(RESEARCH, f"prices_{g}.json"), encoding="utf-8") as f:
            for k, v in json.load(f).items():
                if not k.startswith("_"):
                    kutatas[SLUG_MAP.get(k, k)] = v

    with open(os.path.join(DATA, "anyagok.json"), encoding="utf-8") as f:
        anyagok = {a["slug"]: a for a in json.load(f)}

    kesz, hiany = 0, []
    for slug, anyag in anyagok.items():
        path = os.path.join(ARAK, f"{slug}.json")
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        k = kutatas.get(slug)
        if not k:
            hiany.append(slug)
            continue
        egyseg = EGYSEG.get(slug, k["egyseg"])
        variansok = []
        for v in k["variansok"] + EXTRA_VARIANS.get(slug, []):
            ve = VARIANS_EGYSEG_TISZTIT.sub("", v.get("egyseg", egyseg)).strip() or egyseg
            if ve in ("Ft/l",):
                ve = "Ft/liter"
            variansok.append({"nev": v["nev"], "ar": int(round(v["ar"])), "egyseg": ve})
        variansok.sort(key=lambda v: v["ar"])
        forrasok = [clean_forras(x) for x in k["forrasok"] if x.get("url")]
        d["alap_ar"] = {"min": int(k["min"]), "max": int(k["max"]), "atlag": int(k["atlag"]), "egyseg": egyseg}
        d["variansok"] = variansok
        d["forrasok"] = forrasok
        d["megjegyzes"] = MEGJEGYZES.get(slug, "")
        d["frissitve"] = DATUM
        d["ar_tipus"] = "bruttó bolti ár, szállítás nélkül"
        if slug in ("cement", "osb-lap", "betonacél"):
            kezi_szovegek(slug, d)
        else:
            d["faq"] = faq_general(anyag["nev"], egyseg, d["alap_ar"], variansok, forrasok, d["megjegyzes"])
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        kesz += 1
    print(f"Frissítve: {kesz} anyag. Kutatás nélkül maradt: {hiany or 'nincs'}")


if __name__ == "__main__":
    main()
