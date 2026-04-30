#!/usr/bin/env python3
"""
bootstrap.py – Epitoanyagar.hu projekt inicializáló script
Futtatás: python bootstrap.py
Helye: D:\DEV\Epitoanyagar ar weboldal\bootstrap.py
"""

import os
import json

BASE = os.path.dirname(os.path.abspath(__file__))

def mkdir(path):
    os.makedirs(os.path.join(BASE, path), exist_ok=True)
    print(f"  [OK] {path}/")

def write(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [OK] {path}")

print("\n=== Epitoanyagar.hu Bootstrap ===\n")

# 1. Könyvtárak
print("Konyvtarak letrehozasa...")
for d in ['data/arak', 'scraper', 'site/public', 'site/src']:
    mkdir(d)

# 2. GSC verifikáció
print("\nGoogle Search Console fajl...")
write('site/public/googlec726e779c7a4db7e.html',
      'google-site-verification: googlec726e779c7a4db7e.html')

# 3. robots.txt
print("\nRobots.txt...")
write('site/public/robots.txt',
      'User-agent: *\nAllow: /\nSitemap: https://epitoanyagar.hu/sitemap-index.xml\n')

# 4. Városok JSON
print("\nVarosok JSON...")
varosok = [
    {"id": "budapest",            "nev": "Budapest",            "slug": "budapest",            "megye": "Pest"},
    {"id": "debrecen",            "nev": "Debrecen",            "slug": "debrecen",            "megye": "Hajdú-Bihar"},
    {"id": "miskolc",             "nev": "Miskolc",             "slug": "miskolc",             "megye": "Borsod-Abaúj-Zemplén"},
    {"id": "pecs",                "nev": "Pécs",                "slug": "pecs",                "megye": "Baranya"},
    {"id": "gyor",                "nev": "Győr",                "slug": "gyor",                "megye": "Győr-Moson-Sopron"},
    {"id": "nyiregyhaza",         "nev": "Nyíregyháza",         "slug": "nyiregyhaza",         "megye": "Szabolcs-Szatmár-Bereg"},
    {"id": "kecskemet",           "nev": "Kecskemét",           "slug": "kecskemet",           "megye": "Bács-Kiskun"},
    {"id": "szekesfehervar",      "nev": "Székesfehérvár",      "slug": "szekesfehervar",      "megye": "Fejér"},
    {"id": "szombathely",         "nev": "Szombathely",         "slug": "szombathely",         "megye": "Vas"},
    {"id": "szolnok",             "nev": "Szolnok",             "slug": "szolnok",             "megye": "Jász-Nagykun-Szolnok"},
    {"id": "erd",                 "nev": "Érd",                 "slug": "erd",                 "megye": "Pest"},
    {"id": "tatabanya",           "nev": "Tatabánya",           "slug": "tatabanya",           "megye": "Komárom-Esztergom"},
    {"id": "kaposvar",            "nev": "Kaposvár",            "slug": "kaposvar",            "megye": "Somogy"},
    {"id": "sopron",              "nev": "Sopron",              "slug": "sopron",              "megye": "Győr-Moson-Sopron"},
    {"id": "eger",                "nev": "Eger",                "slug": "eger",                "megye": "Heves"},
    {"id": "veszprem",            "nev": "Veszprém",            "slug": "veszprem",            "megye": "Veszprém"},
    {"id": "zalaegerszeg",        "nev": "Zalaegerszeg",        "slug": "zalaegerszeg",        "megye": "Zala"},
    {"id": "dunaujvaros",         "nev": "Dunaújváros",         "slug": "dunaujvaros",         "megye": "Fejér"},
    {"id": "nagykanizsa",         "nev": "Nagykanizsa",         "slug": "nagykanizsa",         "megye": "Zala"},
    {"id": "hodmezovasarhely",    "nev": "Hódmezővásárhely",    "slug": "hodmezovasarhely",    "megye": "Csongrád-Csanád"},
]
write('data/varosok.json', json.dumps(varosok, ensure_ascii=False, indent=2))

# 5. Anyagok JSON
print("\nAnyagok JSON...")
anyagok = [
    # Alapanyagok
    {"id":"cement","nev":"Cement","slug":"cement","kategoria":"alapanyag","egyseg":"zsák (25 kg)","leiras":"Portland cement, általános célú építőanyag.","seo_title":"Cement ára 2026 – Aktuális cement árak és árlista","seo_desc":"Mennyi a cement ára 2026-ban? Aktuális cement árlista zsákonként és tonnánként, vásárlási tippek.","keresesi_szavak":["cement ár","cement ára","cement árak 2026"]},
    {"id":"beton","nev":"Beton","slug":"beton","kategoria":"alapanyag","egyseg":"m³","leiras":"Kész beton, különböző szilárdságú osztályokban.","seo_title":"Beton ára 2026 – Aktuális betonárak m³-enként","seo_desc":"Mennyi a beton ára 2026-ban? Kész beton árak m³-enként, C16/20-tól C30/37-ig.","keresesi_szavak":["beton ár","beton ára","kész beton ár"]},
    {"id":"soder","nev":"Sóder","slug":"soder","kategoria":"alapanyag","egyseg":"tonna","leiras":"Mosott kavics, különböző szemcseméretekben.","seo_title":"Sóder ára 2026 – Aktuális sóder árak tonnánként","seo_desc":"Mennyi a sóder ára 2026-ban? Aktuális sóder árlista tonnánként és köbméterenként.","keresesi_szavak":["sóder ár","sóder ára","sóder árak"]},
    {"id":"kavics","nev":"Kavics","slug":"kavics","kategoria":"alapanyag","egyseg":"tonna","leiras":"Természetes kavics, feltöltési és betonkészítési célra.","seo_title":"Kavics ára 2026 – Aktuális kavics árak tonnánként","seo_desc":"Mennyi a kavics ára 2026-ban? Kavics árlista tonnánként, különböző szemcseméretekben.","keresesi_szavak":["kavics ár","kavics ára","kavics árak"]},
    {"id":"homok","nev":"Homok","slug":"homok","kategoria":"alapanyag","egyseg":"tonna","leiras":"Építési homok, vakoláshoz és betonhoz.","seo_title":"Homok ára 2026 – Aktuális homok árak építési célra","seo_desc":"Mennyi az építési homok ára 2026-ban? Aktuális homok árlista tonnánként.","keresesi_szavak":["homok ár","homok ára","építési homok ár"]},
    {"id":"mész","nev":"Mész","slug":"mesz","kategoria":"alapanyag","egyseg":"zsák (25 kg)","leiras":"Oltott mész, vakoláshoz és festéshez.","seo_title":"Mész ára 2026 – Aktuális mész árak zsákonként","seo_desc":"Mennyi a mész ára 2026-ban? Oltott mész, hidratált mész árak 2026.","keresesi_szavak":["mész ár","mész ára","oltott mész ár"]},
    {"id":"zuzott-ko","nev":"Zúzott kő","slug":"zuzott-ko","kategoria":"alapanyag","egyseg":"tonna","leiras":"Zúzott mészkő és bazalt, alapozáshoz és útépítéshez.","seo_title":"Zúzott kő ára 2026 – Aktuális árak tonnánként","seo_desc":"Mennyi a zúzott kő ára 2026-ban? Zúzott mészkő, bazalt árlist 2026.","keresesi_szavak":["zúzott kő ár","zúzott kő ára","zúzott mészkő ár"]},
    # Falazat
    {"id":"tegla","nev":"Tégla","slug":"tegla","kategoria":"falazat","egyseg":"db","leiras":"Égetett agyagtégla, falazáshoz.","seo_title":"Tégla ára 2026 – Aktuális tégla árak darabonként","seo_desc":"Mennyi a tégla ára 2026-ban? Égetett tégla, méretezett tégla árlista 2026.","keresesi_szavak":["tégla ár","tégla ára","tégla árak"]},
    {"id":"zsaluko","nev":"Zsalukő","slug":"zsaluko","kategoria":"falazat","egyseg":"db","leiras":"Beton zsalukő, egyszerű falazathoz.","seo_title":"Zsalukő ára 2026 – Aktuális zsalukő árak darabonként","seo_desc":"Mennyi a zsalukő ára 2026-ban? Zsalukő árlista, darab és paletta árak.","keresesi_szavak":["zsalukő ár","zsalukő ára","zsalukő árak"]},
    {"id":"ytong","nev":"Ytong / Porotherm","slug":"ytong","kategoria":"falazat","egyseg":"m²","leiras":"Pórusbeton blokk és kerámia blokk, könnyűszerkezetes falazathoz.","seo_title":"Ytong ára 2026 – Pórusbeton blokk árak m²-enként","seo_desc":"Mennyi az Ytong ára 2026-ban? Pórusbeton, Porotherm blokk árak m²-enként.","keresesi_szavak":["ytong ár","ytong ára","pórusbeton ár"]},
    # Tető
    {"id":"tetocserep","nev":"Tetőcserép","slug":"tetocserep","kategoria":"teto","egyseg":"db / m²","leiras":"Agyag és beton tetőcserép, különböző profilokban.","seo_title":"Tetőcserép ára 2026 – Aktuális cserép árak m²-enként","seo_desc":"Mennyi a tetőcserép ára 2026-ban? Agyag és beton cserép árlista m²-enként.","keresesi_szavak":["tetőcserép ár","tetőcserép ára","cserép árak"]},
    {"id":"bitumenes-zsindely","nev":"Bitumenes zsindely","slug":"bitumenes-zsindely","kategoria":"teto","egyseg":"m²","leiras":"Aszfalt zsindely, egyszerű tetőfedéshez.","seo_title":"Bitumenes zsindely ára 2026 – Aktuális árak m²-enként","seo_desc":"Mennyi a bitumenes zsindely ára 2026-ban? Aszfalt zsindely árlista 2026.","keresesi_szavak":["bitumenes zsindely ár","zsindely ára","aszfalt zsindely ár"]},
    # Szigetelés
    {"id":"kozzetgyapot","nev":"Kőzetgyapot","slug":"kozzetgyapot","kategoria":"szigeteles","egyseg":"m²","leiras":"Ásványgyapot hő- és hangszigetelő lemez.","seo_title":"Kőzetgyapot ára 2026 – Aktuális kőzetgyapot árak m²-enként","seo_desc":"Mennyi a kőzetgyapot ára 2026-ban? Kőzetgyapot szigetelő árlista 2026.","keresesi_szavak":["kőzetgyapot ár","kőzetgyapot ára","kőzetgyapot árak"]},
    {"id":"hungarocell","nev":"Hungarocell / EPS","slug":"hungarocell","kategoria":"szigeteles","egyseg":"m²","leiras":"Expandált polisztirol (EPS) hőszigetelő lap.","seo_title":"Hungarocell ára 2026 – EPS szigetelő árak m²-enként","seo_desc":"Mennyi a hungarocell ára 2026-ban? EPS polisztirol lap árlista, különböző vastagságokban.","keresesi_szavak":["hungarocell ár","EPS lap ár","polisztirol szigetelő ár"]},
    # Burkolat
    {"id":"terko","nev":"Térkő","slug":"terko","kategoria":"burkolat","egyseg":"m²","leiras":"Beton térkő, kültéri burkoláshoz.","seo_title":"Térkő ára 2026 – Aktuális térkő árak m²-enként","seo_desc":"Mennyi a térkő ára 2026-ban? Beton térkő árlista m²-enként, különböző mintákban.","keresesi_szavak":["térkő ár","térkő ára","térkő árak"]},
    {"id":"jaro-lap","nev":"Járólap","slug":"jaro-lap","kategoria":"burkolat","egyseg":"m²","leiras":"Kerámia és gránit járólap, beltéri és kültéri burkoláshoz.","seo_title":"Járólap ára 2026 – Aktuális járólap árak m²-enként","seo_desc":"Mennyi a járólap ára 2026-ban? Kerámia, gránit járólap árlista 2026.","keresesi_szavak":["járólap ár","járólap ára","járólap árak"]},
    {"id":"csempe","nev":"Csempe","slug":"csempe","kategoria":"burkolat","egyseg":"m²","leiras":"Kerámia falicsempe fürdőszobába és konyhába.","seo_title":"Csempe ára 2026 – Aktuális csempe árak m²-enként","seo_desc":"Mennyi a csempe ára 2026-ban? Kerámia csempe árlista m²-enként.","keresesi_szavak":["csempe ár","csempe ára","csempe árak"]},
    {"id":"parkett","nev":"Parkett","slug":"parkett","kategoria":"burkolat","egyseg":"m²","leiras":"Fa parkett és laminált padló.","seo_title":"Parkett ára 2026 – Aktuális parkett árak m²-enként","seo_desc":"Mennyi a parkett ára 2026-ban? Tömörfa és laminált parkett árlista 2026.","keresesi_szavak":["parkett ár","parkett ára","parkett árak"]},
    # Fém
    {"id":"zartszelveny","nev":"Zártszelvény","slug":"zartszelveny","kategoria":"fem","egyseg":"folyóméter","leiras":"Acél zártszelvény, szerkezeti célokra.","seo_title":"Zártszelvény ára 2026 – Aktuális acél zártszelvény árak","seo_desc":"Mennyi a zártszelvény ára 2026-ban? Acél zártszelvény árlista folyóméterenként.","keresesi_szavak":["zártszelvény ár","zártszelvény ára","zártszelvény árak"]},
    {"id":"betonacél","nev":"Betonacél","slug":"betonacél","kategoria":"fem","egyseg":"kg / tonna","leiras":"Bordás betonacél, vasbeton szerkezetekhez.","seo_title":"Betonacél ára 2026 – Aktuális betonacél árak kg-onként","seo_desc":"Mennyi a betonacél ára 2026-ban? Bordás betonacél árlista kg-onként és tonnánként.","keresesi_szavak":["betonacél ár","betonacél ára","betonacél árak"]},
    # Lap
    {"id":"gipszkarton","nev":"Gipszkarton","slug":"gipszkarton","kategoria":"lap","egyseg":"lap (1,25×2,5 m)","leiras":"Gipszkarton lap belső válaszfalakhoz és álmennyezethez.","seo_title":"Gipszkarton ára 2026 – Aktuális gipszkarton árak laponként","seo_desc":"Mennyi a gipszkarton ára 2026-ban? Gipszkarton lap árlista 2026.","keresesi_szavak":["gipszkarton ár","gipszkarton ára","gipszkarton árak"]},
    {"id":"polikarbonát","nev":"Polikarbonát lemez","slug":"polikarbonát","kategoria":"lap","egyseg":"m²","leiras":"Polikarbonát lemez tetőhöz és kerítéshez.","seo_title":"Polikarbonát ára 2026 – Aktuális polikarbonát lemez árak","seo_desc":"Mennyi a polikarbonát ára 2026-ban? Polikarbonát lemez árlista m²-enként.","keresesi_szavak":["polikarbonát ár","polikarbonát ára","polikarbonát árak"]},
    {"id":"osb-lap","nev":"OSB lap","slug":"osb-lap","kategoria":"lap","egyseg":"lap","leiras":"Oriented Strand Board, tetőhéjazathoz és zsaluzáshoz.","seo_title":"OSB lap ára 2026 – Aktuális OSB lap árak laponként","seo_desc":"Mennyi az OSB lap ára 2026-ban? OSB lap árlista különböző vastagságokban.","keresesi_szavak":["OSB lap ár","OSB lap ára","OSB ár"]},
    # Egyéb
    {"id":"vakolat","nev":"Vakolat","slug":"vakolat","kategoria":"egyeb","egyseg":"zsák (25 kg)","leiras":"Gépi és kézi vakolat, belső és külső felhasználásra.","seo_title":"Vakolat ára 2026 – Aktuális vakolat árak zsákonként","seo_desc":"Mennyi a vakolat ára 2026-ban? Gépi és kézi vakolat árlista 2026.","keresesi_szavak":["vakolat ár","vakolat ára","vakolat árak"]},
    {"id":"ragaszto","nev":"Ragasztó / habarcs","slug":"ragaszto","kategoria":"egyeb","egyseg":"zsák (25 kg)","leiras":"Csempéhez, járólaphoz és blokkok ragasztásához.","seo_title":"Ragasztó ára 2026 – Burkolóragasztó és habarcs árak","seo_desc":"Mennyi a burkolóragasztó ára 2026-ban? Csemperagasztó, habarcs árlista zsákonként.","keresesi_szavak":["ragasztó ár","csemperagasztó ár","habarcs ár"]},
]
write('data/anyagok.json', json.dumps(anyagok, ensure_ascii=False, indent=2))

print(f"\n=== Bootstrap kész! ===")
print(f"  Anyagok: {len(anyagok)} db")
print(f"  Varosok: {len(varosok)} db")
print(f"\nKövetkezo lepesek:")
print("  1. cd site && npm create astro@latest . -- --template minimal --no-install --no-git")
print("  2. cd site && npm install && npm install @astrojs/sitemap")
print("  3. Folytasd a SPRINTS.md S1.3 tasktol")
