#!/usr/bin/env python3
"""
generate_data.py – Statikus áradatok generálása
Helye: D:\DEV\Építőanyag ár weboldal\scraper\generate_data.py
Futtatás: python generate_data.py
"""

import json
import os
import random
from datetime import date

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DATA_DIR = os.path.join(BASE, 'data')
ARAK_DIR = os.path.join(DATA_DIR, 'arak')
os.makedirs(ARAK_DIR, exist_ok=True)

FRISSITVE = "2026-01-15"

# Alap árak anyagonként (Ft, reális 2026-os árak)
ARAK = {
    "cement":           {"min": 1200,  "max": 1800,   "atlag": 1450,  "egyseg": "Ft/zsák (25 kg)", "variansok": [("CEM I 42.5N", 1450), ("CEM II/B-V 32.5R", 1200), ("Gyorskötő cement", 1750)]},
    "beton":            {"min": 18000, "max": 26000,   "atlag": 22000, "egyseg": "Ft/m³",          "variansok": [("C16/20", 19000), ("C20/25", 21500), ("C25/30", 23500), ("C30/37", 26000)]},
    "soder":            {"min": 4000,  "max": 7000,    "atlag": 5500,  "egyseg": "Ft/tonna",       "variansok": [("2–4 mm mosott", 5000), ("4–8 mm mosott", 5500), ("8–16 mm mosott", 6000)]},
    "kavics":           {"min": 5000,  "max": 9000,    "atlag": 7000,  "egyseg": "Ft/tonna",       "variansok": [("4–8 mm", 6000), ("8–16 mm", 7000), ("16–32 mm", 8000)]},
    "homok":            {"min": 3500,  "max": 6000,    "atlag": 4500,  "egyseg": "Ft/tonna",       "variansok": [("Vakolóhomok", 3500), ("Betonhomok 0–4 mm", 4500), ("Mosott finom homok", 5500)]},
    "mesz":             {"min": 800,   "max": 1400,    "atlag": 1100,  "egyseg": "Ft/zsák (25 kg)","variansok": [("Oltott mész", 1000), ("Hidratált mész", 1100), ("Kalciumhidroxid", 1300)]},
    "zuzott-ko":        {"min": 4500,  "max": 8000,    "atlag": 6000,  "egyseg": "Ft/tonna",       "variansok": [("0/31 osztályozatlan", 4500), ("16/32 mészkő", 5500), ("32/63 mészkő", 6000), ("Bazalt 0/16", 7500)]},
    "tegla":            {"min": 80,    "max": 150,     "atlag": 110,   "egyseg": "Ft/db",          "variansok": [("NF tégla (25×12×6.5 cm)", 85), ("DF tégla (24×11.5×5.2 cm)", 80), ("Méretezett tégla", 130)]},
    "zsaluko":          {"min": 120,   "max": 220,     "atlag": 160,   "egyseg": "Ft/db",          "variansok": [("25 cm zsalukő", 130), ("30 cm zsalukő", 160), ("38 cm zsalukő", 200)]},
    "ytong":            {"min": 2800,  "max": 5500,    "atlag": 3800,  "egyseg": "Ft/m²",         "variansok": [("Ytong PP2/0.4 (20 cm)", 3200), ("Ytong PP4/0.6 (25 cm)", 3800), ("Porotherm 30 P+W", 4500)]},
    "tetocserep":       {"min": 350,   "max": 1200,    "atlag": 650,   "egyseg": "Ft/db",          "variansok": [("Beton tetőcserép", 400), ("Agyag tetőcserép", 650), ("Prémium agyagcserép", 1100)]},
    "bitumenes-zsindely":{"min": 1800, "max": 4500,    "atlag": 2800,  "egyseg": "Ft/m²",         "variansok": [("3 tab alap", 1800), ("Laminált zsindely", 2800), ("Prémium zsindely", 4200)]},
    "kozzetgyapot":     {"min": 800,   "max": 1800,    "atlag": 1200,  "egyseg": "Ft/m²",         "variansok": [("5 cm KG50", 800), ("10 cm KG50", 1200), ("15 cm KG50", 1700), ("10 cm Frontrock Max E", 1800)]},
    "hungarocell":      {"min": 400,   "max": 1400,    "atlag": 850,   "egyseg": "Ft/m²",         "variansok": [("EPS 70 5 cm", 450), ("EPS 70 10 cm", 800), ("EPS 80 10 cm", 900), ("EPS 100 15 cm", 1300)]},
    "terko":            {"min": 3500,  "max": 8000,    "atlag": 5500,  "egyseg": "Ft/m²",         "variansok": [("Beton térkő 6 cm", 3500), ("Beton térkő 8 cm", 4200), ("Prémium térkő", 6000), ("Gránit térkő", 7500)]},
    "jaro-lap":         {"min": 2000,  "max": 8000,    "atlag": 3800,  "egyseg": "Ft/m²",         "variansok": [("Kerámia 30×30", 2200), ("Kerámia 60×60", 3500), ("Gres porcelanato", 5500), ("Gránit lap", 7800)]},
    "csempe":           {"min": 2500,  "max": 12000,   "atlag": 4500,  "egyseg": "Ft/m²",         "variansok": [("Kerámia falicsempe alap", 2500), ("Kerámia 30×60", 4000), ("Rektifikált csempe", 6000), ("Design csempe", 11000)]},
    "parkett":          {"min": 4000,  "max": 25000,   "atlag": 8000,  "egyseg": "Ft/m²",         "variansok": [("Laminált padló 8 mm", 4000), ("Laminált padló 12 mm", 6000), ("Tömörfa parkett", 12000), ("Többrétegű parkett", 9000)]},
    "zartszelveny":     {"min": 1200,  "max": 4000,    "atlag": 2200,  "egyseg": "Ft/fm",         "variansok": [("20×20×2 mm", 1200), ("40×40×3 mm", 1900), ("60×60×4 mm", 3200), ("100×100×4 mm", 4000)]},
    "betonacél":        {"min": 280,   "max": 450,     "atlag": 360,   "egyseg": "Ft/kg",         "variansok": [("B500B Ø8 mm", 320), ("B500B Ø10 mm", 310), ("B500B Ø12 mm", 300), ("B500B Ø16 mm", 290)]},
    "gipszkarton":      {"min": 1800,  "max": 2800,    "atlag": 2200,  "egyseg": "Ft/lap",        "variansok": [("GKB 12.5 mm standard", 1900), ("GKFI 12.5 mm impregnált", 2400), ("GKF tűzálló", 2700)]},
    "polikarbonát":     {"min": 3000,  "max": 8000,    "atlag": 5000,  "egyseg": "Ft/m²",         "variansok": [("Egyfalu 4 mm", 2800), ("Egyfalu 6 mm", 3500), ("Kettősfalu 10 mm", 5500), ("Kettősfalu 16 mm", 7500)]},
    "osb-lap":          {"min": 2800,  "max": 6500,    "atlag": 4200,  "egyseg": "Ft/lap",        "variansok": [("OSB/2 9 mm", 2800), ("OSB/3 12 mm", 3500), ("OSB/3 18 mm", 4800), ("OSB/3 22 mm", 6000)]},
    "vakolat":          {"min": 700,   "max": 1800,    "atlag": 1100,  "egyseg": "Ft/zsák (25 kg)","variansok": [("Gépi vakolat", 800), ("Kézi vakolat", 1000), ("Hővédő vakolat", 1500), ("Szanálóvakolat", 1700)]},
    "ragaszto":         {"min": 600,   "max": 1600,    "atlag": 900,   "egyseg": "Ft/zsák (25 kg)","variansok": [("C1 csemperagasztó", 650), ("C2 erős ragasztó", 950), ("Flexragasztó", 1400), ("Blokk ragasztóhabarcs", 600)]},
}

