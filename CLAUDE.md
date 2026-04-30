# CLAUDE.md – Építőanyag ár weboldal

> **Session memory file.** Minden Claude Code session elején olvasd el ezt a fájlt.
> Folytatásnál: olvasd el CLAUDE.md + CHANGELOG.md utolsó 20 sorát → tudd meg hol tartunk.

---

## Projekt azonosító

- **Weboldal:** epitoanyagar.hu
- **Mappa:** `D:\DEV\Építőanyag ár weboldal`
- **Stack:** Astro 4 (SSG) + Python scraper + JSON data
- **Cél:** 3 000+ oldal, programmatic SEO, AdSense monetizáció
- **Év:** 2026

---

## Munkamódszer – minimális tokenfelhasználás

1. **Mindig olvasd el először:** `CLAUDE.md`, `CHANGELOG.md` (utolsó 20 sor), `ARCHITECTURE.md`
2. **Sprint alapú munka:** aktuális sprint a `SPRINTS.md`-ben, az éppen aktív sprint jelölve van
3. **Minden task elvégzése után:** frissítsd a `CHANGELOG.md`-t, és jelöld `[DONE]` a SPRINTS.md-ben
4. **Ne kérdezz feleslegeset:** ha a task egyértelmű, hajtsd végre
5. **Fájlokat mindig teljes tartalommal írj** – ne használj `// ... existing code ...` rövidítéseket
6. **Folytatás tokenlimitnél:** a CHANGELOG.md utolsó sora mindig az aktuális állapot

---

## Könyvtárstruktúra

```
D:\DEV\Építőanyag ár weboldal\
├── CLAUDE.md                    ← ez a fájl
├── ARCHITECTURE.md
├── CHANGELOG.md
├── SPRINTS.md
├── data/                        ← Python scraper output (JSON)
│   ├── anyagok.json             ← összes építőanyag lista
│   ├── varosok.json             ← magyar városok listája
│   └── arak/                   ← anyagonként JSON fájlok
│       ├── cement.json
│       ├── soder.json
│       └── ...
├── scraper/                     ← Python scraper
│   ├── requirements.txt
│   ├── scraper.py
│   └── generate_data.py         ← statikus adatgeneráló (scraper nélkül)
└── site/                        ← Astro projekt
    ├── public/
    │   └── googlec726e779c7a4db7e.html
    ├── src/
    │   ├── content/
    │   │   └── config.ts
    │   ├── layouts/
    │   ├── pages/
    │   └── components/
    ├── astro.config.mjs
    └── package.json
```

---

## Google Search Console

- Verifikációs fájl: `site/public/googlec726e779c7a4db7e.html`
- Tartalom: `google-site-verification: googlec726e779c7a4db7e.html`

---

## SEO elvek (minden oldalon kötelező)

- **Title tag:** `[Anyag neve] ára 2026 – Aktuális árak és árlista`
- **Meta description:** `Mennyi a [anyag] ára 2026-ban? Aktuális árlista kg/m2/zsák árak, vásárlási tippek.`
- **H1:** `[Anyag neve] ára 2026`
- **URL struktúra:** `/cement-ara/`, `/cement-ara-budapest/`
- **Schema.org:** FAQPage + Article minden oldalon
- **Canonical URL:** mindig saját URL
- **Sitemap.xml:** automatikus Astro @astrojs/sitemap-mal
- **robots.txt:** Allow all
- **Open Graph** meta tagek minden oldalon
- **Frissítési dátum:** 2026, mindig az aktuális hónap

---

## URL struktúra

```
/                                    ← főoldal
/[anyag-slug]-ara/                   ← pl. /cement-ara/
/[anyag-slug]-ara-[varos-slug]/      ← pl. /cement-ara-budapest/
/sitemap.xml                         ← automatikus
/robots.txt                          ← automatikus
/googlec726e779c7a4db7e.html         ← GSC verifikáció
```

---

## Városok listája (top 20 + főváros)

Budapest, Debrecen, Miskolc, Pécs, Győr, Nyíregyháza, Kecskemét, Székesfehérvár,
Szombathely, Szolnok, Érd, Tatabánya, Kaposvár, Sopron, Eger, Veszprém,
Zalaegerszeg, Dunaújváros, Nagykanizsa, Hódmezővásárhely

---

## Anyagok listája (fő kategóriák)

**Alapanyagok:** cement, beton, sóder, kavics, homok, zúzott kő, mész
**Falazat:** tégla, poroton, zsalukő, ytong, b30-as blokk
**Tető:** tetőcserép, eternit, bitumenes zsindely, tetőfólia
**Szigetelés:** kőzetgyapot, üveggyapot, hungarocell, habosított polisztirol, EPS
**Burkolat:** járólap, csempe, térkő, parkett, laminált padló
**Fém:** zártszelvény, szögvas, betonacél, horganyzott lemez
**Lap:** gipszkarton, polikarbonát, OSB lap, rétegelt lemez
**Egyéb:** vakolat, ragasztó, habarcs, vízszigetelő anyag

---

## Aktuális állapot (mindig frissítsd)

Lásd: CHANGELOG.md utolsó bejegyzés.

---

## Folytatás instrukció

Ha tokenlimitre értél és újraindítod a sessiont:
1. Olvasd el ezt a fájlt
2. Olvasd el CHANGELOG.md utolsó 30 sorát
3. Nézd meg SPRINTS.md-ben melyik task van `[IN PROGRESS]` állapotban
4. Folytasd onnan
