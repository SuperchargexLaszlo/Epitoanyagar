import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://epitoanyagar.hu',
  integrations: [
    sitemap({
      serialize(item) {
        const url = item.url;
        // Főoldal
        if (url === 'https://epitoanyagar.hu/') {
          item.priority = 1.0;
          item.changefreq = 'monthly';
          return item;
        }
        // Kategória oldalak
        if (url.includes('/kategoria/')) {
          item.priority = 0.8;
          item.changefreq = 'monthly';
          return item;
        }
        // Anyag-város kombinált oldalak (tartalmaz második kötőjeles -ara- részt)
        const parts = url.replace('https://epitoanyagar.hu/', '').replace(/\/$/, '').split('-ara-');
        if (parts.length > 1) {
          item.priority = 0.7;
          item.changefreq = 'monthly';
          return item;
        }
        // Anyag főoldalak (*-ara/)
        if (url.includes('-ara/')) {
          item.priority = 0.9;
          item.changefreq = 'monthly';
          return item;
        }
        item.priority = 0.5;
        item.changefreq = 'monthly';
        return item;
      },
    }),
  ],
  output: 'static',
  trailingSlash: 'always',
});
