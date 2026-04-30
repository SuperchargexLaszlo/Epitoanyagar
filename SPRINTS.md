# SPRINTS.md – Építőanyag ár weboldal

> **Státusz jelölések:** `[ ]` = todo | `[IN PROGRESS]` = folyamatban | `[DONE]` = kész | `[SKIP]` = kihagyva

---

## SPRINT 1 – Projekt setup és Astro inicializálás

**Cél:** Működő Astro projekt lokalisan, alapstruktúrával.  
**Becsült tokenfelhasználás:** alacsony  
**Mappa:** `D:\DEV\Építőanyag ár weboldal`

---

### Prompt S1 – Teljes sprint 1

```
Olvasd el: CLAUDE.md, ARCHITECTURE.md, CHANGELOG.md (összes sor)

FELADAT – Sprint 1: Astro projekt setup

Munkamappa: D:\DEV\Építőanyag ár weboldal

Hajtsd végre sorban:

S1.1 [DONE] Könyvtárak létrehozása
  - Hozd létre: data/arak/, scraper/, site/ mappákat
  - Hozd létre: data/anyagok.json, data/varosok.json (üres tömb most)

S1.2 [DONE] Google Search Console verifikációs fájl
  - Hozd létre: site/public/googlec726e779c7a4db7e.html
  - Tartalom pontosan: google-site-verification: googlec726e779c7a4db7e.html

S1.3 [DONE] Astro projekt inicializálás
  - cd site
  - npm create astro@latest . -- --template minimal --no-install --no-git
  - npm install
  - npm install @astrojs/sitemap

S1.4 [DONE] astro.config.mjs konfigurálás
  - site: 'https://epitoanyagar.hu'
  - integrations: [sitemap()]
  - output: 'static'
  - trailingSlash: 'always'

S1.5 [DONE] robots.txt létrehozása
  - Helye: site/public/robots.txt
  - Tartalom:
    User-agent: *
    Allow: /
    Sitemap: https://epitoanyagar.hu/sitemap-index.xml

S1.6 [DONE] Alap Tailwind CDN layout
  - Hozd létre: site/src/layouts/BaseLayout.astro
  - Tartalom: HTML5 alap, Tailwind CDN script tag, meta viewport, charset
  - Props: title, description, canonicalURL, ogImage (opcionális)

S1.7 [DONE] Tesztelés
  - cd site && npm run dev
  - Ellenőrizd: localhost:4321 betölt

S1.8 [DONE] CHANGELOG.md frissítése
  - Add hozzá: [2026-01-15] [S1] Sprint 1 kész – Astro projekt inicializálva

Minden task után jelöld [DONE]-nal a SPRINTS.md-ben.
Ha tokenlimitre érsz, mentsd az állapotot CHANGELOG.md-be és jelöld [IN PROGRESS]-szel.
```

---

## SPRINT 2 – Adat réteg: JSON generátor és anyaglista

**Cél:** Teljes adat struktúra 60+ anyaggal, 20 várossal, árakkal.  
**Becsült tokenfelhasználás:** közepes  

---

### Prompt S2 – Teljes sprint 2

