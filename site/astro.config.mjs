import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://epitoanyagar.hu',
  integrations: [
    tailwind(),
    sitemap({
      serialize(item) {
        const url = item.url;
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
  // A Merkury termékképek a kereskedő feedjéből jönnek. Engedélyezve az Astro
  // build-idejű optimalizálásához: letölti, méretezi, és mi szolgáljuk ki —
  // nem hotlinkelünk, és futásidőben nem függünk tőlük.
  // A halott URL-eket a scraper/merkury-feed.mjs szűri ki.
  image: { domains: ['www.merkurymarket.hu'] },
});
