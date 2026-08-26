/**
 * Affiliate kimenő linkek — EGYETLEN forrás.
 *
 * Nyers kereskedői URL soha ne kerüljön a HTML-be közvetlenül.
 *
 * KÉT ÜZEMMÓD:
 * 1. KÖZVETLEN (ez fut ma): a Dognet link-generátor "Simple version" formája —
 *    https://go.dognet.com/?chid=<csatorna>&url=<URL-kódolt cél>
 *    A kampányt a Dognet a cél-URL domainjéből azonosítja. Nincs subID,
 *    a mérés csatorna-szintű, a Dognet saját riportjából.
 * 2. CLICK-OUT: ha a PUBLIC_CLICKOUT_BASE_URL be van állítva, a saját /go
 *    szolgáltatáson keresztül megy, HMAC-aláírt subID-vel a d1 paraméterben,
 *    így SABLON-SZINTŰ EPC is mérhető.
 */
const CHID = import.meta.env.PUBLIC_DOGNET_CHID ?? 'L1GeUDJR';
const CLICKOUT = import.meta.env.PUBLIC_CLICKOUT_BASE_URL ?? '';

/** Ez az oldal azonosítója a click-out SITE_IDS registryjében. */
export const SITE_ID = 'buildmat-hu';

export interface AffInput {
  destUrl: string;
  merchant: string;
  template: string;
  pagePath?: string;
  offerId?: string | null;
}

export function affUrl({ destUrl, merchant, template, pagePath = '', offerId = null }: AffInput): string {
  if (!destUrl) throw new Error('affUrl: hiányzó destUrl');

  if (!CLICKOUT) {
    return `https://go.dognet.com/?chid=${encodeURIComponent(CHID)}&url=${encodeURIComponent(destUrl)}`;
  }
  const p = new URLSearchParams({
    s: SITE_ID, t: template, p: hashPath(pagePath), m: merchant, u: destUrl,
  });
  if (offerId) p.set('o', offerId);
  return `${CLICKOUT.replace(/\/$/, '')}/go?${p.toString()}`;
}

function hashPath(path: string): string {
  let h = 2166136261;
  for (let i = 0; i < path.length; i++) {
    h ^= path.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return (h >>> 0).toString(36);
}

/** Kötelező attribútumok MINDEN kimenő affiliate linken. */
export const AFF_REL = 'sponsored nofollow noopener';