```
Olvasd el: CLAUDE.md, CHANGELOG.md (utolsó 30 sor)
Ellenőrizd: S1 összes task [DONE] státuszban van-e.

FELADAT – Sprint 2: Adat réteg

S2.1 [DONE] data/varosok.json feltöltése (20 város)
  Hozd létre a teljes fájlt ezzel a 20 várossal:
  Budapest, Debrecen, Miskolc, Pécs, Győr, Nyíregyháza, Kecskemét, 
  Székesfehérvár, Szombathely, Szolnok, Érd, Tatabánya, Kaposvár, 
  Sopron, Eger, Veszprém, Zalaegerszeg, Dunaújváros, Nagykanizsa, Hódmezővásárhely
  
  Séma: [{ "id": "slug", "nev": "Teljes név", "slug": "slug", "megye": "Megye neve" }]

S2.2 [DONE] data/anyagok.json feltöltése (60+ anyag)
  Kategóriánként hozd létre az összes anyagot ARCHITECTURE.md szerint.
  Minden anyagnál kötelező mezők:
  - id, nev, slug, kategoria, egyseg, leiras
  - seo_title: "[Nev] ára 2026 – Aktuális árak és árlista"
  - seo_desc: "Mennyi a [nev] ára 2026-ban? Aktuális [nev] árlista..."
  - keresesi_szavak: array (3-5 szó)

S2.3 [DONE] scraper/generate_data.py létrehozása
  Python script, ami data/anyagok.json-ból olvasva létrehozza 
  data/arak/[slug].json fájlokat az ARCHITECTURE.md adat modellje szerint.
  
  Minden JSON tartalmaz:
  - anyag_id, frissitve (2026-01-15)
  - alap_ar: { min, max, atlag, egyseg }
  - variansok: array (2-4 variáns)
  - varos_szorzok: object (minden városhoz)
  - faq: array (5 kérdés-válasz pár)
  
  Árakat reálisan töltse ki (kutatott ártartományok):
  cement: 1200-1800 Ft/zsák, beton: 18000-26000 Ft/m3, sóder: 4000-7000 Ft/tonna
  kavics: 5000-9000 Ft/tonna, homok: 3500-6000 Ft/tonna
  térkő: 3500-8000 Ft/m2, csempe: 2500-12000 Ft/m2, gipszkarton: 1800-2800 Ft/lap
  kőzetgyapot: 800-1800 Ft/m2, tégla: 80-150 Ft/db, járólap: 2000-8000 Ft/m2
  polikarbonát: 3000-8000 Ft/m2, zártszelvény: 1200-4000 Ft/m
  
  FAQ kérdések formátuma: "Mennyibe kerül [anyag] 2026-ban?"

S2.4 [DONE] scraper/requirements.txt
  requests==2.31.0
  beautifulsoup4==4.12.2
  lxml==4.9.3

S2.5 [DONE] Generate futtatása
  cd scraper && python generate_data.py
  Ellenőrizd: data/arak/ mappa tartalmaz-e JSON fájlokat

S2.6 [DONE] CHANGELOG.md frissítése
  [2026-01-20] [S2] Sprint 2 kész – [X] anyag JSON generálva, [X] város beállítva
```

---

## SPRINT 3 – Astro Content Collections és oldalak

**Cél:** Működő dinamikus oldalak Astro-ban, minden anyaghoz és városhoz.  
**Becsült tokenfelhasználás:** magas (sok fájl)  

---

### Prompt S3a – Content Collections konfig és anyag oldalak

