/**
 * MerkuryMarket.hu Google Merchant feed -> data/merkury.json
 *
 * A teljes feed 114 MB / 70 000+ termék, ezért STREAMELVE dolgozzuk fel:
 * a fájl sosem kerül egészben a memóriába.
 *
 * Csak az "Építkezés; felújítás" ág kerül be (~10 700 termék). A bútor és a
 * lakberendezés (50 000+ tétel) nem tartozik az epitoanyagar.hu profiljába.
 *
 * Futtatás:
 *   node scraper/merkury-feed.mjs [feed-útvonal-vagy-URL]
 *
 * Alapértelmezett forrás:
 *   D:\DEV\Affiliate master\Productfeeds\merkurymarket.hu-gmc.xml
 */
import { createReadStream, createWriteStream, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const DEFAULT_FEED = 'D:/DEV/Affiliate master/Productfeeds/merkurymarket.hu-gmc.xml';
const OUT = join(ROOT, 'data', 'merkury.json');
const src = process.argv.find((a) => !a.startsWith('-') && /\.(xml|txt)$/i.test(a)) ?? DEFAULT_FEED;

/**
 * CSOPORTOK. Kulcs = a site-on használt slug, érték = a Merkury
 * kategóriaútvonalának 2-3. szintje.
 *
 * `anyag`: ha kitöltött, ehhez a meglévő /[anyag]-ara/ oldalhoz kapcsoljuk
 *          a termékeket. Ha null, önálló termékkategória-oldal lesz belőle.
 */
const CSOPORTOK = [
  // --- meglévő anyag-oldalakhoz kötve ---
  { slug: 'falicsempe',        nev: 'Falicsempe',            anyag: 'csempe',         utak: ['Csempék és járólapok > Falicsempe', 'Csempék és járólapok > Kerámia csempék'], kell: /csempe|mozaik/i, tilt: /díszléc|profil|fuga|ragaszt|élvéd/i },
  { slug: 'padlolap',          nev: 'Padlólap',              anyag: 'jarolap',        utak: ['Csempék és járólapok > Padlólapok'], kell: /padlólap|járólap|gres|lap /i, tilt: /díszléc|profil|fuga|ragaszt/i },
  { slug: 'padloburkolat',     nev: 'Padlóburkolat',         anyag: 'laminalt-padlo', utak: ['Padlók és padlólapok > Padlóburkolat'], kell: /padló|laminál/i, tilt: /szegély|léc|alátét/i },
  { slug: 'vinyl-padlo',       nev: 'Vinyl padló',           anyag: 'vinyl-padlo',    utak: ['Padlók és padlólapok > Vinyl padlók'], kell: /vinyl|vinil|padló/i, tilt: /szegély|léc/i },
  { slug: 'parketta',          nev: 'Parketta',              anyag: 'parkett',        utak: ['Padlók és padlólapok > Parketták'], kell: /parketta|padló/i, tilt: /szegély|léc/i },
  // --- önálló termékkategóriák ---
  { slug: 'csaptelep',         nev: 'Fürdőszobai csaptelep', anyag: null, utak: ['Fürdőszobai berendezések > Csaptelepek'], kell: /csaptelep/i, tilt: /csaptelepekhez|csaphoz|oring|o-ring|tömítés|pearlator|perlátor|levegőztető|kifolyó|anya |alátét|sarokbázis|bázis|készlet|szabályozó|hosszabbító|adapter|tömlő|szelep|betét/i, minAr: 3000 },
  { slug: 'zuhanytalca',       nev: 'Zuhanytálca',           anyag: null, utak: ['Fürdőszobai berendezések > Zuhanytálcák'], kell: /tálca|zuhanytálca/i, tilt: /szifon|lefolyó|láb|takaró/i },
  { slug: 'zuhanykabin',       nev: 'Zuhanykabin',           anyag: null, utak: ['Fürdőszobai berendezések > Zuhanykabinok'], kell: /zuhanykabin|zuhanyajtó|zuhanyfal|kabin/i, tilt: /fogantyú|kerek|kerék|lista|görgő|tömítés|profil|alkatrész/i },
  { slug: 'kad',               nev: 'Kád és kádparaván',     anyag: null, utak: ['Fürdőszobai berendezések > Kádak és kádparavánok'], kell: /kád|paraván/i, tilt: /láb|szifon|takaró|fogantyú|kapaszkodó/i },
  { slug: 'furdoszoba-keramia',nev: 'Fürdőszoba kerámia',    anyag: null, utak: ['Fürdőszobai berendezések > Fürdőszoba kerámia'], kell: /wc|mosdó|bidé|kagyló|csésze/i, tilt: /tömítés|szifon|csavar|rögzít|alátét|gumi|kefe|szelep|kifolyó|dugó|tartó/i, minAr: 8000 },
  { slug: 'zuhany-felszereles',nev: 'Zuhany felszerelés',    anyag: null, utak: ['Fürdőszobai berendezések > Zuhany felszerelés'], kell: /zuhany/i, tilt: /tálca|kabin|ajtó|tömítés|oring|tartó|akasztó|szappan/i, minAr: 5000 },
  { slug: 'ajtokilincs',       nev: 'Ajtókilincs',           anyag: null, utak: ['Ajtók és kilincsek > Ajtókilincsek'], kell: /kilincs/i, tilt: /rozetta|csavar|betét|tengely/i, minAr: 3000 },
  { slug: 'belteri-ajto',      nev: 'Beltéri ajtó',          anyag: null, utak: ['Ajtók és kilincsek > Beltéri ajtók és ajtókeretek'], kell: /ajtó/i, tilt: /kilincs|zár|pánt|küszöb|tömítés|felső része|alsó része|oldalsó|takaróléc|kiegészít|szellőző|csavar/i, minAr: 15000 },
  { slug: 'konyhai-csaptelep', nev: 'Konyhai csaptelep',     anyag: null, utak: ['Konyhai berendezések > Konyhai csaptelepek'], kell: /csaptelep/i, tilt: /csaptelepekhez|csaphoz|oring|o-ring|tömítés|pearlator|perlátor|levegőztető|kifolyó|alátét|szabályozó|hosszabbító|készlet|adapter|szelep|betét/i, minAr: 5000 },
  { slug: 'konyhai-mosogato',  nev: 'Konyhai mosogató',      anyag: null, utak: ['Konyhai berendezések > Konyhai mosogatók'], kell: /mosogató|mosogatótálca/i, tilt: /szifon|dugó|szűrő|kosár|tartozék/i },
  { slug: 'konyhai-munkalap',  nev: 'Konyhai munkalap',      anyag: null, utak: ['Konyhai berendezések > Konyhai munkalap'], kell: /munkalap/i, tilt: /profil|záróléc|csavar/i },
  { slug: 'szegelylec',        nev: 'Szegélyléc',            anyag: null, utak: ['Padlók és padlólapok > Szegélylécek'], kell: /szegélyléc|lábazat|léc/i, tilt: /csavar|klip|rögzít|toldó|sarok/i },
  { slug: 'falburkolat',       nev: 'Falburkolat',           anyag: null, utak: ['Falburkolat > Falburkolás', 'Falburkolat > Lecek lamella falburkolathoz', 'Falburkolat > Lécek falra'], kell: /panel|burkolat|lamella|léc/i, tilt: /ragaszt|csavar|profil/i },
];

// --- apró segédek ---------------------------------------------------------
function cdata(s) {
  return s.replace(/^\s*<!\[CDATA\[/, '').replace(/\]\]>\s*$/, '')
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'").replace(/&amp;/g, '&').trim();
}
function tag(item, name) {
  const m = item.match(new RegExp(`<${name}>([\\s\\S]*?)</${name}>`));
  return m ? cdata(m[1]) : null;
}
/**
 * CSAPDA: minden terméknek KÉT <g:price> mezője van - a sajátja, és egy
 * másik a <g:shipping> blokkon belül (a szállítási díj). Ha az elsőt vesszük
 * ki naivan, a szállítási díj lesz a termékár. Ezért a shipping blokkot
 * kivágjuk, mielőtt árat keresünk.
 */
function arNelkulShipping(item) {
  return item.replace(/<g:shipping>[\s\S]*?<\/g:shipping>/g, '');
}
function huf(s) {
  if (!s) return null;
  const n = Number(String(s).replace(/[^\d]/g, ''));
  return Number.isFinite(n) && n > 0 ? n : null;
}

// --- feldolgozás ----------------------------------------------------------
const utvonalIndex = new Map();
for (const cs of CSOPORTOK) for (const u of cs.utak) utvonalIndex.set(u, cs);

const talalat = new Map(CSOPORTOK.map((c) => [c.slug, []]));
let osszes = 0, epitkezes = 0, arNelkul = 0, kiszurt = 0;

let buf = '';
await new Promise((res, rej) => {
  createReadStream(resolve(src), { encoding: 'utf8', highWaterMark: 4 << 20 })
    .on('data', (chunk) => {
      buf += chunk;
      let i;
      while ((i = buf.indexOf('</item>')) !== -1) {
        const item = buf.slice(0, i);
        buf = buf.slice(i + 7);
        osszes++;

        const ptRaw = tag(item, 'g:product_type');
        if (!ptRaw) continue;
        // CSAPDA: a mező TÖBB útvonalat tartalmaz, vesszővel összefűzve.
        const utak = ptRaw.split(',').map((s) => s.trim()).filter(Boolean);
        if (!utak.some((u) => u.startsWith('Építkezés; felújítás'))) continue;
        epitkezes++;

        // Melyik csoportba tartozik? A leghosszabb (legpontosabb) egyezés nyer.
        let csoport = null;
        for (const u of utak) {
          const r = u.split('>').map((s) => s.trim());
          const kulcs = r.slice(1, 3).join(' > ');
          const c = utvonalIndex.get(kulcs);
          if (c) { csoport = c; break; }
        }
        if (!csoport) continue;

        const tiszta = arNelkulShipping(item);
        const ar = huf(tag(tiszta, 'g:price'));
        if (!ar) { arNelkul++; continue; }

        talalat.get(csoport.slug).push({
          id: tag(item, 'g:id'),
          nev: tag(item, 'g:title'),
          url: tag(item, 'g:link'),
          kep: tag(item, 'g:image_link'),
          ar,
          ar_label: ar.toLocaleString('hu-HU') + ' Ft',
          marka: tag(item, 'g:brand'),
          gtin: tag(item, 'g:gtin'),
          keszlet: (tag(item, 'g:availability') ?? '') === 'in stock',
          csoport: csoport.slug,
          anyag: csoport.anyag,
          merchant: 'merkurymarket-hu-for-content',
        });
      }
      if (buf.length > 600000) buf = buf.slice(-300000);
    })
    .on('end', res).on('error', rej);
});

// Determinisztikus sorrend + csoportonkénti korlát.
// A cél nem az, hogy mind a 10 700 termék kikerüljön: egy 1 000 soros
// táblázatot senki nem olvas el, viszont lassú és thin. Csoportonként a
// legolcsóbb N raktáron lévő tétel kerül ki, ez fedi a keresési szándékot.
const LIMIT = Number(process.env.MERKURY_LIMIT ?? 60);
const kimenet = [];
for (const cs of CSOPORTOK) {
  /**
   * A kereskedo a POTALKATRESZEKET is a fo kategoria ala sorolja: a
   * "Csaptelepek" alatt o-gyuru keszlet es perlator is van, a "Zuhanykabinok"
   * alatt fogantyu es gorgo. Ha ezt nem szurjuk, egy "Csaptelep" cimu oldal
   * 330 Ft-os o-gyurukkel indulna - ertektelen es gyanus.
   *
   * Ezert a termeknevnek tartalmaznia kell a kategoria fonevet (kell), es
   * nem tartalmazhatja a tipikus alkatresz-szavakat (tilt).
   */
  const nyers = talalat.get(cs.slug).filter((t) => t.id && t.nev && t.url);
  const lista = nyers
    .filter((t) => (!cs.kell || cs.kell.test(t.nev)) && (!cs.tilt || !cs.tilt.test(t.nev)))
    // Arkuszob biztonsagi haloként: egy valodi csaptelep nem 900 Ft. Ami ez
    // alatt van, az szinte biztosan alkatresz, amit a nevszuro nem fogott meg.
    .filter((t) => !cs.minAr || t.ar >= cs.minAr)
    .sort((a, b) => a.ar - b.ar || a.id.localeCompare(b.id));
  kiszurt += nyers.length - lista.length;
  const raktaron = lista.filter((t) => t.keszlet);
  const valasztott = (raktaron.length >= 10 ? raktaron : lista).slice(0, LIMIT);
  kimenet.push({
    slug: cs.slug, nev: cs.nev, anyag: cs.anyag,
    osszes: lista.length,
    minAr: lista.length ? lista[0].ar : null,
    maxAr: lista.length ? lista[lista.length - 1].ar : null,
    termekek: valasztott,
  });
}

// --- kepek ellenorzese ----------------------------------------------------
/**
 * Az Astro a kepeket BUILD IDOBEN tolti le es optimalizalja. Ha egy kep
 * idokozben eltunt a kereskedo szerverererol, a BUILD ALL MEG - egy 404-es
 * termekfoto nem viheti el az egesz oldalt.
 *
 * Ezert HEAD-del ellenorzunk, es a halott URL-t kivesszuk: a termek ilyenkor
 * kep nelkul, de hibatlanul megjelenik.
 */
async function ellenorizKepek(csoportok, kihagy) {
  const mind = csoportok.flatMap((c) => c.termekek);
  const egyediek = [...new Set(mind.map((t) => t.kep).filter(Boolean))];
  if (kihagy) {
    console.log(`  kepek: ${egyediek.length} egyedi URL (ellenorzes kihagyva)`);
    return 0;
  }
  const jo = new Set();
  let rossz = 0;
  const BATCH = 12;
  for (let i = 0; i < egyediek.length; i += BATCH) {
    await Promise.all(egyediek.slice(i, i + BATCH).map(async (u) => {
      try {
        const r = await fetch(u, { method: 'HEAD', signal: AbortSignal.timeout(15000) });
        const ct = r.headers.get('content-type') ?? '';
        if (r.ok && ct.startsWith('image/')) jo.add(u); else rossz++;
      } catch { rossz++; }
    }));
    if (i && i % 240 === 0) process.stdout.write(`\r  kepek ellenorzese: ${i}/${egyediek.length}`);
  }
  process.stdout.write('\r'.padEnd(50) + '\r');
  for (const t of mind) if (t.kep && !jo.has(t.kep)) t.kep = null;
  console.log(`  kepek: ${jo.size}/${egyediek.length} egyedi URL rendben${rossz ? `, ${rossz} elerhetetlen (kep nelkul jelenik meg)` : ''}`);
  return rossz;
}
await ellenorizKepek(kimenet, process.argv.includes('--skip-image-check'));

const kiirt = kimenet.reduce((n, c) => n + c.termekek.length, 0);
if (epitkezes < 5000) {
  console.error(`HIBA: csak ${epitkezes} építkezési termék (várt 5000+). A feed valószínűleg csonka - a kimenet NEM íródott felül.`);
  process.exit(1);
}

mkdirSync(dirname(OUT), { recursive: true });
writeFileSync(OUT, JSON.stringify(kimenet, null, 1) + '\n', 'utf8');

console.log(`merkury.json: ${kimenet.length} csoport, ${kiirt} kiírt termék`);
console.log(`  feed: ${osszes.toLocaleString('hu-HU')} termék, ebből építkezés/felújítás: ${epitkezes.toLocaleString('hu-HU')}`);
if (arNelkul) console.log(`  ár nélkül kihagyva: ${arNelkul}`);
console.log(`  alkatrészként kiszűrve: ${kiszurt}`);
console.log('');
for (const c of kimenet) {
  const jel = c.anyag ? `-> /${c.anyag}-ara/` : '(önálló oldal)';
  console.log(`  ${c.slug.padEnd(24)} ${String(c.termekek.length).padStart(3)}/${String(c.osszes).padStart(5)}  ${c.minAr ? c.minAr.toLocaleString('hu-HU') + '-' + c.maxAr.toLocaleString('hu-HU') + ' Ft' : '-'}  ${jel}`);
}