# Városszorzók (Budapest a drágább, vidék olcsóbb)
VAROS_SZORZOK = {
    "budapest":         1.10,
    "debrecen":         0.97,
    "miskolc":          0.94,
    "pecs":             0.96,
    "gyor":             1.03,
    "nyiregyhaza":      0.93,
    "kecskemet":        0.98,
    "szekesfehervar":   1.01,
    "szombathely":      0.99,
    "szolnok":          0.95,
    "erd":              1.07,
    "tatabanya":        1.02,
    "kaposvar":         0.92,
    "sopron":           1.04,
    "eger":             0.96,
    "veszprem":         0.98,
    "zalaegerszeg":     0.94,
    "dunaujvaros":      0.97,
    "nagykanizsa":      0.93,
    "hodmezovasarhely": 0.91,
}

FAQ_SABLONOK = {
    "cement": [
        ("Mennyibe kerül egy zsák cement 2026-ban?", "Egy 25 kg-os zsák cement ára 2026-ban 1 200–1 800 Ft között mozog, az átlagos piaci ár kb. 1 450 Ft/zsák."),
        ("Hány zsák cement kell 1 m³ betonhoz?", "1 m³ beton elkészítéséhez általában 6–8 zsák (150–200 kg) cement szükséges, az arány a beton szilárdságától függ."),
        ("Mikor érdemes cementet venni?", "A legolcsóbb árak tavasszal és télen jellemzők, amikor az építőipari kereslet alacsonyabb. Nagyobb mennyiségnél érdemes palettában rendelni."),
        ("Mi a különbség a CEM I és CEM II cement között?", "A CEM I tiszta Portland cement, magasabb szilárdságú. A CEM II adalékot (salak, pernye, mészkő) tartalmaz, olcsóbb és elegendő általános építési munkákhoz."),
        ("Hol a legolcsóbb cementet venni?", "Nagykereskedőknél és ipari áruházakban (Bauhaus, OBI, Hornbach) vásárolva 5–15%-ot takaríthatsz meg a kiskereskedelmi árhoz képest."),
    ],
}