```
Olvasd el: CLAUDE.md, CHANGELOG.md (utolsó 30 sor)
Ellenőrizd: S2 [DONE], data/arak/ mappában vannak JSON fájlok.

FELADAT – Sprint 3a: Astro oldalak (1. rész)

S3.1 [ ] site/src/content/config.ts – Content Collections séma
  Defináld a 'anyagok' és 'arak' collection-öket Zod schema-val.
  Az anyagok a data/anyagok.json-ból, az arak data/arak/*.json-ból jönnek.
  FONTOS: Astro Content Collections nem tud közvetlenül data/ mappából olvasni –
  ehelyett használj getStaticPaths()-ban Astro.glob() vagy fs.readFileSync megoldást.

S3.2 [ ] site/src/layouts/BaseLayout.astro – teljes SEO layout
  Props: title, description, canonicalURL, schema (JSON-LD string)
  Tartalmaz:
  - <html lang="hu">
  - charset, viewport meta
  - title tag (max 60 kar)
  - meta description (max 160 kar)
  - canonical link
  - Open Graph (og:title, og:description, og:url, og:type, og:locale hu_HU)
  - Twitter card (summary)
  - JSON-LD schema (inline script type="application/ld+json")
  - Tailwind CDN (csak CDN, nincs npm install)
  - Google Fonts: Inter (display=swap, preconnect)

S3.3 [ ] site/src/components/PriceTable.astro
  Props: variansok array, egyseg string
  Táblázat: Variáns neve | Ár | Egység
  Tailwind styled, mobilon is jól néz ki (overflow-x-auto)

S3.4 [ ] site/src/components/FAQ.astro
  Props: faq array [{kerdes, valasz}]
  <details>/<summary> HTML elem, stílusos Tailwind
  Ez egyben schema.org FAQPage-hez is fel lesz használva

S3.5 [ ] site/src/components/Breadcrumb.astro
  Props: items [{label, href}]
  Schema.org BreadcrumbList JSON-LD-vel

S3.6 [ ] site/src/pages/[anyag].astro – anyag lap template
  URL: /[anyag-slug]-ara/
  
  getStaticPaths():
  - Olvasd be data/anyagok.json-t (fs.readFileSync)
  - Minden anyaghoz path: params.anyag = slug + "-ara"
  
  Lap tartalma:
  - <h1>[Anyag neve] ára 2026</h1>
  - Bevezető bekezdés (100-150 szó, kulcsszó sűrűség ~2%)
  - PriceTable komponens
  - H2: "Mire figyelj [anyag] vásárlásakor?"
  - H2: "[Anyag] ára városonként" → linkek a város oldalakra
  - FAQ komponens (5 kérdés)
  - Schema: Article + FAQPage JSON-LD

S3.7 [ ] CHANGELOG.md frissítése
```

---

### Prompt S3b – Város-anyag oldalak és főoldal

```
Olvasd el: CLAUDE.md, CHANGELOG.md (utolsó 30 sor)
Ellenőrizd: S3.1–S3.6 [DONE]

FELADAT – Sprint 3b: Város oldalak és főoldal

S3.8 [ ] site/src/pages/[anyag]-[varos].astro – város-anyag lap
  URL: /[anyag-slug]-ara-[varos-slug]/
  
  getStaticPaths():
  - Olvasd be data/anyagok.json + data/varosok.json
  - Minden kombinációhoz: params.anyag = slug, params.varos = varos_slug
  - Összesen: ~60 × 20 = 1 200 oldal
  
  FONTOS URL struktúra: az oldal URL-je /[anyag]-ara-[varos]/
  Pl. /cement-ara-budapest/ – ezt egyetlen dinamikus route-ból kezeld:
  [slug].astro ahol a slug "cement-ara-budapest" formátumú
  
  Lap tartalma:
  - <h1>[Anyag neve] ára [Városban] 2026</h1>
  - Lokalizált intro (város neve beillesztve)
  - Helyi ár kalkulálva: alap_ar × varos_szorzo
  - PriceTable (lokális árakkal)
  - FAQ (3 helyi kérdés)
  - Visszalink az anyag főlapjára
  - Schema: Article + FAQPage + BreadcrumbList

S3.9 [ ] site/src/pages/index.astro – főoldal
  Tartalom:
  - H1: "Építőanyag árak 2026 – Aktuális árlista"
  - Bevezető (200 szó, természetes kulcsszó használat)
  - Kategória kártyák (8 kategória grid)
  - Legnépszerűbb anyagok (top 10, linkekkel)
  - Miért változnak az árak? szekció
  - Schema: WebSite + SearchAction

S3.10 [ ] site/src/pages/kategoria/[kat].astro – kategória oldalak
  8 kategória: alapanyag, falazat, teto, szigeteles, burkolat, fem, lap, egyeb
  Lista az adott kategória anyagairól

S3.11 [ ] Tesztelés
  npm run dev → ellenőrizd:
  - / betölt
  - /cement-ara/ betölt
  - /cement-ara-budapest/ betölt
  - /sitemap-index.xml elérhető
  npm run build → 0 hiba

S3.12 [ ] CHANGELOG.md frissítése
  [2026-01-25] [S3] Sprint 3 kész – [X] anyag oldal, [X] város-anyag oldal generálva
```

