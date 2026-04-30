# ARCHITECTURE.md – Építőanyag ár weboldal

**Utolsó frissítés:** 2026-01-01  
**Verzió:** 1.0.0

---

## Rendszer áttekintés

```
Python Scraper / Statikus adatgeneráló
         │
         ▼
   data/arak/*.json          (nyers áradatok)
         │
         ▼
  Astro Build Pipeline
         │
    ┌────┴────┐
    │         │
[anyag]-ara/  [anyag]-ara-[varos]/
    │         │
    └────┬────┘
         ▼
   Static HTML (dist/)
         │
         ▼
   Netlify / szerver
```

---

## Stack

| Réteg | Technológia | Verzió |
|-------|-------------|--------|
| Framework | Astro | 4.x |
| Rendering | SSG (Static Site Generation) | – |
| Adatforrás | JSON fájlok (data/) | – |
| Scraper | Python + requests + BeautifulSoup | 3.11+ |
| Sitemap | @astrojs/sitemap | legújabb |
| Styling | Tailwind CSS (CDN, nincs build) | – |
| Schema | JSON-LD (inline) | – |
| Hosting (tervezett) | Netlify | – |

---

## Oldaltípusok és sablonok

### 1. Főoldal (`/`)
- Legkeresettebb anyagok listája
- Kategóriák
- Schema: WebSite + SearchAction

### 2. Anyag oldal (`/[anyag-slug]-ara/`)
- H1: `[Anyag neve] ára 2026`
- Árlista táblázat (zsák/kg/m2 bontásban)
- FAQ szekció (min. 5 kérdés)
- Kapcsolódó anyagok
- Schema: Article + FAQPage
- Belső linkek: városokra

### 3. Város-anyag oldal (`/[anyag-slug]-ara-[varos-slug]/`)
- H1: `[Anyag neve] ára [Városban] 2026`
- Helyi kiegészítő szöveg
- Adatbázis: országos ár ± lokális szorzó
- Schema: Article + FAQPage + LocalBusiness

---

## Adat modell

### `data/anyagok.json`
```json
[
  {
    "id": "cement",
    "nev": "Cement",
    "slug": "cement",
    "kategoria": "alapanyag",
    "egyseg": "zsák (25 kg)",
    "leiras": "Portland cement, általános célú építőanyag",
    "seo_title": "Cement ára 2026 – Aktuális árak és árlista",
    "seo_desc": "Mennyi a cement ára 2026-ban? Aktuális cement árlista zsákonként és tonnánként.",
    "keresesi_szavak": ["cement ár", "cement ára", "cementek árak"]
  }
]
```

### `data/arak/cement.json`
```json
{
  "anyag_id": "cement",
  "frissitve": "2026-01-15",
  "alap_ar": {
    "min": 1200,
    "max": 1800,
    "atlag": 1450,
    "egyseg": "Ft/zsák (25 kg)"
  },
  "variansok": [
    { "nev": "CEM I 42.5N", "ar": 1450, "egyseg": "Ft/zsák" },
    { "nev": "CEM II/B-V 32.5R", "ar": 1200, "egyseg": "Ft/zsák" }
  ],
  "varos_szorzok": {
    "budapest": 1.08,
    "debrecen": 0.97,
    "pecs": 0.95,
    "gyor": 1.02
  },
  "faq": [
    {
      "kerdes": "Mennyibe kerül egy zsák cement 2026-ban?",
      "valasz": "Egy 25 kg-os zsák cement ára 2026-ban 1 200–1 800 Ft között mozog."
    }
  ]
}
```

### `data/varosok.json`
```json
[
  { "id": "budapest", "nev": "Budapest", "slug": "budapest", "megye": "Pest" },
  { "id": "debrecen", "nev": "Debrecen", "slug": "debrecen", "megye": "Hajdú-Bihar" }
]
```

---

## SEO architektúra

### URL kanonizálás
```
/cement-ara/              ← canonical
/cement-ara-budapest/     ← canonical (nem /cement-ara/ altalpageja!)
```

### Belső linkelési struktúra
```
Főoldal
  └── Cement ára 2026 (/cement-ara/)
        ├── Cement ára Budapest (/cement-ara-budapest/)
        ├── Cement ára Debrecen (/cement-ara-debrecen/)
        └── ...
```

### Sitemap struktúra
- Prioritás 1.0: főoldal
- Prioritás 0.9: anyag oldalak
- Prioritás 0.7: város-anyag oldalak
- changefreq: monthly (árak havonta változnak)

---

## Scraper architektúra

```
scraper/
├── scraper.py          ← fő scraper (Bauhaus, OBI, Hornbach)
├── generate_data.py    ← statikus fallback (scraper nélkül is működik)
└── requirements.txt
```

### Scraping stratégia
1. `generate_data.py` fut először → seed JSON adatok
2. `scraper.py` felülírja az árakat valós adatokkal (opcionális)
3. Astro build a `data/` mappából olvas

---

## Oldalszám becslés

| Típus | Darab |
|-------|-------|
| Anyag oldalak | ~60 anyag |
| Város-anyag oldalak | 60 × 20 város = 1 200 |
| Kategória oldalak | ~8 |
| Egyéb (főoldal, about) | ~5 |
| **Összesen** | **~1 273** |

Bővítéssel (50 város, 100 anyag): **5 000+ oldal**

---

## Build folyamat

```bash
# 1. Adatok generálása
cd scraper && python generate_data.py

# 2. (Opcionális) valós scraping
cd scraper && python scraper.py

# 3. Astro build
cd site && npm run build

# 4. Lokális preview
cd site && npm run preview
```

---

## Teljesítmény célok

- Core Web Vitals: LCP < 1.5s, CLS = 0, INP < 100ms
- Oldalméret: < 50KB HTML, nulla JS (SSG)
- Lighthouse score: 95+