def get_faq(anyag_id, anyag_nev, egyseg, atlag_ar):
    if anyag_id in FAQ_SABLONOK:
        return [{"kerdes": k, "valasz": v} for k, v in FAQ_SABLONOK[anyag_id]]
    return [
        {"kerdes": f"Mennyibe kerül a {anyag_nev} 2026-ban?", "valasz": f"A {anyag_nev} ára 2026-ban {ARAK.get(anyag_id,{}).get('min','N/A'):,}–{ARAK.get(anyag_id,{}).get('max','N/A'):,} Ft/{egyseg.split('(')[0].strip()} között mozog, az átlag kb. {atlag_ar:,} Ft.".replace(",",".")},
        {"kerdes": f"Hol lehet olcsón {anyag_nev.lower()}t venni?", "valasz": f"A legkedvezőbb {anyag_nev.lower()} árak nagykereskedőknél és barkácsáruházakban (Bauhaus, OBI, Hornbach, Praktiker) találhatók. Online megrendeléssel szállítási kedvezmény is elérhető."},
        {"kerdes": f"Mikor érdemes {anyag_nev.lower()}t vásárolni?", "valasz": f"Az árak általában tavasszal emelkednek, amikor megindul az építési szezon. A legkedvezőbb árakra télen és kora tavasszal van esély."},
        {"kerdes": f"Mennyi {anyag_nev.lower()} kell egy átlagos projekthez?", "valasz": f"A szükséges mennyiség a projekt méretétől függ. Érdemes 10–15%-os tartalékkal számolni a veszteségek és hibák fedezésére."},
        {"kerdes": f"Milyen minőségű {anyag_nev.lower()}t érdemes venni?", "valasz": f"Mindig a feladatnak megfelelő minőséget válassza. Tartószerkezeteknél ne spóroljon a minőségen, de burkolóanyagoknál megtalálhatja a megfelelő ár–érték arányt."},
    ]

# Anyagok betöltése
with open(os.path.join(DATA_DIR, 'anyagok.json'), 'r', encoding='utf-8') as f:
    anyagok = json.load(f)

generalt = 0
for anyag in anyagok:
    slug = anyag['id']
    if slug not in ARAK:
        # Generikus ár ha nincs specifikus
        ar_data = {"min": 1000, "max": 5000, "atlag": 2500, "egyseg": f"Ft/{anyag['egyseg']}", "variansok": [(anyag['nev'] + " standard", 2500)]}
    else:
        ar_data = ARAK[slug]

    faq = get_faq(slug, anyag['nev'], anyag['egyseg'], ar_data['atlag'])

    output = {
        "anyag_id": slug,
        "frissitve": FRISSITVE,
        "alap_ar": {
            "min": ar_data["min"],
            "max": ar_data["max"],
            "atlag": ar_data["atlag"],
            "egyseg": ar_data["egyseg"]
        },
        "variansok": [
            {"nev": v[0], "ar": v[1], "egyseg": ar_data["egyseg"]}
            for v in ar_data["variansok"]
        ],
        "varos_szorzok": VAROS_SZORZOK,
        "faq": faq
    }

    out_path = os.path.join(ARAK_DIR, f"{slug}.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    generalt += 1
    print(f"  [OK] {slug}.json")

print(f"\nGenerálva: {generalt} anyag JSON fájl")
print(f"Helye: {ARAK_DIR}")