---

## SPRINT 4 – SEO finomhangolás és schema.org

**Cél:** Minden SEO elem helyes, schema.org validálható, sitemap teljes.  
**Becsült tokenfelhasználás:** közepes  

---

### Prompt S4 – SEO sprint

```
Olvasd el: CLAUDE.md, CHANGELOG.md (utolsó 30 sor)
Ellenőrizd: S3 összes task [DONE], npm run build sikeresen lefut.

FELADAT – Sprint 4: SEO finomhangolás

S4.1 [ ] Schema.org ellenőrzés és javítás
  Minden oldalon ellenőrizd és javítsd:
  - Article schema: headline (max 110 kar), datePublished 2026-01-15, 
    dateModified (ma), author {name: "epitoanyagar.hu team"},
    publisher {name: "Építőanyag ár", url: "https://epitoanyagar.hu"}
  - FAQPage schema: minden kérdés-válasz pár
  - BreadcrumbList: helyes pozíciószámok
  - WebSite schema főoldalon: SearchAction potential action

S4.2 [ ] Belső linkelés audit
  Minden anyag oldalon:
  - H2 szekció: "[Anyag] ára városonként" → linkek a top 5 városra
  - Lábléc: Kapcsolódó anyagok (3-5 link)
  - Minden város-anyag oldalon: vissza az anyag főlapjára

S4.3 [ ] Sitemap prioritások beállítása
  astro.config.mjs-ben customizeEntries:
  - / → priority: 1.0, changefreq: monthly
  - /*-ara/ → priority: 0.9, changefreq: monthly
  - /*-ara-*/→ priority: 0.7, changefreq: monthly

S4.4 [ ] Meta robots beállítás
  Minden oldalon: <meta name="robots" content="index, follow">
  Duplikáció megelőzés: canonicalURL mindig a saját URL

S4.5 [ ] Képek (ha vannak) alt text audit
  Minden img tag: descriptive alt text magyarul

S4.6 [ ] Performance ellenőrzés
  npm run build
  Ellenőrizd a dist/ mappa méretét
  Cél: minden HTML fájl < 50KB

S4.7 [ ] CHANGELOG.md frissítése
  [2026-02-01] [S4] Sprint 4 kész – SEO audit elvégezve, schema.org validált
```

---

## SPRINT 5 – Design és UI csiszolás

**Cél:** Professzionális megjelenés, jó UX, AdSense-ready.  
**Becsült tokenfelhasználás:** közepes  

---

### Prompt S5 – Design sprint

```
Olvasd el: CLAUDE.md, CHANGELOG.md (utolsó 30 sor)
Ellenőrizd: S4 [DONE]

FELADAT – Sprint 5: Design és UI

S5.1 [ ] Header komponens (site/src/components/Header.astro)
  - Logo: "Építőanyag ár" szöveges logo
  - Navigáció: Főoldal | Kategóriák | Legkeresettebb árak
  - Mobile: hamburger menu nélkül (egyszerű wrapping)
  - Tailwind: fehér háttér, shadow-sm, sticky top-0

S5.2 [ ] Footer komponens (site/src/components/Footer.astro)
  - Jogi szöveg: "Az árak tájékoztató jellegűek, 2026-os adatok alapján."
  - Kategória linkek 2 oszlopban
  - Copyright: © 2026 epitoanyagar.hu
  - Utolsó frissítés: 2026-01-15

S5.3 [ ] Ár kártya komponens (site/src/components/PriceCard.astro)
  - Kiemelő kártya az átlagárral
  - Zöld szín (alacsony ár tartomány), sárga (közepes), piros (magas)
  - Props: min, max, atlag, egyseg

S5.4 [ ] Kategória kártya (site/src/components/CategoryCard.astro)
  - Ikon (emoji), cím, leírás, link
  - Hover effekt

S5.5 [ ] 404 oldal (site/src/pages/404.astro)
  - Magyar szöveg
  - Link a főoldalra
  - Keresési javaslatok

S5.6 [ ] Mobilon tesztelés
  - Chrome DevTools mobile view
  - Minden oldaltípus mobilon olvasható

S5.7 [ ] AdSense placeholder helyek megjelölése
  - Minden anyag oldalon: 1 banner (cikk után)
  - Minden város-anyag oldalon: 1 banner
  - Kommentként jelöld: <!-- ADSENSE_PLACEHOLDER -->

S5.8 [ ] CHANGELOG.md frissítése
  [2026-02-10] [S5] Sprint 5 kész – Design kész, AdSense helyek megjelölve
```

