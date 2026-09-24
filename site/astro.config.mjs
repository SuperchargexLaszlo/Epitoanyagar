import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';
import fs from 'fs';
import path from 'path';

// lastmod a sitemapben: az anyag áradatának frissítési dátuma (data/arak/*.json → frissitve).
// Így a Google látja, melyik oldal változott, és ennek alapján ütemezi az újrafeltérképezést.
const dataDir = path.resolve('..', 'data');
const anyagSlugok = JSON.parse(fs.readFileSync(path.join(dataDir, 'anyagok.json'), 'utf-8'))
  .map((a) => a.slug)
  .sort((a, b) => b.length - a.length);
const frissitesek = {};
let legfrissebb = '2026-01-15';
for (const s of anyagSlugok) {
  try {
    const d = JSON.parse(fs.readFileSync(path.join(dataDir, 'arak', `${s}.json`), 'utf-8')).frissitve;
    if (d) { frissitesek[s] = d; if (d > legfrissebb) legfrissebb = d; }
  } catch { /* nincs áradat */ }
}
const lastmodFor = (url) => {
  const p = decodeURIComponent(url.replace('https://epitoanyagar.hu/', ''));
  const s = anyagSlugok.find((x) => p === `${x}-ara/` || p.startsWith(`${x}-ara-`));
  return new Date(s && frissitesek[s] ? frissitesek[s] : legfrissebb).toISOString();
};

export default defineConfig({
  site: 'https://epitoanyagar.hu',
  integrations: [
    tailwind(),
    sitemap({
      filter: (page) => !page.includes('/404'),
      serialize(item) {
        const url = item.url;
        item.lastmod = lastmodFor(url);
        // Főoldal
        if (url === 'https://epitoanyagar.hu/') {
          item.priority = 1.0;
          item.changefreq = 'weekly';
          return item;
        }
        // Kategória oldalak
        if (url.includes('/kategoria/')) {
          item.priority = 0.8;
          item.changefreq = 'weekly';
          return item;
        }
        // Városi gyűjtőoldalak
        if (url.includes('/varos/')) {
          item.priority = 0.6;
          item.changefreq = 'weekly';
          return item;
        }
        // Anyag-város kombinált oldalak (tartalmaz második kötőjeles -ara- részt)
        const parts = url.replace('https://epitoanyagar.hu/', '').replace(/\/$/, '').split('-ara-');
        if (parts.length > 1) {
          item.priority = 0.7;
          item.changefreq = 'weekly';
          return item;
        }
        // Anyag főoldalak (*-ara/)
        if (url.includes('-ara/')) {
          item.priority = 0.9;
          item.changefreq = 'weekly';
          return item;
        }
        item.priority = 0.5;
        item.changefreq = 'weekly';
        return item;
      },
    }),
  ],
  output: 'static',
  trailingSlash: 'always',
});
