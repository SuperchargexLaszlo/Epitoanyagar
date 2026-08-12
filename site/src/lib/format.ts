// Közös segédfüggvények – árformázás, dátum, séma
export const SITE = 'https://epitoanyagar.hu';

const HONAPOK = [
  'január', 'február', 'március', 'április', 'május', 'június',
  'július', 'augusztus', 'szeptember', 'október', 'november', 'december',
];

// Ezres tagolás nem törő szóközzel (magyar konvenció: 1 200), determinisztikusan
export function huf(n: number): string {
  return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}

// "Ft/zsák (25 kg)" -> "Ft/zsák"  (címhez, hogy rövid maradjon)
export function rovidEgyseg(egyseg: string): string {
  return egyseg.replace(/\s*\(.*?\)\s*/g, '').trim();
}

// ISO dátum ("2026-08-01") -> "2026. augusztus 1."
export function datumHosszu(iso: string): string {
  const [y, m, d] = iso.split('-').map(Number);
  if (!y || !m) return iso;
  return `${y}. ${HONAPOK[m - 1]}${d ? ` ${d}.` : ''}`;
}

// ISO dátum -> "2026. augusztus"
export function honapEv(iso: string): string {
  const [y, m] = iso.split('-').map(Number);
  if (!y || !m) return iso;
  return `${y}. ${HONAPOK[m - 1]}`;
}

// AggregateOffer termékséma egy ár-oldalhoz
export function termekSchema(opts: {
  nev: string;
  leiras: string;
  kategoria?: string;
  url: string;
  min: number;
  max: number;
  egyseg: string;
  ajanlatDb: number;
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: opts.nev,
    description: opts.leiras,
    ...(opts.kategoria ? { category: opts.kategoria } : {}),
    url: opts.url,
    offers: {
      '@type': 'AggregateOffer',
      priceCurrency: 'HUF',
      lowPrice: opts.min,
      highPrice: opts.max,
      offerCount: opts.ajanlatDb,
      availability: 'https://schema.org/InStock',
      priceValidUntil: '2026-12-31',
    },
  };
}