---

## SPRINT 6 – Tartalom bővítés és végleges ellenőrzés

**Cél:** Minden oldal tartalma egyedi és értékes, build hibátlan.  
**Becsült tokenfelhasználás:** magas  

---

### Prompt S6 – Tartalom és finálé

```
Olvasd el: CLAUDE.md, CHANGELOG.md (utolsó 30 sor)
Ellenőrizd: S5 [DONE]

FELADAT – Sprint 6: Tartalom és végleges ellenőrzés

S6.1 [ ] Bevezető szövegek ellenőrzése
  Minden anyag oldalon ellenőrizd:
  - Legalább 300 szó oldalanként
  - A kulcsszó (pl. "cement ára") szerepel H1-ben, első bekezdésben, 
    legalább 2x a szövegben
  - Természetes, nem AI-szagú szöveg
  - Konkrét árak megemlítve

S6.2 [ ] FAQ tartalom audit
  Minden FAQ oldal legalább 5 kérdés-választ tartalmaz.
  Kérdések legyenek természetesek: "Hol vegyek olcsón cementet?"

S6.3 [ ] Végleges build teszt
  npm run build
  - 0 TypeScript hiba
  - 0 build hiba
  - sitemap generálva
  - robotst.txt megvan
  - googlec726e779c7a4db7e.html megvan a dist/-ban

S6.4 [ ] Linkek ellenőrzése
  Ellenőrizd, hogy nincsenek törött belső linkek.
  Minden anyag oldalon linkelt városoldalak léteznek.

S6.5 [ ] Oldalszám számolás
  Futtasd: find dist -name "*.html" | wc -l
  Jegyezd fel CHANGELOG.md-be.

S6.6 [ ] Localhost végső teszt
  npm run preview
  Ellenőrizd manuálisan:
  - Főoldal: /
  - 3 különböző anyag oldal
  - 3 különböző város-anyag oldal
  - /sitemap-index.xml
  - /robots.txt
  - /googlec726e779c7a4db7e.html

S6.7 [ ] README.md létrehozása a site/ mappában
  Tartalom: npm run dev / build / preview parancsok leírása

S6.8 [ ] CHANGELOG.md végleges frissítése
  [2026-02-15] [S6] PROJEKT KÉSZ – [X] oldal, localhost-on fut, deploy-ready
```

---

## QUICK REFERENCE – Folytatás tokenlimit után

Ha megszakad a session, az új sessionben ezzel a prompttal indíts:

```
Olvasd el CLAUDE.md-t, majd CHANGELOG.md utolsó 30 sorát.
Nézd meg SPRINTS.md-ben melyik task van [IN PROGRESS] vagy az utolsó [DONE] után mi következik.
Folytasd onnan. Ne kérdezz, hajtsd végre.
```

---

## Státusz összefoglaló

| Sprint | Leírás | Állapot |
|--------|---------|---------|
| S1 | Projekt setup | [DONE] |
| S2 | Adat réteg | [DONE] |
| S3a | Anyag oldalak | [DONE] |
| S3b | Város oldalak + főoldal | [DONE] |
| S4 | SEO finomhangolás | [DONE] |
| S5 | Design és UI | [DONE] |
| S6 | Tartalom és finálé | [DONE] |
