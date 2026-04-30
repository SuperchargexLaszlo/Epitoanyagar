# epitoanyagar.hu – Astro site

## Parancsok

```bash
# Fejlesztői szerver
npm run dev

# Statikus build (dist/ mappába)
npm run build

# Build előnézet
npm run preview
```

## Adatok frissítése

```bash
# JSON adatok újragenerálása
cd ../scraper && python generate_data.py

# Ezután újrabuildelés
cd ../site && npm run build
```

## Struktúra

- `src/pages/[anyag].astro` – anyag főoldalak (/cement-ara/)
- `src/pages/[slug].astro` – város-anyag oldalak (/cement-ara-budapest/)
- `src/pages/kategoria/[kat].astro` – kategória oldalak
- `src/components/` – PriceTable, PriceCard, FAQ, Breadcrumb, Header, Footer
- `../data/` – JSON adatforrások
