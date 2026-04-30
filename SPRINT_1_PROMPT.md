# SPRINT_1_PROMPT.md
# Ezt másold be Claude Code-ba az S1 session indításakor

Olvasd el: CLAUDE.md, ARCHITECTURE.md, CHANGELOG.md

---

FELADAT – Sprint 1: Astro projekt setup

Munkamappa: D:\DEV\Építőanyag ár weboldal\site

**S1.1** Futtasd bootstrap.py-t a gyökérmappából:
```
python bootstrap.py
```

**S1.2** Astro inicializálás:
```
cd site
npm create astro@latest . -- --template minimal --install --no-git
npm install @astrojs/sitemap
```

**S1.3** Írd felül az astro.config.mjs-t:
```js
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://epitoanyagar.hu',
  trailingSlash: 'always',
  output: 'static',
  integrations: [
    sitemap({
      changefreq: 'monthly',
      priority: 0.9,
      lastmod: new Date('2026-01-15'),
    }),
  ],
});
```

**S1.4** Hozd létre site/src/layouts/BaseLayout.astro-t a teljes SEO meta tagekkel (CLAUDE.md SEO elvek szerint).

**S1.5** Tesztelés: `npm run dev` → localhost:4321 betölt

**S1.6** CHANGELOG.md frissítése:
```
[2026-01-15] [S1] Sprint 1 kész – Astro inicializálva, BaseLayout kész
```

Ha tokenlimitre érsz: jelöld az aktuális task-ot [IN PROGRESS]-szel SPRINTS.md-ben és frissítsd CHANGELOG.md-t.
