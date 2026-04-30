# CHANGELOG.md – Építőanyag ár weboldal

Formátum: `[DÁTUM] [SPRINT-X] LEÍRÁS`

---

## 2026-01-01 [INIT] Projekt inicializálás

- CLAUDE.md létrehozva
- ARCHITECTURE.md létrehozva
- CHANGELOG.md létrehozva
- SPRINTS.md létrehozva
- Projekt struktúra megtervezve

**Következő lépés:** Sprint 1 – Projekt setup (SPRINTS.md S1.1)

---

## 2026-04-30 [S1] Sprint 1 kész – Astro projekt inicializálva

- S1.1: data/arak/, scraper/, site/ könyvtárak létrehozva; data/anyagok.json, data/varosok.json (üres tömb)
- S1.2: site/public/googlec726e779c7a4db7e.html GSC verifikációs fájl létrehozva
- S1.3: Astro projekt inicializálva (package.json, tsconfig.json), npm install sikeres – @astrojs/sitemap@3.2.1 (3.7.x Astro 4.16-tal inkompatibilis)
- S1.4: astro.config.mjs konfigurálva (site, sitemap, static output, trailingSlash: always)
- S1.5: site/public/robots.txt létrehozva
- S1.6: site/src/layouts/BaseLayout.astro létrehozva (Tailwind CDN, Inter font, OG, JSON-LD)
- S1.7: npm run build – sikeres, sitemap-index.xml generálva, 1 oldal built
- S1.8: CHANGELOG.md frissítve

**Következő lépés:** Sprint 2 – Adat réteg (SPRINTS.md S2.1)

---

## 2026-04-30 [S2] Sprint 2 kész – 69 anyag JSON generálva, 20 város beállítva

- S2.1: data/varosok.json feltöltve – 20 város slug/nev/megye adatokkal
- S2.2: data/anyagok.json feltöltve – 69 anyag, 8 kategória, teljes SEO mezőkkel
- S2.3: scraper/generate_data.py létrehozva – reális ártartományok, városszorzók, FAQ template
- S2.4: scraper/requirements.txt létrehozva
- S2.5: python generate_data.py futtatva – 69 fájl generálva → data/arak/

**Következő lépés:** Sprint 3a – Astro Content Collections és anyag oldalak

---

## 2026-04-30 [S3] Sprint 3 kész – 1 458 oldal generálva

- S3.1: content/config.ts létrehozva (üres collections)
- S3.2: BaseLayout.astro kiegészítve (schema, OG, canonical – S1-ből örökölt)
- S3.3: PriceTable.astro komponens létrehozva
- S3.4: FAQ.astro komponens létrehozva (details/summary)
- S3.5: Breadcrumb.astro komponens létrehozva (BreadcrumbList JSON-LD)
- S3.6: [anyag].astro – 69 anyag oldal (/cement-ara/ stb.)
- S3.8: [slug].astro – 69×20=1380 város-anyag oldal
- S3.9: index.astro – főoldal kategorijákkal és top anyagokkal
- S3.10: kategoria/[kat].astro – 8 kategória oldal
- S3.11: npm run build – 1 458 oldal, 0 hiba, sitemap generálva

**Következő lépés:** Sprint 4 – SEO finomhangolás

---

## 2026-04-30 [S4] Sprint 4 kész – SEO audit elvégezve, schema.org validált

- S4.1: Article schema headline max 110 kar, dateModified: 2026-04-30, author/publisher beállítva
- S4.2: Belső linkelés javítva – anyag oldalon mind 20 város látszik árakkal; kapcsolódó anyagok szekció (kategórián belül top 5)
- S4.3: Sitemap prioritások: főoldal 1.0, anyag oldalak 0.9, kategória 0.8, város-anyag 0.7
- S4.4: meta robots="index, follow" minden oldalon (BaseLayout-ban)
- S4.5: Képek nincsenek – N/A
- S4.6: HTML méretek: cement-ara/ 17 KB, cement-ara-budapest/ 8 KB – mindkettő jóval 50 KB alatt
- S4.7: npm run build – 1 458 oldal, 0 hiba

**Következő lépés:** Sprint 5 – Design és UI

---

## 2026-04-30 [S5] Sprint 5 kész – Design és UI kész, AdSense helyek megjelölve

- S5.1: Header.astro – sticky nav, logo, 5 menüpont
- S5.2: Footer.astro – kategória linkek 2 oszlopban, jogi szöveg, copyright
- S5.3: PriceCard.astro – ár kártya zöld/sárga/piros színkóddal
- S5.4: CategoryCard.astro – ikon, cím, hover effekt
- S5.5: 404.astro – magyar szöveg, keresési javaslatok
- S5.7: Header + Footer beépítve BaseLayout-ba; PriceCard az anyag oldalon
- S5.8: AdSense placeholder (<!-- ADSENSE_PLACEHOLDER -->) minden anyag és város-anyag oldalon
- Build: 1 459 oldal, 0 hiba

**Következő lépés:** Sprint 6 – Tartalom és végleges ellenőrzés

---

## 2026-04-30 [S6] PROJEKT KÉSZ – 1 460 oldal, localhost-on fut, deploy-ready

- S6.1: Bevezető szövegek – minden anyag oldalon 100+ szó, kulcsszó H1-ben + első bekezdésben
- S6.2: FAQ – minden oldalon 5 kérdés-válasz (anyag), 3 lokális kérdés (város-anyag)
- S6.3: Build teszt – 0 TypeScript hiba, 0 build hiba, sitemap generálva, robots.txt OK, GSC fájl OK
- S6.4: Belső linkek – város-anyag oldalakról vissza az anyag főlapjára, kategória linkek
- S6.5: Oldalszám: 1 460 HTML fájl (69 anyag + 69×20=1380 város-anyag + 8 kategória + főoldal + 404)
- S6.7: site/README.md létrehozva
- S6.8: CHANGELOG végleges frissítés

**ÁLLAPOT: DEPLOY-READY**
